import sqlite3


class Database:
    connection = None
    def __init__(self, dbname : str):
        connection = sqlite3.connect(dbname, check_same_thread=False)
        with connection:
            connection.execute("""
                     CREATE TABLE IF NOT EXISTS `company` (
            `id` integer PRIMARY KEY AUTOINCREMENT,
            `name` char(45) DEFAULT NULL ) 
                  """)

            connection.execute("""
                     CREATE TABLE IF NOT EXISTS `data` (
            `id` integer PRIMARY KEY AUTOINCREMENT,
            `Qoil` integer DEFAULT 0,
            `Qliq` integer DEFAULT 0,
            `comp_id`integer DEFAULT 0,
            `Type` char(10) DEFAULT NULL,
            `Date` date ) 
                  """)
        self.connection = connection

    def get_comp_id(self, comp_name : str):
        cur = self.connection.cursor()
        cur.execute(f"SELECT id FROM company where name='{comp_name}'")
        rows = cur.fetchone()
        return rows[0] if rows else -1

    def truncate_data(self):
        self.connection.execute("""
            DELETE FROM data
        """)
        self.connection.commit()

    def delete_company(self, company : str):
        comp_id = self.get_comp_id(comp_name=company)
        if comp_id > -1:
            self.connection.execute(f"""
                DELETE FROM data WHERE comp_id = {comp_id}
            """)
            self.connection.execute(f"""
                DELETE FROM company WHERE id = {comp_id}
            """)
            self.connection.commit()

    def add_data(self,company : str,type : str, qliq : list, qoil : list, dt : str):
        if len(qliq) != len(qoil):
            return -1 # Some mismatch in the input file
        comp_id = self.get_comp_id(comp_name=company)
        if comp_id == -1:
            self.connection.execute(f"""
                INSERT INTO company(name) VALUES ('{company}') 
            """)
            self.connection.commit()
            comp_id = self.get_comp_id(comp_name=company)

        for i, qliq_ in enumerate(qliq):
            self.connection.execute(f"""
                INSERT INTO data(Qoil,Qliq,Type,comp_id,date) VALUES ({qoil[i]},{qliq_},'{type}',{comp_id},'{dt}') 
            """)
        self.connection.commit()
        return 0

    def print_total(self):
        cur = self.connection.cursor()
        cur.execute(f"SELECT data.Date, sum(data.Qoil) as QoilTotal, sum(data.Qliq) as QliqTotal\
        FROM company, data \
        WHERE company.id = data.comp_id\
        GROUP BY data.Date\
        ORDER BY data.Date;")
        rows = cur.fetchall()
        rows.insert(0,("Date", "Total Qoil", "Total Qliq "))
        return rows
