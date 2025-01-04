

#ancienne methode (plus de temps pour entrer de nouveaux clients), a utiliser dans le pire des cas

import pytz
from datetime import datetime, timedelta, timezone
import imaplib
import email
from email.header import decode_header
import re
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime



username = " "
password = " "


"""Parse différents formats de dates d'email et retourne un objet datetime avec fuseau horaire."""

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
def get_confirmation_code(username, password):
    try:
        # Connexion au serveur IMAP de Gmail
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(username, password)

        # Sélectionner la boîte de réception
        imap.select("inbox")

        # Limiter la recherche aux emails des 10 dernières minutes
        ten_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=10)
        status, messages = imap.search(None, "ALL")
        
        if status != "OK" or not messages[0]:
            print("Aucun email trouvé.")
            return None

        # Parcourir les emails du plus récent au plus ancien
        for mail_id in reversed(messages[0].split()):
            status, msg_data = imap.fetch(mail_id, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            email_date = parse_email_date(msg["Date"])

            if email_date and email_date >= ten_minutes_ago:
                # Décoder le sujet
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                print("Sujet:", subject)

                # Extraire le corps de l'email
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            print("Corps du message:", body)
                            match = re.search(r'\b\d{6}\b', body)
                            if match:
                                code = match.group(0)
                                #imap.logout()
                                #return code
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                    print("Corps du message:", body)
                    match = re.search(r'\b\d{6}\b', body)
                    if match:
                        code = match.group(0)
                        #imap.logout()
                        #return code
            else :
                return 1111
        imap.logout()
        print("Aucun code de confirmation trouvé.")
        return None

    except Exception as e:
        print(f"Erreur : {e}")
        return None


confirmation_code = get_confirmation_code(username, password)
if confirmation_code:
    print("Code de confirmation reçu :", confirmation_code)