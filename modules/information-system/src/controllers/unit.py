from src.models.units import Unit

class UnitController():
    def __init__(self, id=None):
        if id:
            self.model = Unit.query.get_or_404(id)
    
    def list_all(self):
        return Unit.get_with_state()
    
    def list_only_base(self):
        return Unit.get_base_units()
    
    def add(self, name, description, amount, base_unit_id):
        row = Unit(name=name,
                   description=description,
                   amount=amount)
        
        if base_unit_id != 'None':
            row.base_unit_id = base_unit_id
        
        new_row = Unit.add_with_state(row, Unit.STATES.ACTIVE)   
        
        self.model = new_row
        self.model.save()
        return new_row
    
    def edit(self, name, amount, description, state_number, state_name, base_unit_id):       
        self.model.name = name
        self.model.amount = amount
        self.model.description = description
        
        if base_unit_id == 'None':
            self.model.base_unit_id = None
        elif base_unit_id == None:
            self.model.base_unit_id = None
        elif int(self.model.id) == int(base_unit_id):
            self.model.base_unit_id = None
        else:
            self.model.base_unit_id = int(base_unit_id)

        self.model.set_state(state_number, state_name)

        self.model.save()


    
