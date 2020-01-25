# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().magic('matplotlib inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# %%
import numpy as np
import pandas as pd


# %%
import datetime as dt
import calendar

# %% [markdown]
# # Reflect Tables into SQLAlchemy ORM

# %%
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import extract 


# %%
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# %%
# reflect an existing database into a new model
Base.prepare(engine, reflect=True)
# reflect the tables


# %%
# We can view all of the classes that automap found
Base.classes.keys()

# %%
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# %%
# Create our session (link) from Python to the DB
session = Session(engine)
# %% [markdown]
# # Exploratory Climate Analysis

# %%
# Design a query to retrieve the data for month of June accross all stations and years
# Perform a query to retrieve the date, precipitation scores, stations and temperatures
june = []
june = session.query(Measurement.date, Measurement.prcp, Measurement.tobs, Measurement.station).filter(extract('month', Measurement.date)==6).all()
print(june)
# %%
# Save the query results as a Pandas DataFrame and set the index to the date column
df_june = pd.DataFrame(june, columns=['date','precipitation','tobs','station'])
df_june.set_index(df_june['date'], inplace=True)
df_june.head()

# %%
# Sort the dataframe by date
df_june = df_june.sort_index()
df_june.head()
# %%
print(df_june.to_string(index=False))
# %%
# Use Pandas Plotting with Matplotlib to plot the data
df_june.plot()

# %%
# Use Pandas to calcualte the summary statistics for the precipitation data
df_june.describe()
#print(ds)

# %%
# Design a query to retrieve the data for month of June accross all stations and years
# Perform a query to retrieve the date, precipitation scores, stations and temperatures
december = []
december = session.query(Measurement.date, Measurement.prcp, Measurement.tobs, Measurement.station).filter(extract('month', Measurement.date)==12).all()
print(december)
# %%
# Save the query results as a Pandas DataFrame and set the index to the date column
df_dec = pd.DataFrame(december, columns=['date','precipitation','tobs','station'])
df_dec.set_index(df_dec['date'], inplace=True)
df_dec.head()

# %%
# Sort the dataframe by date
df_dec = df_dec.sort_index()
df_dec.head()
# %%
print(df_dec.to_string(index=False))
# %%
# Use Pandas Plotting with Matplotlib to plot the data
df_dec.plot()

# %%
# Use Pandas to calcualte the summary statistics for the precipitation data
df_dec.describe()

# %%
# %%
# How many stations are available in this dataset?
session.query()
session.query(func.count(Station.station)).all()
# %%
# What are the most active stations?
session.query()
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).\
group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

# %%
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
session.query()
#session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.station == 'USC00519281').all()
# %%
# Choose the station with the highest number of temperature observations.
results = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= prev_year).all()
df = pd.DataFrame(results, columns=['tobs'])
# %%
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
df.plot.hist(bins=12)
plt.tight_layout()

# %%
# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

# %% [markdown]
# # Challenge

# %%


