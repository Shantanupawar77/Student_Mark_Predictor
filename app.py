import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

model = joblib.load("student_mark_predictor.pkl")

df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global df
    input_features = [int(x) for x in request.form.values()]
    features_value = np.array(input_features)
    
    # Validate input hours
    if input_features[0] < 0 or input_features[0] > 24:
        return render_template('index.html', prediction_text='Please enter valid hours between 1 to 24')
    
    output = model.predict([features_value])[0][0].round(2)

    # Input and predicted value store in df then save in csv file
    df = pd.concat([df, pd.DataFrame({'Study Hours': input_features, 'Predicted Output': [output]})], ignore_index=True)
    df.to_csv('smp_data_from_app.csv')

    # Modified predicted output sentence
    if(output>100):
        output=99
    
    return render_template('index.html', prediction_text='Based on our analysis, you are expected to achieve a remarkable score of [{}%] when dedicating [{}] hours to your studies each day.'.format(output, int(features_value[0])))

