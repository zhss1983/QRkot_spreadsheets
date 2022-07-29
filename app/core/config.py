from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "Благотворительного фонда поддержки котиков QRKot."
    path: str = "./"
    database_url: str = "sqlite+aiosqlite:///./QRKot.db"
    secret: str = "dvlkdfnkaskjs+cku#guo876t8higy*&T&bljviu6gIUI&T&^*kjhfytgkj"
    first_superuser_email: Optional[EmailStr] = "root@mail.ru"
    first_superuser_password: Optional[str] = "root0000"
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
