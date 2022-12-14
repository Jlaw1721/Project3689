from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

class searchData(FlaskForm):
  zips = StringField('Enter a Location(zip code):', validators=[DataRequired()])
  gas = SelectField('Choose a Gas Type', choices=[('regular', 'Regular'), ('premium', 'Premium'), ('mid-grade', 'Mid-Grade'), ('diesel', 'Diesel')], validators=[DataRequired()])


#
searchResults = list(range(2))

def store_data(data, plc):
    searchResults[plc] = data
    # print(zips)
    # print("This is your zip code: ", my_song)

@app.route('/', methods=('GET', 'POST'))
def index():
    form = searchData()
    if form.validate_on_submit():
        store_data(form.zips.data, 0)
        store_data(form.gas.data, 1)
        # print("This is your zip code: ", zips)
        
        return redirect('/testAction')
    return render_template('app_template.html', form=form)

# print("This is your zip code: ", zips)

@app.route('/testAction', methods=('GET', 'POST'))
def display():
    # select = request.form.get('selector')
    url = ''
    if searchResults[1] == "regular":
        url = f"https://www.autoblog.com/{searchResults[0]}-gas-prices/"
    else:
        url = f"https://www.autoblog.com/{searchResults[0]}-gas-prices/{searchResults[1]}/"

    results = requests.get(url)

    soup = BeautifulSoup(results.content, 'html.parser')
    names = []
    addresses = []
    prices = []
    for row in soup.find_all('li', attrs = {'class':'name'}):
        names.append(row.h4.text)
        addresses.append(row.address.text)
    for row in soup.find_all('data', attrs = {'class':'price'}):
        prices.append(row["value"])
    
    
    

    return render_template('app_template2.html', names = names, addresses = addresses, prices = prices, len = len(names))

