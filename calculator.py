from flask import Flask, render_template, request, session, redirect, url_for, g
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import Optional
from flask_babel import Babel, gettext
from flask_session import Session

# Define the supported languages
LANGUAGES = ['en', 'lv']

app = Flask(__name__)
app.config['SECRET_KEY'] = '!%9{!yor=dV2umkZ$WC@Mk|M5{:AdX'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.config['LANGUAGES'] = LANGUAGES
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)
def get_locale():
    print("User Language:", g.user_language) #Just to test if language switching works
    return g.user_language


@app.before_request
def before_request():
    g.user_language = session.get('lang') or request.args.get('lang') or request.accept_languages.best_match(LANGUAGES)

def init_babel(app):
    babel.init_app(app, locale_selector=get_locale)

init_babel(app)

def zero_if_empty(form, field):
    if field.data == '':
        field.data = 0

class CalorieForm(FlaskForm):
    protein = FloatField(gettext('Protein (g)'), validators=[Optional(), zero_if_empty])
    carbs = FloatField(gettext('Carbs (g)'), validators=[Optional(), zero_if_empty])
    fat = FloatField(gettext('Fat (g)'), validators=[Optional(), zero_if_empty])
    submit = SubmitField(gettext('Calculate Calories'))

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
            result = gettext('Invalid input. Please enter numeric values for protein, carbs, and fat.')

    return render_template('index.html', form=form, result=result, recommendation=recommendation, get_locale=get_locale)

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    g.user_language = lang
    return redirect(request.referrer or url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
