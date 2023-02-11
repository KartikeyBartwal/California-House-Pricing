from flask import Flask,request,render_template
import pandas
import sklearn
import numpy
from flask_cors import cross_origin
import pickle

app=Flask(__name__)
model=pickle.load(open("california_housing_model.pkl","rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/prediction",methods=["GET","POST"])
@cross_origin()
def predict():
    if request.method == "POST":
      #Latitude
      latitude_=request.form["latitudeid"]
      latitude=float(latitude_)
      def scale_down_latitude(latitude):
        latitude=( latitude -  35.633531)/2.136343
        return latitude


      #Longitude
      longitude_=request.form["longitude id"]
      longitude=float(longitude_)  
      def scale_down_longitude(longitude):
        longitude=( longitude + 119.571075 )/2.003685
        return longitude   


      #housing Median Age
      housing_median_age_=request.form["housing_median_age id"]
      housing_median_age=float(housing_median_age_)


      #Total Rooms
      total_rooms_=request.form["total_rooms id"]
      total_rooms=int(total_rooms_)
      def scale_down_total_rooms(total_rooms):
        total_rooms=( total_rooms - 2636.451996)/2185.252346
        return total_rooms


      #Population
      population_=request.form["population id"]
      population=int(population_)
      def scale_down_population(population):
        population=( population - 1424.963985 )/1133.284195
        return population


      #median income
      median_income_=request.form["median_income_id"]
      median_income=float(median_income_)


      #ocean_proximity <1H OCEAN removed to deal with dummy variable trap
      ocean_proximity_=request.form["ocean_proximity"]
      if ocean_proximity_=="NEAR_BAY":
          NEAR_BAY=1
          NEAR_OCEAN=0
          ISLAND=0
          INLAND=0
      elif ocean_proximity_=="NEAR_OCEAN":
          NEAR_BAY=0
          NEAR_OCEAN=1
          ISLAND=0
          INLAND=0
      elif ocean_proximity_=="ISLAND":
          NEAR_BAY=0
          NEAR_OCEAN=0
          ISLAND=1
          INLAND=0
      elif ocean_proximity_=="INLAND":
          NEAR_BAY=0
          NEAR_OCEAN=0
          ISLAND=0
          INLAND=1 
      elif ocean_proximity_=="1H OCEAN":
          NEAR_BAY=0
          NEAR_OCEAN=0
          ISLAND=0
          INLAND=0                

      

      prediction_scaled=model.predict([[housing_median_age, median_income, scale_down_longitude(longitude), scale_down_latitude(latitude),
       scale_down_total_rooms(total_rooms), scale_down_population(population), INLAND, ISLAND, NEAR_BAY,
       NEAR_OCEAN]])   
      
      prediction=(prediction_scaled * 115428.048)+206863.25  
      prediction=float(prediction)
      prediction=round(prediction,2)
      return render_template("home.html",prediction_text="The price value of the house will be ${}".format(prediction))


if __name__ =="__main__":
    app.run(debug=True)
