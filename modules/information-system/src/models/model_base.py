from src.extensions.database import db
from src.extensions.cache import cache
from enum import Enum
from src.models.states import State

class BaseModelException(Exception):
    pass
class StateEnum(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3

class ModelBase():
    STATES = StateEnum

    STATE_TRANSITIONS = {
        STATES.ACTIVE.value: [STATES.ACTIVE, STATES.INACTIVE],
        STATES.INACTIVE.value: [STATES.INACTIVE, STATES.ACTIVE]
    }

    def get_available_states(self):
        transitions = []
        if self.state:
            transitions = [(state.value, state.name) for state in self.STATE_TRANSITIONS[self.state.state_number]]
        return transitions

    def save(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise BaseModelException("Could not save data!")    
    
    @classmethod
    def add(cls, new_row):
        try:            
            db.session.add(new_row)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            raise BaseModelException("Could not add data!")    
        return new_row
    
    @classmethod
    def add_with_state(cls, new_row, state_enum):
        try: 
            new_state = State(state_number=state_enum.value, 
                      state_name=state_enum.name)
            db.session.add(new_state)
            db.session.flush()

            new_row.state_id = new_state.id     
            db.session.add(new_row)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print("db model", e)
            raise BaseModelException("Could not add data!")    
        return new_row

    def set_state(self, state_number, state_name):
        if not self.is_state_transition_valid(state_number):
            raise BaseModelException("State transition is not possible!")
        self.state.state_number = state_number
        self.state.state_name = state_name
    
    def is_state_transition_valid(self, state_number):
        for state in self.STATE_TRANSITIONS[self.state.state_number]:
            if(state.value == int(state_number)):
                return True

        return False 
