# app.py
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Enhanced sample data with more details
garden_data = [
    {
        'id': 1,
        'name': 'Tomato Plant',
        'plant_date': '2024-01-01',
        'last_watered': '2024-01-13 08:00:00',
        'water_frequency': 2,  # days
        'sunlight': 'full',
        'plant_type': 'vegetable',
        'notes': 'Cherry tomatoes growing well!',
        'tasks': ['Remove yellow leaves', 'Check for pests'],
        'growth_stage': 'flowering'
    },
    {
        'id': 2,
        'name': 'Basil',
        'plant_date': '2024-01-05',
        'last_watered': '2024-01-13 08:00:00',
        'water_frequency': 1,  # days
        'sunlight': 'partial',
        'plant_type': 'herb',
        'notes': 'Perfect for homemade pesto',
        'tasks': ['Pinch off flower buds'],
        'growth_stage': 'mature'
    },
    {
        'id': 3,
        'name': 'Mint',
        'plant_date': '2024-01-10',
        'last_watered': None,
        'water_frequency': 3,  # days
        'sunlight': 'partial',
        'plant_type': 'herb',
        'notes': 'Growing like crazy! Good for tea',
        'tasks': ['Contain roots'],
        'growth_stage': 'growing'
    }
]

tips_by_type = {
    'vegetable': [
        'Rotate your crops yearly',
        'Watch for signs of pests',
        'Ensure good air circulation'
    ],
    'herb': [
        'Harvest regularly to promote growth',
        'Most herbs prefer well-draining soil',
        'Prune to prevent flowering'
    ]
}

@app.route('/')
def home():
    # Add watering status for each plant
    for plant in garden_data:
        if plant['last_watered']:
            last_watered = datetime.strptime(plant['last_watered'], '%Y-%m-%d %H:%M:%S')
            next_water = last_watered + timedelta(days=plant['water_frequency'])
            plant['needs_water'] = datetime.now() > next_water
            plant['days_until_water'] = (next_water - datetime.now()).days
        else:
            plant['needs_water'] = True
            plant['days_until_water'] = 0
    
    return render_template('home.html', plants=garden_data)

@app.route('/add_plant')
def add_plant():
    return render_template('add_plant.html')

@app.route('/water/<int:plant_id>')
def water_plant(plant_id):
    for plant in garden_data:
        if plant['id'] == plant_id:
            plant['last_watered'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return redirect(url_for('home'))

@app.route('/plant/<int:plant_id>')
def plant_details(plant_id):
    plant = next((p for p in garden_data if p['id'] == plant_id), None)
    if plant:
        tips = tips_by_type.get(plant['plant_type'], [])
        return render_template('plant_details.html', plant=plant, tips=tips)
    return redirect(url_for('home'))

@app.route('/complete_task/<int:plant_id>/<int:task_index>')
def complete_task(plant_id, task_index):
    for plant in garden_data:
        if plant['id'] == plant_id:
            if 0 <= task_index < len(plant['tasks']):
                plant['tasks'].pop(task_index)
    return redirect(url_for('plant_details', plant_id=plant_id))

if __name__ == '__main__':
    app.run(debug=True)