import hashlib
import mysql.connector
import yaml
from pprint import pprint
from datetime import timedelta, date, datetime
from random import randint


class Database:
    """Used to connect Database"""

    def __init__(self):
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

    def add_user(self, user: list):
        """Adds a user_id to the database, by accepting a list consisting of username, password and email.
        And returns the updated table values in a list of key value pairs"""
        u_name, email, password = user

        try:
            self.__cursor.execute(
                f"INSERT iNTO users VALUES (null, '{u_name}', '{email}', '{hashlib.md5(password.encode()).hexdigest()}')")
        except mysql.connector.errors.IntegrityError:
            return None

        self.__cursor.execute(f"SELECT * FROM users")

        return [{
            "user_id": userData[0],
            "user_name": userData[1],
            "email": userData[2],
            "password": userData[3]
        } for userData in self.__cursor.fetchall()]

    def does_user_exist(self, userData: list):
        """Checks if the user_id exists in the database"""
        self.__cursor.execute(
            f"""SELECT *
                FROM users
                WHERE user_name = '{userData[0]}' AND
                password = '{hashlib.md5(userData[1].encode()).hexdigest()}'"""
        )
        result = self.__cursor.fetchall()
        return result

    def get_user_id_by_user_name(self, userName):
        """Returns user_id for given user_name"""
        self.__cursor.execute(f"""
            SELECT *
            FROM users
            WHERE user_name = '{userName}';
            """)
        res = self.__cursor.fetchall()
        return res[0][0] if res else None

    def convert_date_format(self, date):
        date = str(date).split('-')
        return f"{date[-1]}-{date[-2]}-{date[-3]}"

    def calculate_reaching_date(self, days, travellingDate):
        temp = travellingDate.split('-')
        travellingDate = date(int(temp[2]), int(temp[1]), int(temp[0]))
        travellingDate = travellingDate + timedelta(int(days))
        return self.convert_date_format(travellingDate)

    def convert_time_format(self, time):
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
        self.__cursor.execute("SELECT stat_name FROM stations")
        return [station[0] for station in self.__cursor.fetchall()]

    def get_trains(self, sourceName, destinationName):
        trains_list = []
        self.__cursor.execute(
            f"""
            SELECT A.stat_id, B.stat_id
            FROM stations A, stations B
            WHERE A.stat_name = '{sourceName}' AND
                B.stat_name = '{destinationName}';""")
        source, destination = self.__cursor.fetchall()[0]
        self.__cursor.execute('SELECT train_no FROM trains')
        train_nos = self.__cursor.fetchall()
        for trainNo in train_nos:
            self.__cursor.execute(
                f"""SELECT seq_no, arrival_time
                FROM covers
                WHERE train_no = {trainNo[0]} AND stat_id = {destination};""")
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
                    f"SELECT train_name FROM trains WHERE train_no = {trainNo[0]}")
                trainName = self.__cursor.fetchall()[0][0]
                trains_list.append({
                    "train_no": trainNo[0],
                    "train_name": trainName,
                    "source": sourceName,
                    "destination": destinationName,
                    "arrival_time": self.convert_time_format(arrivalTime),
                    "departure_time": self.convert_time_format(departureTime),
                    "reaching_time": self.convert_time_format(reachingTime),
                    "price": self.__price,
                })
        return trains_list

    def add_passengers_ticket(self, passengerDetails):
        self.__cursor.execute(f"""
        SELECT A.stat_id, B.stat_id
        FROM stations A, stations B
        WHERE A.stat_name='{passengerDetails['source']}' AND
        B.stat_name='{passengerDetails['destination']}'
        """)
        stations = self.__cursor.fetchall()

        travelDateList = str(passengerDetails['travel_date']).split('-')

        self.__cursor.execute(
            f"""INSERT INTO tickets VALUES (null, {stations[0][0]}, {stations[0][1]}, '{datetime.today().year}-{datetime.today().month}-{datetime.today().day}', '{travelDateList[0]}-{travelDateList[1]}-{travelDateList[2]}', {passengerDetails['user_id']}, {passengerDetails['train_no']}, null)""")

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
        seat_no = randint(1, 500)
        self.__totalPrice = 0

        for passenger in passengerDetails['passengers']:
            self.__cursor.execute(
                f"""INSERT INTO passengers VALUES (null, '{passenger['p_name']}', {passenger['p_age']}, {seat_no}, {pnr})""")
            self.__totalPrice += self.__price
            print("\n\n", self.__totalPrice)
            seat_no += 1
        self.__cursor.execute(
            f"""UPDATE tickets SET price={self.__totalPrice} WHERE pnr={pnr}""")

    def cancel_ticket(self, pnr):
        self.__cursor.execute(f"""DELETE FROM tickets WHERE pnr = {pnr}""")

    def get_totalprice(self, passenger_details):
        price = 0
        for _ in passenger_details['passengers']:
            price += self.__price

        return price

    def get_train_details(self):
        self.__cursor.callproc("trains_info")
        for result in self.__cursor.stored_results():
            trainDetails = result.fetchall()
        trainNos = []
        for tr in [train[0] for train in trainDetails]:
            if tr not in trainNos:
                trainNos.append(tr)
        trainNames = []
        for tr in [train[1] for train in trainDetails]:
            if tr not in trainNames:
                trainNames.append(tr)

        return [{
            "train_no": trainNos[i],
            "train_name": trainNames[i],
            "stations_list": [tr[2] for tr in trainDetails if trainNos[i] == tr[0]],
            "arrival_times": [self.convert_time_format(tr[3]) for tr in trainDetails if trainNos[i] == tr[0]],
            "depart_times": [self.convert_time_format(tr[4]) for tr in trainDetails if trainNos[i] == tr[0]],
            "no_of_stations": len([tr[2] for tr in trainDetails if trainNos[i] == tr[0]])
        } for i in range(len(trainNos))]


# DATE_SUB(CURDATE(), INTERVAL 1 DAY)

# SELECT
# T.pnr,
# p_name,
# p_age,
# seat_no
# FROM
# tickets T
# JOIN users U on T.user_id = U.user_id
# JOIN trains TR on T.train_no = TR.train_no
# join passengers P on P.pnr = T.pnr,
# stations A,
# stations B
# WHERE
# T.pnr = p
# AND A.stat_id IN(
#     SELECT
#     from_station
#     FROM
#     tickets
#     WHERE
#     pnr=p
# )
# AND B.stat_id IN(
#     SELECT
#     to_station
#     FROM
#     tickets
#     WHERE
#     pnr=p
# )
# ORDER BY
# seat_no


# SELECT
# T.pnr,
# travel_date,
# T.train_no,
# TR.train_name,
# A.stat_loc,
# B.stat_loc,
# booking_date,
# T.price
# FROM
# tickets T
# JOIN users U on T.user_id = U.user_id
# JOIN trains TR on T.train_no = TR.train_no,
# stations A,
# stations B
# WHERE
# T.pnr = p
# AND A.stat_id IN(
#     SELECT
#     from_station
#     FROM
#     tickets
#     WHERE
#     pnr=p
# )
# AND B.stat_id IN(
#     SELECT
#     to_station
#     FROM
#     tickets
#     WHERE
#     pnr=p
# )
# ORDER BY
# travel_date

# SELECT
# train_no,
# train_name,
# stat_name,
# arrival_time,
# depart_time
# FROM
# all_train_info
# ORDER BY
# train_no,
# seq_no
