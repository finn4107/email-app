import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Listbox, Text

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Mail App")

        # Benutzeranmeldung
        self.create_login_interface()

        self.logged_in = False
        self.emails = [] # Liste zur Speicherung der E-Mail-Inhalte

    def create_login_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Deine E-Mail-Adresse:").grid(row=0, column=0)
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self.root, text="App-Passwort:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, width=50, show='*')
        self.password_entry.grid(row=1, column=1)

        login_button = tk.Button(self.root, text="Anmelden", command=self.login)
        login_button.grid(row=2, columnspan=2)

    def login(self):
        self.email = self.email_entry.get()
        self.app_password = self.password_entry.get()
        
        self.logged_in = True
        messagebox.showinfo("Erfolg", "Erfolgreich angemeldet!")
        
        self.show_email_interface()

    def show_email_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # E-Mails empfangen Button
        receive_button = tk.Button(self.root, text="E-Mails empfangen", command=self.receive_email)
        receive_button.grid(row=0, column=0)

        # E-Mails schreiben Button
        compose_button = tk.Button(self.root, text="E-Mail schreiben", command=self.compose_email)
        compose_button.grid(row=0, column=1)

        # Logout Button
        logout_button = tk.Button(self.root, text="Abmelden", command=self.logout)
        logout_button.grid(row=0, column=2)

        # Liste der empfangenen E-Mails
        tk.Label(self.root, text="Empfangene E-Mails:").grid(row=1, column=0, columnspan=3)
        self.email_list = Listbox(self.root, width=100, height=10)
        self.email_list.grid(row=2, column=0, columnspan=3)

        # Scrollbar
        scrollbar = Scrollbar(self.root)
        scrollbar.grid(row=2, column=3, sticky='ns')
        self.email_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.email_list.yview)

        # Doppelklick-Ereignis für die E-Mail-Listbox
        self.email_list.bind('<Double-1>', self.show_email_content)

    def receive_email(self):
        if not self.logged_in:
            messagebox.showerror("Fehler", "Bitte melde dich zuerst an.")
            return

        try:
            imap_server = 'imap.gmail.com'

            with imaplib.IMAP4_SSL(imap_server) as mail:
                mail.login(self.email, self.app_password)
                mail.select('inbox')

                status, messages = mail.search(None, 'ALL')
                mail_ids = messages[0].split()

                self.email_list.delete(0, tk.END)  # Vorherige E-Mails löschen
                self.emails = []  # Liste zur Speicherung der E-Mail-Inhalte

                for mail_id in mail_ids[-10:]:  # Letzte 5 E-Mails abrufen
                    status, msg_data = mail.fetch(mail_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    email_info = {
                        'from': msg['From'],
                        'subject': msg['Subject'],
                        'body': self.get_email_body(msg)
                    }
                    self.emails.append(email_info)
                    self.email_list.insert(tk.END, f"Von: {msg['From']} - Betreff: {msg['Subject']}")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Empfangen der E-Mails: {e}")

    def get_email_body(self, msg):
        # E-Mail abrufen
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""

    def show_email_content(self, event):
        selected_index = self.email_list.curselection()
        if selected_index:
            email_content = self.emails[selected_index[0]]
            self.open_email_window(email_content)

    def open_email_window(self, email_content):
        # Neues Fenster für den E-Mail-Inhalt
        email_window = Toplevel(self.root)
        email_window.title("E-Mail Inhalt")

        tk.Label(email_window, text=f"Von: {email_content['from']}").pack()
        tk.Label(email_window, text=f"Betreff: {email_content['subject']}").pack()
        tk.Label(email_window, text="Nachricht:").pack()

        # Textfeld für den E-Mail-Inhalt
        body_text = Text(email_window, wrap='word', height=15, width=50)
        body_text.pack()
        body_text.insert(tk.END, email_content['body'])
        body_text.config(state='disabled') 

    def compose_email(self):
        if not self.logged_in:
            messagebox.showerror("Fehler", "Bitte melde dich zuerst an.")
            return

        # Neues Fenster für das Verfassen der E-Mail
        compose_window = Toplevel(self.root)
        compose_window.title("E-Mail schreiben")

        tk.Label(compose_window, text="Empfänger E-Mail-Adresse:").grid(row=0, column=0)
        recipient_entry = tk.Entry(compose_window, width=50)
        recipient_entry.grid(row=0, column=1)

        tk.Label(compose_window, text="Betreff:").grid(row=1, column=0)
        subject_entry = tk.Entry(compose_window, width=50)
        subject_entry.grid(row=1, column=1)

        tk.Label(compose_window, text="Nachricht:").grid(row=2, column=0)
        body_text = Text(compose_window, width=50, height=10)
        body_text.grid(row=2, column=1)

        send_button = tk.Button(compose_window, text="E-Mail senden",
                                command=lambda: self.send_email(recipient_entry.get(), subject_entry.get(), body_text.get("1.0", tk.END)))
        send_button.grid(row=3, columnspan=2)

    def send_email(self, recipient_email, subject, body):
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

            messagebox.showinfo("Erfolg", "E-Mail erfolgreich gesendet!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Senden der E-Mail: {e}")

    def logout(self):
        self.logged_in = False
        messagebox.showinfo("Abmeldung", "Erfolgreich abgemeldet!")
        self.create_login_interface()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()