from starlette.config import Config
from sqlalchemy.orm import declarative_base


class Settings:
    # .env 로드
    env_file = Config(".env")

    # SQLAlchemy Base metadata
    METADATA = declarative_base().metadata

    # DB URL (PyMySQL 사용)
    MYSQL_VIEW = (
        f"mysql+pymysql://"
        f"{env_file.get('DBUSER')}:"
        f"{env_file.get('PASSWORD')}@"
        f"{env_file.get('HOST')}:"
        f"{env_file.get('PORT')}/"
        f"{env_file.get('DATABASE')}"
    )

    # (옵션) MariaDB도 같은 방식으로 사용 가능
    # MARIADB_VIEW = (
    #     f"mysql+pymysql://"
    #     f"{env_file.get('DBUSER2')}:"
    #     f"{env_file.get('PASSWORD2')}@"
    #     f"{env_file.get('HOST2')}:"
    #     f"{env_file.get('PORT2')}/"
    #     f"{env_file.get('DATABASE2')}"
    # )

    # (옵션) CORS 설정
    # CORS_ORIGINS = (
    #     env_file.get('CORS_TRUSTED_ORIGINS1') +
    #     env_file.get('CORS_TRUSTED_ORIGINS2')
    # ).split(',')

    # (옵션) 시간 설정
    # TIMEDELTA_SETTING = int(env_file.get('TIMEDELTA_SETTING'))


# Settings instance
settings = Settings()