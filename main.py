# main.py
from models.ticket_system import TicketSystem
from models.attendee import Attendee

def demo_flow():
    ts = TicketSystem()
    # Create sample data on first run
    ts.create_sample_data()

    print("=== Exhibitions & Workshops ===")
    for ex in ts.exhibitions:
        print(ex)
        for w in ex.workshops:
            print("  ", w)

    # Register an attendee
    print("\n=== Register Attendee ===")
    attendee = Attendee(attendee_id=1, name="Alice Green", email="alice@example.com", phone="00971-555-000")
    try:
        ts.register_attendee(attendee)
        print("Registered:", attendee)
    except ValueError as e:
        print("Could not register (maybe already exists):", e)
        attendee = ts.find_attendee_by_email("alice@example.com")
        print("Loaded attendee:", attendee)

    # Purchase a pass (Exhibition 1 only)
    pass_to_buy = ts.find_pass_by_id(1)  # ExhibitionPass for exhibition 1
    print("\n=== Purchase Pass ===")
    ts.purchase_pass(attendee, pass_to_buy)
    print("Attendee pass:", attendee.purchased_pass)

    # Try reserving a workshop in exhibition 1 (should succeed)
    print("\n=== Reserve Workshop (should succeed) ===")
    workshop = ts.find_workshop_by_id(101)  # Adaptive Traffic Signals
    try:
        ts.reserve_workshop(attendee, workshop)
        print("Reserved workshop:", workshop)
    except Exception as e:
        print("Failed to reserve:", e)

    # Try reserving a workshop in exhibition 2 (should fail due to pass)
    print("\n=== Reserve Workshop in Exhibition 2 (should fail) ===")
    workshop2 = ts.find_workshop_by_id(201)  # Solar Microgrids (exhibition 2)
    try:
        ts.reserve_workshop(attendee, workshop2)
        print("Reserved workshop:", workshop2)
    except Exception as e:
        print("Expected failure:", e)

    # Test capacity enforcement: attempt to overbook workshop 102 (capacity 2)
    print("\n=== Capacity Test (overbooking) ===")
    # Register two more attendees and reserve same workshop
    a2 = Attendee(2, "Bob", "bob@example.com", "00971-555-111")
    a3 = Attendee(3, "Carol", "carol@example.com", "00971-555-222")
    for a in [a2, a3]:
        try:
            ts.register_attendee(a)
        except ValueError:
            pass
        # Give them a pass that includes exhibition 1
        ts.purchase_pass(a, ts.find_pass_by_id(1))
    w = ts.find_workshop_by_id(102)  # EV Charging Infrastructure (capacity 2)
    # current attendee has not reserved w yet
    try:
        ts.reserve_workshop(attendee, w)
        print("Alice reserved w102")
    except Exception as e:
        print("Alice reserve failed:", e)
    try:
        ts.reserve_workshop(a2, w)
        print("Bob reserved w102")
    except Exception as e:
        print("Bob reserve failed:", e)
    try:
        ts.reserve_workshop(a3, w)
        print("Carol reserved w102 (should fail if capacity reached)")
    except Exception as e:
        print("Carol reserve failed as expected:", e)

    # Print workshop attendee lists
    print("\n=== Workshop attendee lists ===")
    for ex in ts.exhibitions:
        for w in ex.workshops:
            print(w)

    # Upgrade Alice to include exhibition 2, then reserve workshop in exhibition 2
    print("\n=== Upgrade Pass & Reserve in Exhibition 2 ===")
    ts.upgrade_pass(attendee, [2])
    print("Alice pass after upgrade:", attendee.purchased_pass.exhibitions_access)
    try:
        ts.reserve_workshop(attendee, workshop2)
        print("Alice successfully reserved workshop in exhibition 2:", workshop2)
    except Exception as e:
        print("Failed after upgrade:", e)

    # Show sales log and reports
    print("\n=== Sales log ===")
    print(ts.daily_sales())

    print("\n=== Capacity report ===")
    for row in ts.workshop_capacity_report():
        print(row)

    print("\nDemo complete. Data saved to storage/data/ as pickle files.")

if __name__ == "__main__":
    demo_flow()
