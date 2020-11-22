# ----------------------------------------------------------------------------------
# This API is based on the solution to 10.3 Activity 10-Ins_Flask_with_ORM 
# Published by J. Luong 9/11/2020
# ----------------------------------------------------------------------------------

# Import dependencies
from IPython.display import Image, display, Markdown
import numpy as np
import datetime as dt
from datetime import timedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from dateutil.relativedelta import relativedelta
from sqlalchemy import cast, Date

# Import Flask
from flask import Flask, jsonify

# Create engine and connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

# Set a start and end date for later use
start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
end = start + dt.timedelta(days=365)

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

# Start session to database
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# ----------------------------------------------------------------------------------
       #Landing page
# ----------------------------------------------------------------------------------
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the SQLalchemy API for Hawaiian Climate Data!🌏<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation 🌧 <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs 🌞 <br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        f"/api/v2.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
            )

# ----------------------------------------------------------------------------------
       #Preciptiation page 
# ----------------------------------------------------------------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query observations
    results = session.query(measurement.date, measurement.prcp)\
              .order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    precip_complete = list(np.ravel(results))
    precip_complete = {precip_complete[i]: precip_complete[i + 1] for i in range(0, len(precip_complete), 2)} 

    return jsonify(precip_complete)

# ----------------------------------------------------------------------------------
       #Station list page
# ----------------------------------------------------------------------------------
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query stations
    results = session.query(station.station)\
              .order_by(station.station).all()

    session.close()
    
    # Flatten arry into list
    stations_complete = list(np.ravel(results))
    
    return jsonify(stations_complete)

# ----------------------------------------------------------------------------------
       #Temperature observations
# ----------------------------------------------------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session 
    session = Session(engine)

    # Query temp obs
    results = session.query(measurement.date, measurement.tobs)\
              .filter(measurement.date >= '2017-05-05')\
              .order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_complete = list(np.ravel(results))
    tobs_complete = {tobs_complete[i]: tobs_complete[i + 1] for i in range(0, len(tobs_complete), 2)} 

    return jsonify(tobs_complete)

# ----------------------------------------------------------------------------------
       # Temp data after start date
# ----------------------------------------------------------------------------------
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    session = Session(engine)
    
    # Reusing the min-avg-max from the provided function
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    
    results = session.query(*sel)\
                .filter(measurement.date >= start_date).all()
    
    session.close()
    
    # Declare list for results 
    tobs_start = []
    
    # Loop through appending results to list
    for minimum, average, maximum in results:
       
        #Dict to store data
        tobs_start_dict = {}
        tobs_start_dict["min"] = minimum
        tobs_start_dict["avg"] = round(average,1)
        tobs_start_dict["max"] = maximum
        
        # Append to list
        tobs_start.append(tobs_start_dict)
        
        return jsonify(tobs_start)
    

# ----------------------------------------------------------------------------------
       #Temp data between start and end 
# ----------------------------------------------------------------------------------

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    
    # Start session
    session = Session(engine)
    
    # Setup query string
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)]
    
    # Run query
    results = session.query(*sel)\
              .filter(Measurement.date>= start_date)\
              .filter(Measurement.date <= end_date).all()

    session.close()
    
    # Declare list
    tobs_se = []
    
    #Loop through and append data
    for minimum, average, maximum in results:
        tobs_se_dict = {}
        tobs_se_dict["min"] = minimum
        tobs_se_dict["avg"] = round(average,2)
        tobs_se_dict["max"] = maximum
        tobs_se.append(tobs_se_dict)

        return jsonify(tobs_se) 

   
if __name__ == '__main__':
        app.run(debug=True)


    


