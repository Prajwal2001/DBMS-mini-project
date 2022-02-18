import mysql.connector
import yaml


with open('./credentials.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def create_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user=data["user"],
        password=data["password"],
        autocommit=True
    )

    mydb.cursor().execute("CREATE DATABASE IF NOT EXISTS railways")

    mydb = mysql.connector.connect(
        host="localhost",
        user=data["user"],
        password=data["password"],
        database=data["database"],
        autocommit=True
    )

    cursor = mydb.cursor()

    cursor.execute("SHOW TABLES")

    if not cursor.fetchall():

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id int NOT NULL AUTO_INCREMENT,
                user_name varchar(25) NOT NULL UNIQUE,
                email varchar(30) NOT NULL UNIQUE,
                password varchar(50) DEFAULT NULL,
                PRIMARY KEY (user_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS trains (
                train_no INT NOT NULL AUTO_INCREMENT,
                train_name varchar(25) NOT NULL,
                PRIMARY KEY (train_no)
        )""")

        cursor.execute(
                "INSERT INTO trains VALUES(1000, 'A-train'), (1002, 'C-train'), (1003, 'B-train')")

        cursor.execute("""CREATE TABLE IF NOT EXISTS stations (
                stat_id int NOT NULL AUTO_INCREMENT,
                stat_name varchar(25) NOT NULL,
                stat_loc varchar(25) NOT NULL,
                PRIMARY KEY (stat_id)
        )""")

        cursor.execute(
                "INSERT INTO stations VALUES (200,'A','A'),(201,'B','B'),(202,'C','C'),(203,'D','D'),(204,'E','E'),(205,'F','F'),(206,'G','G'),(207,'H','H'),(208,'I','I')")

        cursor.execute("""CREATE TABLE IF NOT EXISTS covers (
                stat_id int NOT NULL,
                train_no int NOT NULL,
                arrival_time time NOT NULL,
                depart_time time NOT NULL,
                days int NOT NULL DEFAULT '0',
                seq_no int NOT NULL,
                FOREIGN KEY (stat_id) REFERENCES stations (stat_id) ON DELETE CASCADE,
                FOREIGN KEY (train_no) REFERENCES trains (train_no) ON DELETE CASCADE
        )""")
        cursor.execute("INSERT INTO `covers` VALUES (200,1000,'00:30:00','00:31:00',0,1),(201,1000,'01:00:00','01:01:00',0,2),(202,1000,'02:00:00','02:01:00',0,3),(203,1000,'03:00:00','03:01:00',0,4),(204,1000,'04:00:00','04:01:00',0,5),(205,1000,'05:00:00','05:01:00',0,6),(206,1000,'06:00:00','06:01:00',0,7),(208,1002,'08:00:00','08:01:00',0,1),(206,1002,'09:00:00','09:01:00',0,2),(205,1002,'10:00:00','10:01:00',0,3),(203,1002,'11:00:00','11:01:00',0,4),(202,1002,'12:00:00','12:01:00',0,5),(201,1002,'13:00:00','13:01:00',0,6),(200,1002,'14:00:00','14:01:00',0,7),(200,1003,'20:00:00','20:01:00',0,1),(201,1003,'21:00:00','21:01:00',0,2),(202,1003,'22:00:00','22:01:00',0,3),(203,1003,'23:00:00','23:01:00',0,4),(204,1003,'00:00:00','00:01:00',1,5),(205,1003,'01:00:00','01:01:00',1,6),(206,1003,'02:00:00','02:01:00',1,7)")

        cursor.execute("""CREATE TABLE IF NOT EXISTS tickets (
                pnr int NOT NULL AUTO_INCREMENT,
                from_station int NOT NULL,
                to_station int NOT NULL,
                booking_date date NOT NULL,
                travel_date date NOT NULL,
                user_id int NOT NULL,
                train_no int NOT NULL,
                price int DEFAULT NULL,
                PRIMARY KEY (pnr),
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (train_no) REFERENCES trains (train_no) ON DELETE CASCADE,
                FOREIGN KEY (from_station) REFERENCES stations (stat_id) ON DELETE CASCADE,
                FOREIGN KEY (to_station) REFERENCES stations (stat_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS passengers (
                p_id int NOT NULL AUTO_INCREMENT,
                p_name varchar(25) NOT NULL,
                p_age int NOT NULL,
                seat_no int NOT NULL,
                pnr int NOT NULL,
                PRIMARY KEY (p_id),
                FOREIGN KEY (pnr) REFERENCES tickets (pnr) ON DELETE CASCADE
        )""")

        cursor.execute("DROP VIEW IF EXISTS all_train_info")

        cursor.execute("""CREATE VIEW all_train_info AS
                SELECT t.train_no AS train_no, t.train_name AS train_name, s.stat_name AS stat_name, c.arrival_time AS arrival_time, c.depart_time AS depart_time, c.seq_no AS seq_no
                FROM ((trains t JOIN stations s)
                    JOIN covers c ON (((t.train_no = c.train_no) and (s.stat_id = c.stat_id))))""")

        cursor.execute("DROP VIEW IF EXISTS available_seats")

        cursor.execute("""CREATE VIEW available_seats AS
                SELECT t.pnr AS pnr, t.travel_date AS travel_date, tr.train_no AS train_no, COUNT(p.p_id) AS no_of_seats, MAX(p.seat_no) AS seats_reserved
                FROM ( trains tr LEFT JOIN ( tickets t JOIN passengers p ON ((t.pnr = p.pnr))) ON ((t.train_no = tr.train_no)))
                GROUP BY t.pnr
                ORDER BY t.pnr""")

        cursor.execute("DROP PROCEDURE IF EXISTS get_passengers")

        cursor.execute("""CREATE PROCEDURE get_passengers (p int)
                BEGIN
                SELECT T.pnr, p_name, p_age, seat_no
                FROM tickets T JOIN users U ON T.user_id = U.user_id
                    JOIN trains TR ON T.train_no = TR.train_no
                    JOIN passengers P ON P.pnr = T.pnr, stations A, stations B
                WHERE T.pnr = p AND 
                    A.stat_id IN (
                        SELECT from_station
                        FROM tickets
                        WHERE pnr = p
                    ) AND 
                    B.stat_id IN (
                        SELECT to_station
                        FROM tickets
                        WHERE pnr = p
                    )
                ORDER BY seat_no;
                END""")

        cursor.execute("DROP PROCEDURE IF EXISTS get_tickets")

        cursor.execute("""CREATE PROCEDURE get_tickets (p int)
                BEGIN
                SELECT T.pnr, travel_date, T.train_no, TR.train_name, A.stat_loc, B.stat_loc, booking_date, T.price
                FROM tickets T JOIN users U on T.user_id = U.user_id 
                    JOIN trains TR on T.train_no = TR.train_no, stations A, stations B
                WHERE T.pnr = p
                AND A.stat_id IN (
                    SELECT from_station
                    FROM tickets
                    WHERE pnr = p
                    ) AND 
                    B.stat_id IN (
                    SELECT to_station
                    FROM tickets
                    WHERE pnr = p
                )
                ORDER BY travel_date;
                END""")

        cursor.execute("DROP PROCEDURE IF EXISTS trains_info")

        cursor.execute("""CREATE PROCEDURE trains_info ()
                BEGIN
                SELECT train_no, stat_name, arrival_time, depart_time
                FROM all_train_info
                ORDER BY train_no, seq_no;
                END""")
