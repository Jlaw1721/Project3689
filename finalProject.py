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

# these are the forms that we used for the web scrapping data
class searchData(FlaskForm):
  zips = StringField('Enter a Location(zip code):', validators=[DataRequired()])
  gas = SelectField('Choose a Gas Type', choices=[('regular', 'Regular'), ('premium', 'Premium'), ('mid-grade', 'Mid-Grade'), ('diesel', 'Diesel')], validators=[DataRequired()])


# variable to store form data
searchResults = list(range(2))

def store_data(data, plc):
    searchResults[plc] = data

# first route which serves to retrieve data from the user
@app.route('/', methods=('GET', 'POST'))
def index():
    form = searchData()
    if form.validate_on_submit():
        store_data(form.zips.data, 0)
        store_data(form.gas.data, 1)
       
        
        return redirect('/testAction')
    return render_template('app_template.html', form=form)

# route which webscrapes and displays result to user
@app.route('/testAction', methods=('GET', 'POST'))
def display():
    #these two lines fix the issue of multi-word city names not working as well as removing the case sensitivity
    cityName = searchResults[0].lower()
    cityName = cityName.replace(" ", "-")
    
    url = ''
    if searchResults[1] == "regular":
        url = f"https://www.autoblog.com/{cityName}-gas-prices/"
    else:
        url = f"https://www.autoblog.com/{cityName}-gas-prices/{searchResults[1]}/"

    results = requests.get(url)

    soup = BeautifulSoup(results.content, 'html.parser')
    #lists to store the retrieved data
    names = []
    #Not entirely sure how the OG website calculates the distance values. Best guess is that it calculates the distance relative to some point in the searched location itself, rather than the user's location
    distances = []
    addresses = []
    prices = []
    #populate lists
    for row in soup.find_all('li', attrs = {'class':'name'}):
        names.append(row.h4.text)
        addresses.append(row.address.text)
    for row in soup.find_all('data', attrs = {'class':'price'}):
        prices.append(row["value"])
    for row in soup.find_all('data', attrs = {'class':'distance'}):
        distances.append(row.text)
    
    

    return render_template('app_template2.html', names = names, addresses = addresses, prices = prices, len = len(names), distances = distances)

