# Vedic Astrology API Documentation

## Base Models

### BirthDetails

```json
{
  "year": 1990,
  "month": 6,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Fields**:

- `year`: Integer (birth year)
- `month`: Integer 1-12
- `day`: Integer 1-31
- `hour`: Integer 0-23
- `minute`: Integer 0-59
- `tz`: "IST" or "UTC"
- `lat`: Float (-90.0 to 90.0)
- `lon`: Float (-180.0 to 180.0)
- `ayanamsa`: "lahiri" or "kp"
- `node_type`: "true" or "mean"

---

## 1. Panchang Endpoint

### POST /api/v1/panchang

**Purpose**: Calculates daily panchang (Hindu calendar elements)

**Request Payload**:

```json
{
  "year": 2024,
  "month": 3,
  "day": 15,
  "hour": 6,
  "minute": 0,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "Paksham": "Shukla",
    "Vara": "Friday",
    "Tithi": "Panchami",
    "Nakshatram": {
      "name": "Rohini",
      "padam": 2,
      "full_format": "Rohini-2"
    },
    "Yogam": "Siddhi",
    "Karanam": "Bava",
    "Sunrise": "06:23 UTC",
    "Sunset": "18:45 UTC"
  }
}
```

**Response Fields**:

- `Paksham`: "Shukla" or "Krishna" (waxing/waning moon)
- `Vara`: Day of week
- `Tithi`: Lunar phase (1-15 for each paksham)
- `Nakshatram`: Constellation with padam (1-4)
- `Yogam`: Planetary combination (27 types)
- `Karanam`: Half-tithi (11 types)
- `Sunrise/Sunset`: UTC times

---

## 2. Vargas (Divisional Charts) Endpoint

### POST /api/v1/chart/vargas

**Purpose**: Returns all 16 divisional charts

**Request Payload**:

```json
{
  "year": 1990,
  "month": 6,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "D1_Rasi": {
      "Julian_Day": 2447892.123,
      "Sun": {
        "longitude_360": 72.34,
        "sign_index": 2,
        "sign_name": "Gemini",
        "degree": 12,
        "minute": 20,
        "second": 24.0,
        "is_retrograde": false
      },
      "Moon": {
        /* same structure */
      },
      "Mars": {
        /* same structure */
      },
      "Mercury": {
        /* same structure */
      },
      "Jupiter": {
        /* same structure */
      },
      "Venus": {
        /* same structure */
      },
      "Saturn": {
        /* same structure */
      },
      "Rahu": {
        /* same structure */
      },
      "Ketu": {
        /* same structure */
      },
      "Ascendant": {
        /* same structure */
      },
      "Houses": {
        "House_1": {
          /* longitude structure */
        },
        "House_2": {
          /* longitude structure */
        }
        // ... up to House_12
      }
    },
    "D2": {
      /* same structure as D1 */
    },
    "D3": {
      /* same structure as D1 */
    }
    // ... up to D60
  }
}
```

**Response Structure**:

- `D1_Rasi`: Birth chart (Rasi)
- `D2` to `D60`: All 15 divisional charts
- Each chart contains planets and houses with longitude data

---

## 3. Dashas Endpoint

### POST /api/v1/chart/dashas

**Purpose**: Complete 120-year Vimshottari Mahadasha timeline

**Request Payload**:

```json
{
  "year": 1990,
  "month": 6,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": [
    {
      "lord": "Venus",
      "start_date": "1990-06-15",
      "end_date": "2010-06-15",
      "antardashas": [
        {
          "lord": "Venus",
          "start_date": "1990-06-15",
          "end_date": "1991-08-23"
        },
        {
          "lord": "Sun",
          "start_date": "1991-08-23",
          "end_date": "1992-08-23"
        }
        // ... 8 antardashas per mahadasha
      ]
    }
    // ... 9 mahadashas total
  ]
}
```

**Response Structure**:

- Array of 9 Mahadashas (120 years total)
- Each Mahadasha has lord, dates, and 9 Antardashas
- Dates in YYYY-MM-DD format

---

## 4. Advanced Tables Endpoint

### POST /api/v1/chart/advanced-tables

**Purpose**: Planetary and house tables with hierarchical lords

**Request Payload**:

```json
{
  "year": 1990,
  "month": 6,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "Planetary_Table": [
      {
        "Planet": "Sun",
        "Sign": "Gem",
        "Position": "12:20:24",
        "House": 7,
        "Star": "Ardra-4",
        "Sign Lord": "Mercury",
        "Star Lord": "Rahu",
        "Sub Lord": "Venus",
        "SS Lord": "Saturn",
        "SSS Lord": "Jupiter"
      }
      // ... 9 planets (Sun to Ketu)
    ],
    "House_Table": [
      {
        "House": 1,
        "Sign": "Can",
        "Position": "15:30:45",
        "Star": "Pushya-2",
        "Sign Lord": "Moon",
        "Star Lord": "Saturn",
        "Sub Lord": "Mercury",
        "SS Lord": "Venus",
        "SSS Lord": "Mars"
      }
      // ... 12 houses
    ]
  }
}
```

**Response Structure**:

- `Planetary_Table`: Array of 9 planets with positions and lords
- `House_Table`: Array of 12 houses with positions and lords
- Lords: Sign Lord (SiL), Star Lord (StL), Sub Lord (SL), Sub-Sub Lord (SSL), Sub-Sub-Sub Lord (SSSL)

---

## 5. Ashtakavarga Endpoint

### POST /api/v1/chart/ashtakavarga

**Purpose**: Complete Ashtakavarga analysis with reductions

**Request Payload**:

```json
{
  "year": 1990,
  "month": 6,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "tz": "IST",
  "lat": 28.6139,
  "lon": 77.209,
  "ayanamsa": "lahiri",
  "node_type": "true"
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "BAV": {
      "Sun": [3, 5, 4, 2, 6, 3, 4, 5, 2, 4, 3, 6],
      "Moon": [4, 3, 5, 6, 2, 4, 5, 3, 6, 2, 4, 3],
      "Mars": [2, 4, 6, 3, 5, 2, 4, 3, 5, 6, 2, 4],
      "Mercury": [5, 3, 4, 6, 2, 5, 3, 4, 6, 2, 5, 3],
      "Jupiter": [4, 6, 2, 5, 3, 4, 6, 2, 5, 3, 4, 6],
      "Venus": [3, 5, 2, 4, 6, 3, 5, 2, 4, 6, 3, 5],
      "Saturn": [6, 2, 4, 3, 5, 6, 2, 4, 3, 5, 6, 2]
    },
    "SAV": [26, 28, 27, 29, 24, 27, 26, 25, 29, 24, 28, 26],
    "Trikona": {
      "Sun": [2, 4, 3, 1, 5, 2, 3, 4, 1, 3, 2, 5]
      // ... same for other planets
    },
    "Trikona_SAV": [23, 25, 24, 26, 21, 24, 23, 22, 26, 21, 25, 23],
    "Ekadhipatya": {
      "Sun": [1, 3, 2, 0, 4, 1, 2, 3, 0, 2, 1, 4]
      // ... same for other planets
    },
    "Ekadhipatya_SAV": [20, 22, 21, 23, 18, 21, 20, 19, 23, 18, 22, 20],
    "Total_Bindus": 26
  }
}
```

**Response Structure**:

- `BAV`: Individual planetary bindu arrays (12 signs each)
- `SAV`: Sarvashtakavarga (sum of all BAVs)
- `Trikona`: After triangular reduction
- `Trikona_SAV`: Sum after trikona reduction
- `Ekadhipatya`: After planetary occupation reduction
- `Ekadhipatya_SAV`: Final reduced values
- `Total_Bindus`: Sum of SAV for the chart

---

## 6. Transit Chart Endpoint

### POST /api/v1/chart/transit

**Purpose**: Transit chart with natal relationships

**Request Payload**:

```json
{
  "birth": {
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  },
  "transit": {
    "year": 2024,
    "month": 3,
    "day": 15,
    "hour": 12,
    "minute": 0,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  }
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "Natal_Chart": {
      // Full natal chart data (same as D1_Rasi)
    },
    "Transit_Chart": {
      // Full transit chart data (same as D1_Rasi)
    },
    "Transit_Relations": {
      "Sun": {
        "transit_sign_index": 2,
        "transit_sign_name": "Gemini",
        "degree_format": "12° 20'",
        "is_retrograde": false,
        "house_from_ascendant": 7,
        "house_from_moon": 3
      },
      "Moon": {
        // ... same structure for all planets
      }
      // ... all 9 planets
    }
  }
}
```

**Response Structure**:

- `Natal_Chart`: Complete birth chart
- `Transit_Chart`: Complete transit chart
- `Transit_Relations`: Each planet's transit position and house relationships

---

## 7. Progression Endpoint

### POST /api/v1/chart/progression

**Purpose**: Secondary progressions (1 day = 1 year)

**Request Payload**:

```json
{
  "birth": {
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  },
  "transit": {
    "year": 2024,
    "month": 3,
    "day": 15,
    "hour": 12,
    "minute": 0,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  }
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "Natal_Chart": {
      // Full natal chart data
    },
    "Progressed_Chart": {
      // Full progressed chart data with Metadata
      "Metadata": {
        "Progressed_Age": 33.75,
        "Progressed_Date_UTC": "2024-03-15 12:00"
      }
    },
    "Progression_Relations": {
      // Same structure as Transit_Relations
    }
  }
}
```

**Response Structure**:

- `Natal_Chart`: Original birth chart
- `Progressed_Chart`: Mathematically progressed positions
- `Progression_Relations`: Progressed planets' house relationships to natal

---

## 8. Ashtakootam (Compatibility) Endpoint

### POST /api/v1/match/ashtakootam

**Purpose**: 36-point Kundali Milan compatibility analysis

**Request Payload**:

```json
{
  "boy": {
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  },
  "girl": {
    "year": 1992,
    "month": 8,
    "day": 20,
    "hour": 16,
    "minute": 45,
    "tz": "IST",
    "lat": 28.6139,
    "lon": 77.209,
    "ayanamsa": "lahiri",
    "node_type": "true"
  }
}
```

**Response Payload**:

```json
{
  "status": "success",
  "data": {
    "Match_Table": [
      {
        "Attribute": "Varna",
        "Desc": "Natural Refinement / Work",
        "Male": "Kshatriya",
        "Female": "Vaishya",
        "Outof": 1,
        "Received": 0.0
      },
      {
        "Attribute": "Vashya",
        "Desc": "Innate Giving / Attraction towards each other",
        "Male": "Manav",
        "Female": "Jalchara",
        "Outof": 2,
        "Received": 1.0
      },
      {
        "Attribute": "Tara",
        "Desc": "Comfort - Prosperity - Health",
        "Male": "Rohini",
        "Female": "Swati",
        "Outof": 3,
        "Received": 1.5
      },
      {
        "Attribute": "Yoni",
        "Desc": "Intimate Physical",
        "Male": "Gau",
        "Female": "Mahish",
        "Outof": 4,
        "Received": 2.0
      },
      {
        "Attribute": "Maitri",
        "Desc": "Friendship",
        "Male": "Venus",
        "Female": "Mercury",
        "Outof": 5,
        "Received": 4.0
      },
      {
        "Attribute": "Gan",
        "Desc": "Temperament",
        "Male": "Deva",
        "Female": "Manushya",
        "Outof": 6,
        "Received": 5.0
      },
      {
        "Attribute": "Bhakut",
        "Desc": "Constructive Ability / Society and Couple",
        "Male": "Gemini",
        "Female": "Libra",
        "Outof": 7,
        "Received": 7.0
      },
      {
        "Attribute": "Nadi",
        "Desc": "Progeny / Excess",
        "Male": "Madhya",
        "Female": "Antya",
        "Outof": 8,
        "Received": 8.0
      }
    ],
    "Total_Score": 28.5,
    "Max_Possible": 36.0,
    "Percentage": "79.17%"
  }
}
```

**Response Structure**:

- `Match_Table`: Array of 8 compatibility factors
- Each factor shows Male/Female values, max points, and received points
- `Total_Score`: Sum of all received points
- `Max_Possible`: 36.0
- `Percentage`: Compatibility percentage

---

## Error Response Format

All endpoints return errors in this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Common HTTP Status Codes

- `200`: Success
- `422`: Validation error (invalid input data)
- `500`: Internal server error

## Notes for Frontend Development

1. All coordinates use decimal degrees (lat/lon)
2. Times are in 24-hour format
3. All responses include `"status": "success"` on success
4. Longitude data includes both 360° and sign-based formats
5. Arrays are 0-indexed for signs (0=Aries, 11=Pisces)
6. House numbers are 1-12 (not 0-11)
