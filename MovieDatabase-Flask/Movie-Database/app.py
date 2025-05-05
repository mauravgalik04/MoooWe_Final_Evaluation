from flask import Flask, render_template, redirect, request, url_for, flash 
from flask_sqlalchemy import SQLAlchemy 
import os 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user 
from flask_bcrypt import Bcrypt 
from werkzeug.utils import secure_filename
from functools import wraps
from random import choice
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager , create_access_token , jwt_required , get_jwt_identity

basedir = os.path.abspath(os.path.dirname(__file__)) 
app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" +  os.path.join(basedir, "app.db") 
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SECRET_KEY"] = "Your_secret_key" 
app.config['JWT_SECRET_KEY'] = 'my_secret_key'
jwt = JWTManager(app)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
api = Api(app)

class Movie(db.Model , UserMixin):
    __tablename__ = "movie"
    sno = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String(100) )
    release_year = db.Column(db.Integer )
    imdb_rating = db.Column(db.Float )
    genre = db.Column(db.String )
    description = db.Column(db.String(200) ) 
    cast = db.Column(db.String(100) )
    poster = db.Column(db.String(2000) )
    landscape = db.Column(db.String(2000) )
    watchlist = db.Column(db.String , default = False)
    
    def as_dict(self):
        return {
            "sno":self.sno,
            "name":self.name,
            "release_year":self.release_year,
            "imdb_rating":self.imdb_rating,
            "genre":self.genre,
            "description":self.description,
            "cast":self.cast,
            "poster":self.poster,
            "landscape":self.landscape,
            "watchlist":self.watchlist
        }

class MovieResource(Resource):
    def get(self,sno):
        movie = db.session.get(Movie,sno)
        if movie:
            return movie.as_dict()
        else:
            return {"message":"Movie Not Found!"},404
    def post(self):
        data = request.get_json()
        name = data.get("name")
        year = data.get('release_year')
        genre = data.get('genre')
        story = data.get('description')
        cast = data.get('cast')
        imdb_rating = data.get('imdb_rating')
        poster = request.files.get('poster')
        landscape = request.files.get('landscape')

        if not all([name, year, genre, story, cast, imdb_rating, poster, landscape]):
            return {"message": "All fields are required."}, 400
        new_movie = Movie(
            name=name,
            release_year=year,
            genre=genre,
            description=story,
            imdb_rating=imdb_rating,
            cast=cast,
            poster=poster,
            landscape=landscape
        )
        db.session.add(new_movie)
        db.session.commit()

        return {"message": "Movie Added Successfully"}, 201

    def put(self,sno):
        movie = db.session.get(Movie,sno)
        if movie:
            data = request.get_json()
            movie.name = data.get('movie-name')
            movie.release_year = data.get('release-year')
            movie.genre = data.get('genre')
            movie.description = data.get('movie-description')
            movie.imdb_rating = data.get('imdb-rating')
            movie.cast = data.get('cast')
            db.session.commit()
            return {"message":"Movie Updated Successfully"},200
        else:
            return {"message":"Movie Not Found!!"},404
    def delete(self,sno):
        movie = db.session.get(Movie ,sno)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {"message":"Movie deleted Successfully"}
        else:
            return {"message":"Movie not found!!"},404
    def patch(self, sno):
        movie = db.session.get(Movie, sno)
        if not movie:
            return {"message": "Movie Not Found!"}, 404

        data = request.get_json()
        if 'movie-name' in data:
            movie.name = data['movie-name']
        if 'release-year' in data:
            movie.release_year = data['release-year']
        if 'genre' in data:
            movie.genre = data['genre']
        if 'movie-description' in data:
            movie.description = data['movie-description']
        if 'imdb-rating' in data:
            movie.imdb_rating = data['imdb-rating']
        if 'movie-cast' in data:
            movie.cast = data['movie-cast']
        if 'watchlist' in data:
            movie.watchlist = data['watchlist']  

        db.session.commit()
        return {"message": "Movie partially updated successfully"}, 200

class MoviesResource(Resource):
    def get(self):
        all_movies = Movie.query.all()
        movies = []
        for movie in all_movies:
            movies.append(movie.as_dict())
        if movies:
            return {"movies":movies}
        else:
            return {"message":"No Movies Found"}
    def post(self):
        data = request.get_json()
        name = data.get("name")
        year = data.get("release_year")
        genre = data.get("genre")
        story = data.get("description")
        cast = data.get("cast")
        imdb_rating = data.get("imdb_rating")
        poster = data.get("poster")
        landscape = data.get("landscape")

        if not all([name, year, genre, story, cast, imdb_rating, poster, landscape]):
            return {"message": "All fields are required."}, 400
        new_movie = Movie(
            name=name,
            release_year=year,
            genre=genre,
            description=story,
            imdb_rating=imdb_rating,
            cast=cast,
            poster=poster,
            landscape=landscape
        )
        db.session.add(new_movie)
        db.session.commit()

        return {"message": "Movie Added Successfully"}, 201
class User(db.Model , UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50) , nullable = False)
    email = db.Column(db.String(50) , nullable =True ,unique = True)
    password_hash = db.Column(db.String(100) , nullable =False)
    role = db.Column(db.String(50), nullable=False, default="user") 
    def set_password(self, password): 
        self.password_hash = bcrypt.generate_password_hash(password) 
    def check_password(self, password): 
        return bcrypt.check_password_hash(self.password_hash, password)
