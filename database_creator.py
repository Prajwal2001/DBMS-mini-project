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
                password varchar(150) DEFAULT NULL,
                PRIMARY KEY (user_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS trains (
                train_no INT NOT NULL AUTO_INCREMENT,
                train_name varchar(25) NOT NULL,
                PRIMARY KEY (train_no)
        )""")

        cursor.execute(
            "INSERT INTO trains VALUES (1000, 'Janshatabdi Express'),(1001, 'Rani Chennamma Express'),(1002, 'Janshatabdi Exp'),(1003, 'Rani Chennamma Exp'),(1004, 'Lalbagh Express'),(1005, 'Brindavan Express'),(1006, 'Lalbagh Exp'),(1007, 'Brindavan Exp')")

        cursor.execute("""CREATE TABLE IF NOT EXISTS stations (
                stat_id int NOT NULL AUTO_INCREMENT,
                stat_name varchar(25) NOT NULL,
                stat_loc varchar(25) NOT NULL,
                PRIMARY KEY (stat_id)
        )""")

        cursor.execute(
            "INSERT INTO stations VALUES (210,'KSR Bengaluru','Bengaluru'),(211,'YPR Yesvantapur','Yesvantapur'),(212,'Tumkur','Tumkuru'),(213,'Arsikere Jn','Arsikere'),(214,'Davangere','Davangere'),(215,'Harihara','Harihara'),(216,'Ranibennur','RaniBennur'),(217,'Hubli Jn','Hubli'),(219,'Bengaluru Cant','Bengaluru Cant'),(220,'Baiyyappanahalli','Baiyyappanahalli'),(221,'KR Puram','KR Puram'),(222,'Malur','Malur'),(223,'Bangarpete','Bangarpete'),(224,'Champion','Champion Reef'),(225,'Oorgaum','Oorgaum');")

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
        cursor.execute("INSERT INTO `covers` VALUES (210, 1000, '05:30:00', '06:00:00', 0, 1),(211, 1000, '06:12:00', '06:20:00', 0, 2),(212, 1000, '07:02:00', '07:10:00', 0, 3),(213, 1000, '08:15:00', '08:20:00', 0, 4),(214, 1000, '10:15:00', '10:20:00', 0, 5),(215, 1000, '10:27:00', '10:30:00', 0, 6),(216, 1000, '10:48:00', '10:55:00', 0, 7),(217, 1000, '12:00:00', '12:30:00', 0, 8),(210, 1001, '21:30:00', '22:05:00', 0, 1),(211, 1001, '22:17:00', '22:20:00', 0, 2),(212, 1001, '23:07:00', '23:10:00', 0, 3),(213, 1001, '00:30:00', '00:35:00', 1, 4),(214, 1001, '02:35:00', '02:40:00', 1, 5),(215, 1001, '02:55:00', '03:00:00', 1, 6),(216, 1001, '03:15:00', '03:20:00', 1, 7),(217, 1001, '05:45:00', '06:15:00', 1, 8),(217, 1002, '13:00:00', '13:40:00', 0, 1),(216, 1002, '15:07:00', '15:09:00', 0, 2),(215, 1002, '15:29:00', '15:31:00', 0, 3),(214, 1002, '15:45:00', '15:47:00', 0, 4),(213, 1002, '17:45:00', '17:50:00', 0, 5),(212, 1002, '19:08:00', '19:10:00', 0, 6),(211, 1002, '20:15:00', '20:17:00', 0, 7),(210, 1002, '21:00:00', '21:30:00', 0, 8),(217, 1003, '22:20:00', '22:30:00', 0, 1),(216, 1003, '00:08:00', '00:10:00', 1, 2),(215, 1003, '00:29:00', '00:31:00', 1, 3),(214, 1003, '00:48:00', '00:50:00', 1, 4),(213, 1003, '03:03:00', '03:05:00', 1, 5),(212, 1003, '04:28:00', '04:30:00', 1, 6),(211, 1003, '05:50:00', '05:52:00', 1, 7),(210, 1003, '06:30:00', '06:45:00', 1, 8),(210, 1004, '18:00:00', '18:05:00', 0, 1),(219, 1004, '18:14:00', '18:16:00', 0, 2),(220, 1004, '18:26:00', '18:28:00', 0, 3),(221, 1004, '18:32:00', '18:34:00', 0, 4),(222, 1004, '19:02:00', '19:04:00', 0, 5),(223, 1004, '19:51:00', '19:55:00', 0, 6),(224, 1004, '20:18:00', '20:20:00', 0, 7),(225, 1004, '21:10:00', '21:30:00', 0, 8),(210, 1005, '19:00:00', '19:05:00', 0, 1),(219, 1005, '19:14:00', '19:16:00', 0, 2),(220, 1005, '19:26:00', '19:28:00', 0, 3),(221, 1005, '19:32:00', '19:34:00', 0, 4),(222, 1005, '20:02:00', '20:04:00', 0, 5),(223, 1005, '20:51:00', '20:55:00', 0, 6),(224, 1005, '21:18:00', '21:20:00', 0, 7),(225, 1005, '22:10:00', '22:30:00', 0, 8),(210, 1006, '21:00:00', '21:05:00', 0, 8),(219, 1006, '21:14:00', '21:16:00', 0, 7),(220, 1006, '21:26:00', '21:28:00', 0, 6),(221, 1006, '21:32:00', '21:34:00', 0, 5),(222, 1006, '22:02:00', '22:04:00', 0, 4),(223, 1006, '22:51:00', '22:55:00', 0, 3),(224, 1006, '23:18:00', '23:20:00', 0, 2),(225, 1006, '00:10:00', '00:30:00', 1, 1),(210, 1007, '23:00:00', '23:05:00', 0, 8),(219, 1007, '23:14:00', '23:16:00', 0, 7),(220, 1007, '23:26:00', '23:28:00', 0, 6),(221, 1007, '23:32:00', '23:34:00', 0, 5),(222, 1007, '00:02:00', '00:04:00', 1, 4),(223, 1007, '00:51:00', '00:55:00', 1, 3),(224, 1007, '01:18:00', '01:20:00', 1, 2),(225, 1007, '02:10:00', '02:30:00', 1, 1)")

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
