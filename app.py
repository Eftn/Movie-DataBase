
from flask import Flask, request, render_template,session, redirect,json,jsonify,flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm,MovieForm,DeleteForm
from models import User, connect_db, db, Movie, Recommendation
from werkzeug.exceptions import Unauthorized
import requests
import pdb
from sqlalchemy import create_engine
engine = create_engine('postgresql:///movies')
connection = engine.raw_connection()
cursor = connection.cursor()






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
connect_db(app)
db.create_all()


# the toolbar is only enabled in debug mode:
toolbar = DebugToolbarExtension(app)


def request_movie(movie):
    data_URL = f'http://www.omdbapi.com/?apikey=93254880&t={movie}'
    response=requests.get(data_URL) 
    data=response.json()
    title= data['Title']
    actors= data['Actors']
    plot= data['Plot']
    movie_details={'Title':title, 'Actors':actors, 'Plot':plot}
    return movie_details


def find_fav(id):
    """ Find Movie"""
    cursor.execute(f"select * from movie where id ={id}")
    result= cursor.fetchall()
    for row in result:
        movie={ "ID": row[0],"Title": row[1],"Actors": row[2], "Plot": row[3], "Username": row[4]}
    
    return movie

def user_fav(username):
    """Map favorite movie"""
    cursor.execute(f"select * from Likes where username='{username}'")
    result= cursor.fetchall()
    for row in result:
        movie={ "ID": row[0],"Title": row[1],"Actors": row[2], "Plot": row[3], "Username": row[4]}    
    return movie
    

@app.route("/")
def homepage():
    """Show Homepage"""
    return redirect('/register')

################USER ROUTES#######################
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  
        
            user=User.register(
            username= form.username.data,
            password= form.password.data ,  
            email= form.email.data)
            db.session.add(user)
    
            db.session.commit()
            session['username']= user.username
            
            
            return redirect(f"/users/{user.username}")
    else:
        return render_template("/users/register.html", form=form)
    


@app.route('/login', methods=["GET","POST"])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form= LoginForm()
    
    if form.validate_on_submit():
        user=User.authenticate(
            username= form.username.data,
            password= form.password.data ,  
            )
        
        if user:
            session['username']= user.username
        
        return redirect(f"/users/{user.username}/movies/new")
    else:

        return render_template("/users/login.html", form=form)
    

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")



@app.route("/users/<username>")
def show_user(username):
    """logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = DeleteForm()

    return render_template("users/show.html",user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user // redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")



############### MOVIE ROUTES #################
@app.route('/recommended')
def recommend():
    """return all recommended movies"""
    movies=  Recommendation.query.all()
    return render_template('recommended.html',movies=movies)

@app.route("/recommended/<int:movie_id>")
def recommended_deets(movie_id):
    """Show detail on a specific  recommended movie"""
    movie = Recommendation.query.get_or_404(movie_id)
    return render_template('recommend.html',movie=movie)


@app.route('/movies')
def show():
    """return all movies"""
    movies=  Movie.query.all()
    user= User.query.all()
    return render_template('movies.html',user=user,movies=movies)

@app.route("/movies/<int:movie_id>")
def movie_deets(movie_id):
    """Show detail on a specific movie"""
    movie = Movie.query.get_or_404(movie_id)
    user= User.query.all()
    return render_template('movie.html',user=user,movie=movie)



@app.route("/movies/<username>", methods=["GET", "POST"])
def movie_show_main(username):
  ### search form for view all route
    
    form= MovieForm()
    
    if form.validate_on_submit():
        title = request.form['title']
        actors= request.form['actors']
        plot =request.form['plot']
    
        mdetails=request_movie(title)    
       
        
        #update the form data
        title= mdetails['Title']
        actors=mdetails['Actors']
        plot=mdetails['Plot']
      


        
        #Movie Model Blueprint
        movie = Movie( 
        title=(title),
        actors=(actors),
        plot= (plot),
        username=username)
        
        db.session.add(movie)
       
        db.session.commit()
        

        return redirect(f"/users/{movie.username}")
       
    else:     
        
        return render_template("movies/new.html", form=form)



@app.route("/users/<username>/movies/new", methods=["GET", "POST"])
def movie_show(username):
    
    """Show  Movie Search Form and process it."""
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    form= MovieForm()
    
    if form.validate_on_submit():
        title = request.form['title']
        actors= request.form['actors']
        plot =request.form['plot']
        mdetails=request_movie(title)    
        
        #update the form data
        title= mdetails['Title']
        actors=mdetails['Actors']
        plot=mdetails['Plot']


        
        #Movie Model Blueprint
        movie = Movie( 
        title=(title),
        actors=(actors),
        plot= (plot),
        username=(username))
        
        db.session.add(movie)
       
        db.session.commit()

        return redirect(f"/users/{movie.username}")
       
    else:      
        return render_template("movies/new.html", form=form)



@app.route('/users/<username>/<int:movie_id>/like', methods=['POST','GET'])
def add_like(username,movie_id):
    """Handle Likes"""
    find_fav(movie_id)   
    favorites= find_fav(movie_id)
    
        #update the form data
    id = favorites['ID']
    title_id= favorites['Title']
    actors=favorites['Actors']
    plot=favorites['Plot']
    username=favorites['Username']
    
    #Movie Model Blueprint
    movie = Recommendation( 
    id= (id),
    title_id=(title_id),
    actors=(actors),
    plot= (plot),
    username=(username))
    
    db.session.add(movie) 
   
    db.session.commit()

    return redirect(f"/users/{username}")


@app.route('/users/<username>')
def go_back(username):
   
    return redirect(f"/users/{username}")


@app.route("/movies/<username>/<int:movie_id>/update", methods=["GET", "POST"])
def update_movie(username,movie_id):
    """Show update-movie title  and process it."""

    movie = Movie.query.get(movie_id)
    
    if "username" not in session or movie.username != session['username']:
        raise Unauthorized()
    form= MovieForm()
    
    
    if form.validate_on_submit():
        movie.title = form.title.data
       
        db.session.commit()

        return redirect(f"/users/{movie.username}")


    return render_template("/movies/edit.html", form=form,username=username, movie=movie)




@app.route("/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(movie_id):
    """Delete Movie."""

    movie = Movie.query.get(movie_id)
    if "username" not in session or movie.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(movie)
        db.session.commit()

    return redirect(f"/users/{movie.username}")

    
        
