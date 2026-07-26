import json
import os
from rich import print

class Operator:
    """
    Base class representing the Netrunner (Player).
    Strictly follows OOP principles: Encapsulation, Getters/Setters, and File I/O.
    """
    
    def __init__(self, profile_id="1", db_path="data/local_drive.db"):
        self.profile_id = str(profile_id)
        self.combo = 0
        self.db_path = db_path
        self.local_drive = []
        
        try:
            with open("data/classes.json", "r", encoding="utf-8") as file:
                classes = json.load(file)
                profile = classes.get(self.profile_id, classes.get("1", {}))
                self.name = profile.get("name", "Unknown Hacker")
                self.passive = profile.get("passive", "none")
        except (FileNotFoundError, json.JSONDecodeError):
            self.name = "Unknown Hacker"
            self.passive = "none"

    def get_name(self):
        return self.name

    def get_passive(self):
        return self.passive

    def get_combo(self):
        return self.combo

    def add_combo(self, amount=1):
        self.combo += amount

    def reset_combo(self):
        self.combo = 0

    def extract_data(self, item_name):
        self.local_drive.append(item_name)
        
    def read_local_drive(self):
        return self.local_drive