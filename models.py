from pydantic import BaseModel, Field
from typing import Literal, Optional

class BirthDetails(BaseModel):
    year: int = Field(...)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    tz: Literal["IST", "UTC"] = Field("IST")
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    
    # Advanced Calculation Toggles
    ayanamsa: Literal["lahiri", "kp"] = Field("lahiri", description="Ayanamsa system")
    node_type: Literal["true", "mean"] = Field("true", description="Rahu/Ketu calculation")
    
    # NEW: Optional language parameter (Defaults to English)
    lang: Optional[str] = Field("en", description="Language code (e.g., 'en', 'te')")

class TransitRequest(BaseModel):
    birth: BirthDetails
    transit: BirthDetails
    lang: Optional[str] = Field("en", description="Response language")

class MatchRequest(BaseModel):
    boy: BirthDetails
    girl: BirthDetails
    lang: Optional[str] = Field("en", description="Response language")