class Attendee:
    """
    Represents a registered conference attendee.
    
    Responsibilities:
    - Store personal details
    - Maintain the attendee's purchased pass
    - Manage workshop reservations
    - Allow modification of profile information
    - Provide helper utilities for GUI and backend logic
    """

    def __init__(self, attendee_id, name, email, phone):
        self.attendee_id = attendee_id
        self.name = name
        self.email = email
        self.phone = phone
        
        # The pass that the attendee purchased (None initially)
        self.purchased_pass = None
        
        # List of Workshop objects the attendee has reserved
        self.reservations = []

    # ----------------------------------------------------------
    # Profile Management
    # ----------------------------------------------------------

    def update_name(self, new_name):
        """Update attendee's name."""
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = new_name

    def update_email(self, new_email):
        """Update attendee's email."""
        if "@" not in new_email or "." not in new_email:
            raise ValueError("Invalid email address.")
        self.email = new_email

    def update_phone(self, new_phone):
        """Update phone number."""
        if len(new_phone) < 5:
            raise ValueError("Phone number too short.")
        self.phone = new_phone

    # ----------------------------------------------------------
    # Workshop Reservations
    # ----------------------------------------------------------

    def reserve_workshop(self, workshop):
        """
        Reserve a workshop.
        This method is used internally by TicketSystem.
        """
        if workshop in self.reservations:
            raise ValueError("Workshop already reserved.")

        self.reservations.append(workshop)

    def cancel_reservation(self, workshop):
        """
        Cancel a previously reserved workshop.
        """
        if workshop not in self.reservations:
            raise ValueError("You have not reserved this workshop.")

        self.reservations.remove(workshop)

        # Remove attendee from workshop attendee list as well
        if self.attendee_id in workshop.attendees:
            workshop.attendees.remove(self.attendee_id)

    # ----------------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------------

    def has_pass(self):
        """Check if attendee has purchased any pass."""
        return self.purchased_pass is not None

    def get_reserved_workshop_titles(self):
        """Return list of workshop names for GUI display."""
        return [w.title for w in self.reservations]

    def __str__(self):
        """Human-readable formatting."""
        return f"{self.attendee_id} - {self.name} ({self.email})"

    def __repr__(self):
        """Debug-friendly representation."""
        return f"Attendee({self.attendee_id}, {self.name}, {self.email})"
