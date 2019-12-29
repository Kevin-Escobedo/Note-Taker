#Author: Kevin C. Escobedo
#Email: escobedo001@gmail.com
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from socket import gethostbyname, gaierror
from tkinter import messagebox
from tkinter import filedialog
import smtplib
import tkinter
import os
import sys

class NoteTaker:
    def __init__(self):
        '''Sets up the GUI'''
        self.root_window = tkinter.Tk()
        self.root_window.geometry("550x560")
        self.root_window.title("Note Taker")
        self.root_window.resizable(0, 0)
        self.root_window.iconbitmap(self.resource_path("quill.ico"))
        self.email_user = "" #Add own email here
        self.email_password = "" #Add own password here
        self.email_recipient = tkinter.Entry(self.root_window, width = 75)
        self.note_title = tkinter.Entry(self.root_window, width = 75)
        self.notes = tkinter.Text(self.root_window, width = 50, height = 28)

    def resource_path(self, relative_path):
        '''Get absolute path to resource, works for dev and for PyInstaller'''
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def no_invalid_characters(self, title):
        '''Checks for valid name'''
        self.invalid_characters = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        for character in self.invalid_characters:
            if character in title:
                return False
        return True

    def check_not_empty(self, title):
        '''Checks if the title is not empty'''
        return len(title) > 0

    def get_title(self):
        '''Gets the title of the notes'''
        try:
            title = self.note_title.get()
            if self.no_invalid_characters(title):# and self.check_not_empty(title):
                return title
            else:
                raise ValueError
        except ValueError:
            messagebox.showinfo("Error", message = "Invalid Title")
            
    def get_notes(self):
        '''Gets the notes taken'''
        return self.notes.get(1.0, tkinter.END)

    def get_email_recipient(self):
        try:
            recipient = self.email_recipient.get()
            if self.check_not_empty(recipient):
                return recipient
            else:
                raise ValueError
        except ValueError:
            messagebox.showinfo("Error", message = "Invalid Recipient")
    
    def save_to_file(self):
        '''Saves notes to a file'''
        title = self.get_title()
        try:
            outfile = open("{}.txt".format(title.strip()), "w", encoding = "utf-8")
            notes = self.get_notes()
            outfile.write(notes)
            outfile.flush()
            outfile.close()
            messagebox.showinfo("Success", message = "Notes saved successfully!")
        except AttributeError:
            pass

    def load_file(self):
        '''Loads previous notes'''
        title = self.get_title()
        if len(title) != 0:
            try:
                infile = open("{}.txt".format(title.strip()), "r", encoding = "utf-8")
                self.notes.insert(tkinter.END, infile.read())
                infile.close()
            except FileNotFoundError:
                messagebox.showinfo("Error", message = "Notes not found")
            except:
                pass
        else:
                file_path = filedialog.askopenfilename()
                title = file_path.split("/")[-1]
                title = title.split(".")[0]
                infile = open("{}".format(file_path), "r", encoding = "utf-8")
                self.note_title.insert(tkinter.END, title)
                self.notes.insert(tkinter.END, infile.read())
                infile.close()


    def clear_text(self):
        '''Clears the text box'''
        self.notes.delete(1.0, tkinter.END)

    def send_notes(self):
        try:
            title = self.get_title().strip()
            if title.split()[-1].strip().lower() == "notes":
                subject = "{}".format(title)
            else:
                subject = "{} Notes".format(title)

            recipient = self.get_email_recipient()

            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient
            msg['Subject'] = subject

            body = self.get_notes()
            msg.attach(MIMEText(body, "plain"))

            text = msg.as_string()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email_user, self.email_password)

            
            server.sendmail(self.email_user, recipient, text)

            server.quit()

            messagebox.showinfo("Success", message = "Notes sent successfully!")
            
        except gaierror:
            showinfo("Error", message = "No Internet Connection")

        except AttributeError:
            pass

        except TypeError:
            pass

    def on_close(self):
        '''Runs when the GUI is closed'''
        if len(self.get_title().strip()):
            self.save_to_file()
        self.root_window.destroy()

    def run(self):
        '''Runs the GUI'''
        tkinter.Label(self.root_window, text = "Name of Notes").grid(row = 0, column = 0)
        self.note_title.grid(row = 0, column = 1, sticky = tkinter.NSEW)
        
        tkinter.Label(self.root_window, text = "Email Recipient").grid(row = 1, column = 0)
        self.email_recipient.grid(row = 1, column = 1, sticky = tkinter.NSEW)

        tkinter.Label(self.root_window, text = "Notes").grid(row = 2, column = 0)
        self.notes.grid(row = 2, column = 1, columnspan = 2, sticky = tkinter.NSEW)

        save_button = tkinter.Button(self.root_window, text = "Save", command = self.save_to_file, width = 31)
        save_button.grid(row = 3, column = 1, columnspan = 2, sticky = tkinter.W)

        send_button = tkinter.Button(self.root_window, text = "Send", command = self.send_notes, width = 31)
        send_button.grid(row = 3, column = 1, columnspan = 2, sticky = tkinter.E)

        load_button = tkinter.Button(self.root_window, text = "Load", command = self.load_file, width = 31)
        load_button.grid(row = 4, column = 1, columnspan = 2, sticky = tkinter.W)

        clear_button = tkinter.Button(self.root_window, text = "Clear", command = self.clear_text, width = 31)
        clear_button.grid(row = 4, column = 1, columnspan = 2, sticky = tkinter.E)

        self.root_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root_window.mainloop()
        
if __name__ == "__main__":
    NoteTaker().run()
