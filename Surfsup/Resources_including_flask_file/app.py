######################################################
# Import the dependencies.

import numpy as np

import sqlalchemy
import datetime as dt
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
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
#if creating a session link the same as "Create a database session object" if so the code is as follows
session = Session(engine)

#################################################
# Flask Setup
#################################################
#name the flask 
#ie app = Flask(__name__)
app = Flask(__name__)
#should i just name it name

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
       #??? f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

#Convert the query results from your precipitation analysis 
#(i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.



@app.route("/api/v1.0/precipitation")
def precipitation(): 
    " this page gives you the precipitation for the last 12 months ........"
    
    #Part A - last year of data
    year_prior_to_most_recent_data_point = (dt.date(2017,8,23)) - dt.timedelta(days=365)
    #Part B - filter the precipitation results, don't really need to order them or make them into a dataframe
    prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_prior_to_most_recent_data_point).\
        order_by(measurement.date).all()
    #print(prcp_results)   
    result = { date: prcp for date, prcp in prcp_results}    #this is callled a dictionary comprehension
 #   result = np.ravel(prcp_results)
    return jsonify(result) 
    
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations(): 
    " this page gives you a list of all the unique stations in the measurement database, assuming the hawaii_stations database is now called stations"
    results = session.query(measurement.station).distinct().all()
    results = list(np.ravel(results))   
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs(): 

#Query the dates and temperature observations of the most-active station for the previous year of data.

#part A - most active station
    year_prior_to_most_recent_data_point = (dt.date(2017,8,23)) - dt.timedelta(days=365)

    most_frequent_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

#part B - dates and temp for most frequent station for past year. 
    date_temp_most_frequent_station = session.query(measurement.date, measurement.tobs).filter(measurement.station =='USC00519281')\
                    .filter(measurement.date >= year_prior_to_most_recent_data_point).all()


#Return a JSON list of temperature observations for the previous year.
    last_year_temps = session.query(measurement.tobs).filter(measurement.date >= year_prior_to_most_recent_data_point).all()
    results = list(np.ravel(last_year_temps))   
    return jsonify(results)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
#This page will return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a 
#specified start or start-end range.
    
    # Select statement
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date,
#inclusive.

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Hints
#Join the station and measurement tables for some of the queries.
# BUT HOW CAN WE JOIN THE TABLES WHEN SQLITE ONLY HAS THE MEASUREMENT TABLE.

#Use the Flask jsonify function to convert your API data to a valid JSON response object.


#i've added define main behaviour
if __name__ == "__main__":
   app.run(debug=True)




