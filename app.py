from flask import Flask, render_template, url_for
from routes import routes

app = Flask(__name__)

app.register_blueprint(routes)


@app.route("/")
def index():
    url_for('static', filename='style.css')
    return render_template('index.html', track_src='#', track_title='Track Title')
