from datetime import date
import datetime
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location
from .db_locations.crud import get_location_by_name, update_location_firerisk
import math
import numpy as np

# Initialize the Fire Risk API
frc = METFireRiskAPI()


def get_fire_risk(loc: str, days_past: int = 7, weatherdata: bool = False):
    """
    Fetches weather data and fire risk predictions for a given location.
    """

    # Define the location with their latitude and longitude
    location_db = get_location_by_name(loc)
    if location_db is None:
        return {"error": "Location not found in the database."}

    coordinates = location_db["coordinates"]
    location = Location(latitude=coordinates["latitude"], longitude=coordinates["longitude"])
    obs_delta = datetime.timedelta(days=days_past)

    lastModified = location_db.get("lastModified")
    beenModified = False
    if lastModified and lastModified == date.today().isoformat():
        beenModified = True
        data = {
                "location": {"name": loc, "latitude": location.latitude, "longitude": location.longitude},
                "fireRiskPrediction": location_db["fireRiskPrediction"]
            }

    try:
        fire_risk = frc.compute_now(location, obs_delta)

        fire_risk_dict = serialize_fire_risk_prediction(fire_risk)
        update_location_firerisk(loc, fire_risk_dict)
        if not beenModified:
            data = {
                "location": {"name": loc, "latitude": location.latitude, "longitude": location.longitude},
                "fireRiskPrediction": fire_risk
            }

        if (weatherdata):
            raw_weatherdata = frc.get_weatherdata_now(location, obs_delta)
            data["weatherdata"] = clean_data(raw_weatherdata)

        return data
    except Exception as e:
        return {"Problem fetching fire risk prediction, error: " + str(e)}


def clean_data(data):
    """
    Recursively clean data by replacing NaN values with "Not Available".
    Handles nested dictionaries, lists, and custom objects.
    """

    if isinstance(data, float) and math.isnan(data):
        return "Not Available"
    elif isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif hasattr(data, "__dict__"):
        return {key: clean_data(value) for key, value in vars(data).items()}
    else:
        return data


def serialize_fire_risk_prediction(fire_risk_prediction):
    """
    Serializes a FireRiskPrediction object into a dictionary using clean_data.
    """
    # Extract the firerisks attribute
    firerisks = getattr(fire_risk_prediction, "firerisks", [])
    # Serialize each FireRisk object in the firerisks list
    serialized_firerisk_list = [clean_data(firerisk) for firerisk in firerisks]

    # Return the serialized dictionary
    return {
        "firerisks": serialized_firerisk_list
    }


def get_fire_risk_trends(loc: str):
    fire_risk_data = get_fire_risk(loc, 7, False)

    firerisks = fire_risk_data["fireRiskPrediction"]["firerisks"]

    # Extract fire risk values and timestamps
    fire_risk_values = [p["ttf"] for p in firerisks]
    timestamps = [p["timestamp"] for p in firerisks]

    def trenddetector(list_of_index, array_of_data, order=1):
        result = np.polyfit(list_of_index, list(array_of_data), order)
        slope = result[-2]
        return float(slope)

    trend = trenddetector(range(len(fire_risk_values)), fire_risk_values, order=1)

    trends = {
        "average_fire_risk": sum(fire_risk_values) / len(fire_risk_values),
        "max_fire_risk": max(fire_risk_values),
        "min_fire_risk": min(fire_risk_values),
        "rate_of_change": [
            fire_risk_values[i] - fire_risk_values[i - 1]
            for i in range(1, len(fire_risk_values))
        ],
        "trend_direction": "increasing" if trend > 0 else "decreasing",
        "timestamps": timestamps,
    }

    return trends
