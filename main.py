#! python

from pydantic import BaseSettings, EmailStr

from secrets import LoadSecrets

app_secret = LoadSecrets('./secrets')

class Settings(BaseSettings):
    app_title: str = "Благотворительного фонда поддержки котиков QRKot."
    path: str = "./"
    database_url: str = "sqlite+aiosqlite:///./QRKot.db"
    secret: str = app_secret.secret
    first_superuser_email: EmailStr | None = app_secret.first_superuser_email
    first_superuser_password: str | None = app_secret.first_superuser_password
    type: str | None = app_secret.type
    project_id: str | None = app_secret.project_id
    private_key_id: str | None = app_secret.private_key_id
    private_key: str | None = app_secret.private_key
    client_email: str | None = app_secret.client_email
    client_id: str | None = app_secret.client_id
    auth_uri: str | None = app_secret.auth_uri
    token_url: str | None = app_secret.token_url
    auth_provider_x509_cert_url:str | None = app_secret.auth_provider_x509_cert_url
    client_x509_cert_url: str | None = app_secret.client_x509_cert_url
    email: str | None = app_secret.email

    class Config:
        env_file = ".env"


settings = Settings()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
