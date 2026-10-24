"""Safety-first red-flag rules. These run BEFORE any LLM and decide the triage level.
Keywords cover English, Hindi, Marathi (transliteration-free: native script + common roman).
Decision support only, not a diagnosis. Have a clinician review before real use."""

RULES = [
    # id, level, keywords, advice per language
    ("chest_pain", "red", ["chest pain", "सीने में दर्द", "छाती में दर्द", "छातीत दुखत", "chhati"],
     {"en": "Possible heart emergency. Keep patient seated, calm. Refer to nearest hospital NOW.",
      "hi": "हृदय की आपात स्थिति हो सकती है। मरीज को बैठाकर शांत रखें। तुरंत अस्पताल भेजें।",
      "mr": "हृदयाची आपत्कालीन स्थिती असू शकते. रुग्णाला बसवून शांत ठेवा. त्वरित रुग्णालयात पाठवा."}),
    ("breathing", "red", ["difficulty breathing", "breathless", "सांस लेने में", "साँस फूल", "श्वास घेण्यास", "धाप लागते"],
     {"en": "Breathing difficulty is an emergency. Sit upright, refer to hospital NOW.",
      "hi": "सांस की तकलीफ आपात स्थिति है। सीधा बैठाएं, तुरंत अस्पताल भेजें।",
      "mr": "श्वासाचा त्रास ही आपत्कालीन स्थिती आहे. सरळ बसवा, त्वरित रुग्णालयात पाठवा."}),
    ("convulsion", "red", ["convulsion", "seizure", "fits", "दौरा", "झटके", "मिर्गी", "झटके येत", "फिट"],
     {"en": "Seizure. Lay on side, nothing in mouth, refer to hospital NOW.",
      "hi": "दौरा। करवट लिटाएं, मुँह में कुछ न डालें, तुरंत अस्पताल भेजें।",
      "mr": "झटके. कुशीवर झोपवा, तोंडात काही घालू नका, त्वरित रुग्णालयात पाठवा."}),
    ("unconscious", "red", ["unconscious", "not responding", "faint", "बेहोश", "बेशुद्ध", "भोवळ"],
     {"en": "Unconscious or fainting. Check breathing, refer to hospital NOW.",
      "hi": "बेहोशी। सांस जांचें, तुरंत अस्पताल भेजें।",
      "mr": "बेशुद्धावस्था. श्वास तपासा, त्वरित रुग्णालयात पाठवा."}),
    ("stiff_neck_fever", "red", ["stiff neck", "गर्दन अकड़", "मान ताठ"],
     {"en": "Fever with stiff neck may be meningitis. Refer to hospital NOW.",
      "hi": "बुखार के साथ गर्दन अकड़ना मेनिनजाइटिस हो सकता है। तुरंत अस्पताल भेजें।",
      "mr": "ताप आणि मान ताठ होणे मेंदुज्वर असू शकतो. त्वरित रुग्णालयात पाठवा."}),
    ("preg_danger", "red", ["pregnant bleeding", "bleeding pregnancy", "गर्भवती रक्तस्राव", "गर्भवती खून", "गरोदर रक्तस्राव", "swelling pregnant", "pregnant fits"],
     {"en": "Pregnancy danger sign. Refer to hospital with delivery facility NOW.",
      "hi": "गर्भावस्था का खतरे का संकेत। तुरंत प्रसूति सुविधा वाले अस्पताल भेजें।",
      "mr": "गरोदरपणातील धोक्याचे लक्षण. त्वरित प्रसूती सुविधा असलेल्या रुग्णालयात पाठवा."}),
    ("severe_bleeding", "red", ["heavy bleeding", "vomiting blood", "blood in stool", "खून बहुत", "खून की उल्टी", "रक्ताची उलटी", "खूप रक्त"],
     {"en": "Severe bleeding. Apply pressure, refer to hospital NOW.",
      "hi": "गंभीर रक्तस्राव। दबाव डालें, तुरंत अस्पताल भेजें।",
      "mr": "गंभीर रक्तस्राव. दाब द्या, त्वरित रुग्णालयात पाठवा."}),
    ("child_danger", "red", ["child not drinking", "child lethargic", "बच्चा दूध नहीं", "बच्चा सुस्त", "बाळ दूध पित नाही", "बाळ सुस्त"],
     {"en": "Child danger sign (not feeding / lethargic). Refer to hospital NOW.",
      "hi": "बच्चे में खतरे का संकेत। तुरंत अस्पताल भेजें।",
      "mr": "बाळामध्ये धोक्याचे लक्षण. त्वरित रुग्णालयात पाठवा."}),
    # yellow: see a doctor today / PHC
    ("fever", "yellow", ["fever", "temperature", "बुखार", "ताप", "ज्वर"],
     {"en": "Fever: give paracetamol as per protocol, fluids. Visit PHC today; test for malaria/dengue if >2 days.",
      "hi": "बुखार: प्रोटोकॉल अनुसार पैरासिटामॉल, खूब पानी। आज PHC जाएं; 2 दिन से ज्यादा हो तो जांच कराएं।",
      "mr": "ताप: प्रोटोकॉलनुसार पॅरासिटामॉल, भरपूर पाणी. आज PHC ला जा; 2 दिवसांहून जास्त असल्यास चाचणी करा."}),
    ("diarrhoea", "yellow", ["diarrhea", "diarrhoea", "loose motion", "दस्त", "पतले दस्त", "जुलाब"],
     {"en": "Start ORS now. Visit PHC if more than 3 days, blood in stool, or child is weak.",
      "hi": "तुरंत ORS दें। 3 दिन से ज्यादा, खून या बच्चा कमजोर हो तो PHC जाएं।",
      "mr": "त्वरित ORS द्या. 3 दिवसांहून जास्त, रक्त किंवा बाळ अशक्त असल्यास PHC ला जा."}),
    ("cough", "yellow", ["cough", "खांसी", "खाँसी", "खोकला"],
     {"en": "Cough over 2 weeks needs TB test at PHC. Otherwise rest, warm fluids.",
      "hi": "2 सप्ताह से ज्यादा खांसी में PHC पर TB जांच कराएं। अन्यथा आराम, गर्म पानी।",
      "mr": "2 आठवड्यांहून जास्त खोकल्यास PHC मध्ये TB तपासणी करा. अन्यथा विश्रांती, कोमट पाणी."}),
    ("vomiting", "yellow", ["vomiting", "उल्टी", "उलटी"],
     {"en": "Small sips of ORS. Visit PHC if unable to keep fluids down.",
      "hi": "ORS छोटे घूँट में दें। तरल न रुके तो PHC जाएं।",
      "mr": "ORS थोडे थोडे द्या. द्रव टिकत नसल्यास PHC ला जा."}),
    ("injury", "yellow", ["injury", "fracture", "wound", "चोट", "घाव", "जखम", "फ्रैक्चर"],
     {"en": "Clean wound, immobilise limb. Visit PHC today for dressing / tetanus.",
      "hi": "घाव साफ करें, अंग को स्थिर रखें। ड्रेसिंग/टिटनेस के लिए आज PHC जाएं।",
      "mr": "जखम स्वच्छ करा, अवयव स्थिर ठेवा. ड्रेसिंग/टिटॅनससाठी आज PHC ला जा."}),
    ("headache", "green", ["headache", "सिर दर्द", "सिरदर्द", "डोकेदुखी"],
     {"en": "Rest, water. Visit PHC if it lasts over 3 days or comes with vomiting or vision change.",
      "hi": "आराम, पानी। 3 दिन से ज्यादा या उल्टी/नजर में बदलाव हो तो PHC जाएं।",
      "mr": "विश्रांती, पाणी. 3 दिवसांहून जास्त किंवा उलटी/दृष्टी बदल असल्यास PHC ला जा."}),
    ("cold", "green", ["cold", "runny nose", "सर्दी", "जुकाम", "सर्दी पडसे", "पडसे"],
     {"en": "Rest, warm fluids, steam. Monitor for fever or breathing trouble.",
      "hi": "आराम, गर्म पानी, भाप। बुखार या सांस में तकलीफ पर नजर रखें।",
      "mr": "विश्रांती, कोमट पाणी, वाफ. ताप किंवा श्वासाचा त्रास असल्यास लक्ष ठेवा."}),
]

