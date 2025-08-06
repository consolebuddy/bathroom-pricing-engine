def get_vat_rate(task):
    # Assume renovation VAT = 10%, luxury finish = 20%
    if "tiles" in task.lower() or "plumbing" in task.lower():
        return 0.10
    return 0.20
