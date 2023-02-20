import psycopg2
import pandas as pd

class PostgresETL:
    
    def __init__(self, source_conn_string, dest_conn_string):
        self.source_conn_string = source_conn_string
        self.dest_conn_string = dest_conn_string
        
    def extract(self, query):
        conn = psycopg2.connect(self.source_conn_string)
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    
    def transform(self, data, transform_func):
        return transform_func(data)
    
    def load(self, data, table_name):
        conn = psycopg2.connect(self.dest_conn_string)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(f"CREATE TABLE {table_name} ({', '.join(data.columns)});")
        for i, row in data.iterrows():
            sql = f"INSERT INTO {table_name} ({', '.join(data.columns)}) VALUES ({', '.join(['%s' for i in range(len(row))])})"
            cur.execute(sql, tuple(row))
        conn.commit()
        conn.close()

# Example usage:
etl = PostgresETL('postgresql://user:password@localhost:5432/source_db', 
                  'postgresql://user:password@localhost:5432/dest_db')

# Extract data from source database
data = etl.extract('SELECT * FROM mytable')

# Transform data by squaring values in a specific column
def transform_func(df):
    df['new_column'] = df['old_column']**2
    return df
transformed_data = etl.transform(data, transform_func)

# Load transformed data into destination database
etl.load(transformed_data, 'mytable_transformed')
