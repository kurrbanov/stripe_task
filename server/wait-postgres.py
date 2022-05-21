import os
import psycopg2
import time


def health_check():
    flag = False
    while not flag:
        try:
            psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("HOST"),
                port=5432
            )
            flag = True
        except psycopg2.Error:
            time.sleep(1)


if __name__ == '__main__':
    health_check()
