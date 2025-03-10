import datetime

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

if __name__ == "__main__":

    frc = METFireRiskAPI()

    location = Location(latitude=60.383, longitude=5.3327)

    obs_delta = datetime.timedelta(days=1)

    wd = frc.get_weatherdata_now(location, obs_delta)
    print(wd)

    predictions = frc.compute_now(location, obs_delta)

    print(predictions)