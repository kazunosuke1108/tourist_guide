import json
import asyncio

import winsdk.windows.devices.geolocation as wdg
import requests


async def getCoodinates():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]


def getLocation():
    try:
        return asyncio.run(getCoodinates())
    except Exception as e:
        print(e)

class getGeoInfo():
    def __init__(self):
        pass

    def get_geo_info(self,lat=None,lng=None):
        if lat is None or lng is None:
            lat, lng = getLocation()
        print(f'{lat:.3f} {lng:.3f} by Windows')
        url = f'https://geoapi.heartrails.com/api/json?method=searchByGeoLocation&x={lng}&y={lat}'
        r = requests.get(url)
        loc = json.loads(r.content.decode('utf-8'))['response']['location'][0]
        print(loc)
        print(f"{float(loc['y']):.3f} {float(loc['x']):.3f} {loc['prefecture']}{loc['city']}{loc['town']}")

        return lat,lng,loc

if __name__ == '__main__':
    cls=getGeoInfo()
    for i in range(10):
        cls.get_geo_info()