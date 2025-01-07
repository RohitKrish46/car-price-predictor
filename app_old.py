from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model and preprocessor
with open('./models/model.pkl', 'rb') as file:
    model = pickle.load(file)
    
with open('preprocessor.pkl', 'rb') as file:
    preprocessor = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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
        
        # Format prediction as currency
        formatted_prediction = "₹{:,.2f}".format(prediction)
        
        return render_template('index.html', 
                             prediction_text=f'Estimated car price is: {formatted_prediction}',
                             features=features)
    
    except Exception as e:
        return render_template('index.html', 
                             error_text=f'Error making prediction: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)