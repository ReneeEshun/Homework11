# 1. import Flask and loading up sqlalchemy from Climate Analysis
from flask import Flask, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import date
#Connect to the database
engine=create_engine("sqlite:///hawaii.sqlite")

#Reading the tables from the database
Base=automap_base()
Base.prepare(engine, reflect=True)

#creating a session
from sqlalchemy.orm import sessionmaker
Session=sessionmaker(bind=engine)
session=Session()

#Reading the tables
Station=Base.classes.station
Measurement=Base.classes.measurement

# 2. Create an app, being sure to pass __name__
app=Flask(__name__)

dates_temps=[]

# 3. Define what to do when a user hits the index route
#@app.route("/api/v1.0/percipitation")
#def percipitation (): #   return jsonify(?)

@app.route("/api/v1.0/stations")
def get_stations():
    #list all the stations
    stations=session.query(Station.station).all()
    return jsonify(stations)
    
@app.route("/api/v1.0/percipitation")
def percipitation():
    #Get the date and tempearature for the last year
    today=date.today()
    lastyr=date(today.year-1,today.month,today.day)
    prcp_results=session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > lastyr).\
    order_by(Measurement.date).all()
    #For loop to turn data into dictionary
    percipitation_output={}
    for measurement in prcp_results:
        #date
        d=measurement[0]
        #percipation results
        p=measurement[1]
        #creating new keys for each date
        percipitation_output[str(d)]=p
    return jsonify(percipitation_output)

@app.route("/api/v1.0/tobs")
def tobs():
    #Get the date and tempearature for the last year
    today=date.today()
    lastyr=date(today.year-1,today.month,today.day)
    tob_results=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > lastyr).\
    order_by(Measurement.date).all()
    tobs_output={}
    for measurement in tob_results:
        #date
        d=measurement[0]
        #tob results
        t=measurement[1]
        #creating new keys for each date
        tobs_output[str(d)]=t
    return jsonify(tobs_output)
#Creating a route with start and end for temperature data
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start,end=None):
    temp=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= start)
    if end!=None:
        temp=temp.filter(Measurement.date<=end)
    temp_df=pd.DataFrame(temp.all())
    return jsonify([float(temp_df.tobs.min()),float(temp_df.tobs.mean()),float(temp_df.tobs.max())])



if __name__ == "__main__":
    app.run(debug=True)
 