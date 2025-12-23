import os
import uuid
from datetime import datetime
import openpyxl
from openpyxl import Workbook
import smtplib
from email.mime.text import MIMEText
myEmail = 'nammapakkam83@gmail.com'

# --- Pydantic Schema for Tool Input ---
def create_claim(claim_descr: str, claims_amount: float, member_id: str) -> str:
    """
    Generates a unique Claim ID and writes the full record to the claims log.
    """
    try:
        file_path = "claims_log.xlsx"
        new_claim_id = "CID-" + str(uuid.uuid4())[:8].upper()
        claim_status = "IN_PROGRESS"
        
        # Check if file exists, else create with headers
        if not os.path.exists(file_path):
            wb = Workbook()
            ws = wb.active
            # Ensure the header order matches the data appended below
            ws.append(["Claim_ID", "Member_ID", "Claim_Amount", "Claim_Description", "Claim_Status", "Created_At", "Updated_At"])
            wb.save(file_path)

        # Append new claim
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        current_timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        
        ws.append([
            new_claim_id,
            member_id,
            claims_amount,
            claim_descr,
            claim_status,
            current_timestamp, # created_datetimestamp
            current_timestamp  # modified_datetimestamp
        ])
        wb.save(file_path)
        
        print(f"New Claim ID generated: {new_claim_id}. Logged successfully to {file_path}. Status: {claim_status}")
        
        send_gmail(new_claim_id, member_id, claims_amount, claim_descr)

        return {"new_claim_id": new_claim_id}
        
    except Exception as e:
        # Return failure message to the LLM
        return f"ERROR: Failed to log claim data. Reason: {e}"
    
def send_gmail(claim_id: str, member_id: str, claim_amount: float, claim_descr: str):
    """
    Sends an email using the Gmail SMTP server.

    NOTE: For security, Gmail requires an 'App Password' to be used instead of
    your regular account password when sending mail via external applications.
    You must generate this password in your Google Account security settings.

    Args:
        sender_email (str): The email address of the sender (your Gmail address).
        app_password (str): The Google App Password generated for this purpose.
        recipient_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The main content of the email (plain text).
    """
    
    # 1. Define server details
    smtp_server = "smtp.gmail.com"
    port = 587  # For SSL

    # 2. Create the message object
    msg = MIMEText(
        'Hello approver,\n\n'
        'A new claim has been submitted with the following details:\n\n'
        f'Claim ID: {claim_id}\n'
        f'Member ID: {member_id}\n'
        f'Claim Amount: {claim_amount}\n'
        f'Claim Description: {claim_descr}\n\n'
        'Please review and approve it using the link https://your-approval-link.com at your earliest convenience.\n\n'
        '\n'
        'Best regards,\n'
        'Cura Automated Notification System'
    )
    msg['Subject'] = 'New claim ID: ' + claim_id + ' is waiting for your approval'
    msg['From'] = myEmail
    msg['To'] = myEmail

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(myEmail, "eozxeiefngnomfyu")
    server.sendmail(myEmail, myEmail, msg.as_string())
    server.quit()
            
    print("✅ Email sent successfully!")
