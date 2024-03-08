FROM python:3.8
LABEL authors="Nils Stenkēvičs"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV APP_NAME CalorieCalculator

# Run app.py when the container launches
CMD ["python", "calculator.py"]