import json
import os

def load_material_prices():
    path = os.path.join(os.path.dirname(__file__), '../data/materials.json')
    with open(path, 'r') as file:
        return json.load(file)

def get_material_cost(task):
    material_map = {
        "tiles": "ceramic_tiles",
        "paint": "paint",
        "toilet": "toilet",
        "vanity": "vanity",
        "plumbing": "plumbing_fittings"
    }
    materials = load_material_prices()
    for key in material_map:
        if key in task.lower():
            return materials.get(material_map[key], 0)
    return 10  # default minimal material cost
