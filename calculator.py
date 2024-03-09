from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import Optional
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '!%9{!yor=dV2umkZ$WC@Mk|M5{:AdX'

def zero_if_empty(form, field):
    if field.data == '':
        field.data = 0

class CalorieForm(FlaskForm):
    protein = FloatField('Protein (g)', validators=[Optional(), zero_if_empty])
    carbs = FloatField('Carbs (g)', validators=[Optional(), zero_if_empty])
    fat = FloatField('Fat (g)', validators=[Optional(), zero_if_empty])
    submit = SubmitField('Calculate Calories')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CalorieForm()
    result = None
    recommendation = None  # Initialize recommendation

    if form.validate_on_submit():
        try:
            # Get user input from the form, defaulting to 0 if the field is empty
            protein = form.protein.data if form.protein.data else 0
            carbs = form.carbs.data if form.carbs.data else 0
            fat = form.fat.data if form.fat.data else 0

            # Calculate calories using the macronutrient distribution
            calories = (protein * 4) + (carbs * 4) + (fat * 9)
            result = round(calories, 2)

            # Calculate total macronutrients
            total_macronutrients = protein + carbs + fat

            # Calculate percentages
            protein_percentage = (protein / total_macronutrients) * 100
            carbs_percentage = (carbs / total_macronutrients) * 100
            fat_percentage = (fat / total_macronutrients) * 100

            # Provide recommendations based on fitness goals
            recommendations = {
                'weight_loss': {'protein': 30, 'carbs': 40, 'fat': 30},
                'muscle_gain': {'protein': 40, 'carbs': 40, 'fat': 20},
                'maintenance': {'protein': 25, 'carbs': 50, 'fat': 25}
            }

            # Determine the closest recommendation based on user input
            min_distance = float('inf')
            for goal, values in recommendations.items():
                distance = sum((values[nutrient] - user_percentage) ** 2 for nutrient, user_percentage in zip(['protein', 'carbs', 'fat'], [protein_percentage, carbs_percentage, fat_percentage]))
                if distance < min_distance:
                    min_distance = distance
                    recommendation = goal

        except ValueError:
            result = "Invalid input. Please enter numeric values for protein, carbs, and fat."

    return render_template('index.html', form=form, result=result, recommendation=recommendation)


@app.route('/recommendation', methods=['POST'])
def get_macronutrient_recommendation():
    # Get user input from the form
    protein = float(request.form['protein']) if request.form['protein'] else 0
    carbs = float(request.form['carbs']) if request.form['carbs'] else 0
    fat = float(request.form['fat']) if request.form['fat'] else 0

    # Calculate total macronutrients
    total_macronutrients = protein + carbs + fat

    # Calculate percentages
    protein_percentage = (protein / total_macronutrients) * 100
    carbs_percentage = (carbs / total_macronutrients) * 100
    fat_percentage = (fat / total_macronutrients) * 100

    # Provide recommendations based on fitness goals
    recommendations = {
        'weight_loss': {'protein': 30, 'carbs': 40, 'fat': 30},
        'muscle_gain': {'protein': 40, 'carbs': 40, 'fat': 20},
        'maintenance': {'protein': 25, 'carbs': 50, 'fat': 25}
    }

    return jsonify({
        'user_input': {'protein': protein_percentage, 'carbs': carbs_percentage, 'fat': fat_percentage},
        'recommendations': recommendations
    })

@app.route('/chart_data', methods=['POST'])
def get_chart_data():
    # Get user input from the form
    protein = float(request.form['protein']) if request.form['protein'] else 0
    carbs = float(request.form['carbs']) if request.form['carbs'] else 0
    fat = float(request.form['fat']) if request.form['fat'] else 0

    # Calculate percentages
    protein_percentage = (protein / (protein + carbs + fat)) * 100
    carbs_percentage = (carbs / (protein + carbs + fat)) * 100
    fat_percentage = (fat / (protein + carbs + fat)) * 100

    return jsonify({
        'labels': ['Protein', 'Carbs', 'Fat'],
        'data': [protein_percentage, carbs_percentage, fat_percentage]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
