from .base import Base
from sqlalchemy import Column, String, Table, ForeignKey


model_cur_association = Table(
    "model_cur",
    Base.metadata,
    Column(
        "processed_model_id",
        String,
        ForeignKey("processed_models.model_id"),
        primary_key=True,
    ),
    Column(
        "processed_cur_id",
        String,
        ForeignKey("processed_curs.cur_id"),
        primary_key=True,
    ),
)
