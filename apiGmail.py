from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import re
import os
import base64
import email.utils
import time 

# Scopes requis pour lire les emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_client():
    """Authentifie le client via OAuth2 et génère un token."""
    creds = None
    if os.path.exists('token_client1.json'):
        creds = Credentials.from_authorized_user_file('token_client1.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_client1.json', 'w') as token_file:
            token_file.write(creds.to_json())
    return creds



def parse_email_date(email_date):
    try:
        # Expression régulière pour extraire la partie date et fuseau horaire
        date_pattern = r"(\d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2}) ([+-]\d{4}|GMT|UTC|CET|[A-Z]{3,4})?"
        match = re.search(date_pattern, email_date)
        
        if match:
            date_str, tz_str = match.groups()
            # Essayer de parser la date sans le fuseau horaire
            dt = datetime.strptime(date_str, "%d %b %Y %H:%M:%S")
            
            # Si un fuseau horaire est présent, le gérer
            if tz_str:
                if tz_str in ["GMT", "UTC"]:
                    dt = dt.replace(tzinfo=timezone.utc)
                elif tz_str in pytz.all_timezones:
                    tz = pytz.timezone(tz_str)
                    dt = tz.localize(dt)
                else:
                    # Convertir le décalage horaire (+0100 ou -0600) en fuseau horaire
                    offset_hours = int(tz_str[:3])
                    offset_minutes = int(tz_str[0] + tz_str[3:])  # Garde le signe
                    offset = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
                    dt = dt.replace(tzinfo=offset)
            else:
                # Si pas de fuseau horaire, on considère UTC par défaut
                dt = dt.replace(tzinfo=timezone.utc)
            
            return dt
        
        print(f"Format de date non pris en charge: {email_date}")
        return None

    except Exception as e:
        print(f"Erreur lors du parsing de la date : {e}")
        return None



def get_recent_emails(creds):
    """Récupère les emails reçus dans les 10 dernières minutes et extrait les codes de confirmation."""
    try:
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        if not messages:
            print("Aucun message reçu probleme .")
            return None

        # Parcourir les emails
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sans sujet')
            #print(f"Sujet : {subject}")

            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Date non disponible')
            #print(f"Date : {date}")

            email_date_str = message['internalDate']
            now = datetime.now()
            time_minus_10 = now - timedelta(minutes=1)
            timestamp = int(time_minus_10.timestamp())
            if int(email_date_str)/1000 >= timestamp:
                # Extraire le corps de l'email
                for part in message['payload'].get('parts', []):
                    if part['mimeType'] == 'text/plain':
                        body = part['body']['data']
                        body_decoded = base64.urlsafe_b64decode(body).decode('utf-8')
                        print("Corps du message :", body_decoded)

                        # Rechercher un code de confirmation à 6 chiffres
                        match = re.search(r'\b\d{6}\b', body_decoded)
                        if match:
                            code = match.group(0)
                            print(f"Code de confirmation trouvé : {code}")
                            return code

        print("Aucun code de confirmation trouvé.")
        return None

    except Exception as e:
        print(f"Erreur : {e}")
        return None

def wait_for_email(creds, retry_interval=10, max_attempts=30):
    """
    Appelle get_recent_emails tant que le retour est None.
    
    Args:
        creds: Les credentials d'authentification.
        retry_interval: Intervalle de temps (en secondes) entre chaque tentative.
        max_attempts: Nombre maximum de tentatives avant d'abandonner.
        
    Returns:
        str: Le code de confirmation si trouvé, None si max_attempts est atteint.
    """
    attempt = 0
    while attempt < max_attempts:
        confirmation_code = get_recent_emails(creds)
        if confirmation_code is not None:
            return confirmation_code
        print(f"Tentative {attempt + 1}/{max_attempts} : Aucun email trouvé, nouvelle tentative dans {retry_interval} secondes...")
        time.sleep(retry_interval)
        attempt += 1
    
    print("Nombre maximum de tentatives atteint. Aucun email reçu.")
    return None


if __name__ == '__main__':
    creds = authenticate_client()
    wait_for_email(creds)
    confirmation_code = get_recent_emails(creds)
    if confirmation_code:
        print("Code de confirmation reçu :", confirmation_code)