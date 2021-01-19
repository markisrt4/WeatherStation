from pyowm.owm import OWM
from datetime import datetime
from sense_hat import SenseHat
import time

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

sense = SenseHat()

owm = OWM('529ba6f1c4c018b7b2cf0e317c79cbbd')  # My OpenWeatherMap API Key
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=42.8725, lon=-83.0269, exclude='minutely,hourly', units='metric')

observation = one_call.current

for i,j in observation.to_dict().items():
    if i == "snow":
        print("hi")
        rain_dict = observation.snow
        for k,l in rain_dict.items():
            print(k, " => ", l)
    print(i, " => ", j)



while True:
    one_call = mgr.one_call(lat=42.8725, lon=-83.0269, exclude='minutely,hourly', units='metric')

    assert isinstance(one_call.current, object)
    observation = one_call.current

    timestamp = datetime.fromtimestamp(observation.ref_time)
    iso_dt = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    xfer_dt = '1970-01-01 00:00:00'

    outdoor_pressure = observation.pressure["press"]
    outdoor_humidity = observation.humidity
    outdoor_dewpoint = observation.dewpoint
    outdoor_temp = observation.temp["temp"]
    outdoor_temp_feel = observation.temp["feels_like"]
    outdoor_wind_ave = 0
    outdoor_wind_gust = observation.wnd["speed"]
    outdoor_wind_dir = degToCompass(observation.wnd["deg"])
    outdoor_rain_1hr = .15  # observation.rain['1h'] + observation.snow["1h"]

    indoor_humidity = round(sense.get_humidity(),2)
    indoor_temp     = round(sense.get_temperature(),2)

    print("0,",\
          xfer_dt,",",\
          iso_dt, ",",\
          ".5,",\
          indoor_humidity, ",",\
          indoor_temp, ",",\
          outdoor_humidity, ",",\
          outdoor_dewpoint, ",",\
          outdoor_temp, ",",\
          outdoor_temp_feel, ",",\
          "0, ",\
          outdoor_pressure, ",",\
          outdoor_wind_ave, ",",\
          "0,",\
          outdoor_wind_gust, ",",\
          "0,",\
          "0,",\
          outdoor_wind_dir, ",",\
          "0,",\
          "0,",\
          "0,",\
          outdoor_rain_1hr, ",",\
          "0,",\
          "0,",\
          "0,",\
          "0 ")

    time.sleep(5)

# 0 - Record no
# 1 - Transfer date
# 2 - Transfer time
# 3 - Reading date (yyyy-mm-dd)
# 4 - Reading time (hh:mm:ss)
# NOTE: Cumulus only checks the 'reading time' to identify whether there is a new reading, the computer time is used when Cumulus processes the record. See this forum topic.
#
# 5 - Interval
# 6 - Indoor Hum (Must be integer)
# 7 - Indoor Temp
# 8 - Outdoor Hum (Must be integer)
# 9 - Outdoor Temp
# 10 - dew point
# 11 - wind chill
# 12 - absolute pressure
# 13 - rel pressure
# 14 - wind average
# 15 - wind average bft
# 16 - wind gust (Used for 'latest')
# 17 - wind gust bft
# 18 - wind direction number
# 19 - wind direction text (N, ENE etc, using English)
# 20 - rain tip counter
# 21 - rain total
# 22 - rain since last reading
# 23 - rain in last hour (used as Cumulus rain rate, i.e. a rain amount for a period of one hour is the rate in units of amount per hour)
# 24 - rain last 24 hours
# 25 - rain last 7 days
# 26 - rain last 30 days
# 27 - rain last year (Used as Cumulus rain counter which can be any ever-increasing counter, but it needs to be in the same units as 23 - rain in last hour). The longer this counter continues before resetting to zero, the better for Cumulus.
# For easyweatherplus.dat only:
#
# 28 - light reading (in Lux)
# 29 - UV index
