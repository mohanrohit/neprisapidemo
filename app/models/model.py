#import sqlite3

from app import get_db

from pydantic import BaseModel

class Model(BaseModel):
    __tablename__ = None # override in subclasses

    @classmethod
    def all(cls, **params):
        db = get_db()

        limit = params.pop("limit") if params and params.get("limit") else 10
        offset = params.pop("offset") if params and params.get("offset") else 0

        sql = f"SELECT * FROM {cls.__tablename__}"

        if params:
            filters = []

            for key in params:
                filters.append(f"{key} = {params[key]}")

            sql = sql + " WHERE "  + " AND ".join(filters)

        cursor = db.cursor()
        cursor.execute(sql)

        result = [{column.lower(): row[column] for column in row.keys()} for row in cursor]

        return result

    @classmethod
    def one(cls, **params):
        db = get_db()

        sql = f"SELECT * FROM {cls.__tablename__}"

        if params:
            filters = []

            for key in params:
                filters.append(f"{key} = {params[key]}")

            sql = sql + " WHERE "  + " AND ".join(filters)

        sql = sql + " LIMIT 1"

        cursor = db.cursor()
        cursor.execute(sql)

        result = [{column.lower(): row[column] for column in row.keys()} for row in cursor]

        return {} if len(result) == 0 else result[0]


    @classmethod
    def new(cls, **params):
        db = get_db()

        columns = params.keys()
        values = [f"'{params[column]}'" for column in columns]

        sql = f"INSERT INTO {cls.__tablename__} ({', '.join(columns)}) VALUES ("

        sql = sql + ", ".join(values) + ")"

        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        return cls.one(id=cursor.lastrowid)
