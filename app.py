from flask import Flask, render_template, request
import pickle
import pandas as pd
import locale
app = Flask(__name__)


# Set locale to Indian format
locale.setlocale(locale.LC_ALL, 'en_IN')

def format_currency(value):
    return locale.format_string("%d", value, grouping=True)

# Load the trained model and preprocessor
with open('./models/model.pkl', 'rb') as file:
    model = pickle.load(file)
    
with open('preprocessor.pkl', 'rb') as file:
    preprocessor = pickle.load(file)

@app.route('/')
def home():
    return render_template('carprice.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data and create DataFrame with proper column names
            features = {
                # Numeric features
                'km_driven': float(request.form['km_driven']),
                'mileage': float(request.form['mileage']),
                'engine': float(request.form['engine']),
                'max_power': float(request.form['max_power']),
                'year': int(request.form['year']),
                'vehicle_age':int(request.form['vehicle_age']),
                'seats': int(request.form['seats']),
                
                # OneHot encoded features
                'seller_type': request.form['seller_type'],
                'fuel_type': request.form['fuel_type'],
                'transmission_type': request.form['transmission_type'],
                
                # Binary encoded feature
                'car_name': request.form['car_name']
            }
            
            # Convert to DataFrame
            features_df = pd.DataFrame([features])
            
            # Apply preprocessing
            features_processed = preprocessor.transform(features_df)
            
            # Make prediction
            prediction = model.predict(features_processed)[0]
            print(prediction)
            # Format prediction as currency
            formatted_prediction = format_currency(prediction)
            return render_template('result.html', price=formatted_prediction, car_name=features['car_name'])
        
        except Exception as e:
            return render_template('index.html', 
                                error_text=f'Error making prediction: {str(e)}')
        
    return render_template('predict.html')

@app.route('/about')
def about():
    return "About Page (Coming Soon!)"

@app.route('/contact')
def contact():
    return "Contact Page (Coming Soon!)"

if __name__ == '__main__':
    app.run(debug=True)
