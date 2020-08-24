# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Done: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
from Models import *
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    # Show Recent Listed Artists and Recently Listed Venues on the homepage
    recent_venues = Venue.query.order_by(desc(Venue.id)).limit(10).all()
    recent_artists = Artist.query.order_by(desc(Artist.id)).limit(10).all()
    return render_template('pages/home.html',recent_venues=recent_venues,recent_artists=recent_artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Done: replace with real venues data.
    #  num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    try:
        venues = Venue.query.distinct(Venue.city, Venue.state).all()
        if venues:
            for venue in venues:
                try:
                    No_of_upcoming_shows = len(Venue.query.join(Shows)
                                     .filter(Shows.c.start_time > datetime.utcnow(),
                                             Shows.c.venue_id == venue.id).all())
                except:
                    No_of_upcoming_shows = 0

                data.append({
                    "city": venue.city,
                    "state": venue.state,
                    "venues": [{
                        "id": venue1.id,
                        "name": venue1.name,
                        "num_upcoming_shows": No_of_upcoming_shows
                    } for venue1 in Venue.query.filter_by(city=venue.city, state=venue.state).all()]
                })
        else:
            flash("No Record saved")
    except :
        flash("something error")
    return render_template('pages/venues.html', areas=data)


# search venue
@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    search_name = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    data = []
    if search_term: # use logic to prevent search on empty search term
        # we suggest if user want to search with venue name he use one string without comma
        # if user use comma to sparate city and state for search
        if search_term.find(',') == -1:  # one string
            # case 1 user use one string to search with venue name
            for venue in search_name:
                data.append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(Venue.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow(),
                                                                             Shows.c.venue_id == venue.id).all())
                })
        else: # 2 string    City, state
            # case 2 user use two string separated by comma to search with city, state
            # use strip to remove white spaces
            search_term1 = search_term.split(',')[0].strip() # city
            search_term2 = search_term.split(',')[1].strip()  # state
            search_city_state = Venue.query.filter(Venue.city.ilike(f"%{search_term1}%"),Venue.state.ilike(f"%{search_term2}%")).all()
            for venue in search_city_state:
                data.append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(Venue.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow(),
                                                                             Shows.c.venue_id == venue.id).all())
                })

    else:
        data=[]

    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=search_term)

# show venue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # Done: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get_or_404(venue_id)
    shows = db.session.query(Shows).filter(Shows.c.venue_id == venue.id).all()
    artist_up_show = []
    artist_past_show = []
    for show in shows:
        artist = Artist.query.filter_by(id=show.artist_id).first()
        artist_show = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%A %B, %d, %Y at %H:%M %p")
        }
        if show.start_time >= datetime.utcnow():
            artist_up_show.append(artist_show)
        elif show.start_time < datetime.utcnow():
            artist_past_show.append(artist_show)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "upcoming_shows": artist_up_show,
        "upcoming_shows_count": len(artist_up_show),
        "past_shows": artist_past_show,
        "past_shows_count": len(artist_past_show),

    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # Done: insert form data as a new Venue record in the db, instead
    # Done: modify data to be the data object returned from db insertion
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
                      phone=form.phone.data, image_link=form.image_link.data,
                      facebook_link=form.facebook_link.data, genres=form.genres.data,
                      website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                      seeking_description=form.seeking_description.data)
        try:
            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            # Done: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash("An error occurred. Venue " + request.form['name'] + " could not be listed.")
        finally:
            db.session.close()
    else:
        # show form validation Error
        for field_name, field_errors in form.errors.items():
            flash(field_name + ': ' + str(field_errors))
    return render_template('pages/home.html')


# Delete Venue
@app.route('/venues/<venue_id>/', methods=['DELETE'])
def delete_venue(venue_id):
    # Done: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    error=False
    try:
        venue = Venue.query.get_or_404(venue_id)
        venue_name = venue.name
        db.session.delete(venue)
        db.session.commit()
        flash('Venue '+ venue_name + ' Deleted Successfully')
    except:
        db.session.rollback()
        print(sys.exc_info())
        error=True
        flash('Venue cannot be deleted')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})


