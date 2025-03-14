import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Temperature

router = APIRouter()

async def fetch_temperature(city_name: str):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=YOUR_API_KEY"
        async with session.get(url) as response:
            data = await response.json()
            return data["main"]["temp"]

@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(SessionLocal)):
    cities = db.query(City).all()
    for city in cities:
        temp = await fetch_temperature(city.name)
        temperature = Temperature(city_id=city.id, temperature=temp)
        db.add(temperature)
    db.commit()
    return {"message": "Temperatures updated"}