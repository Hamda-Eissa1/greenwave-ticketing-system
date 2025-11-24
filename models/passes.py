# models/passes.py
from typing import List

class Pass:
    """
    Base Pass class
    """
    def __init__(self, pass_id: int, price: float, exhibitions_access: List[int], features: List[str] = None):
        self.pass_id = pass_id
        self.price = price
        self.exhibitions_access = list(exhibitions_access)
        self.features = features or []

    def allows_exhibition(self, exhibition_id: int) -> bool:
        return exhibition_id in self.exhibitions_access

    def add_exhibition(self, exhibition_id: int):
        if exhibition_id not in self.exhibitions_access:
            self.exhibitions_access.append(exhibition_id)

    def __str__(self):
        return f"Pass({self.pass_id}) price={self.price} access={self.exhibitions_access}"

class ExhibitionPass(Pass):
    """
    Pass allowing access to a specific set of exhibition IDs.
    """
    def __init__(self, pass_id: int, price: float, exhibitions_access: List[int], features: List[str] = None):
        super().__init__(pass_id, price, exhibitions_access, features)

class AllAccessPass(Pass):
    """
    All access — can be represented as allowing any exhibition by convention.
    In this implementation we will store access to all known exhibitions when created.
    """
    def __init__(self, pass_id: int, price: float, features: List[str] = None):
        super().__init__(pass_id, price, exhibitions_access=[], features=features)
