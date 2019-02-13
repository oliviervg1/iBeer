from sqlalchemy import Column, MetaData, Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy.types import String


metadata = MetaData()

MYSQL_DEFAULTS = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8"
}


beers = Table(
    "beers", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("rating", Integer, nullable=False),
    Column("comment", String(255), nullable=True),
    Column("brewerydb_id", String(255), nullable=False),
    UniqueConstraint("name"),
    **MYSQL_DEFAULTS
)
