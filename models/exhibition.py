# models/exhibition.py
from typing import List
from models.workshop import Workshop

class Exhibition:
    """
    Represents an Exhibition which contains multiple workshops.
    """
    def __init__(self, exhibition_id: int, name: str, description: str = ""):
        self.exhibition_id = exhibition_id
        self.name = name
        self.description = description
        self.workshops: List[Workshop] = []

    def add_workshop(self, workshop: Workshop):
        if workshop not in self.workshops:
            self.workshops.append(workshop)

    def remove_workshop(self, workshop: Workshop):
        if workshop in self.workshops:
            self.workshops.remove(workshop)

    def get_workshop_by_id(self, wid: int):
        for w in self.workshops:
            if w.workshop_id == wid:
                return w
        return None

    def __str__(self):
        return f"Exhibition({self.exhibition_id}) {self.name} - {len(self.workshops)} workshops"