LEVEL_ORDER = {"green": 0, "yellow": 1, "red": 2}
LEVEL_TEXT = {
    "red": {"en": "EMERGENCY: refer now", "hi": "आपात: तुरंत रेफर करें", "mr": "आपत्कालीन: त्वरित रेफर करा"},
    "yellow": {"en": "See a doctor today", "hi": "आज डॉक्टर को दिखाएं", "mr": "आज डॉक्टरांना दाखवा"},
    "green": {"en": "Home care, monitor", "hi": "घर पर देखभाल, निगरानी", "mr": "घरी काळजी, निरीक्षण"},
}

def triage(text: str, age=None, days=None, lang="en"):
    t = (text or "").lower()
    hits = []
    for rid, level, kws, advice in RULES:
        if any(k.lower() in t for k in kws):
            hits.append({"id": rid, "level": level, "advice": advice.get(lang, advice["en"])})
    level = "green"
    for h in hits:
        if LEVEL_ORDER[h["level"]] > LEVEL_ORDER[level]:
            level = h["level"]
    # escalation rules
    if level != "red":
        if age is not None and (age < 2 or age > 65) and hits:
            level = "yellow" if level == "green" else level
        if days is not None and days >= 3 and hits:
            level = "yellow" if level == "green" else level
        if len(hits) >= 3:
            level = "yellow" if level == "green" else level
    if not hits:
        level = "yellow"  # unknown symptoms: do not reassure
    return {"level": level, "label": LEVEL_TEXT[level].get(lang, LEVEL_TEXT[level]["en"]), "flags": hits}
