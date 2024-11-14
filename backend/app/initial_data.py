from sqlmodel import Session
from app.core.db import engine, init_db
from app.core.logger import logger



def init() -> None:
    """
    Initialize the database.

    This function creates a new session with the database engine and attempts to initialize the database
    by calling the `init_db` function. If the initialization is successful, it logs an info message.
    If an exception occurs during initialization, it logs the error and an error message indicating
    that the database initialization failed.

    Raises:
        Exception: If an error occurs during database initialization.
    """
    with Session(engine) as session:
        try:
            init_db(session)
            logger.info("Database initialized")
        except Exception as e:
            logger.error(e)
            logger.error("Database initialization failed")


def main() -> None:
    logger.info("creating initial data")
    init()
    logger.info("initial data created")


if __name__ == "__main__":
    main()
