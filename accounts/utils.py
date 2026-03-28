# accounts/utils.py

# Simple example logic; you can replace this with an AI/ML model later
# accounts/utils.py

SYMPTOM_DIAGNOSIS_MAP = {
    "fever": "Possible infection or flu",
    "cough": "Possible cold, flu, or respiratory infection",
    "headache": "Possible migraine, tension headache, or dehydration",
    "fatigue": "Could be anemia, thyroid issue, or general tiredness",
    "shortness of breath": "Possible asthma, respiratory infection, or heart issue",
    "chest pain": "Possible heart problem, acid reflux, or muscle strain",
    "sore throat": "Possible viral infection or strep throat",
    "nausea": "Could be food poisoning, gastritis, or early pregnancy",
    "vomiting": "Possible gastroenteritis or food poisoning",
    "diarrhea": "Could be infection, food poisoning, or IBS",
    "dizziness": "Possible low blood pressure, dehydration, or vertigo",
    "rash": "Possible allergic reaction, infection, or skin condition",
    "joint pain": "Possible arthritis, injury, or infection",
    "muscle pain": "Could be overuse, injury, or viral infection",
    "loss of appetite": "Could be infection, depression, or chronic illness",
    "weight loss": "Could be thyroid issue, diabetes, or chronic illness",
    "blurred vision": "Possible eye strain, diabetes, or neurological issue",
    "runny nose": "Common cold, allergies, or sinus infection",
    "sneezing": "Allergies or cold",
    "chills": "Possible infection or flu",
    "body ache": "Viral infection or flu",
    "insomnia": "Stress, anxiety, or sleep disorder",
    "anxiety": "Mental health concern or stress",
    "depression": "Mental health concern",
}

def simple_symptom_checker(symptoms_input):
    """
    Take comma-separated symptoms and suggest a diagnosis.
    Returns a string with possible diagnosis.
    """
    symptoms = [s.strip().lower() for s in symptoms_input.split(",") if s.strip()]
    diagnoses = set()

    for symptom in symptoms:
        if symptom in SYMPTOM_DIAGNOSIS_MAP:
            diagnoses.add(SYMPTOM_DIAGNOSIS_MAP[symptom])
    
    if not diagnoses:
        return "No clear diagnosis. Please consult a doctor."
    
    return ", ".join(diagnoses)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import uuid

def create_google_meet_event():
    creds = Credentials.from_authorized_user_file('token.json')

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Medical Consultation',
        'start': {
            'dateTime': datetime.utcnow().isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.utcnow() + timedelta(minutes=30)).isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return event['conferenceData']['entryPoints'][0]['uri']