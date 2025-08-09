#!/usr/bin/env python3
# test_gmail.py - Standalone Gmail SMTP test

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_smtp():
    # Replace with your actual credentials
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL = 'nancykaroki49@gmail.com'
    APP_PASSWORD = 'ffckzevyvgztxcns'  # Replace with fresh app password
    
    print("🔧 Testing Gmail SMTP Configuration")
    print(f"📧 Email: {EMAIL}")
    print(f"🔒 App Password: {'*' * len(APP_PASSWORD)}")
    print(f"🌐 Server: {SMTP_SERVER}:{SMTP_PORT}")
    print("-" * 50)
    
    try:
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = EMAIL  # Send to yourself
        msg['Subject'] = '✅ Test Email - Richman Travel SMTP'
        
        body = """
        🎉 Success! Your Gmail SMTP configuration is working correctly.
        
        This test email confirms that:
        ✅ 2-Factor Authentication is enabled
        ✅ App Password is valid
        ✅ SMTP connection is successful
        
        Your Richman Travel booking system can now send emails!
        
        Best regards,
        Richman Travel System
        """
        
        msg.attach(MIMEText(body.strip(), 'plain'))
        
        # Test connection
        print("1️⃣ Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        print("2️⃣ Starting TLS encryption...")
        server.starttls()
        
        print("3️⃣ Authenticating with App Password...")
        server.login(EMAIL, APP_PASSWORD)
        
        print("4️⃣ Sending test email...")
        server.send_message(msg)
        
        print("5️⃣ Closing connection...")
        server.quit()
        
        print("\n🎉 SUCCESS! Test email sent successfully!")
        print(f"📬 Check your inbox at {EMAIL}")
        print("\n✅ Your SMTP configuration is working correctly.")
        print("You can now use this App Password in your .env file.")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION FAILED: {e}")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Verify 2-Step Verification is enabled on your Google Account")
        print("2. Generate a NEW App Password:")
        print("   - Go to https://myaccount.google.com/security")
        print("   - App passwords → Select app: Mail → Generate")
        print("3. Copy the 16-character password (no spaces)")
        print("4. Update the APP_PASSWORD variable above")
        print("5. Run this test again")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == '__main__':
    test_gmail_smtp()
