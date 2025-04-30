import requests



def Coordinates(location):
    key = "AIzaSyAKf94Hsy2SIdbPlJojSNTuW_xKuZJmBSw"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={key}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return latitude, longitude
    else:
        print("Error:", data["status"])



print(Coordinates("komedia bath"))