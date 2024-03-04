from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

class Settings(SettingsBase):
    dbms_name: str = ""
    dbms_driver: str = ""
    database_hostname: str = ""
    database_port: int = 0
    database_password: str = ""
    database_name: str = ""
    database_username: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    jwt_access_token_expire_minutes: int = 0