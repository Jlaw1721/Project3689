from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('app_template.html')

@app.route('/testAction', methods=('GET', 'POST'))
def display():
    return render_template('app_template2.html')

