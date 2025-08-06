def get_city_profile(city: str):
    city = city.lower()

    profiles = {
        "marseille": {
            "labor_multiplier": 1.0,
            "material_multiplier": 1.0,
            "confidence_boost": 0.1
        },
        "paris": {
            "labor_multiplier": 1.2,
            "material_multiplier": 1.1,
            "confidence_boost": 0.0
        },
        "lyon": {
            "labor_multiplier": 1.1,
            "material_multiplier": 1.0,
            "confidence_boost": 0.05
        }
    }

    return profiles.get(city, {
        "labor_multiplier": 1.15,
        "material_multiplier": 1.1,
        "confidence_boost": 0.0
    })  # Default profile for unknown cities
