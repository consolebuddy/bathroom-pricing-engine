
# 🛠️ Smart Renovation Pricing Engine

A modular Python-based pricing engine that parses messy renovation transcripts into clean, structured renovation quotes — with estimated labor, materials, VAT, margin, and confidence scoring.

---

## 📦 Repo Structure

```
/bathroom-pricing-engine/
├── pricing_engine.py                # Main script to run the pricing engine
├── pricing_logic/
│   ├── material_db.py              # Loads material pricing
│   ├── labor_calc.py               # Labor estimation logic
│   ├── vat_rules.py                # VAT rate rules per task
│   ├── task_templates.py           # Maps keywords to structured tasks
│   ├── feedback_memory.py          # Feedback loop logic
│
├── data/
│   ├── materials.json              # Material base prices
│   ├── price_templates.csv         # Task templates and pricing rules
│   └── feedback_memory.json        # Persisted memory from feedback
│
├── output/
│   └── sample_quote.json           # Auto-generated structured quote
│
├── tests/
│   └── test_logic.py               # Unit tests for all components
│
├── README.md                       # You're here
└── LICENSE                         # (Optional)
```

---

## 🧠 How It Works

### ✅ Step-by-step Pipeline:

1. **Transcript Parsing**: Identifies tasks like “install vanity” or “replace toilet” from messy user input.
2. **Task Matching**: Uses `price_templates.csv` to map phrases to structured task definitions.
3. **Labor Estimation**: Calculates time × hourly rate × city-based multiplier.
4. **Material Pricing**: Fetches cost from `materials.json`, also city-adjusted.
5. **VAT Logic**: Applies renovation-specific VAT per task.
6. **Margin Logic**: Dynamically fetched from historical feedback using a memory loop.
7. **Confidence Scoring**: Based on transcript clarity, task count, city info, and user history.
8. **Quote Generation**: Structured JSON output grouped by zone and task.

---

## 💬 Example Transcript Input

```
“Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, redo the plumbing for the shower, replace the toilet, install a vanity, repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille.”
```

---

## 📤 Output (sample_quote.json)

```json
{
  "zone": "bathroom",
  "city": "Marseille",
  "tasks": [
    {
      "task": "remove old tiles",
      "labor": 160.0,
      "materials": 25.0,
      "estimated_duration": "4h",
      "vat_rate": 0.1,
      "total_price": 229.25,
      "margin": 27.75,
      "confidence_score": 0.91
    }
  ],
  "global_confidence": 0.91
}
```

---

## 🏙️ Simulated City-Based Pricing

| City      | Labor Multiplier | Material Multiplier | Confidence Boost |
|-----------|------------------|---------------------|------------------|
| Marseille | 1.0              | 1.0                 | +0.1             |
| Paris     | 1.2              | 1.1                 |  0.0             |
| Lyon      | 1.1              | 1.0                 | +0.05            |

City affects:
- Labor & material cost
- Confidence score
- Can be extended to contractor history & supply chains

---

## 🔁 Feedback Memory Loop

- After each run, user inputs whether the quote was **accepted** or **rejected**
- This updates `feedback_memory.json`
- Margin rates are then **learned** over time per task
- Example:

```json
{
  "replace toilet": {
    "accepted_count": 3,
    "rejected_count": 1,
    "total_margin": 50.0
  }
}
```

→ This will reduce/increase future margin on "replace toilet" based on past user decisions.

---

## ⚙️ How to Run

```bash
# Run the pricing engine
python pricing_engine.py
```

💡 After generating a quote, you'll be asked:

```bash
Was the quote accepted? (y/n):
```

Answering `y` or `n` will update the pricing memory for future improvements.

---

## ✅ Tests

```bash
python -m unittest tests/test_logic.py
```

---

## 📊 Output JSON Schema

| Field              | Description                              |
|-------------------|------------------------------------------|
| `zone`            | Zone of the renovation (e.g., bathroom)   |
| `city`            | City context for pricing                  |
| `tasks`           | List of structured task quote objects     |
| `global_confidence` | System confidence in total quote        |

Each task object includes:
- `task`, `labor`, `materials`, `estimated_duration`, `vat_rate`, `total_price`, `margin`, `confidence_score`

---

## 🔮 Future Improvements

- Integrate **pgvector/Chroma** to store embeddings of past quotes & feedback
- Connect to **live supplier APIs** for real-time material pricing
- Store **contractor performance history** by city & task
- Build frontend for client-facing instant quote visualization
- Deploy as a **microservice** (FastAPI + SQLite/PostgreSQL + Docker)

---

## 👤 Author

Palen Pushkar
