import os
import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# Load Secrets
GEMINI_KEY = os.environ["GEMINI_API_KEY"]
EMAIL_USER = os.environ["SECONDARY_EMAIL"]
EMAIL_PASS = os.environ["EMAIL_APP_PASSWORD"]
MAIN_EMAIL = os.environ["MAIN_EMAIL"]

def get_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('INBOX') # Switch to your label name if needed
        
        _, data = mail.search(None, 'UNSEEN')
        articles = []
        
        for num in data[0].split():
            _, msg_data = mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                articles.append(part.get_payload(decode=True).decode(errors='ignore'))
                    else:
                        articles.append(msg.get_payload(decode=True).decode(errors='ignore'))
        return articles
    except Exception as e:
        print(f"Error fetching mail: {e}")
        return []

def summarize_with_gemini(text_list):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    content = "\n\n---\n\n".join(text_list)
    
    # THE RUTHLESS DISTILLER PROMPT
    prompt = f"""
    You are the Lead Technical Researcher for 'The Robotics Pulse'. 
    Reader: AI & Robotics Student.
    
    INSTRUCTIONS:
    1. Select the 5 most technically dense stories. 
    2. Combine overlapping news into single entries.
    3. For every story, add a brief 'ROBOTICS IMPACT' sentence explaining how this tech/exploit applies to physical AI or autonomous systems.
    
    FORMATTING:
    - NO Markdown (** or ##). 
    - Use <h2> for Titles.
    - Use <p style="font-size: 17px; margin-bottom: 8px;"> for the Summary.
    - Use <strong>[Robotics Impact]</strong> followed by the explanation.
    - CODE BLOCKS: Use the <div> with monospace font ONLY for actual code snippets (2+ lines) or technical stats lists. Do NOT put single words or variables in a box.
    - LINK: You MUST include the [Read Source →] link.

    NEWS CONTENT:
    {content}
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_html_email(html_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "⚡ The Robotics Pulse: Top 5 Briefing"
    msg['From'] = EMAIL_USER
    msg['To'] = MAIN_EMAIL

    styled_html = f"""
    <html>
      <body style="background-color: #f8f9fa; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <div style="background-color: #ffffff; 
                    max-width: 650px; 
                    margin: 0 auto; 
                    padding: 40px; 
                    border: 1px solid #e1e4e8;
                    border-radius: 8px;">
            
            <div style="text-align: left; margin-bottom: 40px; border-bottom: 4px solid #1a73e8; padding-bottom: 10px;">
                <h1 style="margin: 0; font-size: 24px; color: #1a73e8;">THE ROBOTICS PULSE</h1>
                <p style="margin: 5px 0 0 0; color: #586069; font-size: 14px; font-weight: bold;">
                    ESTIMATED READ TIME: 90 SECONDS
                </p>
            </div>
            
            <div style="color: #24292e; line-height: 1.5;">
                {html_content}
            </div>

            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e1e4e8; text-align: center; color: #586069; font-size: 12px;">
                Curation Engine v2.1 • Robotics & AI Research Agent
            </div>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(styled_html, 'html'))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# Execution logic
news = get_emails()
if news:
    print(f"Summarizing {len(news)} newsletters...")
    summary_html = summarize_with_gemini(news)
    send_html_email(summary_html)
    print("Beautiful summary sent!")
else:
    print("No new mail.")
