from fastapi import APIRouter,Depends,Response
from models.location import Location
from api.openweather import get_report
from api import report
from typing import Optional, List

from utils import cache
from models.error import Error
from models.reports import Report, ReportSubmittal

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

@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    return await report.get_reports()


@router.post('/api/reports', name='add_report', status_code=201, response_model=Report)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location

    return await report.add_report(d, loc)
