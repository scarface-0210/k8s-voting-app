import json
import os
import time

import psycopg2
import redis

REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "redis"
)

DB_HOST = os.getenv(
    "DB_HOST",
    "postgres"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "voting"
)

DB_USER = os.getenv(
    "DB_USER",
    "voting"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "voting"
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)


def get_db_connection():

    return psycopg2.connect(

        host=DB_HOST,

        database=DB_NAME,

        user=DB_USER,

        password=DB_PASSWORD

    )


def initialize_database():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS votes (

            id SERIAL PRIMARY KEY,

            choice VARCHAR(10) NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    cursor.close()

    conn.close()


def process_vote(vote):

    choice = vote["choice"]

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO votes (choice)
        VALUES (%s)
        """,

        (choice,)

    )

    conn.commit()

    cursor.close()

    conn.close()

    redis_client.hincrby(
        "results",
        choice,
        1
    )


def main():

    print("Worker starting...")

    while True:

        try:

            initialize_database()

            break

        except Exception as error:  # noqa: BLE001

            print(
                f"Database unavailable: {error}"
            )

            time.sleep(5)


    print("Worker ready.")

    while True:

        try:

            result = redis_client.blpop(
                "votes",
                timeout=5
            )

            if result is None:

                continue

            _, vote_data = result

            vote = json.loads(
                vote_data
            )

            print(
                f"Processing vote: {vote}"
            )

            process_vote(vote)

        except Exception as error:  # noqa: BLE001

            print(
                f"Worker error: {error}"
            )

            time.sleep(2)


if __name__ == "__main__":

    main()
