from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

class Playlist(FlaskForm):
  song_title = StringField(
	'Enter a zip code:',
	validators=[DataRequired()]
)


#
zips = []
# def store_song(my_song):
#     zips.append(dict(zip = my_song,))
#     # print(zips)
#     # print("This is your zip code: ", my_song)

@app.route('/', methods=('GET', 'POST'))
def index():
    form = Playlist()
    if form.validate_on_submit():
        zips.append(form.song_title.data)
        # print("This is your zip code: ", zips)
        
        return redirect('/testAction')
    return render_template('app_template.html', form=form)

# print("This is your zip code: ", zips)

@app.route('/testAction', methods=('GET', 'POST'))
def display():
    select = request.form.get('selector')
    print(select)
    print(zips)
    return render_template('app_template2.html',zipNew = zips,gasType=select)

