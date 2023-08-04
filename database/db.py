from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'your_username', 'your_password', 'your_host', 'your_database' with actual PostgreSQL details
DATABASE_URL = "postgresql://postgres:password@localhost:5432/reddit_scraper_1"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    post_title = Column(String(255))
    permalink = Column(String(255))
    subreddit = Column(String(100))
    author = Column(String(100))
    num_comments = Column(Integer)
    post_score = Column(Integer)
    post_content = Column(Text)
    time_stamp = Column(TIMESTAMP)

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Now you can use the session to add, query, and manipulate Post objects

