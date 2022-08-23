# Благотворительный фонда поддержки котиков QRKot.

## Описание:
Фонд собирает пожертвования на различные целевые проекты: 
- на медицинское обслуживание нуждающихся хвостатых
- на обустройство кошачьей колонии в подвале
- на корм оставшимся без попечения кошкам
- на любые цели, связанные с поддержкой кошачьей популяции
- и т.д. и т.п.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.

Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

## Стек технологий:

**[Python 3](https://www.python.org/downloads/), 
 [FastAPI](https://fastapi.tiangolo.com/), 
 [SQLite3](https://www.sqlite.org/docs.html),
 [SQLAlchemy](https://www.sqlalchemy.org/),
 [Uvicorn](https://www.uvicorn.org/).**
 
 ## Установка:

```sh
git clone https://github.com/zhss1983/cat_charity_fund
cd cat_charity_fund
python3 -m venv env
source env/bin/activate
pip3 install -r requirement.txt
```

Необходимо заполнить файл переменных среды - .env

Пример заполнения:

```txt
APP_TITLE='Благотворительного фонда поддержки котиков QRKot.'
PATH=./
DATABASE_URL=sqlite+aiosqlite:///./QRKot.db
SECRET=*****************************************
FIRST_SUPERUSER_EMAIL=****@****.***
FIRST_SUPERUSER_PASSWORD=********
```

После заполнения .env файла необходимо создать базу данныйх и запустить uvicorn.

```sh
alembic upgrade 01
uvicorn main.app:app --reload
```
