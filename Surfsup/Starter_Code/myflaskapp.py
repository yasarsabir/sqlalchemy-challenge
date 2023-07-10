######################################################
# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
#EXTRA BIT TO HELP ME WORK OUT THE COLUMN NAMES CAN EXECUTE IN JUPYTER NOTEBOOK
Base.classes.keys()

# Save reference to the table
weather = Base.classes.weather


# Create our session (link) from Python to the DB
#if creating a session link the same as "Create a database session object" if so the code is as follows
session = Session(engine)

#################################################
# Flask Setup
#################################################
#name the flask 
#ie app = Flask(__name__)
app = Flask(_climatewizard_)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"

    )
#Convert the query results from your precipitation analysis 
#(i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

/api/v1.0/precipitation
def precipitation(): 
    " this page gives you the precipitation in formation for the last 12 months ........"
    prcp_dict = {"date": "value" }
    prcp_dict = (dt.date(2017,8,23)) - dt.timedelta(days=365)
##i added return the dictrionary
    return(prcp_dict)
#Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)

if __climatewizard__ == "__main__":
    app.run(debug=True)

/api/v1.0/stations
def stations(): 
    " this page gives you a list of all the stations in the stations database, assuming the hawaii_stations database is now called stations"
     results = session.query(station.station).all()
results = (dt.date(2017,8,23)) - dt.timedelta(days=365)
return jsonify(results)


#Return a JSON list of stations from the dataset.
/api/v1.0/tobs

#Query the dates and temperature observations of the most-active station for the previous year of data.

#Return a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

#Hints
#Join the station and measurement tables for some of the queries.

#Use the Flask jsonify function to convert your API data to a valid JSON response object.


#i've added define main behaviour
if _name_ == "__main__":
   app.run(debug=True)