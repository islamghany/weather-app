from fastapi import APIRouter,Depends
from models.location import Location
from api.openweather import get_report
router = APIRouter()

@router.get('/api/weather/{city}')
def weather(loc:Location= Depends()):
    report = get_report(loc.city,loc.state,loc.country,loc.units)
    return loc
