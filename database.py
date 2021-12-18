import hashlib
import mysql.connector
import yaml
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
            "user_id": item[0],
            "user_name": item[1],
            "email": item[2],
            "password": item[3]
        } for item in self.__cursor.fetchall()]

    def does_user_exist(self, user_id: list):
        """Checks if the user_id exists in the database"""
        self.__cursor.execute(
            f"""SELECT * 
            FROM users 
            WHERE user_name = '{user_id[0]}' and 
            password = '{hashlib.md5(user_id[1].encode()).hexdigest()}'""")
        res = self.__cursor.fetchall()
        return res

    def get_user_id_by_user_name(self, user_name):
        """Returns user_id for given user_name"""
        self.__cursor.execute(f"""
            SELECT * 
            FROM users 
            WHERE user_name = '{user_name}';
            """)
        res = self.__cursor.fetchall()
        if res:
            return res[0][0]
        return None

    def convert_date_format(self, date):
        date = str(date).split('-')
        return f"{date[-1]}-{date[-2]}-{date[-3]}"

    def calculate_reaching_date(self, days, travelling_date):
        temp = travelling_date.split('-')
        travelling_date = date(int(temp[2]), int(temp[1]), int(temp[0]))
        travelling_date = travelling_date + timedelta(int(days))
        return self.convert_date_format(travelling_date)

    def get_tickets(self, user_id: int):
        """Returns tickets for given user_id"""

        self.__cursor.execute(
            f"""
            SELECT pnr 
            FROM tickets 
            WHERE user_id = {user_id}
            """)
        tickets_list = []
        for pnr in self.__cursor.fetchall():

            self.__cursor.execute(
                f"""SELECT T.pnr, travel_date, T.train_no, TR.train_name, A.stat_loc, B.stat_loc, booking_date 
                FROM tickets T join users U on T.user_id = U.user_id join trains TR on T.train_no = TR.train_no, stations A, stations B 
                WHERE T.pnr = { pnr[0] } and 
                    A.stat_id in (SELECT from_station FROM tickets WHERE pnr = { pnr[0] }) and 
                    B.stat_id in (SELECT to_station FROM tickets WHERE pnr = { pnr[0] })
                ORDER BY travel_date;"""
            )
            ticket = self.__cursor.fetchall()

            self.__cursor.execute(
                f"""SELECT T.pnr, p_name, p_age, seat_no 
                FROM tickets T join users U on T.user_id = U.user_id join trains TR on T.train_no = TR.train_no join passengers P on P.pnr = T.pnr , stations A, stations B 
                WHERE T.pnr = { pnr[0] } and 
                    A.stat_id in (SELECT from_station FROM tickets WHERE pnr = { pnr[0] }) and 
                    B.stat_id in (SELECT to_station FROM tickets WHERE pnr = { pnr[0] })
                ORDER BY p_name;"""
            )
            passengers = self.__cursor.fetchall()

            self.__cursor.execute(
                f"""
                SELECT arrival_time, depart_time 
                FROM covers 
                WHERE train_no = {ticket[0][2]} AND 
                    stat_id = (SELECT stat_id 
                                FROM stations
                                WHERE stat_loc = '{ticket[0][4]}')""")
            source_timing = self.__cursor.fetchall()

            self.__cursor.execute(
                f"""
                SELECT arrival_time, days 
                FROM covers 
                WHERE train_no = {ticket[0][2]} AND
                    stat_id = (SELECT stat_id 
                                FROM stations 
                                WHERE stat_loc = '{ticket[0][5]}')""")
            destination_timing = self.__cursor.fetchall()

            tickets_list.append(
                {
                    "pnr": ticket[0][0],
                    "travelling_date": self.convert_date_format(ticket[0][1]),
                    "train_no": ticket[0][2],
                    "train_name": ticket[0][3],
                    "from_station": ticket[0][4],
                    "to_station": ticket[0][5],
                    "passengers": [[passenger[1], passenger[2], passenger[3]] for passenger in passengers if passenger[0] == ticket[0][0]],
                    "booking_date": self.convert_date_format(ticket[0][6]),
                    "arrival_time": source_timing[0][0],
                    "depart_time": source_timing[0][1],
                    "reaching_time": destination_timing[0][0],
                    "reaching_date": self.calculate_reaching_date(destination_timing[0][1], self.convert_date_format(ticket[0][1]))
                }
            )

        return tickets_list

    def get_stations(self):
        self.__cursor.execute("SELECT stat_name FROM stations")
        return [station[0] for station in self.__cursor.fetchall()]

    def get_trains(self, source_name, destination_name):
        trains_list = []
        self.__cursor.execute(
            f"""
            SELECT A.stat_id, B.stat_id 
            FROM stations A, stations B 
            WHERE A.stat_name = '{source_name}' AND 
                B.stat_name = '{destination_name}';""")
        source, destination = self.__cursor.fetchall()[0]
        self.__cursor.execute('SELECT train_no FROM trains')
        train_nos = self.__cursor.fetchall()
        for train_no in train_nos:
            self.__cursor.execute(
                f"""SELECT seq_no, arrival_time 
                FROM covers 
                WHERE train_no = {train_no[0]} AND stat_id = {destination};""")
            destData = self.__cursor.fetchall()
            if destData:
                destData = destData[0]
            destSeqno = destData[0] if destData else None
            self.__cursor.execute(
                f"""SELECT seq_no, arrival_time, depart_time 
                FROM covers 
                WHERE train_no = {train_no[0]} AND stat_id = {source};""")
            sourceData = self.__cursor.fetchall()
            if sourceData:
                sourceData = sourceData[0]
            sourceSeqno = sourceData[0] if sourceData else None
            if sourceSeqno and destSeqno and sourceSeqno < destSeqno:
                self.__cursor.execute(
                    f"SELECT train_name FROM trains WHERE train_no = {train_no[0]}")
                train_name = self.__cursor.fetchall()[0][0]
                trains_list.append({
                    "train_no": train_no[0],
                    "train_name": train_name,
                    "source": source_name,
                    "destination": destination_name,
                    "arrival_time": sourceData[1],
                    "departure_time": sourceData[2],
                    "reaching_time": destData[1],
                })
        return trains_list

    def add_passengers_ticket(self, ticket_details):
        self.__cursor.execute(f"""
        SELECT A.stat_id, B.stat_id
        FROM stations A, stations B
        WHERE A.stat_name='{ticket_details['source']}' AND
        B.stat_name='{ticket_details['destination']}'
        """)
        stations = self.__cursor.fetchall()

        travel_date_list = str(ticket_details['travel_date']).split('-')

        print(travel_date_list)

        self.__cursor.execute(
            f"""INSERT INTO tickets VALUES (null, {stations[0][0]}, {stations[0][1]}, '{datetime.today().year}-{datetime.today().month}-{datetime.today().day}', '{travel_date_list[0]}-{travel_date_list[1]}-{travel_date_list[2]}', {ticket_details['user_id']}, {ticket_details['train_no']})""")
        self.__cursor.execute(f"""
        SELECT pnr
        FROM tickets
        WHERE from_station = '{stations[0][0]}' AND
            to_station = '{stations[0][1]}' AND
            booking_date = '{datetime.today().year}-{datetime.today().month}-{datetime.today().day}' AND
            travel_date = '{travel_date_list[0]}-{travel_date_list[1]}-{travel_date_list[2]}' AND
            user_id = {ticket_details['user_id']} AND
            train_no = {ticket_details['train_no']}
        """)
        pnr = int(self.__cursor.fetchall()[0][0])
        seat_no = randint(1, 500)
        for passenger in ticket_details['passengers']:
            self.__cursor.execute(
                f"""INSERT INTO passengers VALUES (null, '{passenger['p_name']}', {passenger['p_age']}, {seat_no}, {pnr})""")
            seat_no += 1

    def cancel_ticket(self, pnr):
        self.__cursor.execute(f"""DELETE FROM tickets WHERE pnr = {pnr}""")
