from flask import Flask, render_template, request
from modelservice import ModelService

app = Flask(__name__)

model_service = ModelService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form.get('username', '')

    # Use modelservice to get recommendations or data
    recommendations, brands = model_service.get_top_n_recommendations_based_on_item(username)
    
    if not recommendations or not brands:
        return render_template('error.html', message="No recommendations found for the user.")
    
    # Prepare data for rendering in the template
    table_data = []
    for brand, rating in recommendations.items():
        table_data.append({
            'brand': brand,
            'rating': rating
        })
    return render_template('results.html', username=username, table_data=table_data)

if __name__ == '__main__':
    app.run()
