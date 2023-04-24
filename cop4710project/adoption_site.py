import os

from forms import AddForm, DelForm, AddRatingForm, gameSearchForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, url_for, redirect, flash, request
from sqlalchemy.orm import Query
from tables import Results


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey';

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


# db.init_app(app)
# db.app = app


class VideoGame(db.Model):
    query: db.Query
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.String)
    price = db.Column(db.Text)

    # many video games to many genres and many platforms
    genres = db.relationship('Genre', secondary='video_game_genre', backref='video_game_g')
    compatibility = db.relationship('Platform', secondary='video_game_platform', backref='video_game_p')
    # many video games to one company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref=db.backref("video_game_c", order_by=id, lazy=True))

    def __init__(self, name, description, release_date, price, company):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.price = price
        self.company = company

    def __repr__(self):
        return f"GAME: {self.name}\nDescription: {self.description}\nRelease Date: {self.release_date}\nPrice: {self.price}\nCompany: {self.company}\n"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeric_rating = db.Column(db.Integer)
    verbal_rating = db.Column(db.Text)
    # many ratings to one video game
    video_game_id = db.Column(db.Integer, db.ForeignKey('video_game.id'))
    video_game = db.relationship('VideoGame', backref=db.backref("rating", cascade="all,delete"))

    def __init__(self, numeric_rating, verbal_rating, video_game_id):
        self.numeric_rating = numeric_rating
        self.verbal_rating = verbal_rating
        self.video_game_id = video_game_id

    def __repr__(self):
        return f"Video Game ID: {self.video_game_id}, Numeric Rating: {self.numeric_rating}, Verbal Rating: {self.verbal_rating}"


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"GENRE ......."


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    platform_device = db.Column(db.Text)
    manufacturer = db.Column(db.Text)

    def __init__(self, name, platform_device, manufacturer):
        self.name = name
        self.platform_device = platform_device
        self.manufacturer = manufacturer

    def __repr__(self):
        return f"Platform ... "


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # my idea behind location is we can just put general like America or Japan
    # but we can add a hyperlink to the company website
    location = db.Column(db.Text)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        return f"name = {self.name}, location = {self.location}"


video_game_genre = db.Table('video_game_genre',
                            db.Column('video_game_id', db.Integer, db.ForeignKey('video_game.id')),
                            db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                            )

video_game_platform = db.Table('video_game_platform',
                               db.Column('video_game_id', db.Integer, db.ForeignKey('video_game.id')),
                               db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'))
                               )

