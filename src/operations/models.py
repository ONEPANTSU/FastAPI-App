from sqlalchemy import TIMESTAMP, Column, Integer, MetaData, String, Table

metadata = MetaData()

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String, nullable=True),
    Column("figi", String, nullable=True),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP, nullable=True),
    Column("type", String),
)
