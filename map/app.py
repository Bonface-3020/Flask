from flask import Flask, render_template,request,jsonify
from geopy.geocoders import Nominatim

app=Flask(__name__)
geolocator = Nominatim(user_agent="locate_me_app")

@app.route('/')
def home():
    return render_template('index.html')
@app.route("/geocode",methods=['POST'])
def geocode():
    location=request.json.get("location")
    if not location:
        return jsonify({"error":"Location is required"}),400
    
    location=geolocator.geocode(location)
    if location:
        return jsonify({
            "latitude":location.latitude,
            "longitude":location.longitude,
            "display_name": location.address
        })
    else:
        return jsonify({"error":"Location not found"}),404
    
if __name__=="__main__":
    app.run(debug=True)