import mysql.connector
import yaml
from datetime import timedelta, date, datetime
from mail_generator import ticket_mail
from ticket_pdf_generator import generate_ticket_pdf
from time import sleep
from database_creator import create_database
from werkzeug.security import check_password_hash, generate_password_hash


class Database:
    """Used to connect Database"""

    def __init__(self):
        create_database()
        with open('./credentials.yaml') as f:
            self.__data = yaml.load(f, Loader=yaml.FullLoader)
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user=self.__data["user"],
            password=self.__data["password"],
            database=self.__data["database"],
            autocommit=True
        )

        self.__price = 0
        self.__totalPrice = 0

        self.__cursor = self.__mydb.cursor()

    def add_user(self, user: dict):
        """Adds a user_id to the database, by accepting a list consisting of username, password and email.
        And returns the updated table values in a list of key value pairs"""
        try:
            self.__cursor.execute(
                f"INSERT iNTO users VALUES (null, '{user['username']}', '{user['email']}', '{generate_password_hash(password=user['password'], salt_length=8)}')")
        except mysql.connector.errors.IntegrityError:
            return None

        self.__cursor.execute(f"SELECT * FROM users")

        return [{
            "user_id": userData[0],
            "user_name": userData[1],
            "email": userData[2],
            "password": userData[3]
        } for userData in self.__cursor.fetchall()]

    def does_user_exist(self, userData: dict):
        """Checks if the user_id exists in the database"""
        self.__cursor.execute(
            f"""SELECT password
                FROM users
                WHERE user_name = '{userData["username"]}'"""
        )
        user = self.__cursor.fetchall()
        if user:
            user = check_password_hash(user[0][0], userData["password"])
        return user

    def get_user_id_by_user_name(self, userName: str):
        """Returns user_id for given user_name"""
        self.__cursor.execute(f"""
            SELECT *
            FROM users
            WHERE user_name = '{userName}';
            """)
        res = self.__cursor.fetchall()
        return res[0][0] if res else None

    def convert_date_format(self, date: date):
        """Returns given date in dd-mm-yyyy format"""
        date = str(date).split('-')
        return f"{date[-1]}-{date[-2]}-{date[-3]}"

    def calculate_reaching_date(self, days: int, travellingDate):
        """Adds the given number of day to given date and returns date in dd-mm-yyyy format"""
        temp = travellingDate.split('-')
        travellingDate = date(int(temp[2]), int(temp[1]), int(temp[0]))
        travellingDate = travellingDate + timedelta(int(days))
        return self.convert_date_format(travellingDate)

    def convert_time_format(self, time):
        """Returns given time in hh:mm:ss format"""
        hours = time.seconds//3600
        mins = (time.seconds % 3600)//60
        return "%.2d:%.2d:00" % (hours, mins)

    def get_tickets(self, userId: int):
        """Returns tickets for given user_id"""

        self.__cursor.execute(
            f"""
            SELECT pnr
            FROM tickets
            WHERE user_id = {userId}
            """)
        ticketsList = []
        for pnr in self.__cursor.fetchall():
            self.__cursor.callproc("get_tickets", [pnr[0]])
            for res in self.__cursor.stored_results():
                ticket = res.fetchall()

            self.__cursor.callproc("get_passengers", [pnr[0]])
            for res in self.__cursor.stored_results():
                passengers = res.fetchall()

            self.__cursor.execute(
                f"""
                SELECT arrival_time, depart_time
                FROM covers
                WHERE train_no = {ticket[0][2]} AND
                    stat_id = (SELECT stat_id
                                FROM stations
                                WHERE stat_loc = '{ticket[0][4]}')""")
            sourceTiming = self.__cursor.fetchall()

            self.__cursor.execute(
                f"""
                SELECT arrival_time, days
                FROM covers
                WHERE train_no = {ticket[0][2]} AND
                    stat_id = (SELECT stat_id
                                FROM stations
                                WHERE stat_loc = '{ticket[0][5]}')""")
            destinationTiming = self.__cursor.fetchall()

            ticketsList.append(
                {
                    "pnr": ticket[0][0],
                    "travelling_date": self.convert_date_format(ticket[0][1]),
                    "train_no": ticket[0][2],
                    "train_name": ticket[0][3],
                    "from_station": ticket[0][4],
                    "to_station": ticket[0][5],
                    "passengers": [[passenger[1], passenger[2], passenger[3]] for passenger in passengers if passenger[0] == ticket[0][0]],
                    "booking_date": self.convert_date_format(ticket[0][6]),
                    "arrival_time": self.convert_time_format(sourceTiming[0][0]),
                    "depart_time": self.convert_time_format(sourceTiming[0][1]),
                    "reaching_time": self.convert_time_format(destinationTiming[0][0]),
                    "reaching_date": self.calculate_reaching_date(destinationTiming[0][1], self.convert_date_format(ticket[0][1])),
                    "price": ticket[0][7]
                }
            )

        return ticketsList

    def get_stations(self):
        """Returns all the stations in the database"""
        self.__cursor.execute("SELECT stat_name FROM stations")
        return [station[0] for station in self.__cursor.fetchall()]

    def get_trains(self, travelDetails: dict):
        """Returns list of trains for given source, destination and travel date"""
        trainsList = []
        self.__cursor.execute(
            f"""
            SELECT A.stat_id, B.stat_id
            FROM stations A, stations B
            WHERE A.stat_name = '{travelDetails['source']}' AND
                B.stat_name = '{travelDetails['destination']}';""")
        source, destination = self.__cursor.fetchall()[0]
        self.__cursor.execute('SELECT train_no FROM trains')
        trainNos = self.__cursor.fetchall()
        for trainNo in trainNos:
            self.__cursor.execute(f"""
            SELECT SUM(no_of_seats)
            FROM available_seats
            WHERE train_no = {trainNo[0]} AND 
                travel_date = '{travelDetails['travel_date']}';
            """)
            noOfSeatsReserved = self.__cursor.fetchall()
            noOfSeatsReserved = noOfSeatsReserved[0][0] if noOfSeatsReserved[0][0] else 0
            self.__cursor.execute(
                f"""SELECT seq_no, arrival_time
                FROM covers
                WHERE train_no = {trainNo[0]} AND 
                    stat_id = {destination};""")
            destData = self.__cursor.fetchall()
            if destData:
                destSeqno, reachingTime = destData[0]
            else:
                destSeqno = None
            self.__cursor.execute(
                f"""SELECT seq_no, arrival_time, depart_time
                FROM covers
                WHERE train_no = {trainNo[0]} AND stat_id = {source};""")
            sourceData = self.__cursor.fetchall()
            if sourceData:
                sourceSeqno, arrivalTime, departureTime = sourceData[0]
            else:
                sourceSeqno = None
            if sourceSeqno and destSeqno and sourceSeqno < destSeqno:
                noOfStats = destSeqno - sourceSeqno
                self.__price = 10 * noOfStats
                self.__cursor.execute(
                    f"""
                    SELECT train_name 
                    FROM trains 
                    WHERE train_no = {trainNo[0]}""")
                trainName = self.__cursor.fetchall()[0][0]
                trainsList.append({
                    "train_no": trainNo[0],
                    "train_name": trainName,
                    "source": travelDetails['source'],
                    "destination": travelDetails['destination'],
                    "arrival_time": self.convert_time_format(arrivalTime),
                    "departure_time": self.convert_time_format(departureTime),
                    "reaching_time": self.convert_time_format(reachingTime),
                    "seats_available": 1000 - noOfSeatsReserved,
                    "price": self.__price,
                })
        return trainsList

    def add_passengers_ticket(self, passengerDetails: dict):
        """Adds given passengers to the ticket and creates PDF of the ticket and mails the same"""
        self.__cursor.execute(f"""
        SELECT A.stat_id, B.stat_id
        FROM stations A, stations B
        WHERE A.stat_name='{passengerDetails['source']}' AND
        B.stat_name='{passengerDetails['destination']}'
        """)
        stations = self.__cursor.fetchall()

        travelDateList = str(passengerDetails['travel_date']).split('-')

        self.__cursor.execute(
            f"""INSERT INTO tickets (from_station, to_station, travel_date, user_id, train_no, price) VALUES ({stations[0][0]}, {stations[0][1]}, '{travelDateList[0]}-{travelDateList[1]}-{travelDateList[2]}', {passengerDetails['user_id']}, {passengerDetails['train_no']}, null)""")

        self.__cursor.execute(f"""
        SELECT pnr
        FROM tickets
        WHERE from_station = '{stations[0][0]}' AND
            to_station = '{stations[0][1]}' AND
            booking_date = '{datetime.today().year}-{datetime.today().month}-{datetime.today().day}' AND
            travel_date = '{travelDateList[0]}-{travelDateList[1]}-{travelDateList[2]}' AND
            user_id = {passengerDetails['user_id']} AND
            train_no = {passengerDetails['train_no']}
        """)

        pnr = int(self.__cursor.fetchall()[0][0])

        self.__cursor.execute(f"""
        SELECT train_no
        FROM tickets
        WHERE pnr = {pnr}
        """)

        trainNo = self.__cursor.fetchall()[0][0]

        self.__cursor.execute(f"""
            SELECT MAX(seats_reserved)
            FROM available_seats
            WHERE train_no = {trainNo} AND travel_date = '{passengerDetails["travel_date"]}';
            """)
        seatsReserved = self.__cursor.fetchall()
        seatsReserved = seatsReserved[0][0] if seatsReserved[0][0] else 0

        seat_no = seatsReserved + 1
        self.__totalPrice = 0

        for passenger in passengerDetails['passengers']:
            self.__cursor.execute(
                f"""INSERT INTO passengers VALUES (null, '{passenger['p_name']}', {passenger['p_age']}, {seat_no}, {pnr})""")
            self.__totalPrice += self.__price
            seat_no += 1
        self.__cursor.execute(
            f"""UPDATE tickets SET price={self.__totalPrice} WHERE pnr={pnr}""")
        self.__cursor.execute(f"""
        SELECT user_id, user_name, email
        FROM users
        WHERE user_id = (SELECT user_id 
                        FROM tickets
                        WHERE pnr = {pnr});
        """)
        userData = self.__cursor.fetchall()
        tickets = self.get_tickets(userData[0][0])
        ticket = [i for i in tickets if i["pnr"] == pnr][0]
        fileName = generate_ticket_pdf(ticket)
        sleep(1)
        ticket_mail(userData[0][2], userData[0][1], fileName, pnr)

    def get_ticket(self, pnr: int):
        self.__cursor.callproc("get_tickets", [pnr])
        for res in self.__cursor.stored_results():
            ticket = res.fetchall()

        self.__cursor.callproc("get_passengers", [pnr])
        for res in self.__cursor.stored_results():
            passengers = res.fetchall()

        return {
            "pnr": ticket[0][0],
            "travelling_date": self.convert_date_format(ticket[0][1]),
            "train_no": ticket[0][2],
            "train_name": ticket[0][3],
            "from_station": ticket[0][4],
            "to_station": ticket[0][5],
            "passengers": [[passenger[1], passenger[2], passenger[3], passenger[4]] for passenger in passengers if passenger[0] == ticket[0][0]],
            "booking_date": self.convert_date_format(ticket[0][6]),
            "price": ticket[0][7]
        }

    def delete_passenger(self, p_id: int, pnr: int):

        self.__cursor.execute(f"""
        DELETE FROM passengers WHERE p_id = {p_id};
        """)

        self.__cursor.execute(f"""
        SELECT *
        FROM passengers
        WHERE pnr = {pnr}
        """)

        pssgrs = self.__cursor.fetchall()

        if not pssgrs:
            self.__cursor.execute(f"""
            DELETE FROM tickets WHERE pnr = {pnr}
            """)

        return pssgrs

    def get_totalprice(self, passenger_details: dict):
        """Returns total price for a ticket"""
        price = 0
        for _ in passenger_details['passengers']:
            price += self.__price

        return price

    def get_train_details(self):
        """Returns list of all trains available and stations they cover"""
        self.__cursor.callproc("trains_info")
        for result in self.__cursor.stored_results():
            trainDetails = result.fetchall()
        self.__cursor.execute(f"""
        SELECT * FROM
        trains""")
        trains = self.__cursor.fetchall()

        return [{
            "train_no": train[0],
            "train_name": train[1],
            "stations_list": [tr[1] for tr in trainDetails if train[0] == tr[0]],
            "arrival_times": [self.convert_time_format(tr[2]) for tr in trainDetails if train[0] == tr[0]],
            "depart_times": [self.convert_time_format(tr[3]) for tr in trainDetails if train[0] == tr[0]],
            "no_of_stations": len([tr[1] for tr in trainDetails if train[0] == tr[0]])
        } for train in trains]
