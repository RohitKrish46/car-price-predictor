from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('carprice.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        car_details = {
            'make': request.form['make'],
            'model': request.form['model'],
            'year': int(request.form['year']),
            'mileage': int(request.form['mileage'])
        }
        # Placeholder logic for prediction
        estimated_price = 15000  # Replace with your model's output
        return render_template('result.html', price=estimated_price)
    return render_template('predict.html')

@app.route('/about')
def about():
    return "About Page (Coming Soon!)"

@app.route('/contact')
def contact():
    return "Contact Page (Coming Soon!)"

if __name__ == '__main__':
    app.run(debug=True)
