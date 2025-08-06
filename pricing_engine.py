import json
from pricing_logic.task_templates import match_tasks
from pricing_logic.material_db import load_material_prices
from pricing_logic.city_profile import get_city_profile
from vector_memory import store_quote, search_similar
import os


print("🔍 Absolute Chroma Path:", os.path.abspath("chroma_store"))


def calculate_margin(base_price):
    return base_price * 0.15


def calculate_confidence(transcript, task_count):
    score = 0.5
    if task_count > 3: score += 0.3
    if "budget" in transcript.lower(): score += 0.1
    if "location" in transcript.lower() or "marseille" in transcript.lower(): score += 0.1
    return round(min(score, 1.0), 2)


def estimate_margin_from_memory(task, context, default_margin=0.15):
    similar = search_similar(task, context)
    if not similar or not similar["metadatas"]:
        return default_margin

    accepted_margins = [
        meta["margin"]
        for meta in similar["metadatas"][0]
        if meta.get("accepted", False)
    ]
    if accepted_margins:
        return round(sum(accepted_margins) / len(accepted_margins), 2)
    return default_margin


def estimate_labor_cost(hours, multiplier=1.0):
    base_rate = 40
    return round(hours * base_rate * multiplier, 2)



def generate_quote(transcript, city="Marseille"):
    task_templates = match_tasks(transcript)
    materials = load_material_prices()
    city_profile = get_city_profile(city)

    confidence = calculate_confidence(transcript, len(task_templates)) + city_profile["confidence_boost"]
    confidence = min(confidence, 1.0)

    quote = {"zone": "bathroom", "city": city, "tasks": [], "global_confidence": round(confidence, 2)}

    for task in task_templates:
        labor = estimate_labor_cost(task["default_hours"], city_profile["labor_multiplier"])
        material_cost = materials.get(task["material_key"], 10) * city_profile["material_multiplier"]
        material_cost = round(material_cost, 2)

        subtotal = labor + material_cost
        context_str = f"{city}, small bathroom, budget-conscious"

        margin_rate = estimate_margin_from_memory(task["standard_task"], context_str)
        margin = round(margin_rate * subtotal, 2)

        vat = task["vat"]
        total = round(subtotal + margin + (subtotal * vat), 2)

        quote["tasks"].append({
            "task": task["standard_task"],
            "labor": labor,
            "materials": material_cost,
            "estimated_duration": f"{task['default_hours']}h",
            "vat_rate": vat,
            "total_price": total,
            "margin": margin,
            "confidence_score": confidence
        })

    return quote


if __name__ == "__main__":
    transcript = "Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, redo the plumbing for the shower, replace the toilet, install a vanity, repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille."
    quote = generate_quote(transcript)
    feedback = input("Was the quote accepted? (y/n): ").strip().lower()
    accepted = feedback == 'y'

    for task in quote["tasks"]:
        store_quote(
            task=task["task"],
            context=f"{quote['city']}, small bathroom, budget-conscious",
            margin=task["margin"] / (task["labor"] + task["materials"]),  # margin rate
            accepted=accepted
        )

    print("✅ Feedback recorded and memory updated.")

    with open("output/sample_quote.json", "w") as f:
        json.dump(quote, f, indent=4)
    print(json.dumps(quote, indent=4))
