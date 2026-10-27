"""Campus Shuttle Timetable & Fleet Tracker.

Logs passenger counts per trip, computes average loads, flags
under-used routes and syncs fleet data to a JSON file.
"""
import json
import secrets
from datetime import datetime

ROUTES = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and append a log line.

    Rejects unknown routes and counts that are not non-negative integers.
    """
    if logs is None:
        logs = []
    if route_id not in ROUTES:
        raise KeyError(f"Unknown route: {route_id}")
    if isinstance(passenger_count, bool) or not isinstance(
            passenger_count, int) or passenger_count < 0:
        raise ValueError(
            f"Invalid passenger count for {route_id}: {passenger_count!r}")
    ROUTES[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Remove a route from the fleet if it exists."""
    ROUTES.pop(route_id, None)


def average_load(route_id):
    """Return the average passengers per trip, or None if no data."""
    route = ROUTES.get(route_id)
    if route is None or not route["trips"]:
        return None
    trips = route["trips"]
    return sum(trips) / len(trips)


def underused_routes():
    """Return route ids whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in ROUTES:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver():
    """Pick a driver for a route."""
    return secrets.choice(DRIVERS)


def sync_fleet_data(file="fleet.json"):
    """Write the fleet data to disk and reload it into ROUTES."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(ROUTES, handle)
    with open(file, encoding="utf-8") as handle:
        loaded = json.load(handle)
    ROUTES.clear()
    ROUTES.update(loaded)


def log_trip_safely(route_id, passenger_count):
    """Log a trip, reporting invalid input instead of crashing."""
    try:
        add_trip_log(route_id, passenger_count)
    except (KeyError, ValueError) as err:
        print("Skipped:", err)


def main():
    """Run a short demo of the shuttle tracker."""
    log_trip_safely("R1", 32)
    log_trip_safely("R1", 28)
    log_trip_safely("R2", 4)
    log_trip_safely("R2", -6)
    log_trip_safely("R3", "full")
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip() or "R2"
    if choice in ROUTES:
        print("Trips on", choice, ":", ROUTES[choice]["trips"])
    else:
        print("No such route:", choice)
    avg = average_load("R3")
    print("R3 average:", avg if avg is not None else "no data")


if __name__ == "__main__":
    main()
