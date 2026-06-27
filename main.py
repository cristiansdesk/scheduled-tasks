import datetime as date_t
import pandas
import random
import smtplib
import os

# 1. Pull secure credentials from GitHub environment variablesMY_EMAIL = os.environ.get("MY_EMAIL")
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
file_list = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]

# 2. Read the birthday database
b_csv = pandas.read_csv("birthdays.csv")

# 3. Check current date logic directly
now = date_t.datetime.now()
b_days = b_csv[(b_csv.month == now.month) & (b_csv.day == now.day)]

# 4. Loop through matching birthdays and send emails
if not b_days.empty:
    for (index, row) in b_days.iterrows():
        new_file = random.choice(file_list)
        
        with open(new_file) as ran:
            rand_file = ran.read()

        # Customize the template letter        
        new_card = rand_file.replace("[NAME]", row["name"])

        # Fixed outer double quotes to single quotes to avoid conflict        
        with open(f'Birthday Card to {row["name"]}.txt', "w") as file:
            file.write(new_card)

        # Connect to Gmail SMTP server and send        
        with smtplib.SMTP("smtp.gmail.com") as send:
            send.starttls()
            send.login(user=MY_EMAIL, password=PASSWORD)
            send.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=row["email"],
                msg=f"Subject:Happy Birthday!\n\n{new_card}"
            )



















