
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash,check_password_hash
from sqlalchemy.sql.schema import Constraint, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """Site user."""

    __tablename__ = "users" 

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, 
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False)
    movie = db.relationship("Movie", 
                            backref="user", 
                            cascade="all,delete")
 
      
    #registration
    @classmethod
    def register(cls, username, password, email):
        """Register user with hashed password and return user"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")
        
        user= cls(username=username, 
                   password=hashed_pwd, 
                   email=email,
                   )
        
        
        return user
    
    
    
    #authenticate
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct
        Return user if valid or return false."""
        
        u= cls.query.filter_by(
            username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, password):
            #return user instance
            return u
        else:
            return False
        
class Movie(db.Model):
    """movies."""

    __tablename__ = "movie"

    id = db.Column(db.Integer, 
                   primary_key=True)
    title = db.Column(db.String(300),
                      nullable=False)
    
    actors = db.Column(db.String(300))
    
    plot = db.Column(db.String(300),
                     )
    
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        unique=False,
        nullable=False,
    )  
 
    
    def to_dict(self):
        """Serialize a dict of movie info."""
        return{
            "id":self.id,
            "title": self.title,
            "actors":self.actors,
            "plot":self.plot
        }
	   

    def __repr__(self):
        return f"<Movie {self.id} title {self.title} actors{self.actors} plot{self.plot}>"

class Recommendation(db.Model):
    """User's Favorite movies"""

    __tablename__ = "likes"
    id =db.Column(db.Integer,
                         primary_key=True,                   
                    )
    title_id = db.Column(db.String(300),                   
                    )
    actors = db.Column(db.String(300),                    
                    )
    plot = db.Column(db.String(300),                    
                    )
    username = db.Column(
        db.String(20),
        nullable=False,
    )  
def __repr__(self):
        return f"<Recommendation {self.id} title {self.title} actors{self.actors} plot{self.plot} username{self.username}>"





def connect_db(app):
    """connect to database"""
    db.app=app
    db.init_app(app)
    



