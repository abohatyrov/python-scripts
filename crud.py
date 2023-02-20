import psycopg2

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor()

    def execute(self, query, values=None):
        self.cur.execute(query, values)
        return self.cur.fetchall()

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s']*len(columns))})"
        self.cur.execute(query, values)
        self.conn.commit()
        return self.cur.rowcount

    def update(self, table, set_columns, set_values, condition_columns, condition_values):
        set_clause = ','.join([f"{column} = %s" for column in set_columns])
        condition_clause = ' AND '.join([f"{column} = %s" for column in condition_columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition_clause}"
        values = set_values + condition_values
        self.cur.execute(query, values)
        self.conn.commit()
        return self.cur.rowcount

    def delete(self, table, condition_columns, condition_values):
        condition_clause = ' AND '.join([f"{column} = %s" for column in condition_columns])
        query = f"DELETE FROM {table} WHERE {condition_clause}"
        self.cur.execute(query, condition_values)
        self.conn.commit()
        return self.cur.rowcount

    def __del__(self):
        self.cur.close()
        self.conn.close()
