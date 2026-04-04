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

TE_PLANET = {
    "Sun": "సూర్యుడు", "Moon": "చంద్రుడు", "Mars": "కుజుడు", 
    "Mercury": "బుధుడు", "Jupiter": "గురుడు", "Venus": "శుక్రుడు", 
    "Saturn": "శని", "Rahu": "రాహువు", "Ketu": "కేతువు", "Ascendant": "లగ్నం"
}

# --- ASHTAKOOTAM DICTIONARIES ---
TE_VARNA = {"Brahmin": "బ్రాహ్మణ", "Kshatriya": "క్షత్రియ", "Vaishya": "వైశ్య", "Shoodra": "శూద్ర"}
TE_VASHYA = {"Chatuspad": "చతుష్పద", "Maanav": "మానవ", "Jalchara": "జలచర", "Vanchara": "వనచర", "Keeta": "కీటక"}
TE_GANA = {"Deva": "దేవ", "Manushya": "మనుష్య", "Rakshasa": "రాక్షస"}
TE_NADI = {"Adi": "ఆది", "Madhya": "మధ్య", "Antya": "అంత్య"}
TE_YONI = {
    "Ashwa": "అశ్వ (గుర్రం)", "Gaj": "గజ (ఏనుగు)", "Mesh": "మేష (గొర్రె)", 
    "Sarp": "సర్ప (పాము)", "Shwan": "శ్వాన (కుక్క)", "Marjar": "మార్జాల (పిల్లి)", 
    "Mooshak": "మూషిక (ఎలుక)", "Gau": "గోవు (ఆవు)", "Mahish": "మహిష (గేదె)", 
    "Vyaghra": "వ్యాఘ్ర (పులి)", "Mrig": "మృగ (జింక)", "Vaanar": "వానర (కోతి)", 
    "Simha": "సింహ (సింహం)", "Nakul": "నకుల (ముంగిస)"
}

TE_KOOTA_ATTR = {
    "Varna": "వర్ణ", "Vashya": "వశ్య", "Tara": "తార", "Yoni": "యోని",
    "Maitri": "గ్రహ మైత్రి", "Gan": "గణ", "Bhakut": "భకూట్ (రాశి)", "Nadi": "నాడి"
}

TE_KOOTA_DESC = {
    "Natural Refinement / Work": "సహజ ప్రవర్తన / పనితీరు",
    "Innate Giving / Attraction towards each other": "సహజ ఆకర్షణ / అన్యోన్యత",
    "Comfort - Prosperity - Health": "ఆరోగ్యం - శ్రేయస్సు - సౌకర్యం",
    "Intimate Physical": "శారీరక అనుకూలత",
    "Friendship": "మానసిక స్నేహం",
    "Temperament": "మానసిక స్వభావం",
    "Constructive Ability / Society and Couple": "కుటుంబ మరియు సామాజిక అనుబంధం",
    "Progeny / Excess": "సంతానం / జన్యు అనుకూలత"
}

TE_PLANET_SHORT = {
    "Sun": "సూ", "Moon": "చం", "Mars": "కు", 
    "Mercury": "బు", "Jupiter": "గు", "Venus": "శు", 
    "Saturn": "శ", "Rahu": "రా", "Ketu": "కే", "Ascendant": "ల"
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
        if category == "planet": return TE_PLANET.get(term, term)
        if category == "planet_short": return TE_PLANET_SHORT.get(term, term)
        if category == "varna": return TE_VARNA.get(term, term)
        if category == "vashya": return TE_VASHYA.get(term, term)
        if category == "gana": return TE_GANA.get(term, term)
        if category == "nadi": return TE_NADI.get(term, term)
        if category == "yoni": return TE_YONI.get(term, term)
        if category == "koota_attr": return TE_KOOTA_ATTR.get(term, term)
        if category == "koota_desc": return TE_KOOTA_DESC.get(term, term)
    return term