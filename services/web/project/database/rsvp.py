from sqlalchemy import Column, Integer, ForeignKey, Boolean

from project import BaseModel


class RSVP(BaseModel):
    __tablename__ = "rsvp"

    party_id = Column(Integer, ForeignKey("party.id"), primary_key=True)
    attending = Column(Boolean, server_default="0")
