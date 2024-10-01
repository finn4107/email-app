# E-Mail App

Mit dieser E-Mail App kann man einfach und schnell E-Mails empfangen und versenden.

## Funktionen
- **Login**: Anmelden mit deiner Gmail-Adresse und einem App-Passwort.
- **E-Mails empfangen**: Zeigt die letzten 10 E-Mails aus deinem Posteingang.
- **E-Mail-Inhalt anzeigen**: Öffne eine ausgewählte E-Mail zum Lesen.
- **E-Mail schreiben**: Verfasse und sende eine neue E-Mail.
- **Logout**: Abmelden und zurück zum Anmeldebildschirm.

## Voraussetzungen
- **Python 3.x**
- Standardbibliotheken: `smtplib`, `imaplib`, `email` (werden mit Python geliefert).

## Verwendung
1. **App-Passwort für Gmail erstellen**:
   - Gehe zu [Google Konto > Sicherheit](https://myaccount.google.com/security).
   - Aktiviere die **2-Schritt-Verifizierung**.
   - Gehe zu **App-Passwörter** und erstelle ein neues Passwort für "E-Mail" und "Computer".
   - Verwende dieses Passwort anstelle deines regulären Gmail-Passworts im Programm.

2. **Programm starten**:
   ```bash
   python email_console_app.py
