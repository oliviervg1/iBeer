from sqlalchemy import Column, MetaData, Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer, Text


metadata = MetaData()

MYSQL_DEFAULTS = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8"
}


beers = Table(
    "beers", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("rating", Integer, nullable=False),
    Column("comment", Text, nullable=True),
    Column("brewerydb_id", Text, nullable=False),
    UniqueConstraint("name"),
    **MYSQL_DEFAULTS
)
