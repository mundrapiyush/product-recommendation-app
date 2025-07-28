from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    username = request.form.get('username', '')

    # Example logic to generate table data based on username
    # Here, we create a list of dictionaries representing rows in the table
    table_data = [
        {"ID": i+1, "Username": username, "Info": f"Info {i+1}"} for i in range(5)
    ]

    return render_template('results.html', username=username, table_data=table_data)

if __name__ == '__main__':
    app.run()
