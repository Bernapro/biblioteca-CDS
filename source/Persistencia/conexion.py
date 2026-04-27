import psycopg

def get_conn():
    return psycopg.connect(
        dbname="biblioteca_cds",
        user="postgres",
        password="unach2025",
        host="localhost",
        port="5432"
    )