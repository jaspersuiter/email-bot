import smtplib
import csv
import re
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import os
from dotenv import load_dotenv
import FreeSimpleGUI as sg

load_dotenv()
email_pattern = r"^\s*([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})\s*$"

coaches_data = {}
athlete_data = []

user_email = os.getenv("email_address")
user_password = os.getenv("email_password")

def set_null_for_non_breaking_space(value):
  """Checks if the value is a non-breaking space and returns None if it is,
     otherwise returns the original value."""
  if value == 'Â\xa0':
    return ''
  else:
    return value
  
def pronoun_selector1(coach_contact):
    if len(coaches_data[coach_contact]) > 1:
        return "their"
    else:
        if coaches_data[coach_contact][0]['gender'] == 'Men':
            return "his"
        elif coaches_data[coach_contact][0]['gender'] == 'Women':
            return "her"  
    return "their"    

def pronoun_selector2(coach_contact):
    if len(coaches_data[coach_contact]) > 1:
        return "they want"
    else:
        if coaches_data[coach_contact][0]['gender'] == 'Men':
            return "he wants"
        elif coaches_data[coach_contact][0]['gender'] == 'Women':
            return "she wants" 
    return "they want"     

def create_email_content_coach(coach_contact):
    content = "Good afternoon Coach " + coaches_data[coach_contact][0]['coach_name'] + ",\n\n" + "I am Ballard Suiter the jumps and sprints coach at Frostburg State University. I would like to get in contact with"
    for athlete in coaches_data[coach_contact]:
        if len(coaches_data[coach_contact]) == 1:
            content += " " + coaches_data[coach_contact][0]['name']
        else:
            for index, athlete in enumerate(coaches_data[coach_contact]):
                if index == len(coaches_data[coach_contact]) - 1:
                    content += " and " + athlete['name']
                else:
                    content += " " + athlete['name'] + ","
    content += " to see what " + pronoun_selector1(coach_contact) + " plans are for next year and if "
    content += pronoun_selector2(coach_contact) + " to do track at the next level. I look forward to hearing back from you.\n\nThanks,\n"
    content += "Ballard Suiter, MBA\nAssistant Coach Track & Field\nJumps/Multis\nFrostburg State University\nC: 317-748-8043\nUSTFCCCA Level 1 Jumps Specialist"
    
    return content        

def create_email_content_athlete(athlete):
    content = "Hello " + athlete['name'].split()[0].capitalize().rstrip() + ",\n\n"
    content += '''
    I am coach Suiter the jumps and sprints coach at Frostburg. We are a D2 located in western Maryland with a school size around 3000 students. How it’s been described by other recruits “a small school with a big school feel”. 
    
    I got your contact information from your coach and wanted to reach out and express our interest in you. Based on your performances you have achieved over your career we would like to reach out with the opportunity to be a part of our Track and Field Family. 
    
    So do me a favor, if you want to talk some more, just send me an email and say, “I’m interested.” No commitments we’ll just talk some more, okay? 

    Thanks,
    Ballard Suiter, MBA\nAssistant Coach Track & Field\nJumps/Multis\nFrostburg State University\nC: 317-748-8043\nUSTFCCCA Level 1 Jumps Specialist
    '''

    return content

