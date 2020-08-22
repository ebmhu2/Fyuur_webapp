from datetime import datetime
from flask_wtf import FlaskForm ,Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField
from wtforms.validators import DataRequired, Length, URL,ValidationError,Regexp

state_list = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]


genres_list = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Swing', 'Swing'),
            ('Other', 'Other'),
        ]


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],choices = state_list)
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[
            Regexp(regex='^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message="Phone Number must be in Format xxx-xxx-xxxx.")]
    )
    image_link = StringField('image_link')
    # Done implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired()],choices=genres_list)
    facebook_link = StringField('facebook_link', validators=[URL(), Regexp(
            regex='^(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?$',
            message='Facebook link not valid')]
    )
    website_link = StringField('website_link', validators=[URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description', validators=[Length(max=500)])


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],choices=state_list)
    # Done implement validation logic for state
    phone = StringField(
        'phone',validators=[Regexp(regex='^[0-9]{3}-[0-9]{3}-[0-9]{4}$',message="Phone Number must be in Format xxx-xxx-xxxx.")]
    )
    image_link = StringField('image_link')
    # Done implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired()],choices=genres_list)
    facebook_link = StringField(
        'facebook_link', validators=[URL(),Regexp(regex='^(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?$',message='Facebook link not valid')]
    )
    website_link = StringField('website_link', validators=[URL()])
    seeking_venue = BooleanField('seeking_venue',default=False)
    seeking_description = StringField('seeking_description', validators=[Length(max=500)])
# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
