from src.extensions.database import db
from src.extensions.cache import cache
from sqlalchemy import Column, Integer, String, ForeignKey, func, case
from src.models.states import State
from src.models.user_roles import UserRole
from src.models.roles import Role
from sqlalchemy.orm import relationship

# from flask_login import UserMixin
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from src.models.model_base import ModelBase

from enum import Enum 

class StateEnum(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3

class User(UserMixin, db.Model, ModelBase):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'analytics'}

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    login_failed_attempts = Column(Integer, default=0)

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    user_role = relationship("UserRole", lazy='joined')

    # Relationships
    # roles = db.relationship('Role', secondary='analytics.user_roles',
    #                         backref=db.backref('analytics.users', lazy='dynamic'))
    

    STATES = StateEnum

    STATE_TRANSITIONS = {
        STATES.ACTIVE.value: [STATES.ACTIVE, STATES.INACTIVE, STATES.DELETED],
        STATES.INACTIVE.value: [STATES.INACTIVE, STATES.ACTIVE, STATES.DELETED],
        STATES.DELETED.value: [STATES.DELETED]
    }

    @classmethod
    def get_with_state(cls):
        subquery_granted_roles = db.session.query(
            UserRole.user_id,
            func.array_to_string(func.array_agg(Role.name), ', ').label("Roles")
        ).join(
            State, State.id == UserRole.state_id
        ).join(
            Role, Role.id == UserRole.role_id
        ).filter(
            State.state_name == UserRole.STATES.GRANTED.name
        ).group_by(UserRole.user_id).subquery()


        results = db.session.query(
            cls.user_id.label("ID"),
            cls.name.label("Name"),
            cls.email.label("Email"),
            func.concat(subquery_granted_roles.c.Roles,'').label("Roles"),
            State.state_name.label("State"),
            func.concat(func.cast(State.changed_ts, db.String(10)), " ").label("Last Change")
        ).join(
            State, State.id == cls.state_id, isouter=True
        ).outerjoin(
            subquery_granted_roles,
            subquery_granted_roles.c.user_id == cls.user_id
        ).filter(
            State.state_name != cls.STATES.DELETED.name
        ).all()

        return [dict(row) for row in results]
  
    def get_all_available_roles(self):
        results = db.session.query(
            UserRole.user_id,
            State.state_name.label("state"),
            Role.name.label("Name"),
            Role.id.label("ID")
        ).join(
            State, State.id == UserRole.state_id
        ).join(
            Role, Role.id == UserRole.role_id
        ).filter(
            UserRole.user_id == self.user_id
        ).all()
        
        return [dict(row) for row in results]

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return db.session.query(
            User.user_id.label("ID"),
        ).join(
            State, State.id==User.state_id
        ).filter(
            State.state_name == User.STATES.ACTIVE.name,
            self.user_id == User.user_id
        ).first() is not None

    def is_anonymous(self):
        return False
    
    def print(self):
        print("a")


