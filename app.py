import os
import psutil
from flask import Flask, render_template
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# --- Email Configuration ---
# Authentication & Server Settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Must be an integer
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'  # Must be Boolean
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Sender & Recipient Identity
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_RECIPIENT'] = os.getenv('MAIL_RECIPIENT')


mail = Mail(app)

# Track if alert was already sent to avoid spamming every 5 mins
alert_sent = False

@app.route("/")
def index():
    global alert_sent

    # Gather metrics
    cpu_percentage = psutil.cpu_percent(interval=1)
    mem_percentage = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent  # Added Disk usage for "Health Monitor" feel
    
    # Logic for status alerts
    status = "Healthy"
    status_class = "bg-success"
    
    if cpu_percentage > 80 or mem_percentage > 80:
        status = "Warning"
        status_class = "bg-danger"
        if not alert_sent:
            send_alert_email(cpu_percentage, mem_percentage)
            alert_sent = True
    else:
        alert_sent = False # Reset once healthy

    return render_template("index.html", cpu=cpu_percentage, mem=mem_percentage, disk=disk, status=status, status_class=status_class)

def send_alert_email(cpu, mem):
    try:
        recipient = app.config['MAIL_RECIPIENT']
        
        msg = Message(
            "⚠️ SYSTEM ALERT: High Resource Usage",
            recipients=[recipient]
        ) # Your receiving email

        msg.body = f"Alert! High utilization detected.\nCPU: {cpu}%\nMemory: {mem}%"

        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
