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

    # Fetch vectorized reviews for the recommendations
    top_products = model_service.get_top_productes_based_on_vectorized_reviews(recommendations)

    # Read the top_products dataframe and create a table for display
    table_data = top_products.to_dict(orient='records')

    return render_template('results.html', username=username, table_data=table_data)

if __name__ == '__main__':
    app.run()
