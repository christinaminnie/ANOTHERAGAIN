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

    x = 0
    for i in range(0, len(lines), 2):
        x += 1
        print (x)
        name = lines[i].strip()
        location = lines[i+1].strip()
        company = Company(name=name, location=location)
        db.session.add(company)
        print(f'{company.name}\nRelease Date: {company.location}\n')

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
    one.description = "A round-based, 5v5 tactical FPS"
    one.company = Company.query.get(1)

    two = VideoGame.query.get(2)
    two.description = "N/A"
    two.company = Company.query.get(1)

    three = VideoGame.query.get(3)
    three.description = "Single-player, Galaxy-spanning action-adventure"
    three.company = Company.query.get(3)

    four = VideoGame.query.get(4)
    four.description = "Fast-paced FPS"
    four.company = Company.query.get(4)

    five = VideoGame.query.get(5)
    five.description = "MMO Dungeon Raid FPS"
    five.company = Company.query.get(5)

    six = VideoGame.query.get(6)
    six.description = "MMO Action RPG Dungeon"
    six.company = Company.query.get(6)

    seven = VideoGame.query.get(7)
    seven.description = "Realistic Vehicular Combat MMO"
    seven.company = Company.query.get(7)

    eight = VideoGame.query.get(8)
    eight.description = "Open world pirate adventure"
    eight.company = Company.query.get(8)

    nine = VideoGame.query.get(9)
    nine.description = "Fast-paced Battle Royale FPS"
    nine.company = Company.query.get(3)

    ten = VideoGame.query.get(10)
    ten.description = "Open world action-adventure western"
    ten.company = Company.query.get(10)

    eleven = VideoGame.query.get(11)
    eleven.description = "Massive open world Medieval RPG"
    eleven.company = Company.query.get(11)

    twelve = VideoGame.query.get(12)
    twelve.description = "Action RPG zombie survival"
    twelve.company = Company.query.get(12)

    thirteen = VideoGame.query.get(13)
    thirteen.description = "Dynamic Open world, action-adventure shooter"
    thirteen.company = Company.query.get(10)

    fourteen = VideoGame.query.get(14)
    fourteen.description = "Action based RPG 3rd person shooter"
    fourteen.company = Company.query.get(14)

    fifteen = VideoGame.query.get(15)
    fifteen.description = "Strategic and tactical round-based PvP FPS"
    fifteen.company = Company.query.get(15)

    sixteen = VideoGame.query.get(16)
    sixteen.description = "Third person horror survival"
    sixteen.company = Company.query.get(16)

    seventeen = VideoGame.query.get(17)
    seventeen.description = "Fishing adventure RPG"
    seventeen.company = Company.query.get(17)

    eighteen = VideoGame.query.get(18)
    eighteen.description = "Online 2022 NBA basketball"
    eighteen.company = Company.query.get(18)

    nineteen = VideoGame.query.get(19)
    nineteen.description = "Open world horror-survival"
    nineteen.company = Company.query.get(19)

    twenty = VideoGame.query.get(20)
    twenty.description = "Immersive open world Harry Potter RPG"
    twenty.company = Company.query.get(20)

    twenty_one = VideoGame.query.get(21)
    twenty_one.description = "Online dungeon action RPG"
    twenty_one.company = Company.query.get(21)

    twenty_two = VideoGame.query.get(22)
    twenty_two.description = "MMO RPG"
    twenty_two.company = Company.query.get(22)

    twenty_three = VideoGame.query.get(23)
    twenty_three.description = "Co-op horror-based puzzle"
    twenty_three.company = Company.query.get(23)

    twenty_four = VideoGame.query.get(24)
    twenty_four.description = "Online horror-survival"
    twenty_four.company = Company.query.get(24)

    twenty_five = VideoGame.query.get(25)
    twenty_five.description = "Open world, multiplayer survival FPS"
    twenty_five.company = Company.query.get(25)

    twenty_six = VideoGame.query.get(26)
    twenty_six.description = "Co-op adventure FPS Space-based RPG"
    twenty_six.company = Company.query.get(26)

    twenty_seven = VideoGame.query.get(27)
    twenty_seven.description = "Action-adventure survival RPG"
    twenty_seven.company = Company.query.get(27)

    twenty_eight = VideoGame.query.get(28)
    twenty_eight.description = "N/A"
    twenty_eight.company = Company.query.get(1)

    twenty_nine = VideoGame.query.get(29)
    twenty_nine.description = "Collection of Halo Games"
    twenty_nine.company = Company.query.get(5)

    thirty = VideoGame.query.get(30)
    thirty.description = "Real-life sandbox simulation"
    thirty.company = Company.query.get(30)

    thirty_one = VideoGame.query.get(31)
    thirty_one.description = "Fast-paced dungeon crawler RPG"
    thirty_one.company = Company.query.get(31)

    thirty_two = VideoGame.query.get(32)
    thirty_two.description = "Open world RPG action-adventure"
    thirty_two.company = Company.query.get(32)

    thirty_three = VideoGame.query.get(33)
    thirty_three.description = "MW2 battle-pass"
    thirty_three.company = Company.query.get(4)

    thirty_four = VideoGame.query.get(34)
    thirty_four.description = "MMO RPG "
    thirty_four.company = Company.query.get(34)

    thirty_five = VideoGame.query.get(35)
    thirty_five.description = "Turn-based, empire-building strategy"
    thirty_five.company = Company.query.get(35)

    thirty_six = VideoGame.query.get(36)
    thirty_six.description = "Multiplayer fast-paced FPS"
    thirty_six.company = Company.query.get(1)

    thirty_seven = VideoGame.query.get(37)
    thirty_seven.description = "Multiplayer fantasy farming simulator"
    thirty_seven.company = Company.query.get(37)

    thirty_eight = VideoGame.query.get(38)
    thirty_eight.description = "Tactical FPS SWAT RPG"
    thirty_eight.company = Company.query.get(38)

    thirty_nine = VideoGame.query.get(39)
    thirty_nine.description = "Online 2022 FIFA Football"
    thirty_nine.company = Company.query.get(30)

    forty = VideoGame.query.get(40)
    forty.description = "Single-player Action RPG dungeon"
    forty.company = Company.query.get(16)

    forty_one = VideoGame.query.get(41)
    forty_one.description = "Fast-paced FPS"
    forty_one.company = Company.query.get(41)
    
    forty_two = VideoGame.query.get(42)
    forty_two.description = "Fast-paced Multiplayer FPS"
    forty_two.company = Company.query.get(33)
    
    forty_three = VideoGame.query.get(43)
    forty_three.description = "Real-time sandbox strategy"
    forty_three.company = Company.query.get(34)
    
    forty_four = VideoGame.query.get(44)
    forty_four.description = "Action-adventure FPS RPG"
    forty_four.company = Company.query.get(12)
    
    forty_five = VideoGame.query.get(45)
    forty_five.description = "Co-op horror survival"
    forty_five.company = Company.query.get(35)
    
    forty_six = VideoGame.query.get(46)
    forty_six.description = "MMORPG"
    forty_six.company = Company.query.get(36)
    
    forty_seven = VideoGame.query.get(47)
    forty_seven.description = "Zombie survival RPG"
    forty_seven.company = Company.query.get(37)
    
    forty_eight = VideoGame.query.get(48)
    forty_eight.description = "Strategic card-based battle"
    forty_eight.company = Company.query.get(38)
    
    forty_nine = VideoGame.query.get(49)
    forty_nine.description = "Competitive card-based"
    forty_nine.company = Company.query.get(39)
    
    fifty = VideoGame.query.get(50)
    fifty.description = "Dungeon RPG adventure"
    fifty.company = Company.query.get(40)
    
    fifty_one = VideoGame.query.get(51)
    fifty_one.description = "Open world farming simulator"
    fifty_one.company = Company.query.get(41)
    
    fifty_two = VideoGame.query.get(52)
    fifty_two.description = "Farming RPG"
    fifty_two.company = Company.query.get(42)
    
    fifty_three = VideoGame.query.get(53)
    fifty_three.description = "Futuristic action RPG"
    fifty_three.company = Company.query.get(45)
    
    fifty_four = VideoGame.query.get(54)
    fifty_four.description = "Single-player action survival"
    fifty_four.company = Company.query.get(12)
    
    fifty_five = VideoGame.query.get(55)
    fifty_five.description = "Starwars MMORPG"
    fifty_five.company = Company.query.get(31)

    fifty_six = VideoGame.query.get(56)
    fifty_six.description = "Open-world adventure MMORPG"
    fifty_six.company = Company.query.get(40)

    fifty_seven = VideoGame.query.get(57)
    fifty_seven.description = "Vast open-world adventure RPG"
    fifty_seven.company = Company.query.get(45)

    fifty_eight = VideoGame.query.get(58)
    fifty_eight.description = "Nuclear War open-world adventure"
    fifty_eight.company = Company.query.get(19)

    fifty_nine = VideoGame.query.get(59)
    fifty_nine.description = "MMO strategy battle-area"
    fifty_nine.company = Company.query.get(46)

    sixty = VideoGame.query.get(60)
    sixty.description = "Sci-Fi sandbox strategy"
    sixty.company = Company.query.get(47)

    sixty_one = VideoGame.query.get(61)
    sixty_one.description = "Multiplayer team-based FPS"
    sixty_one.company = Company.query.get(48)

    sixty_two = VideoGame.query.get(62)
    sixty_two.description = "Fantasy base constuction simulation"
    sixty_two = Company.query.get(49)

    sixty_three = VideoGame.query.get(63)
    sixty_three.description = "Co-op third-person shooter survival"
    sixty_three.company = Company.query.get(50)

    sixty_four = VideoGame.query.get(64)
    sixty_four.description "City-building business simulation"
    sixty_four.company = Company.query.get(51)

    sixty_five = VideoGame.query.get(65)
    sixty_five.description = "Futuristic action-adventure FPS"
    sixty_five.company = Company.query.get(5)

    sixty_six = VideoGame.query.get(66)
    sixty_six.description = "Multiplayer real-time action strategy building"
    sixty_six.company = Company.query.get(52)

    sixty_seven = VideoGame.query.get(67)
    sixty_seven.description = "Flight simulation RPG"
    sixty_seven.company = Company.query.get(53)

    sixty_eight = VideoGame.query.get(68)
    sixty_eight.description = "Single-player strategy defense"
    sixty_eight.company = Company.query.get(54)

    sixty_nine = VideoGame.query.get(69)
    sizty_nine.description = "Open world online racing"
    sixty_nine.company = Company.query.get(55)

    seventy = VideoGame.query.get(70)
    seventy.description = "First-person RPG horror survival"
    seventy.company = Company.query.get(56)

    seventy_one = VideoGame.query.get(71)
    seventy-one.description = "Tactical battle RPG"
    seventy_one.company = Company.query.get(13)

    seventy_two = VideoGame.query.get(72)
    seventy_two.description = "Open world adventure RPG"
    seventy_two.company = Company.query.get(19)

    seventy_three = VideoGame.query.get(73)
    seventy_three.description = "Nation defense strategy"
    seventy_three.company = Company.query.get(47)

    seventy_four = VideoGame.query.get(74)
    seventy_four.description = "Open world oceanic survival"
    seventy_four.company = Company.query.get(57)

    seventy_five = VideoGame.query.get(75)
    seventy_five.description = "Third-person multiplayer PvP arena battle"
    seventy_five.company = Company.query.get(58)

    seventy_six = VideoGame.query.get(76)
    seventy_six.description = "Multiplayer FPS"
    seventy_six.company = Company.query.get(59)

    seventy_seven = VideoGame.query.get(77)
    seventy_seven.description = "TotalWar: WARHAMER AddOn"
    seventy_seven.company = Company.query.get(28)

    seventy_eight = VideoGame.query.get(78)
    seventy_eight.description = "Single-player action-adventure zombie survival"
    seventy_eight.company = Company.query.get(60)

    seventy_nine = VideoGame.query.get(79)
    seventy_nine.description = "Authentic Boxing"
    seventy_nine.company = Company.query.get(61)

    eighty = VideoGame.query.get(80)
    eighty.description = "MMORPG survival and exploration"
    eighty.company = Company.query.get(62)

    eighty_one = VideoGame.query.get(81)
    eighty_one.description = "Open world barbarian survival"
    eighty_one.company = Company.query.get(63)

    eighty_two = VideoGame.query.get(82)
    eighty_two.description = "Multiplayer sandbox zombie survival"
    eighty_two.company = Company.query.get(64)

    eighty_three = VideoGame.query.get(83)
    eighty_three.description = "Tactical fantasy strategy RPG "
    eighty_three.company = Company.query.get(65)

    eighty_four = VideoGame.query.get(84)
    eighty_four.description = "Turn-based strategic fantasy battle"
    eighty_four.company = Company.query.get(6)

    eighty_five = VideoGame.query.get(85)
    eighty_five.description = "Multiplayer survival platform exploration"
    eighty_five.company = Company.query.get(67)

    eighty_six = VideoGame.query.get(86)
    eighty_six.description = "Single-player action RPG"
    eighty_six.company = Company.query.get(68)

    eighty_seven = VideoGame.query.get(87)
    eighty_seven.description = "Strategy war-simulator RPG"
    eighty_seven.company = Company.query.get(47)

    eighty_eight = VideoGame.query.get(88)
    eighty_eight.description = "Multiplayer vehicle adventure"
    eighty_eight.company = Company.query.get(69)

    eighty_nine = VideoGame.query.get(89)
    eighty_nine.description = "Single-player open-world adventure"
    eighty_nine.company = Company.query.get(12)

    ninety = VideoGame.query.get(90)
    ninety.description = "Multiplayer monster horde survival"
    ninety.company = Company.query.get(70)

    ninety_one = VideoGame.query.get(91)
    ninety_one.description = "Open-world vehicle simulation"
    ninety_one.company = Company.query.get(71)

    ninety_two = VideoGame.query.get(92)
    ninety_two.description = "Multiplayer racing and adventure"
    ninety_two.company = Company.query.get(55)

    ninety_three = VideoGame.query.get(93)
    ninety_three.description = "Multiplayer platform sandbox"
    ninety_three.company = Company.query.get(72)

    ninety_four = VideoGame.query.get(94)
    ninety_four.description = "MMO vehicular warship battles"
    ninety_four.company = Company.query.get(73)

    ninety_five = VideoGame.query.get(95)
    ninety_five.description = "N/A"
    ninety_five = Company.query.get(1)

    ninety_six = VideoGame.query.get(96)
    ninety_six.description = "Multiplayer arcade-like fighting"
    ninety_six.company = Company.query.get(13)

    ninety_seven = VideoGame.query.get(97)
    ninety_seven.description = "Starwars MMORPG third-person shooter"
    ninety_seven = Company.query.get(74)

    ninety_eight = VideoGame.query.get(98)
    ninety_eight.description = "Open-world prehistoric survival"
    ninety_eight.company = Company.query.get(75)

    ninety_nine = VideoGame.query.get(99)
    ninety_nine.description = "Single-player house renovation simulator"
    ninety_nine = Company.query.get(76)

    one_hundred = VideoGame.query.get(100)
    one_hundred.description = "Adventure 18-wheeler truck simulator"
    one_hundred.company = Company.query.get(77)

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
