from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, IntegerField, DateTimeField

db = SqliteDatabase('ranks.db')

class Base(Model):
    class Meta:
        database = db

class User(Base):
    id = PrimaryKeyField()
    username = CharField(unique=True, null=False)
    points = IntegerField(default=1)
