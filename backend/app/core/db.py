from sqlmodel import Session, create_engine, select
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
from app.core.logger import logger
from app.models import User, UserCreate
from app import crud


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI()))
# If database does not exist, create it using SQLAlchemy Utils
if not database_exists(engine.url):
    logger.warning("Database does not exist. Creating database")
    create_database(engine.url)
    logger.info("Database created")


def init_db(session: Session) -> None:
    """
    Initialize the database with a superuser if it does not already exist.

    This function checks if a superuser with the email specified in the settings
    exists in the database. If not, it creates a new superuser using the details
    provided in the environment variables. Superuser password is hashed before
    storing it in the database using the security module.

    Args:
        session (Session): The database session used to execute queries and
                           perform operations.

    Returns:
        None
    """
    user = session.exec(
        # In future change this to select where is_super_admin == True
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()

    # If super admin does not exist, create it from details passed from .env to config
    if not user:
        logger.info(
            "SUPERUSER admin does not exist. Creating SUPERUSER from .env")
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_super_admin=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
        logger.info("SUPERUSER created")
