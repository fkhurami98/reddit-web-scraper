import os
import json
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import inspect


def insert_to_db(database_url, json_folder_path):
    """
    Main function to create table if not exists and insert data from JSON files.

    Args:
        database_url: Database connection URL.
        json_folder_path: Path to the folder containing JSON files.
    """
    # Create the engine
    engine = create_engine(database_url)

    # Declarative base for ORM
    Base = declarative_base()

    # Define the Post class
    class Post(Base):
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

    class Comments(Base):
        __tablename__ = "comments"

        id = Column(Integer, primary_key=True)
        comment_text = Column(Text)
        permalink = Column(Text, ForeignKey("posts.permalink"))
        post = relationship("Post", back_populates="comments")

    # Session creation
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the table exists, create it if not
    inspector = inspect(engine)  # Create an inspector for the engine
    if not inspector.has_table("posts"):  # Use the inspector to check table existence
        Base.metadata.create_all(engine)

    # Iterate through JSON files
    for json_file_name in os.listdir(json_folder_path):
        json_file_path = os.path.join(json_folder_path, json_file_name)

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Insert data into the database
        for post_data in data:
            permalink = post_data.get("Permalink")
            existing_post = session.query(Post).filter_by(permalink=permalink).first()

            if existing_post is None:
                post = Post(
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


if __name__ == "__main__":
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/reddit_scraper_1"
    JSON_FOLDER_PATH = "subreddit_page_data"
    insert_to_db(DATABASE_URL, JSON_FOLDER_PATH)
