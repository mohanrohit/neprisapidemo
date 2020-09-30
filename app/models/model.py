#import sqlite3

from app import app
from app import get_db

from pydantic import BaseModel

class Model(BaseModel):
    __tablename__ = None # override in subclasses

    def __init__(self, **params):
        BaseModel.__init__(self, **params)


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

        #result = [{column.lower(): row[column] for column in row.keys()} for row in cursor]
        result = [cls(**row) for row in cursor]

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

        #return {} if len(result) == 0 else result[0]
        return {} if len(result) == 0 else cls(**result[0])


    @classmethod
    def new(cls, **params):
        db = get_db()

        # exclude the id and uri params of the model. id is assigned after creation
        # and uri is dynamically built
        columns = [k for k in params.keys() if k not in ["id", "uri"]]

        values = [f"'{params[column]}'" for column in columns]

        sql = f"INSERT INTO {cls.__tablename__} ({', '.join(columns)}) VALUES ("

        sql = sql + ", ".join(values) + ")"

        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        new_model = cls.one(id=cursor.lastrowid)

        return new_model


    def get_link(self, endpoint, **params):
        return app.url_path_for(endpoint, **params)
