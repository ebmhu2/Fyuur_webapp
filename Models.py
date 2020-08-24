from app import db
from datetime import datetime

# association_table Show
Shows = db.Table("Shows",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id")),
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id")),
    db.Column("start_time", db.DateTime, default=datetime.utcnow()))

# model Venue
class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False, unique=True)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website_link = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    artists = db.relationship("Artist", secondary=Shows,
                              backref=db.backref('Venue',cascade="all,delete"), lazy=True)
    def __repr__(self):
        return f'<Venue {self.id} {self.name}'

    # Done: implement any missing fields, as a database migration using Flask-Migrate

# model Artist
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False, unique=True)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Artist {self.id} {self.name}'

    # Done: implement any missing fields, as a database migration using Flask-Migrate

# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
