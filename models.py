from pydantic import BaseModel, Field
from typing import Literal

class BirthDetails(BaseModel):
    year: int = Field(..., description="Birth Year")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    day: int = Field(..., ge=1, le=31, description="Day (1-31)")
    hour: int = Field(..., ge=0, le=23, description="Birth Hour (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Birth Minute (0-59)")
    
    # Restricts input to exactly these two strings. Defaults to IST.
    tz: Literal["IST", "UTC"] = Field("IST", description="Timezone of the given birth time")
    
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude")
    lon: float = Field(..., ge=-180.0, le=180.0, description="Longitude")