def parse_file():
     with open("2025 Maryland Senior List.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            gender = set_null_for_non_breaking_space(row[0])
            name = set_null_for_non_breaking_space(row[2])
            email = set_null_for_non_breaking_space(row[6])
            phone = set_null_for_non_breaking_space(row[7])
            coach_name = set_null_for_non_breaking_space(row[8])
            coach_email = set_null_for_non_breaking_space(row[9])
            
            if re.match(email_pattern, coach_email) and coach_email != '':
                if coach_email not in coaches_data:
                    coaches_data[coach_email] = []
                athlete_names = [athlete['name'] for athlete in coaches_data[coach_email]]
                if name not in athlete_names:
                    coaches_data[coach_email].append({
                        "gender": gender,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "coach_name": coach_name.split()[1].capitalize().rstrip()
                    })
                if email != '' and re.match(email_pattern, email):
                    athlete_data.append({
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "coach_name": coach_name
                    })

def email_coaches():
    emailed_group = []
    # Set up the SMTP server
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(user_email, user_password)

    parse_file()

    for coach_contact in coaches_data:
        subject = "Frostburg State T&F Recruiting"
        body = create_email_content_coach(coach_contact)
        # Create the author with a non-ASCII name and an email address
        author = formataddr((str(Header(u'Ballard T Suiter', 'utf-8')), user_email))
        
        # Create a MIME multipart message
        msg = MIMEMultipart('alternative')
        msg['From'] = author
        msg['To'] = coach_contact  # Assuming coach_contact is an email address
        msg['Subject'] = subject
        
        # Attach the body content. If your content is HTML, use MIMEText with 'html', else 'plain' for plain text.
        from email.mime.text import MIMEText
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Send the email. Note: convert the msg object to a string before sending
            # server.sendmail(author, coach_contact, msg.as_string())
            emailed_group.append(coach_contact)
            print(f"{coach_contact}")
        except Exception as e:
            print(f"Failed to send email to {coach_contact}: {e}")

    server.quit()

    return emailed_group
  

def email_athletes():
    emailed_group = []
    # Set up the SMTP server
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(user_email, user_password)

    parse_file()

    for athlete in athlete_data:
        subject = "Frostburg State T&F Recruiting"
        body = create_email_content_athlete(athlete)
        # Create the author with a non-ASCII name and an email address
        author = formataddr((str(Header(u'Ballard T Suiter', 'utf-8')), user_email))
        
        # Create a MIME multipart message
        msg = MIMEMultipart('alternative')
        msg['From'] = author
        msg['To'] = athlete['email']  # Assuming athelete[1] is an email address
        msg['Subject'] = subject
        
        # Attach the body content. If your content is HTML, use MIMEText with 'html', else 'plain' for plain text.
        from email.mime.text import MIMEText
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Send the email. Note: convert the msg object to a string before sending
            # server.sendmail(author, coach_contact, msg.as_string())
            emailed_group.append(athlete['email'])
            print(f"{athlete[1]}")
        except Exception as e:
            print(f"Failed to send email to {athlete['email']}: {e}")

    server.quit()

    return emailed_group


# Assuming your layout looks something like this
layout = [[sg.Text('Who would you like to email?', justification='center')],
          [sg.Column([[sg.Button('Coaches'), sg.Button('Athletes')]], justification='center')],
          [sg.Column([[sg.Button('Cancel')]], justification='center')]]

window = sg.Window('Window Title', layout, size=(400, 200))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    if event == 'Coaches':
        # Run your email sending program here
        emails_sent = email_coaches()
        
        # Create a new layout for the popup window
        layout_popup = [[sg.Text('')],
                    [sg.Column([[sg.Multiline('\n'.join(emails_sent), size=(50, len(emails_sent)), key='-OUT-')]], justification='center')],
                    [sg.Text('')]]        
        # Create a new window with the popup layout
        window_popup = sg.Window('Emails Sent', layout_popup, size=(800, 600))
        
        # Read events from the popup window
        while True:
            event_popup, values_popup = window_popup.read()
            if event_popup == sg.WIN_CLOSED:
                break
        
        # Don't forget to close the popup window
        window_popup.close()
    elif event == 'Athletes':
        # Run your email sending program here
        emails_sent = email_athletes()
        
        # Create a new layout for the popup window
        layout_popup = [[sg.Text('')],
                    [sg.Column([[sg.Multiline('\n'.join(emails_sent), size=(50, len(emails_sent)), key='-OUT-')]], justification='center')],
                    [sg.Text('')]]        
        # Create a new window with the popup layout
        window_popup = sg.Window('Emails Sent', layout_popup, size=(800, 600))
        
        # Read events from the popup window
        while True:
            event_popup, values_popup = window_popup.read()
            if event_popup == sg.WIN_CLOSED:
                break
        
        # Don't forget to close the popup window
        window_popup.close()
        
window.close()