from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from imdb import Cinemagoer


ia = Cinemagoer()
app = Flask(__name__)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=False)


db.create_all()


class UpdateForm(FlaskForm):
    rating = StringField(label='Movie Rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your review', validators=[DataRequired()])

    submit = SubmitField('Submit')


class AddForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])

    submit = SubmitField("Add Movie")

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://static.kinoafisha.info/k/movie_posters/1080x1920/upload/movie_posters/3/0/3/5303/6a3dcdf603045a29b00cdd6ae228153c.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all() #Сортирует фильмы по рейтингу и возвращает словарь
    for i in range(len(all_movies)): 
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        movie = ia.get_movie(movie_id)
        selected_movie = Movie(
            title=movie["title"],
            year=movie["year"],
            description=movie["plot"][0],
            # rating=0,
            # ranking=0,
            # review="",
            img_url=movie["full-size cover url"])
        db.session.add(selected_movie)
        db.session.commit()
        return redirect(url_for("edit", id=selected_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = UpdateForm()
    movie_id = request.args.get("id")  # Получаем аргумент из ссылки <a>
    movie = Movie.query.get(movie_id)
    if edit_form.validate_on_submit():
        movie.rating = request.form["rating"]
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=edit_form)


@app.route('/add', methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        movies = ia.search_movie(request.form["title"])
        return render_template("select.html", movies=movies)
    # movie_id = request.args.get('id')
    # movie_to_delete = Movie.query.get(movie_id)
    # db.session.delete(movie_to_delete)
    # db.session.commit()
    return render_template("add.html", form=add_form)


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

