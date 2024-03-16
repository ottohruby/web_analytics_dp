from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.model_base import ModelBase
from src.models.modules import Module

class ModuleRole(db.Model, ModelBase):
    __tablename__ = 'module_roles'
    __table_args__ = {'schema': 'analytics'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, ForeignKey('analytics.roles.id'))
    module_id = db.Column(db.Integer, ForeignKey('analytics.modules.id'))

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    module = relationship("Module", lazy='joined')

    @classmethod
    def get_required_role_ids(cls, module_name):
        results = db.session.query(
                cls.role_id.label("id")
            ).join(
                Module, cls.module_id == Module.id
            ).filter(
                Module.name == module_name
            ).group_by(cls.role_id).all()
        
        return [dict(row).get("id") for row in results]
    
    @classmethod
    def get_available_modules(cls, user_roles):
        results = db.session.query(
            cls.id.label("tmp"),
            Module.id.label("id"),
            Module.name.label("name"),
            Module.description.label("description")
        ).join(
            Module, cls.module_id == Module.id
        ).filter(
            cls.role_id.in_(user_roles)
        ).order_by(Module.id).all()

        return [dict(row) for row in results]