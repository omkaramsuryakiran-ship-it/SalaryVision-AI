import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
import pandas as pd
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'salary_prediction_secret_key'

# Load the model and data
try:
      with open('model.pkl', 'rb') as f:
                model = pickle.load(f)
            df = pd.read_csv('salary_data.csv')
except:
    # Fallback for demonstration if files don't exist
      model = None
    df = pd.DataFrame()

@app.route('/')
def index():
      return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
      username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'admin':
              session['logged_in'] = True
              return redirect(url_for('dashboard'))
else:
        flash('Invalid credentials')
          return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
      if not session.get('logged_in'):
                return redirect(url_for('index'))
            return render_template('dashboard.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
      if not session.get('logged_in'):
                return redirect(url_for('index'))
            if request.method == 'POST':
                      # Logic for prediction
                      experience = float(request.form.get('experience', 0))
                      # Dummy prediction logic
                      prediction = 30000 + (experience * 5000)
                      return render_template('predict.html', prediction=prediction)
                  return render_template('predict.html')

@app.route('/performance')
def performance():
      if not session.get('logged_in'):
                return redirect(url_for('index'))
            return render_template('performance.html')

@app.route('/charts')
def charts():
      if not session.get('logged_in'):
                return redirect(url_for('index'))
            return render_template('charts.html')

if __name__ == '__main__':
      port_num = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port_num)
