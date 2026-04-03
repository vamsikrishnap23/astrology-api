# Vedic Astrology Backend Project Index

## Project Overview

This is a comprehensive Vedic Astrology API backend built with FastAPI. The project provides astrological calculations including birth charts, divisional charts, dashas, panchang, ashtakavarga, transits, progressions, and compatibility matching (Ashtakootam).

## Architecture

- **Framework**: FastAPI (Python web framework)
- **Core Engine**: Swiss Ephemeris (swisseph) for astronomical calculations
- **Structure**: Modular feature-based organization
- **API Endpoints**: RESTful endpoints for various astrological calculations

## Core Files

### main.py

**Purpose**: Main FastAPI application entry point with all API endpoints.

**Endpoints**:

- `/api/v1/panchang` - Calculates daily panchang (tithi, nakshatra, yoga, karana, vara, sunrise/sunset)
- `/api/v1/chart/vargas` - Returns all 16 divisional charts (D-1 to D-60)
- `/api/v1/chart/dashas` - Calculates complete 120-year Vimshottari Mahadasha timeline
- `/api/v1/chart/advanced-tables` - Planetary and house tables with lords (Star, Sign, Sub, Sub-Sub, Sub-Sub-Sub)
- `/api/v1/chart/ashtakavarga` - Complete Ashtakavarga with BAV, SAV, and reductions (Trikona, Ekadhipatya)
- `/api/v1/chart/transit` - Transit chart analysis with natal relationships
- `/api/v1/chart/progression` - Secondary progressions (1 day = 1 year)
- `/api/v1/match/ashtakootam` - 36-point Kundali Milan compatibility scoring

### models.py

**Purpose**: Pydantic data models for API request/response validation.

**Models**:

- `BirthDetails` - Birth information (date, time, location, ayanamsa, node type)
- `TransitRequest` - Natal + transit birth details
- `MatchRequest` - Boy + girl birth details for compatibility

### core_math.py

**Purpose**: Core astronomical calculation engine using Swiss Ephemeris.

**Functions**:

- `calculate_base_positions()` - Calculates planetary positions, ascendant, and 12 house cusps
- Supports Lahiri/Krishnamurti ayanamsa
- True/Mean lunar nodes
- Placidus house system

### utils.py

**Purpose**: Utility functions for astronomical data formatting and time conversion.

**Functions**:

- `format_longitude()` - Converts decimal degrees to sign/degree/minute/second format
- `get_utc_decimal_hour()` - Timezone-aware UTC conversion
- `jd_to_utc_time()` - Julian day to readable time format
- Zodiac sign mappings and constants

## Features Directory

### panchang.py

**Purpose**: Daily panchang calculations (Hindu calendar and auspicious timings).

**Calculations**:

- Tithi (lunar phase)
- Nakshatra (constellation) with padam
- Yoga (planetary combination)
- Karana (half-tithi)
- Vara (weekday)
- Sunrise/Sunset times

### divisional.py

**Purpose**: Divisional chart calculations (Vargas) for detailed analysis.

**Charts Supported**:

- D-2 (Hora), D-3 (Drekkana), D-4 (Chaturthamsa)
- D-7 (Saptamsa), D-9 (Navamsa), D-10 (Dashamsa)
- D-12 (Dwadasamsa), D-16 (Shodasamsa), D-20 (Vimsamsa)
- D-24 (Chaturvimsamsa), D-27 (Saptavimsamsa), D-30 (Trimsamsa)
- D-40 (Khavedamsa), D-45 (Akshavedamsa), D-60 (Shastiamsa)

**Features**:

- Parashari mapping rules for each varga
- Degree expansion for unequal divisions
- Retrograde status preservation

### dashas.py

**Purpose**: Vimshottari Dasha system calculations.

**Features**:

- True origin calculation based on Moon's nakshatra
- Complete 120-year timeline
- Mahadasha and Antardasha periods
- Vedic calendar math (1 year = 365.2425 days)

### advanced_tables.py

**Purpose**: Detailed planetary and house analysis tables.

**Tables**:

- Planetary Table: Planet, Sign, Position, House, Star/Sign/Sub Lords
- House Table: House, Sign, Position, Star/Sign/Sub Lords

**Features**:

- House placement calculation
- Hierarchical lord system (Star → Sub → Sub-Sub → Sub-Sub-Sub)

### lords.py

**Purpose**: Calculation of astrological lords (rulers) for positions.

**Lord Types**:

- Sign Lord (SiL) - Ruling planet of the sign
- Star Lord (StL) - Ruling planet of the nakshatra
- Sub Lord (SL) - Sub-division ruler
- Sub-Sub Lord (SSL) - Further sub-division
- Sub-Sub-Sub Lord (SSSL) - Finest sub-division

**Features**:

- Vimshottari dasha lord mapping
- Nakshatra-based sub-lord calculations

### ashtakavarga.py

**Purpose**: Ashtakavarga (eight-fold strength) calculations.

**Components**:

- Bhinna Ashtakavarga (BAV) - Individual planetary strengths
- Sarvashtakavarga (SAV) - Combined planetary strengths
- Trikona Shodhana - Triangular reduction
- Ekadhipatya Shodhana - Planetary occupation reduction

**Rules**:

- Parashari reference point mappings
- Elemental group reductions
- 7 Ekadhipatya rules

### transits.py

**Purpose**: Transit chart analysis and natal relationships.

**Features**:

- Transit planet positions
- House placement from natal ascendant
- House placement from natal Moon
- Retrograde status tracking

### progressions.py

**Purpose**: Secondary progression calculations.

**Features**:

- 1 day = 1 year progression formula
- Tropical solar year (365.24219 days)
- Progressed chart generation using core engine
- Age metadata tracking

### ashtakootam.py

**Purpose**: Kundali Milan (marriage compatibility) calculations.

**Ashtakootam Factors**:

- Varna (1 pt) - Social refinement
- Vashya (2 pts) - Attraction compatibility
- Tara/Dina (3 pts) - Health and prosperity
- Yoni (4 pts) - Physical compatibility
- Graha Maitri (5 pts) - Mental friendship
- Gana (6 pts) - Temperament matching
- Bhakoot/Rasi (7 pts) - General indications
- Nadi (8 pts) - Progeny compatibility

**Total**: 36-point system

### ashtakootam_logic.py

**Purpose**: Core logic functions for Ashtakootam calculations.

**Functions**:

- `calc_varna()` - Social duty compatibility
- `calc_tara()` - 9-star cycle evaluation
- `calc_graha_maitri()` - Planetary friendship scoring
- `calc_bhakoot()` - Sign relationship scoring
- `calc_rajju()` - Physical safety (extended system)

### ashtakootam_matrices.py

**Purpose**: Compatibility matrices for Ashtakootam factors.

**Matrices**:

- GANA_MAP - Temperament compatibility (Deva/Manushya/Rakshasa)
- VASHYA_MAP - Attraction compatibility (animal classifications)
- YONI_MAP - Physical compatibility (14 animal archetypes)

## Dependencies

- fastapi - Web framework
- swisseph - Astronomical calculations
- pydantic - Data validation
- uvicorn - ASGI server

## Usage

Run the server with: `uvicorn main:app --reload`

The API provides comprehensive Vedic astrology calculations for birth chart analysis, timing, compatibility, and predictive astrology.
