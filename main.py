from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from linkedin_scraper_v2 import LinkedInScraper
from dotenv import load_dotenv
import os

# Load environment variables dari file .env
load_dotenv()

app = FastAPI()

# Ambil li_at cookie dari file .env
LI_AT_COOKIE = os.getenv("LINKEDIN_LI_AT", "")

@app.get("/profile")
async def get_profile(vanity_name: str = Query(..., description="Vanity name LinkedIn")):
    """
    Scrape profil LinkedIn menggunakan Selenium + li_at cookie + XPath
    
    Query parameter:
    - vanity_name: Vanity name LinkedIn (contoh: naufal-arga-a5b22b2aa)
    """
    
    if not LI_AT_COOKIE:
        return JSONResponse(
            content={
                "data": {},
                "message": "LINKEDIN_LI_AT tidak diset di file .env"
            },
            status_code=500
        )
    
    try:
        # Inisialisasi scraper dengan browser baru setiap request
        scraper = LinkedInScraper(li_at_cookie=LI_AT_COOKIE)
        
        # Scrape profil
        profile_data = scraper.scrape_profile(vanity_name)
        
        if not profile_data or not profile_data.get("data"):
            return JSONResponse(
                content={
                    "data": {},
                    "message": "Profil tidak ditemukan"
                },
                status_code=404
            )
        
        return JSONResponse(content=profile_data)

    except Exception as e:
        return JSONResponse(
            content={
                "data": {},
                "message": str(e)
            },
            status_code=500
        )
