from src.extensions.database import db
from sqlalchemy import Column, Integer, String


class AggWindow(db.Model):

    __tablename__ = 'agg_windows'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    @classmethod
    def get_all(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name")
            ).filter(
                cls.id != '1'
            ).all()

        return results
    
    @classmethod
    def get_name_by_id(cls, id):
        result = db.session.query(
                cls.name
            ).filter(
                cls.id == id
            ).scalar()

        return result