from app.parser import extract_station_data

def test_extract_station_data():
    sample = (
        "Nešković Dubička cesta bb., Prijedor Prijedor RS "
        "LPG 1.30 Benzin 95 2.35 Dizel 2.40 Dizel+ 2.50 "
        "PON - NED 00:00-24:00"
    )

    result = extract_station_data(sample)

    assert "Nešković" in result["name"]
    assert result["fuels"]["LPG"] == 1.30
    assert result["fuels"]["Benzin 95"] == 2.35
    assert result["fuels"]["Dizel"] == 2.40
    assert result["fuels"]["Dizel+"] == 2.50