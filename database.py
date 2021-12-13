import hashlib
import mysql.connector
import yaml
from datetime import timedelta, date


class Database:
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

    def add_user(self, user_id: list):
        """Adds a user_id to the database, by accepting a list consisting of username, password and email.
        And returns the updated table values in a list of key value pairs"""
        u_name, email, password = user_id

        try:
            self.__cursor.execute(
                f"insert into users values(null, '{u_name}', '{email}', '{hashlib.md5(password.encode()).hexdigest()}')")
        except mysql.connector.errors.IntegrityError:
            return None

        self.__cursor.execute(f"select * from users")

        return [{
            "user_id": item[0],
            "user_name": item[1],
            "email": item[2],
            "password": item[3]
        } for item in self.__cursor.fetchall()]

    def does_user_exist(self, user_id: list):
        """Checks if the user_id exists in the database"""
        self.__cursor.execute(
            f"""select * 
            from users 
            where user_name = '{user_id[0]}' and 
            password = '{hashlib.md5(user_id[1].encode()).hexdigest()}'""")
        res = self.__cursor.fetchall()
        return res

    def get_user_id_by_user_name(self, user_name):
        """Returns user_id for given user_name"""
        self.__cursor.execute(
            f"select * from users where user_name = '{user_name}'")
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
            f"select pnr from tickets where user_id = {user_id}")
        tickets_list = []
        for pnr in self.__cursor.fetchall():

            self.__cursor.execute(
                f"""select T.pnr, travel_date, T.train_no, TR.train_name, A.stat_loc, B.stat_loc, booking_date 
                from tickets T join users U on T.user_id = U.user_id join trains TR on T.train_no = TR.train_no, stations A, stations B 
                where T.pnr = { pnr[0] } and 
                A.stat_id in (select from_station from tickets where pnr = { pnr[0] }) and 
                B.stat_id in (select to_station from tickets where pnr = { pnr[0] });"""
            )
            ticket = self.__cursor.fetchall()

            self.__cursor.execute(
                f"""select T.pnr, p_name, p_age, seat_no 
                from tickets T join users U on T.user_id = U.user_id join trains TR on T.train_no = TR.train_no join passengers P on P.pnr = T.pnr , stations A, stations B 
                where T.pnr = { pnr[0] } and 
                A.stat_id in (select from_station from tickets where pnr = { pnr[0] }) and 
                B.stat_id in (select to_station from tickets where pnr = { pnr[0] });"""
            )
            passengers = self.__cursor.fetchall()

            self.__cursor.execute(
                f"select arrival_time, depart_time from covers where train_no = {ticket[0][2]} and stat_id = (select stat_id from stations where stat_loc = '{ticket[0][4]}')")
            source_timing = self.__cursor.fetchall()

            self.__cursor.execute(
                f"select arrival_time, days from covers where train_no = {ticket[0][2]} and stat_id = (select stat_id from stations where stat_loc = '{ticket[0][5]}')")
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
            f"SELECT stat_id FROM stations WHERE stat_name = '{source_name}';")
        source = self.__cursor.fetchall()[0][0]
        self.__cursor.execute(
            f"SELECT stat_id FROM stations WHERE stat_name = '{destination_name}';")
        destination = self.__cursor.fetchall()[0][0]
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
