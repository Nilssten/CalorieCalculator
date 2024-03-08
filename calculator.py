from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm # Change this line
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired, Optional
from wtforms.validators import ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = '!%9{!yor=dV2umkZ$WC@Mk|M5{:AdX'  # Change this to a secure secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Uncomment if you want to use SQLAlchemy

# Uncomment the following lines if you are using SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)

# Example SQLAlchemy model
# class UserData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     protein = db.Column(db.Float, nullable=False)
#     carbs = db.Column(db.Float, nullable=False)
#     fat = db.Column(db.Float, nullable=False)
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

    if form.validate_on_submit():
        try:
            # Get user input from the form, defaulting to 0 if the field is empty
            protein = form.protein.data if form.protein.data else 0
            carbs = form.carbs.data if form.carbs.data else 0
            fat = form.fat.data if form.fat.data else 0

            # Calculate calories using the macronutrient distribution
            calories = (protein * 4) + (carbs * 4) + (fat * 9)
            result = round(calories, 2)

        except ValueError:
            result = "Invalid input. Please enter numeric values for protein, carbs, and fat."

    return render_template('index.html', form=form, result=result)


if __name__ == '__main__':
    # Uncomment the following line if you are using SQLAlchemy
    # db.create_all()
    app.run(host='0.0.0.0', port=80)