# adding parts of video game
with app.app_context():
    db.create_all()

    with open(r'C:\Users\nguye\FlaskStuff\cop4710project\output.txt', 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            name = lines[i].strip()
            release_date = lines[i + 1].strip()
            price = lines[i + 2].strip()

            # Check if a video game with the same name already exists in the database
            existing_game = VideoGame.query.filter_by(name=name).first()
            if not existing_game:
                # If not, add the new game to the database
                game = VideoGame(name=name, release_date=release_date, price=price, description=None,
                                 company=None)
                db.session.add(game)

    db.session.commit()

# adding genres
with app.app_context():
    db.create_all()

    with open(r'C:\Users\nguye\FlaskStuff\cop4710project\steamtags.txt', 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 1):
        genre_name = lines[i].strip()
        genre = Genre(name=name)
        db.session.add(genre)

    db.session.commit()

# adding company
with app.app_context():
    db.create_all()

    with open(r'C:\Users\nguye\FlaskStuff\cop4710project\compcountry.txt', 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 2):
        name = lines[i].strip()
        location = lines[i+1].strip()
        company = Company(name=name, location=location)
        db.session.add(company)

    db.session.commit()

# hardcoding
with app.app_context():
    db.create_all()

    comp = Company('testing', 'testing')
    db.session.add(comp)

    # hard coded platforms
    xbox = Platform('Xbox', 'Controller, Mouse/Keyboard', 'Microsoft')
    playstation = Platform('Playstation', 'Controller, Mouse/Keyboard', 'Sony')
    nintendo = Platform('Nintendo', 'Switch', 'Nintendo Co.')
    computer = Platform('Computer', 'Controller, Mouse/Keyboard', 'Varying')
    mobile = Platform('Mobile', 'Phone', 'Varying')
    db.session.add(xbox)
    db.session.add(playstation)
    db.session.add(nintendo)
    db.session.add(computer)
    db.session.add(mobile)

    # hard code descriptions from video games
    one = VideoGame.query.get(1)
    one.description = "A round-based, 5v5 tactical FPS with an Attackers vs Defenders setup and no respawns"

    one.company = Company.query.get(2)

    two = VideoGame.query.get(2)

    three = VideoGame.query.get(3)

    four = VideoGame.query.get(4)

    five = VideoGame.query.get(5)

    six = VideoGame.query.get(6)

    seven = VideoGame.query.get(7)

    eight = VideoGame.query.get(8)

    nine = VideoGame.query.get(9)

    ten = VideoGame.query.get(10)

    eleven = VideoGame.query.get(11)

    twelve = VideoGame.query.get(12)

    thirteen = VideoGame.query.get(13)

    fourteen = VideoGame.query.get(14)

    fifteen = VideoGame.query.get(15)

    sixteen = VideoGame.query.get(16)

    seventeen = VideoGame.query.get(17)

    eighteen = VideoGame.query.get(18)

    nineteen = VideoGame.query.get(19)

    twenty = VideoGame.query.get(20)

    twenty_one = VideoGame.query.get(21)

    twenty_two = VideoGame.query.get(22)

    twenty_three = VideoGame.query.get(23)

    twenty_four = VideoGame.query.get(24)

    twenty_five = VideoGame.query.get(25)

    twenty_six = VideoGame.query.get(26)

    twenty_seven = VideoGame.query.get(27)

    twenty_eight = VideoGame.query.get(28)

    twenty_nine = VideoGame.query.get(29)

    thirty = VideoGame.query.get(30)

    thirty_one = VideoGame.query.get(31)
    thirty_two = VideoGame.query.get(32)
    thirty_three = VideoGame.query.get(33)
    thirty_four = VideoGame.query.get(34)
    thirty_five = VideoGame.query.get(35)
    thirty_six = VideoGame.query.get(36)
    thirty_seven = VideoGame.query.get(37)
    thirty_eight = VideoGame.query.get(38)
    thirty_nine = VideoGame.query.get(39)
    forty = VideoGame.query.get(40)
    forty_one = VideoGame.query.get(41)
    forty_two = VideoGame.query.get(42)
    forty_three = VideoGame.query.get(43)
    forty_four = VideoGame.query.get(44)
    forty_five = VideoGame.query.get(45)
    forty_six = VideoGame.query.get(46)
    forty_seven = VideoGame.query.get(47)
    forty_eight = VideoGame.query.get(48)
    forty_nine = VideoGame.query.get(49)
    fifty = VideoGame.query.get(50)
    fifty_one = VideoGame.query.get(51)
    fifty_two = VideoGame.query.get(51)
    fifty_three = VideoGame.query.get(53)
    fifty_four = VideoGame.query.get(54)
    fifty_five = VideoGame.query.get(55)
    fifty_six = VideoGame.query.get(56)
    fifty_seven = VideoGame.query.get(57)
    fifty_eight = VideoGame.query.get(58)
    fifty_nine = VideoGame.query.get(59)
    sixty = VideoGame.query.get(60)
    sixty_one = VideoGame.query.get(61)
    sixty_two = VideoGame.query.get(62)
    sixty_three = VideoGame.query.get(63)
    sixty_four = VideoGame.query.get(64)
    sixty_five = VideoGame.query.get(65)
    sixty_six = VideoGame.query.get(66)
    sixty_seven = VideoGame.query.get(67)
    sixty_eight = VideoGame.query.get(68)
    sixty_nine = VideoGame.query.get(69)
    seventy = VideoGame.query.get(70)
    seventy_one = VideoGame.query.get(71)
    seventy_two = VideoGame.query.get(72)
    seventy_three = VideoGame.query.get(73)
    seventy_four = VideoGame.query.get(74)
    seventy_five = VideoGame.query.get(75)
    seventy_six = VideoGame.query.get(76)
    seventy_seven = VideoGame.query.get(77)
    seventy_eight = VideoGame.query.get(78)
    seventy_nine = VideoGame.query.get(79)
    eighty = VideoGame.query.get(80)
    eighty_one = VideoGame.query.get(81)
    eighty_two = VideoGame.query.get(82)
    eighty_three = VideoGame.query.get(83)
    eighty_four = VideoGame.query.get(84)
    eighty_five = VideoGame.query.get(85)
    eighty_six = VideoGame.query.get(86)
    eighty_seven = VideoGame.query.get(87)
    eighty_eight = VideoGame.query.get(88)
    eighty_nine = VideoGame.query.get(89)
    ninety = VideoGame.query.get(90)
    ninety_one = VideoGame.query.get(91)
    ninety_two = VideoGame.query.get(92)
    ninety_three = VideoGame.query.get(93)
    ninety_four = VideoGame.query.get(94)
    ninety_five = VideoGame.query.get(95)
    ninety_six = VideoGame.query.get(96)
    ninety_seven = VideoGame.query.get(97)
    ninety_eight = VideoGame.query.get(98)
    ninety_nine = VideoGame.query.get(99)
    one_hundred = VideoGame.query.get(100)

    db.session.commit()


############################################

# VIEWS WITH FORMS

##########################################

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_game():
    form = AddForm(request.form)

    if form.validate_on_submit():
        company = comp
        # company=company(name="company")

        name = form.name.data
        description = form.description.data
        release_date = form.release_date.data
        # compatibility = form.compatibility.data
        price = form.price.data

        new_game = VideoGame(name, description, release_date, price, company)

        check = bool(VideoGame.query.filter_by(name=new_game.name).first())
        if check:
            save_changes(new_game, form, new=False)
        if not check:
            save_changes(new_game, form, new=True)

        return redirect(url_for('list_game'))

    if request.method == 'POST' and form.validate():
        video_game = VideoGame()
        save_changes(video_game, form, new=True)
        flash('Video Game created successfully!')
        return redirect('/list_game')

    return render_template('add.html', form=form)


# save changes to db
def save_changes(video_game, form, new=False):
    company = comp
    # company.name = form.company.data

    video_game.name = form.name.data
    video_game.description = form.description.data
    video_game.release_date = form.release_date.data
    # video_game.compatibility = form.compatibility.data
    video_game.price = form.price.data
    video_game.company = company
    # video_game.company = None

    if new:
        db.session.add(video_game)

    db.session.commit()


@app.route('/search_engine', methods=['GET', 'POST'])
def search_game():
    search = gameSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    if search.validate_on_submit():
        return redirect(url_for('search_engine'))

    return render_template('search.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Name':
            qry = db.session.query(VideoGame).filter(VideoGame.name.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Description':
            qry = db.session.query(VideoGame).filter(VideoGame.description.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Release Date':
            qry = db.session.query(VideoGame).filter(VideoGame.release_date.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Price':
            qry = db.session.query(VideoGame).filter(VideoGame.price.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'CompanyID':
            pass
        else:
            qry = db.session.query(VideoGame)
            results = qry.all()
    else:
        qry = db.session.query(VideoGame)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/search_engine')

    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/list')
def list_game():
    # Grab a list of games from database.
    videogames = VideoGame.query.all()
    return render_template('list.html', videogames=videogames)


@app.route('/delete', methods=['GET', 'POST'])
def del_game():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        game = VideoGame.query.get(id)
        db.session.delete(game)
        db.session.commit()

        return redirect(url_for('list_game'))
    return render_template('delete.html', form=form)


@app.route('/addrating', methods=['GET', 'POST'])
def add_rating():
    form = AddRatingForm()

    if form.validate_on_submit():
        numeric_rating = form.numeric_rating.data
        verbal_rating = form.verbal_rating.data
        video_game_id = form.video_game_id.data

        # Add new rating to database
        new_rating = Rating(numeric_rating, verbal_rating, video_game_id)
        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('list_ratings'))

    return render_template('rating.html', form=form)


@app.route('/listratings')
def list_ratings():
    ratings = Rating.query.all()
    return render_template('ratinglist.html', ratings=ratings)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db.session.query(VideoGame).filter(
        VideoGame.id == id
    )
    video_game = qry.first()

    if video_game:
        form = AddForm(formdata=request.form, obj=video_game)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(video_game, form)
            flash('Video Game updated successfully!')
            return redirect('/search_engine')
        return render_template('edit_video_game.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


if __name__ == '__main__':
    app.run(debug=True)
