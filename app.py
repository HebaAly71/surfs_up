# %%
# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# %%
# Setup the DB
engine = create_engine("sqlite:///hawaii.sqlite")

# %%
Base = automap_base()
# %%
# Reflect tables
Base.prepare(engine, reflect=True)
# %%
# We’ll create a variable for each of the classes to reference them later
measurement = Base.classes.measurement
station = Base.classes.station

# %%
# Create link from python to our DB
session = Session(engine)

# %%
# Flask app
app = Flask(__name__)

# %%
# Welcome route
@app.route("/")
def welcome():
	return( '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


# %%
# Percipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
	filter(measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# %%
# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# %%
# Monthly Temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# %%
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats():
    sel = [func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)