from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    '''
    Application settings model.

    Attributes:
        sqlalchemy_database_url (str): URL for the SQLAlchemy database connection.
        secret_key (str): Secret key for generating tokens.
        algorithm (str): Algorithm for token encryption.
        mail_username (str): Username for SMTP email server.
        mail_password (str): Password for SMTP email server.
        mail_from (str): Email address used as the sender for outgoing emails.
        mail_port (int): Port number for the SMTP email server.
        mail_server (str): SMTP email server address.
        redis_host (str, optional): Hostname or IP address of the Redis server. Defaults to 'localhost'.
        redis_port (int, optional): Port number of the Redis server. Defaults to 6379.
        postgres_db (str): PostgreSQL database name.
        postgres_user (str): PostgreSQL database user.
        postgres_password (str): PostgreSQL database password.
        postgres_port (int): PostgreSQL database port.
        cloudinary_name (str): Cloudinary account name.
        cloudinary_api_key (str): Cloudinary API key.
        cloudinary_api_secret (str): Cloudinary API secret.
    '''
    
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

