# models/workshop.py
from typing import List

class Workshop:
    """
    Represents a single workshop with capacity and a list of attendee IDs.
    """
    def __init__(self, workshop_id: int, title: str, capacity: int):
        self.workshop_id = workshop_id
        self.title = title
        self.capacity = int(capacity)
        self.attendees: List[int] = []

    def reserve_spot(self, attendee_id: int) -> bool:
        """
        Try to reserve a spot for attendee_id.
        Returns True if successful, False if full or already reserved.
        """
        if attendee_id in self.attendees:
            return False
        if len(self.attendees) >= self.capacity:
            return False
        self.attendees.append(attendee_id)
        return True

    def cancel_reservation(self, attendee_id: int) -> bool:
        if attendee_id in self.attendees:
            self.attendees.remove(attendee_id)
            return True
        return False

    def spots_left(self) -> int:
        return max(0, self.capacity - len(self.attendees))

    def __str__(self):
        return f"Workshop({self.workshop_id}) {self.title} [{len(self.attendees)}/{self.capacity}]"
