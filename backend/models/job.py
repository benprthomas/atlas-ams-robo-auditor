from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, text

from .base import Base
from .association import model_cur_association


class Processedmodel(Base):
    __tablename__ = "processed_models"

    model_id = Column(
        String,
        ForeignKey("models.model_id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    model_title = Column(String, nullable=False)
    company_profile = Column(Text, nullable=True)
    effective_date = Column(String, nullable=True)
    date_posted = Column(String, nullable=True)
    employment_type = Column(String, nullable=True)
    model_summary = Column(Text, nullable=False)
    key_responsibilities = Column(JSON, nullable=True)
    qualifications = Column(JSON, nullable=True)
    compensation_and_benfits = Column(JSON, nullable=True)
    application_info = Column(JSON, nullable=True)
    extracted_keywords = Column(JSON, nullable=True)
    processed_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        index=True,
    )

    # one-to-many relation between user and models
    # owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # owner = relationship("User", back_populates="processed_models")
    raw_model = relationship("model", back_populates="raw_model_association")

    # many-to-many relationship in model and cur
    processed_curs = relationship(
        "Processedcur",
        secondary=model_cur_association,
        back_populates="processed_models",
    )


class model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, unique=True, nullable=False)
    cur_id = Column(String, ForeignKey("curs.cur_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        index=True,
    )

    raw_model_association = relationship(
        "Processedmodel", back_populates="raw_model", uselist=False
    )

    curs = relationship("cur", back_populates="models")
