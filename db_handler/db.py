import os
import csv
import json
from sqlalchemy import (
    create_engine,
    text,
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    post_title = Column(Text)
    permalink = Column(Text, unique=True)
    subreddit = Column(String(100))
    author = Column(String(100))
    num_comments = Column(Integer)
    post_score = Column(Integer)
    post_content = Column(Text)
    time_stamp = Column(TIMESTAMP)


def insert_to_db(database_url: str, json_folder_path: str):
    """
    function to create table if not exists and insert data from JSON files.

    Args:
        database_url (str): Database connection URL.
        json_folder_path (str): Path to the folder containing JSON files.
    """
    # Create the engine
    engine = create_engine(database_url)

    # Session creation
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the table exists, create it if not
    inspector = inspect(engine)
    if not inspector.has_table(
        "posts", "comments"
    ):  # Use the inspector to check table existence
        Base.metadata.create_all(engine)

    # Iterate through JSON files
    for json_file_name in os.listdir(json_folder_path):
        json_file_path = os.path.join(json_folder_path, json_file_name)

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Insert data into the database
        for post_data in data:
            permalink = post_data.get("Permalink")
            existing_post = session.query(Posts).filter_by(permalink=permalink).first()

            if existing_post is None:
                post = Posts(
                    post_title=post_data.get("Post Title"),
                    permalink=permalink,
                    subreddit=post_data.get("Subreddit"),
                    author=post_data.get("Author"),
                    num_comments=post_data.get("Number of Comments"),
                    post_score=post_data.get("Post Score"),
                    post_content=post_data.get("Post Content"),
                    time_stamp=post_data.get("Time Stamp"),
                )
                session.add(post)

        # Commit changes after processing each JSON file
        session.commit()

    # Close the session
    session.close()


def get_column_from_table(column: str, table: str):
    """
    Retrieve a specific column from a database table.

    Args:
        column (str): The name of the column to retrieve.
        table (str): The name of the table from which to retrieve the column.

    Returns:
        column_values (list): A list containing the values of the specified column.
    """
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/reddit_scraper_1"

    engine = create_engine(DATABASE_URL)

    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = text(f"SELECT {column} FROM {table};")

    result = session.execute(stmt)
    column_values = [row.permalink for row in result]

    session.close()

    return column_values


if __name__ == "__main__":
    permalink_list = get_column_from_table(column="permalink", table="posts")

    # Get the current directory
    current_directory = os.getcwd()

    # Specify the file path in the current directory
    file_path = "output.csv"

    # Open the CSV file in write mode
    with open(file_path, "w", newline="") as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # Write the header row (optional)
        csv_writer.writerow(["Permalink"])

        # Write each item from the list as a row in the CSV file
        for permalink in permalink_list:
            csv_writer.writerow([permalink])