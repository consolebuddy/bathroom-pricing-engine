import csv
import os

def load_task_templates():
    path = os.path.join(os.path.dirname(__file__), '../data/price_templates.csv')
    tasks = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['default_hours'] = int(row['default_hours'])
            row['vat'] = float(row['vat'])
            tasks.append(row)
    return tasks

def match_tasks(transcript):
    transcript = transcript.lower()
    matched = []
    for template in load_task_templates():
        if template["task_keyword"] in transcript:
            matched.append(template)
    return matched
