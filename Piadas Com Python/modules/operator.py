import json
import os
from rich import print

class Operator:
    """
    Base class representing the Netrunner (Player).
    Strictly follows OOP principles: Encapsulation, Getters/Setters, and File I/O.
    """
    
    def __init__(self, profile_id):
        self._profile_id = str(profile_id)
        self._name = "Unknown"
        self._passive = "None"
        self._description = "No data"
        self._sync_combo = 0
        self._local_drive = [] 
        
        self._load_profile_data()

    def _load_profile_data(self):
        filepath = "data/classes.json"
        
        if not os.path.exists(filepath):
            print(f"[bold #ff0055][SYSTEM ERROR] Configuration file '{filepath}' not found.[/]")
            return

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if self._profile_id in data:
                profile = data[self._profile_id]
                self._name = profile.get("nome", "Unknown")
                self._passive = profile.get("passiva", "None")
                self._description = profile.get("descricao", "No data")
            else:
                self._name = "Rogue AI Override"

    def get_name(self):
        return self._name
        
    def get_passive(self):
        return self._passive
        
    def get_combo(self):
        return self._sync_combo
        
    def add_combo(self, amount=1):
        self._sync_combo += amount
        
    def reset_combo(self):
        self._sync_combo = 0

    def extract_data(self, item_name):
        self._local_drive.append(item_name)
        
    def read_local_drive(self):
        return self._local_drive