import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), '../data/feedback_memory.json')

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

def update_feedback(task_name, margin, accepted=True):
    memory = load_memory()
    task_data = memory.get(task_name, {
        "accepted_count": 0,
        "rejected_count": 0,
        "total_margin": 0.0
    })

    if accepted:
        task_data["accepted_count"] += 1
        task_data["total_margin"] += margin
    else:
        task_data["rejected_count"] += 1

    memory[task_name] = task_data
    save_memory(memory)

def get_adjusted_margin(task_name, default_margin=0.15):
    memory = load_memory()
    task_data = memory.get(task_name)
    if not task_data or task_data["accepted_count"] == 0:
        return default_margin

    avg_margin = task_data["total_margin"] / task_data["accepted_count"]
    return round(avg_margin, 2)
