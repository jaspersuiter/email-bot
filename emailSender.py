import smtplib
import csv

def set_null_for_non_breaking_space(value):
  """Checks if the value is a non-breaking space and returns None if it is,
     otherwise returns the original value."""
  if value == 'Â\xa0':
    return ''
  else:
    return value
  
# Enter your email details
user_email = "your_email@example.com"
user_password = "your_email_password"

# Set up the SMTP server
# smtp_server = "smtp.example.com"
# smtp_port = 587
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()
# server.login(email, password)

coaches_data = {}

with open("2025 Maryland Senior List.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        gender = set_null_for_non_breaking_space(row[0])
        name = set_null_for_non_breaking_space(row[2])
        email = set_null_for_non_breaking_space(row[6])
        phone = set_null_for_non_breaking_space(row[7])
        coach_name = set_null_for_non_breaking_space(row[8])
        coach_email = set_null_for_non_breaking_space(row[9])

        if coach_email not in coaches_data:
            coaches_data[coach_email] = []

        coaches_data[coach_email].append({
            "gender": gender,
            "name": name,
            "email": email,
            "phone": phone,
            "coach_name": coach_name.split(' ', 1)[-1]
        })     



def create_email_content(coach_contact):
    # content = '''
    # Good afternoon Coach {coach_name}\
    # test
    # '''.format(coaches_data[coach_contact])
    print(coaches_data[coach_contact])

for coach_contact in coaches_data:
    create_email_content(coach_contact)
    break