import requests
import csv
from tempfile import NamedTemporaryFile
import shutil
import time


# Copy and paste you own API_KEY inbetween the quotation marks.  If you use an alternate .csv file name
# you enter it under FILE_NAME
API_KEY = ""
filename = "83000-emails-Agency-Hackers.csv"
tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')
fields = ['Campaign', 'fullName', 'firstName', 'lastName', 'companyName', 'title', 'companyNormalName',
          'Domain', 'Email', 'profileUrl', 'Validation Results']


def check_email(email=''):
    # Build a request string using the API_Key and the given email address.
    request_string = "https://emailvalidation.abstractapi.com/v1/?api_key=" + API_KEY + "&email=" + email

    # Query the API using the request_string.
    response = requests.get(request_string)


    # Make sure we get a valid response, and return true if deliverable.
    if response.status_code == 200:
        data = response.json()
        return data['deliverability'] == "DELIVERABLE"
    else:
        print(response.status_code)
        raise Exception("API didn't send a successful response.")


def update_csv():
    with open(filename, 'r', encoding='utf8') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        #next(reader, None)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        i = 0
        for row in reader:
            # Save the headers.
            if i == 0:
                writer.writerow(row)
                i += 1
                continue

            # Extract the email.
            user_email = row['Email']
            #print(user_email)
            #time.sleep(3)
            deliverable = check_email(user_email)
            row['Validation Results'] = deliverable
            row = {'Campaign': row['Campaign'], 'fullName': row['fullName'], 'firstName': row['firstName'],
                   'lastName': row['lastName'], 'companyName': row['companyName'], 'title': row['title'],
                   'companyNormalName': row['companyName'], 'Domain': row['Domain'], 'Email': row['Email'],
                   'profileUrl': row['profileUrl'], 'Validation Results': row['Validation Results']
                   }

            writer.writerow(row)

    shutil.move(tempfile.name, filename)


if __name__ == '__main__':
    update_csv()
    exit()

