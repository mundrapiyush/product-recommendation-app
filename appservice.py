from flask import Flask, render_template, request
from modelservice import ModelService

app = Flask("__name__", template_folder='templates')

model_service = ModelService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form.get('username', '')

    # Use modelservice to get recommendations or data
    recommendations, brands = model_service.get_top_n_recommendations_based_on_user(username)

    table_data = []
    for brand, rating in recommendations.items():
        table_data.append({
            'product': brand.split('#')[-1],
            'rating': rating
        })

    return render_template('results.html', username=username, table_data=table_data)

if __name__ == '__main__':
    app.run()
