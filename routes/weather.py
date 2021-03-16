from fastapi import APIRouter,Depends,Response
from models.location import Location
from api.openweather import get_report
from utils import cache
from models.error import Error 

router = APIRouter()

@router.get('/api/weather/{city}')
async def weather(loc:Location= Depends()):
    forecast = cache.get_weather(loc.city,loc.state,loc.country,loc.units)
    if forecast:
        return forecast
    try:
        report = await get_report(loc.city,loc.state,loc.country,loc.units)
    except Error as err:
        return Response(content=err.error_msg,status_code=err.status_code)
    cache.set_weather(loc.city,loc.state,loc.country,loc.units,report)
    print('fetchig')
    return report
