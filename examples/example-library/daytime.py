from datetime import datetime, time
import requests
import pytz

ENDPOINT = 'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}'
TIME_FORMAT = '%I:%M:%S %p'

def is_it_dark_outside(latitude, longitude, timezone='Europe/London'):
    local_timezone = pytz.timezone(timezone)

    url = ENDPOINT.format(latitude=latitude, longitude=longitude)
    response = requests.get(url).json()
    now = datetime.utcnow().astimezone(local_timezone)
    sunrise = datetime.strptime(response['results']['sunrise'], TIME_FORMAT).replace(year=now.year, month=now.month, day=now.day)
    sunset = datetime.strptime(response['results']['sunset'], TIME_FORMAT).replace(year=now.year, month=now.month, day=now.day)

    return local_timezone.localize(sunrise) < now < local_timezone.localize(sunset)

if __name__ == '__main__':
    print(is_it_dark_outside('51.5', '0.1'))
