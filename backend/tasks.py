import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import csv
import io
from datetime import datetime
import os 


from databse import Reserve, User 
from celery import Celery
from dotenv import load_dotenv



load_dotenv()  

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
@celery.task(name="tasks.send_booking_email")
def send_booking_email(to_email, user_name, parking_location):
    print("Email sending called with:")
    print(f"to_email = {to_email}")
    print(f"user_name = {user_name}")
    print(f"parking_location = {parking_location}")
    
    subject = "Parking Spot Booking Confirmation"
    body = f"Hi {user_name},\n\nYour parking spot at {parking_location} has been booked successfully."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "austin.amelthomas@gmail.com"
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("austin.amelthomas@gmail.com", "miqf kejo mecz ipiz")
        server.sendmail("austin.amelthomas@gmail.com", to_email, msg.as_string())
        server.quit()
        return f"Email sent to {to_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"



@celery.task(name="tasks.send_monthly_report")
def send_monthly_report(to_email, user_name):
    from app import app
    with app.app_context():
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        next_month = datetime(now.year + (now.month // 12), ((now.month % 12) + 1), 1)

        user = User.query.filter_by(username=to_email).first()
        if not user:
            return f"User with email {to_email} not found."

        reservations = Reserve.query.filter(
            Reserve.user_id == user.id,
            Reserve.startdate >= start_of_month,
            Reserve.startdate < next_month
        ).all()

        if not reservations:
            return f"No reservations found for {to_email} in {now.strftime('%B %Y')}."

      
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Vehicle No", "Parking Spot", "Parking Lot", "Start Time", "End Time", "Cost", "Status"])
        for res in reservations:
            writer.writerow([
                res.startdate.strftime('%Y-%m-%d'),
                res.vehicle_no,
                res.parking_spot_id,
                res.parking_lot_id,
                res.starttime.strftime('%H:%M') if res.starttime else '',
                res.endtime.strftime('%H:%M') if res.endtime else '',
                res.cost,
                res.status
            ])
        csv_file.seek(0)

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return "Email credentials not set in environment variables."

     
        msg = MIMEMultipart()
        msg['Subject'] = f"Monthly Parking Report - {now.strftime('%B %Y')}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email

        body = MIMEText(
            f"Hi {user_name},\n\nAttached is your parking reservation report for {now.strftime('%B %Y')}.\n\nBest regards,\nParking Service"
        )
        msg.attach(body)

        attachment = MIMEApplication(csv_file.getvalue(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename="monthly_report.csv")
        msg.attach(attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
            server.quit()
            return f"Monthly report sent to {to_email}"
        except Exception as e:
            return f"Failed to send report: {str(e)}"

@celery.task(name="tasks.send_all_monthly_reports")
def send_all_monthly_reports():
    from app import app  
    with app.app_context():
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        next_month = datetime(now.year + (now.month // 12), ((now.month % 12) + 1), 1)

   
        user_ids = (
            Reserve.query.filter(
                Reserve.startdate >= start_of_month,
                Reserve.startdate < next_month
            )
            .with_entities(Reserve.user_id)
            .distinct()
        )

        users = User.query.filter(User.id.in_([uid[0] for uid in user_ids])).all()

        for user in users:
            send_monthly_report.delay(user.username, user.username) 