# Edit Venue
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Done: populate form with values from venue with ID <venue_id>
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Done: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.address = form.address.data
        venue.website_link = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.image_link= form.image_link.data
        try:
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' Information was updated successfully !')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
        finally:
            db.session.close()
    else:
        # show form validation Error
        for field_name, field_errors in form.errors.items():
            flash(field_name + ': ' + str(field_errors))
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # Done: replace with real data returned from querying the database
    data =[]
    artists = Artist.query.order_by(Artist.id).all()
    if artists:
        try:
            for artist in artists:
                data.append({
                    "id": artist.id,
                    "name":artist.name
                })
        except:
            flash("something error")
    else:
        flash("No Record saved")
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    search_name = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    data = []
    if search_term: # use logic to prevent search on empty search term
        # we suggest if user want to search with artist name he use one string without comma
        # if user use comma to sparate city and state for search
        if search_term.find(',') == -1:  # one string
            # case 1 user use one string to search with artist name
            for artist in search_name:
                data.append({
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": len(Artist.query.join(Shows).filter(Shows.c.start_time > datetime.now(),
                                                                              Shows.c.artist_id == artist.id).all())
                })

        else: # 2 string    City, state
            # case 2 user use two string separated by comma to search with city, state
            # use strip to remove white spaces
            search_term1 = search_term.split(',')[0].strip() # city
            search_term2 = search_term.split(',')[1].strip()  # state
            search_city_state = Artist.query.filter(Artist.city.ilike(f"%{search_term1}%"),Artist.state.ilike(f"%{search_term2}%")).all()
            for artist in search_city_state:
                data.append({
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": len(Artist.query.join(Shows).filter(Shows.c.start_time > datetime.now(),
                                                                              Shows.c.artist_id == artist.id).all())
                })

    else:
        data=[]

    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


# Show Artist
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # Done: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get_or_404(artist_id)
    shows = db.session.query(Shows).filter(Shows.c.artist_id == artist_id).all()
    past_shows = []
    up_shows = []

    for show in shows:
        venue = Venue.query.get_or_404(show.venue_id)
        venue_show = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%A %B, %d, %Y at %H:%M %p")
        }
        # logic to select past show and upcoming show based on start_time
        if show.start_time >= datetime.utcnow():
            up_shows.append(venue_show)
        elif show.start_time < datetime.utcnow():
            past_shows.append(venue_show)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "upcoming_shows_count": len(up_shows),
        "upcoming_shows": up_shows,
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # Done: populate form with fields from artist with ID <artist_id>
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website_link
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue,
    form.seeking_description.data =  artist.seeking_description
    form.image_link.data = artist.image_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)


# edit artist
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # Done: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm()
    if form.validate_on_submit():
        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website_link = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data
        try:
            db.session.commit()
            flash('Artist ' + request.form['name'] + ' Information was updated successfully !')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        finally:
            db.session.close()
    else:
        # show form validation Error
        for field_name, field_errors in form.errors.items():
            flash(field_name + ': ' + str(field_errors))
    return redirect(url_for('show_artist', artist_id=artist_id))


# Delete Artist
@app.route('/artists/<int:artist_id>/', methods=['DELETE'])
def delete_artist(artist_id):
    error =False
    try:
        artist = Artist.query.get_or_404(artist_id)
        artist_name = artist.name
        db.session.delete(artist)
        db.session.commit()
        flash('Artist ' + artist_name + ' Deleted Successfully')
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
        flash('Artist cannot be deleted')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # Done: insert form data as a new Venue record in the db, instead
    # Done: modify data to be the data object returned from db insertion
    form = ArtistForm()
    if form.validate_on_submit():
        artist = Artist(name=form.name.data,city=form.city.data,state=form.state.data,phone=form.phone.data,
                        genres=form.genres.data,image_link=form.image_link.data,facebook_link=form.facebook_link.data,
                        website_link=form.website_link.data,seeking_venue=form.seeking_venue.data,
                        seeking_description=form.seeking_description.data)
        try:
            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            # Done: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
        finally:
            db.session.close()

    else:
        # show form validation Error
        for field_name, field_errors in form.errors.items():
            flash(field_name+': '+ str(field_errors))
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # Done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    try:
        shows = db.session.query(Shows).all()
        for show in shows:
            artist = Artist.query.get_or_404(show.artist_id)
            venue = Venue.query.get_or_404(show.venue_id)
            data.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime("%A %B, %d, %Y at %H:%M %p")
            })
    except :
        data = []
        print(sys.exc_info())
        pass
    return render_template('pages/shows.html', shows=data)

# Render show form
@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

# Create Show
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # Done: insert form data as a new Show record in the db, instead
    form = ShowForm()
    if form.validate_on_submit():
        show = Shows.insert().values(artist_id=form.artist_id.data,venue_id=form.venue_id.data ,
                                     start_time=form.start_time.data)
        try:
            db.session.execute(show)
            db.session.commit()
            # on successful db insert, flash success
            flash("Show was successfully listed!")
        except:
            flash("An error occurred. Show could not be listed.")
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        # show form validation Error
        for field_name, field_errors in form.errors.items():
            flash(field_name + ': ' + str(field_errors))
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
