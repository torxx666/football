import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import httpx
import asyncio
import json
import psycopg2


class Etl:
    def __init__(self) -> None:
        self.parquet_filename = 'https://s3.amazonaws.com/aui-lab-data-engineer-resources/tweets/clubs-tweets.parquet'
        # self.parquet_filename = "clubs-tweets.parquet"
        self.db_config = {
            "dbname": "postgres",
            "user": "admin",
            "password": "pass123",
            "host": "0.0.0.0",
            "port": "5432",
        }

    def load_from_parquet(self):
        self.df = pd.read_parquet(self.parquet_filename)


    async def save_data(self, data_dict):
        conn = psycopg2.connect(**self.db_config)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        upsert_query = """
            INSERT INTO postgres.club_hashtags (club, country, hashtags, lenhash)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (club) DO UPDATE
            SET lenhash = club_hashtags.lenhash + %s
        """

        # Extract data from the dictionary
        club = data_dict.get("club")
        country = data_dict.get("country")
        hashtags = data_dict.get("hashtags")
        lenhash = data_dict.get("lenhash")

        # Execute the SQL query with data
        cursor.execute(upsert_query, (club, country, hashtags, lenhash, lenhash))

        # Commit the transaction
        conn.commit()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

    def get_data(self):
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT club,country,lenhash FROM postgres.club_hashtags   where  club='Barcelona'"
        )
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        cursor.close()
        conn.close()

    async def get_json_data(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=20.0)

            if response.status_code == 200:
                json_data = response.json()
                return json_data
            else:
                print(f"Error : {response.status_code}")
                return None

    async def get_club_details(self, club: int) -> list:
        def extract_text(json_str):
            try:
                data = json.loads(json_str.replace("'", '"'))
                hashtags = data.get("hashtags", [])
                text_values = [tag["text"] for tag in hashtags]
                return ",".join(text_values)
            except json.JSONDecodeError:
                return ""

        url = f"http://0.0.0.0:8000/get_users?user_ids={club}&skip=0"
        json_data = await self.get_json_data(url)
        current = self.df[self.df.user_id_str == club]
        hashtags = current["tweet_entities"].apply(extract_text).tolist()
        hashtags_txt = ",".join(hashtags)
        lenhash = len(hashtags)
        data_to_save = {
            "club": json_data[0]["club"],
            "country": json_data[0]["club_country"],
            "hashtags": hashtags_txt,
            "lenhash": lenhash,
        }
        await self.save_data(data_to_save)

    async def load_club_details(self):
        self.load_from_parquet()
        clubs = [value for value in self.df.user_id_str.unique()]

        with ThreadPoolExecutor() as executor:
            await asyncio.gather(
                *[self.get_club_details(club) for club in clubs]
            )



etl = Etl()
asyncio.run(etl.load_club_details())

# for testing purpose
etl.get_data()
