# features/translator.py

# --- TELUGU DICTIONARIES ---

TE_VARA = {
    "Sunday": "ఆదివారం", "Monday": "సోమవారం", "Tuesday": "మంగళవారం",
    "Wednesday": "బుధవారం", "Thursday": "గురువారం", "Friday": "శుక్రవారం", "Saturday": "శనివారం"
}

TE_PAKSHA = {
    "Shukla": "శుక్ల పక్షం",
    "Krishna": "కృష్ణ పక్షం"
}

TE_TITHI = {
    "Pratipada": "పాడ్యమి", "Dwitiya": "విదియ", "Tritiya": "తదియ",
    "Chaturthi": "చవితి", "Panchami": "పంచమి", "Shashthi": "షష్ఠి",
    "Saptami": "సప్తమి", "Ashtami": "అష్టమి", "Navami": "నవమి",
    "Dashami": "దశమి", "Ekadashi": "ఏకాదశి", "Dwadashi": "ద్వాదశి",
    "Trayodashi": "త్రయోదశి", "Chaturdashi": "చతుర్దశి", 
    "Purnima": "పౌర్ణమి", "Amavasya": "అమావాస్య"
}

TE_YOGA = {
    "Vishkambha": "విష్కంభ", "Priti": "ప్రీతి", "Ayushman": "ఆయుష్మాన్", "Saubhagya": "సౌభాగ్య", 
    "Shobhana": "శోభన", "Atiganda": "అతిగండ", "Sukarma": "సుకర్మ", "Dhriti": "ధృతి", 
    "Shula": "శూల", "Ganda": "గండ", "Vriddhi": "వృద్ధి", "Dhruva": "ధ్రువ", 
    "Vyaghata": "వ్యాఘాత", "Harshana": "హర్షణ", "Vajra": "వజ్ర", "Siddhi": "సిద్ధి", 
    "Vyatipata": "వ్యతీపాత", "Variyan": "వరీయాన్", "Parigha": "పరిఘ", "Shiva": "శివ", 
    "Siddha": "సిద్ధ", "Sadhya": "సాధ్య", "Shubha": "శుభ", "Shukla": "శుక్ల", 
    "Brahma": "బ్రహ్మ", "Indra": "ఇంద్ర", "Vaidhriti": "వైధృతి"
}

TE_KARANA = {
    "Bava": "బవ", "Balava": "బాలవ", "Kaulava": "కౌలవ", "Taitila": "తైతిల", 
    "Gara": "గర", "Vanija": "వణిజ", "Vishti": "విష్టి", "Shakuni": "శకుని", 
    "Chatushpada": "చతుష్పాద", "Naga": "నాగ", "Kintughna": "కింతుఘ్న"
}

TE_NAKSHATRA = {
    "Ashwini": "అశ్విని", "Bharani": "భరణి", "Krittika": "కృత్తిక", "Rohini": "రోహిణి", 
    "Mrigashira": "మృగశిర", "Ardra": "ఆరుద్ర", "Punarvasu": "పునర్వసు", "Pushya": "పుష్యమి", 
    "Ashlesha": "ఆశ్లేష", "Magha": "మఖ", "Purva Phalguni": "పూర్వ ఫల్గుణి", 
    "Uttara Phalguni": "ఉత్తర ఫల్గుణి", "Hasta": "హస్త", "Chitra": "చిత్త", 
    "Swati": "స్వాతి", "Vishakha": "విశాఖ", "Anuradha": "అనూరాధ", "Jyeshtha": "జ్యేష్ఠ", 
    "Mula": "మూల", "Purva Ashadha": "పూర్వాషాఢ", "Uttara Ashadha": "ఉత్తరాషాఢ", 
    "Shravana": "శ్రవణం", "Dhanishta": "ధనిష్ఠ", "Shatabhisha": "శతభిషం", 
    "Purva Bhadrapada": "పూర్వాభాద్ర", "Uttara Bhadrapada": "ఉత్తరాభాద్ర", "Revati": "రేవతి"
}

TE_ZODIAC = {
    "Aries": "మేషం", "Taurus": "వృషభం", "Gemini": "మిథునం", "Cancer": "కర్కాటకం",
    "Leo": "సింహం", "Virgo": "కన్య", "Libra": "తుల", "Scorpio": "వృశ్చికం",
    "Sagittarius": "ధనుస్సు", "Capricorn": "మకరం", "Aquarius": "కుంభం", "Pisces": "మీనం"
}

def translate(term: str, category: str, lang: str) -> str:
    """
    Translates an astrological term. Returns the English term if translation fails or lang is 'en'.
    """
    if lang == "en":
        return term
        
    if lang == "te":
        if category == "vara": return TE_VARA.get(term, term)
        if category == "paksha": return TE_PAKSHA.get(term, term)
        if category == "tithi": return TE_TITHI.get(term, term)
        if category == "yoga": return TE_YOGA.get(term, term)
        if category == "karana": return TE_KARANA.get(term, term)
        if category == "nakshatra": return TE_NAKSHATRA.get(term, term)
        if category == "zodiac": return TE_ZODIAC.get(term, term)
    return term