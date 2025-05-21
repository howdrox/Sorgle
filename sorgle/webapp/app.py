from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    # Simple landing page
    return render_template('home.html')

@app.route('/index')
def profile():
    # Load your JSON data
    with open('C:/Users/wangq/THU/Sorgle/sorgle/data/professors.json') as f:
        professor_data = json.load(f)[0]
    return render_template('index.html', professor=professor_data)

if __name__ == '__main__':
    app.run(debug=True)