@login_manager.user_loader
def load_user(user_id): 
    return db.session.get(User, int(user_id))

def admin_required(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin': 
            flash("Access denied!", "danger") 
            return redirect(url_for('landing'))
        return func(*args, **kwargs) 
    return wrapper 
with app.app_context(): 
    db.create_all()
    if not User.query.filter_by(role="admin").first():
        admin11  = User(username = "movieAdmin" , email = "admin24@gmail.com" ,role = "admin" ) 
        admin11.set_password('adminkey24')
        db.session.add(admin11)
        db.session.commit()


login_images = ['login-1.jpg' , 'login-2.jpg' , 'login-3.jpg' , 'login-4.jpg' , 'login-5.jpg' , 'login-6.jpg' , 'login-7.jpg' , 'login-8.jpg' , 'login-9.jpg','login-10.jpg'] 


@app.route("/") 
def landing(): 
    return render_template("index.html", image = choice(login_images)) 
@app.route("/login", methods=["GET", "POST"] ) 
def login():
    if request.method == "POST": 
        email = request.form.get("email") 
        password = request.form.get("password") 
        role = request.form.get("role") 
        user = User.query.filter_by(email=email, role=role).first() 
        if user and user.check_password(password): 
            login_user(user) 
            flash("Login successful!", "success") 
            return redirect(url_for("landing")) 
        else: 
            flash("Invalid credentials!", "danger") 
    return render_template("login.html" , image = choice(login_images)) 


@app.route("/register", methods=["GET", "POST"]) 
def register(): 
    if request.method == "POST": 
        name = request.form.get("name") 
        email = request.form.get("email") 
        password = request.form.get("password") 
        confirm_password = request.form.get("confirm_password")
         
         # Check if passwords match 
        if password != confirm_password: 
            flash("Passwords do not match!", "danger") 
            return redirect(url_for("register")) # Check if the email already exists 
        if User.query.filter_by(email=email).first(): 
            flash("Email already exists!", "danger")
            return redirect(url_for("register")) 
        new_user = User(username=name, email=email) 
        new_user.set_password(password)
        db.session.add(new_user) 
        db.session.commit() 
        flash("Registration successful! Please log in.", "success") 
        return redirect(url_for("login")) 
    return render_template("/register.html" , image = choice(login_images)) 


@app.route("/logout") 
@login_required 
def logout(): 
    logout_user() 
    flash("Logged out successfully!", "info")
    return redirect(url_for("landing")) 



user_data = {
    "name": "Gaurav",
    "photo": "/static/images/user-image.jpeg",
    "tagline": '"Life is like a movie, write your own ending" - Kermit the Frog',
    "stats": {"watched": 847, "rating": 4.8},
    "about": {
        "location": "Rajpura, Punjab",
        "joined": "February 2025",
        "email": "malik24x07@gmail.com",  # Replace with a valid email for testing
        "link": "@mauravgalik04",
    },
    "genres": [
        {"name": "Sci-Fi", "progress": 85, "count": 234},
        {"name": "Thriller", "progress": 72, "count": 198},
        {"name": "Drama", "progress": 65, "count": 179},
    ],
    "activity": [
        {
            "type": "review",
            "title": "Reviewed Oppenheimer",
            "time": "2 hours ago",
            "text": '"A masterpiece that explores the moral complexities of scientific achievement. Nolan at his finest."',
            "rating": 5,
        },
        {
            "type": "list",
            "title": "Created a new list",
            "time": "Yesterday",
            "text": '"Best Sci-Fi Movies of 2024"',
            "movies": ["Dune: Part Two", "The Creator", "+3 more"],
        },
        {
            "type": "watch",
            "title": "Watched Poor Things",
            "time": "2 days ago",
            "rating": 4,
        },
    ],
}
@app.route('/genres')
def genre():
    genres = ['Action' , 'Adventure' , 'Biography' , 'Romance' , 'Comedy' , 'Drama' , 'Thriller' , 'Sci-Fi' , 'Crime' , 'Horror' , 'Other']
    movies = Movie.query.all()
    return render_template('genre.html' , movies = movies , genres = genres )
@app.route('/watchlist/<int:sno>')
def add_to_watchlist(sno):
    movies = Movie.query.all()
    for movie in movies:
        if movie.sno == sno:
            if movie.watchlist == 'no':
                movie.watchlist = "yes"
                db.session.commit()
                flash("Movie added succesfully." , "info")
            else:
                flash("Already in watchlist" , "info" )
    return redirect(url_for('showMovies' , movie = movie))
@app.route('/removeWatchlist/<int:sno>')
def remove_from_watchlist(sno):
    movie = Movie.query.get(sno)
    if movie.watchlist == 'yes':
        movie.watchlist = 'no'
        flash("Movie removed from watchlist." , 'info')
        db.session.commit()
    return redirect(url_for('showMovies'))

@app.route("/profile") 
@login_required 
def profile(): 
    return render_template("profile.html" , user = user_data)


#Routes
api.add_resource(MoviesResource, '/movies' , methods = ['POST' , "GET"])
api.add_resource(MovieResource, '/movies/<int:sno>')


if __name__=="__main__":
    app.run(debug=True )
