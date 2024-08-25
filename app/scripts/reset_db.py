import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.database import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def reset_database():
    db = SessionLocal()

    try:
        db.execute(
            text(
                "TRUNCATE TABLE candidates, applications, opportunities RESTART IDENTITY CASCADE;"
            )
        )
        db.commit()

        print("Database has been reset successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    reset_database()
