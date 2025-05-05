from unittest.mock import patch
from fireguard_app.Fireguard_API import get_fire_risk, get_fire_risk_trends

@patch("fireguard_app.Fireguard_API.operator_db")
@patch("fireguard_app.Fireguard_API.frc")
def test_get_fire_risk(mock_frc, mock_operator_db):
    # Mock database response
    mock_operator_db.get_location_by_name.return_value = {
        "coordinates": {"latitude": 60.0, "longitude": 5.0},
        "lastModified": None,
        "fireRiskPrediction": {"firerisks": []},
    }

    # Mock frc.compute_now response
    mock_frc.compute_now.return_value = {
        "data": {
            "firerisks": [{"ttf": 3, "timestamp": "2025-05-05"}]
        }
    }

    # Mock frc.get_weatherdata_now response
    mock_frc.get_weatherdata_now.return_value = {
        "weather": [{"temperature": 15, "timestamp": "2025-05-05"}]
    }

    # Call the function
    result = get_fire_risk("Bergen", days_past=7, weatherdata=True)

    print("Result:", result)

    # Assertions
    assert "location" in result
    assert result["location"]["name"] == "Bergen"
    assert "fireRiskPrediction" in result
    assert "weatherdata" in result
    assert result["fireRiskPrediction"]["data"]["firerisks"][0]["ttf"] == 3
    assert result["weatherdata"]["weather"][0]["temperature"] == 15


@patch("fireguard_app.Fireguard_API.get_fire_risk")
def test_get_fire_risk_trends(mock_get_fire_risk):
    # Mock fire risk data
    mock_get_fire_risk.return_value = {
        "fireRiskPrediction": {
            "firerisks": [
                {"ttf": 2, "timestamp": "2023-10-01"},
                {"ttf": 3, "timestamp": "2023-10-02"},
                {"ttf": 5, "timestamp": "2023-10-03"},
            ]
        }
    }

    # Call the function
    trends = get_fire_risk_trends("Bergen")

    # Assertions
    assert round(trends["average_fire_risk"],2) == 3.33  # Rounded value
    assert trends["max_fire_risk"] == 5
    assert trends["min_fire_risk"] == 2
    assert trends["trend_direction"] == "increasing"
    assert len(trends["timestamps"]) == 3
