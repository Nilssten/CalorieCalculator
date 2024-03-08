from flask import Flask, render_template, request, session
from wtforms import FloatField, SubmitField, Form
from wtforms.validators import InputRequired

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

class CalorieForm(Form):  # Change FlaskForm to Form
    protein = FloatField('Protein (g)', validators=[InputRequired()])
    carbs = FloatField('Carbs (g)', validators=[InputRequired()])
    fat = FloatField('Fat (g)', validators=[InputRequired()])
    submit = SubmitField('Calculate Calories')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CalorieForm()
    result = None

    if form.validate_on_submit():
        try:
            # Get user input from the form
            protein = form.protein.data
            carbs = form.carbs.data
            fat = form.fat.data

            # Calculate calories using the macronutrient distribution
            calories = (protein * 4) + (carbs * 4) + (fat * 9)
            result = round(calories, 2)

            # Uncomment the following lines if you are using SQLAlchemy
            # user_data = UserData(protein=protein, carbs=carbs, fat=fat)
            # db.session.add(user_data)
            # db.session.commit()

        except ValueError:
            result = "Invalid input. Please enter numeric values for protein, carbs, and fat."

    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    # Uncomment the following line if you are using SQLAlchemy
    # db.create_all()
    app.run(host='0.0.0.0', port=80)
