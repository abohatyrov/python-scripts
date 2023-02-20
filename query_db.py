import psycopg2

class PostgresDatabase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except psycopg2.Error as e:
            print("Error connecting to database: {}".format(e))
            return None

    def query(self, sql_query):
        conn = self.connect()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                return rows
            except psycopg2.Error as e:
                print("Error executing query: {}".format(e))
            finally:
                cursor.close()
                conn.close()
        else:
            print("Failed to connect to database.")

# Example usage:
database = PostgresDatabase(
    host='localhost',
    port=5432,
    database='my_database',
    user='my_user',
    password='my_password'
)

result = database.query('SELECT * FROM my_table')
print(result)
