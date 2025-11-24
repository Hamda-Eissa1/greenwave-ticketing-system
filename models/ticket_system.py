# models/ticket_system.py
from typing import List, Optional, Dict
import datetime

from storage.data_manager import save_data, load_data
from models.attendee import Attendee
from models.exhibition import Exhibition
from models.workshop import Workshop
from models.passes import Pass, ExhibitionPass, AllAccessPass

class TicketSystem:
    """
    Central controller for attendees, exhibitions, passes, and reservations.
    Responsible for persistence via storage/data_manager.
    """

    ATTENDEES_FILE = "attendees.pkl"
    EXHIBITIONS_FILE = "exhibitions.pkl"
    PASSES_FILE = "passes.pkl"
    SALES_FILE = "sales.pkl"

    def __init__(self):
        # load or initialize
        self.attendees: List[Attendee] = load_data(self.ATTENDEES_FILE) or []
        self.exhibitions: List[Exhibition] = load_data(self.EXHIBITIONS_FILE) or []
        self.passes: List[Pass] = load_data(self.PASSES_FILE) or []
        self.sales_log: Dict[str, int] = load_data(self.SALES_FILE) or {}

        # 🔁 Auto-create sample data if system is empty
        if not self.exhibitions or not self.passes:
            self.create_sample_data()


    # -------------------------
    # Persistence helpers
    # -------------------------
    def _save_all(self):
        save_data(self.ATTENDEES_FILE, self.attendees)
        save_data(self.EXHIBITIONS_FILE, self.exhibitions)
        save_data(self.PASSES_FILE, self.passes)
        save_data(self.SALES_FILE, self.sales_log)

    # -------------------------
    # Attendee management
    # -------------------------
    def register_attendee(self, attendee: Attendee) -> None:
        if self.find_attendee_by_email(attendee.email):
            raise ValueError("Email already registered.")
        self.attendees.append(attendee)
        self._save_all()

    def find_attendee_by_email(self, email: str) -> Optional[Attendee]:
        for a in self.attendees:
            if a.email.lower() == email.lower():
                return a
        return None

    def find_attendee_by_id(self, aid: int) -> Optional[Attendee]:
        for a in self.attendees:
            if a.attendee_id == aid:
                return a
        return None

    # -------------------------
    # Pass management
    # -------------------------
    def add_pass(self, p: Pass):
        self.passes.append(p)
        self._save_all()

    def find_pass_by_id(self, pid: int) -> Optional[Pass]:
        for p in self.passes:
            if getattr(p, "pass_id", None) == pid:
                return p
        return None

    def purchase_pass(self, attendee: Attendee, p: Pass) -> None:
        """
        Allow attendee to purchase a pass only once.
        Prevent duplicate purchases or overwriting an existing pass.
        """

        # --- NEW RULE: Prevent buying a second pass ---
        if attendee.purchased_pass is not None:
            raise ValueError("Attendee has already purchased a pass.")

        # Attach pass to attendee
        attendee.purchased_pass = p

        # If AllAccessPass -> give it all exhibitions automatically
        if isinstance(p, AllAccessPass):
            p.exhibitions_access = [ex.exhibition_id for ex in self.exhibitions]

        # Log sale + save system state
        self._log_sale()
        self._save_all()

    def upgrade_pass(self, attendee: Attendee, additional_exhibitions: List[int]) -> None:
        if not attendee.purchased_pass:
            raise ValueError("Attendee has no pass to upgrade.")
        for eid in additional_exhibitions:
            attendee.purchased_pass.add_exhibition(eid)
        self._save_all()

    # -------------------------
    # Exhibition & Workshop helpers
    # -------------------------
    def add_exhibition(self, exhibition: Exhibition) -> None:
        if self.find_exhibition_by_id(exhibition.exhibition_id):
            raise ValueError("Exhibition with this ID already exists.")
        self.exhibitions.append(exhibition)
        self._save_all()

    def find_exhibition_by_id(self, eid: int) -> Optional[Exhibition]:
        for ex in self.exhibitions:
            if ex.exhibition_id == eid:
                return ex
        return None

    def find_workshop_by_id(self, wid: int) -> Optional[Workshop]:
        for ex in self.exhibitions:
            for w in ex.workshops:
                if w.workshop_id == wid:
                    return w
        return None

    # -------------------------
    # Reservation logic
    # -------------------------
    def reserve_workshop(self, attendee: Attendee, workshop: Workshop) -> None:
        # Pre-checks
        if attendee.purchased_pass is None:
            raise PermissionError("Attendee must purchase a pass before reserving workshops.")

        # find which exhibition this workshop belongs to
        parent_exhibition = None
        for ex in self.exhibitions:
            if workshop in ex.workshops:
                parent_exhibition = ex
                break
        if parent_exhibition is None:
            raise ValueError("Workshop not attached to any exhibition.")

        # Check pass permissions
        if not attendee.purchased_pass.allows_exhibition(parent_exhibition.exhibition_id):
            raise PermissionError("Attendee's pass does not include this exhibition.")

        # Try to reserve spot in workshop
        if not workshop.reserve_spot(attendee.attendee_id):
            raise ValueError("Workshop is full or attendee already reserved.")

        # Add to attendee reservations (store actual Workshop object)
        attendee.reserve_workshop(workshop)
        self._save_all()

    def cancel_reservation(self, attendee: Attendee, workshop: Workshop) -> None:
        # Remove from workshop and attendee
        if attendee.attendee_id in workshop.attendees:
            workshop.cancel_reservation(attendee.attendee_id)
        attendee.cancel_reservation(workshop)
        self._save_all()

    # -------------------------
    # Admin reports
    # -------------------------
    def workshop_capacity_report(self):
        report = []
        for ex in self.exhibitions:
            for w in ex.workshops:
                report.append({
                    "exhibition_id": ex.exhibition_id,
                    "exhibition_name": ex.name,
                    "workshop_id": w.workshop_id,
                    "workshop_title": w.title,
                    "capacity": w.capacity,
                    "registered": len(w.attendees),
                    "spots_left": w.spots_left(),
                })
        return report

    def daily_sales(self):
        return dict(self.sales_log)

    # -------------------------
    # Utility
    # -------------------------
    def _log_sale(self):
        date_key = datetime.date.today().isoformat()
        self.sales_log[date_key] = self.sales_log.get(date_key, 0) + 1

    # -------------------------
    # Sample data creation helper
    # -------------------------
    def create_sample_data(self):
        """
        Populate exhibitions, workshops, and passes if they don't exist.
        Useful for local testing.
        """
        if self.exhibitions:
            return  # don't overwrite existing data

        # Create 3 exhibitions
        e1 = Exhibition(1, "Sustainable Transportation", "Innovations in urban mobility")
        e2 = Exhibition(2, "Renewable Energy", "Solar, wind, and storage solutions")
        e3 = Exhibition(3, "Climate Policy & Community Action", "Policy and outreach")

        # Add workshops
        w1 = Workshop(101, "Adaptive Traffic Signals", 3)
        w2 = Workshop(102, "EV Charging Infrastructure", 2)
        w3 = Workshop(201, "Solar Microgrids", 4)
        w4 = Workshop(202, "Battery Storage Advances", 2)
        w5 = Workshop(301, "Community Organizing 101", 5)

        e1.add_workshop(w1)
        e1.add_workshop(w2)
        e2.add_workshop(w3)
        e2.add_workshop(w4)
        e3.add_workshop(w5)

        self.exhibitions = [e1, e2, e3]

        # Create passes
        p1 = ExhibitionPass(1, price=30.0, exhibitions_access=[1])   # Exhibition 1 only
        p2 = ExhibitionPass(2, price=45.0, exhibitions_access=[1,2]) # two exhibitions
        p3 = AllAccessPass(99, price=100.0)

        # For AllAccessPass, set access to all existing exhibitions
        p3.exhibitions_access = [ex.exhibition_id for ex in self.exhibitions]

        self.passes = [p1, p2, p3]

        self._save_all()
