from fastapi import APIRouter,Depends
from models.location import Location
from api.openweather import get_report
from utils import cache

router = APIRouter()

@router.get('/api/weather/{city}')
async def weather(loc:Location= Depends()):
    forecast = cache.get_weather(loc.city,loc.state,loc.country,loc.units)
    print('sdd',forecast)
    if forecast:
        return forecast
    report = await get_report(loc.city,loc.state,loc.country,loc.units)
    cache.set_weather(loc.city,loc.state,loc.country,loc.units,report)
    print('fetchig')
    return report
