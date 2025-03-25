import datetime

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    frc = METFireRiskAPI()

    location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    # location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund

    # days into the past to retrieve observed weather data
    obs_delta = datetime.timedelta(days=2)

    wd = frc.get_weatherdata_now(location, obs_delta)
    print(wd)

    predictions = frc.compute_now(location, obs_delta)

    print(predictions)


# Initialize the Fire Risk API
frc = METFireRiskAPI()

location = Location(latitude=60.383, longitude=5.3327)  # Bergen

def get_fire_risk(loc: str, days_past: int = 1):
    """
    Fetches weather data and fire risk predictions for a given location.
    """

    # Define known locations
    locations = {
        "Bergen": Location(latitude=60.383, longitude=5.3327),
        "Haugesund": Location(latitude=59.4225, longitude=5.2480),
        "Oslo": Location(latitude=59.9139, longitude=10.7522)
    }

    # Check if the location exists
    if loc not in locations:
        return {"error": "Unknown location"}

    location = locations[loc]
    obs_delta = datetime.timedelta(days=days_past)

    try:
        weather_data = frc.get_weatherdata_now(location, obs_delta)
        fire_risk = frc.compute_now(location, obs_delta)

        return {
            "location": {"name": loc, "latitude": location.latitude, "longitude": location.longitude},
            "weather_data": weather_data,
            "fire_risk": fire_risk
        }
    except Exception as e:
        return {"error": str(e)}
