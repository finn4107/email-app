import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailApp:
    def __init__(self):
        self.logged_in = False
        self.emails = []  # Liste zur Speicherung der E-Mail-Inhalte

    def login(self):
        print("=== Anmeldung ===")
        self.email = input("Deine E-Mail-Adresse: ")
        self.app_password = input("App-Passwort: ")
        self.logged_in = True
        print("Erfolgreich angemeldet!\n")

    def show_menu(self):
        while self.logged_in:
            print("\n=== Hauptmenü ===")
            print("1. E-Mails empfangen")
            print("2. E-Mail schreiben")
            print("3. Abmelden")
            choice = input("Wähle eine Option (1/2/3): ")

            if choice == '1':
                self.receive_email()
            elif choice == '2':
                self.compose_email()
            elif choice == '3':
                self.logout()
            else:
                print("Ungültige Auswahl. Bitte versuche es erneut.")

    def receive_email(self):
        if not self.logged_in:
            print("Fehler: Bitte melde dich zuerst an.")
            return

        try:
            imap_server = 'imap.gmail.com'

            with imaplib.IMAP4_SSL(imap_server) as mail:
                mail.login(self.email, self.app_password)
                mail.select('inbox')

                status, messages = mail.search(None, 'ALL')
                mail_ids = messages[0].split()

                self.emails = []  # Liste zur Speicherung der E-Mail-Inhalte

                print("\nLetzte 5 E-Mails:")
                for mail_id in mail_ids[-5:]:  # Letzte 5 E-Mails abrufen
                    status, msg_data = mail.fetch(mail_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    email_info = {
                        'from': msg['From'],
                        'subject': msg['Subject'],
                        'body': self.get_email_body(msg)
                    }
                    self.emails.append(email_info)
                    print(f"Von: {msg['From']} - Betreff: {msg['Subject']}")

                if not self.emails:
                    print("Keine neuen E-Mails vorhanden.")

                while True:
                    email_choice = input("\nWähle eine E-Mail zum Anzeigen (1-5) oder 'q' zum Beenden: ")
                    if email_choice.lower() == 'q':
                        break
                    elif email_choice.isdigit() and 1 <= int(email_choice) <= len(self.emails):
                        self.show_email_content(int(email_choice) - 1)
                    else:
                        print("Ungültige Auswahl.")

        except Exception as e:
            print(f"Fehler beim Empfangen der E-Mails: {e}")

    def get_email_body(self, msg):
        # E-Mail-Inhalt abrufen
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""

    def show_email_content(self, index):
        email_content = self.emails[index]
        print(f"\n--- E-Mail Inhalt ---")
        print(f"Von: {email_content['from']}")
        print(f"Betreff: {email_content['subject']}")
        print(f"Nachricht:\n{email_content['body']}")

    def compose_email(self):
        if not self.logged_in:
            print("Fehler: Bitte melde dich zuerst an.")
            return

        print("\n=== E-Mail schreiben ===")
        recipient_email = input("Empfänger E-Mail-Adresse: ")
        subject = input("Betreff: ")
        body = input("Nachricht: ")

        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(self.email, self.app_password)
                server.send_message(msg)

            print("E-Mail erfolgreich gesendet!")
        except Exception as e:
            print(f"Fehler beim Senden der E-Mail: {e}")

    def logout(self):
        self.logged_in = False
        print("Erfolgreich abgemeldet!")

# Hauptprogramm
if __name__ == "__main__":
    app = EmailApp()
    app.login()

    if app.logged_in:
        app.show_menu()
