
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
│   └── city_profile.py             # Multiplier logic for cities
│
├── vector_memory.py                # Vector memory using ChromaDB + embeddings
│
├── data/
│   ├── materials.json              # Material base prices
│   ├── price_templates.csv         # Task templates and pricing rules
│
├── output/
│   └── sample_quote.json           # Auto-generated structured quote
│
├── tests/
│   └── test_vector_memory.py       # Vector search test using persistent DB
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
6. **Margin Logic**: Dynamically fetched from vector memory based on similar past accepted quotes.
7. **Confidence Scoring**: Based on transcript clarity, task count, city info, and user history.
8. **Quote Generation**: Structured JSON output grouped by zone and task.

---

## 💬 Example Transcript Input

```
Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, redo the plumbing for the shower, replace the toilet, install a vanity, repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille.
```

---

## 📤 Output (sample_quote.json)

```json
{
  "zone": "bathroom",
  "city": "Marseille",
  "tasks": [
    {
      "task": "install vanity",
      "labor": 120.0,
      "materials": 180.0,
      "estimated_duration": "3h",
      "vat_rate": 0.2,
      "total_price": 405.0,
      "margin": 45.0,
      "confidence_score": 1.0
    }
  ],
  "global_confidence": 1.0
}
```

---

## 🏙️ Simulated City-Based Pricing

| City      | Labor Multiplier | Material Multiplier | Confidence Boost |
|-----------|------------------|---------------------|------------------|
| Marseille | 1.0              | 1.0                 | +0.1             |
| Paris     | 1.2              | 1.1                 |  0.0             |
| Lyon      | 1.1              | 1.0                 | +0.05            |

---

## 🔁 Vector Feedback Memory

- Tasks + context (e.g., city, room size, budget) are embedded into vectors
- Stored and queried from `ChromaDB` persistently
- Margins are recommended based on similar accepted quotes

### Example Stored Vector Memory (Chroma)

```json
{
  "task": "install vanity",
  "context": "marseille, small bathroom, budget-conscious",
  "margin": 0.15,
  "accepted": true
}
```

Quotes are semantically queried using vector search with `sentence-transformers`.

---

## ✅ How to Run

```bash
# Run the pricing engine
python pricing_engine.py
```

💡 After generating a quote, you'll be asked:

```bash
Was the quote accepted? (y/n):
```

If accepted, the quote will be embedded and stored in ChromaDB memory.

---

## 🧪 Vector Memory Test

```bash
python tests/test_vector_memory.py
```

- Confirms how many quotes are stored
- Prints vector search results using raw text and helper function

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
- Deploy as a **FastAPI** microservice

---

## 👤 Author

Palen Pushkar
