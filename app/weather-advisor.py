from flask import Flask,request,jsonify
import requests,os

app=Flask(__name__)

API_KEY=os.getenv("WEATHER_API_KEY")
BASE_URL="https://api.weatherapi.com/v1/current.json"

def get_recommendation(aqi):
    if aqi <=50 :
        return "Excellent air.Go outside"
    elif aqi <=100 :
        return "Moderately good air"
    elif aqi <=150:
        return "Not good air.Be cautious"
    elif aqi <=200:
        return "Poor air quality"
    else:
        return "Dont go outside"
    
@app.route("/weather")
def get_weather() :
    city=request.args.get("city")
    if not city:
        return jsonify({"error" : "Enter valid city name"}),400
    
    try:
        params={"key": API_KEY,"q" :city,"aqi" :"yes"}
        resp=requests.get(BASE_URL,params=params)
        data=resp.json()
        
        if "error" in data:
            return jsonify({"error":data["error"]["message"]}),400
        aqi=data["current"]["air_quality"]["pm2_5"]
        return jsonify({
            "city":data["location"]["name"],
        "country":data["location"]["country"],
        "temprature":f'{data["current"]["temp_c"]} C',
        "condition":data["current"]["condition"]["text"],
        "humidity":f'{data["current"]["humidity"]} %',
        "aqi":aqi,    
        "advice":get_recommendation(aqi)   
        })
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
if __name__ =="__main__":
    app.run(host="0.0.0.0",port=5000)
        
    

