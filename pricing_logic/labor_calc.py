def estimate_labor(task, city="Marseille"):
    base_rate = 40  # per hour
    city_multiplier = 1.0 if city.lower() == "marseille" else 1.2  # Paris more expensive

    hours_map = {
        "remove": 4,
        "plumbing": 6,
        "replace": 3,
        "install": 3,
        "paint": 2,
        "lay": 5
    }

    hours = 2
    for key in hours_map:
        if key in task.lower():
            hours = hours_map[key]

    labor_cost = hours * base_rate * city_multiplier
    return round(labor_cost, 2), f"{hours}h"
