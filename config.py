import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://mahmoud:post_Mah@localhost:5432/fyuur_db'
