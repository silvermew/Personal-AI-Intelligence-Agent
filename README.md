🤖 **Personal Robotics Intelligence Agent**
Live Demo: View a Sample Briefing Here
An autonomous AI agent that distills high-density technical newsletters into actionable "Robotics Impact" briefings.

🚀 **Overview**
In the fast-paced field of Robotics and AI, information overload is a hurdle. This project automates the curation of research-grade news, moving away from social media noise to a structured, technical intelligence report.

*Key Features*
Automated Ingest: Connects to a dedicated research email via IMAP.

Intelligent Distillation: Uses Gemini 2.5 Flash to synthesize multiple sources, removing "marketing fluff" and focusing on technical benchmarks.

Domain-Specific Analysis: Includes a custom "Robotics Impact" section for every story, bridging the gap between cybersecurity/AI news and physical autonomous systems.

Zero-Host Infrastructure: Runs entirely on GitHub Actions via a daily cron job.

🛠️ **Tech Stack**
Language: Python 3.10+

LLM: Google Gemini 2.5 Flash API

Automation: GitHub Actions (CI/CD as a Service)

Protocol: IMAP/SMTP for secure mail handling

📊 **System Architecture**
Trigger: GitHub Actions wakes up daily (08:00 UTC).

Fetch: Python script retrieves unread newsletters labeled ToSummarize.

Process: Text is sent to Gemini with a specialized prompt for technical extraction.

Delivery: A styled HTML briefing is dispatched to my primary device.
