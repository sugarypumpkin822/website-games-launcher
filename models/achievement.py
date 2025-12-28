"""Achievement model"""
from datetime import datetime


class Achievement:
    """Represents an achievement"""
    
    def __init__(self, id, name, description, icon, requirement):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.requirement = requirement
        self.unlocked = False
        self.unlock_date = None

