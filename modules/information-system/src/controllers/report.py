from src.models.reports import Report
import json

class ReportController():
    def __init__(self, id=None):
        if id:
            self.model = Report.query.get_or_404(id)
    
    def list_all(self):
        return Report.get_with_state()
    
    def add(self, name, description, user_id, data):
        print("Add", user_id)
        row = Report(name=name,
                   description=description,
                   user_id=int(user_id),
                   data=data)
        
        new_row = Report.add_with_state(row, Report.STATES.ACTIVE)   
        
        self.model = new_row
        self.model.save()
        return new_row
    
    def edit(self, name, description, user_id, data):       
        self.model.name = name
        self.model.description = description
        self.model.data = data

        self.model.save()


    
