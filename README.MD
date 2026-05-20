# Rinkel Pipeline Audit Engine

Automated, scalable, and production-ready pipeline for Rinkel call data auditing. This system ensures seamless data fetching, deduplication, and archival, designed for high-efficiency enterprise environments.

## 🚀 Key Features
- **Automated Fetching:** Direct integration with Rinkel API to capture real-time call events.
- **Intelligent Deduplication:** Prevents duplicate entries using a robust indexing mechanism.
- **Error Handling:** Built-in alert system (Telegram) to notify on API failures or missing data.
- **Serverless Architecture:** Fully automated on GitHub Actions; no server maintenance required.
- **Modular Design:** Built for easy integration with OpenAI Whisper for transcription and Google Drive for storage.

## ⚙️ Technical Workflow
1. **Fetch:** Pulls raw call logs from Rinkel API.
2. **Validate:** Checks against index to ensure data integrity.
3. **Process:** Normalizes data into clean `.jsonl` records.
4. **Notify:** Real-time status updates via Telegram.
5. **Sync:** Prepares data for Google Drive and Whisper API integration.

## 🛠 Tech Stack
- **Language:** Python
- **Environment:** GitHub Actions (Serverless)
- **Data Format:** JSONL
- **Integration Ready:** OpenAI Whisper API, Google Drive API

---
*Built with passion for automation by Feri.*
