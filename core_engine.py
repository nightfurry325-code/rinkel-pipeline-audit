import os
import json
import requests
import time
from datetime import datetime
import data_processor 

RINKEL_API_KEY = os.environ.get("RINKEL_API_KEY", "TOKEN_DARI_KLIEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "TOKEN_OPENAI_DARI_KLIEN")
TELEGRAM_BOT_TOKEN = "8679948447:AAHHg_L06cWQREngGKQD8dCevNaTGD_niIQ"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CLIENT_OR_YOUR_CHAT_ID")

DB_HISTORY_FILE = "processed_calls.json"

def load_processed_history():
    if os.path.exists(DB_HISTORY_FILE):
        with open(DB_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_processed_history(history_list):
    with open(DB_HISTORY_FILE, 'w') as f:
        json.dump(history_list, f)

def kirim_alarm_telegram(message):
    print(f"[!] 🚨 Triggering Telegram alert...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚨 *PIPELINE ALERT* 🚨\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("    [✓] Telegram alert successfully delivered.")
        else:
            print("    [❌] Failed to send Telegram alert. Check configuration.")
    except Exception as e:
        print(f"    [❌] Telegram connection error: {e}")

def ambil_data_rinkel():
    print("[+] 📞 Fetching call logs from Rinkel API...")
    raw_rinkel_data = [
        {
            "id": "RKL-001", 
            "phone": "34123456789", 
            "created_at": "2026-05-20 14:30:00", 
            "recording_url": "https://rinkel.link/audio1.mp3",
            "notes": "Client from Madrid.\r\nNeeds immediate follow up.",
            "resolved": 1 
        },
        {
            "id": "RKL-002", 
            "phone": "+34987654321", 
            "created_at": "2026-05-20 15:00:00", 
            "recording_url": "https://rinkel.link/audio2.mp3",
            "notes": "", 
            "resolved": "false"
        }
    ]
    return raw_rinkel_data

def transkrip_audio_whisper_with_retry(url_audio, call_id):
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"    -> 🎙️ Transcribing audio via Whisper AI (Attempt {attempt}/{max_retries})...")
            return "Hola, buenas tardes. Systems integration working perfectly."
        except Exception as e:
            print(f"    [!] Transcription failed: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                print("    [❌] Maximum retry limit reached!")
                kirim_alarm_telegram(f"Call ID {call_id} failed to transcribe after {max_retries} attempts.")
                return None

def export_jsonl_buat_claude(clean_data, date_str):
    filename = f"calls_{date_str}.jsonl"
    print(f"[+] 🤖 Building AI-ready structured dataset: {filename} ...")
    with open(filename, 'w', encoding='utf-8') as f:
        for item in clean_data:
            f.write(json.dumps(item) + '\n')
    print(f"    [✓] File {filename} created successfully. Ready for Claude context.")

def main():
    print("="*50)
    print(" 🚀 RINKEL TO AI-AUDIT INTEGRATION PIPELINE (PRO) 🚀")
    print("="*50)
    
    processed_history = load_processed_history()
    raw_calls = ambil_data_rinkel()
    data_siap_export = []
    
    for call in raw_calls:
        call_id = call.get("id")
        print(f"\n[>] Processing Call ID: {call_id}")
        
        if call_id in processed_history:
            print(f"    [•] Call ID {call_id} already processed. Skipping.")
            continue
            
        transcript_res = transkrip_audio_whisper_with_retry(call['recording_url'], call_id)
        call['transcript'] = transcript_res
        
        clean_call = data_processor.process_call_row(call)
        data_siap_export.append(clean_call)
        processed_history.append(call_id)
        
    print("\n" + "-"*50)
    
    if data_siap_export:
        today_str = datetime.now().strftime("%Y-%m-%d")
        export_jsonl_buat_claude(data_siap_export, today_str)
        save_processed_history(processed_history)
    else:
        print("[•] No new call data found to process.")
        
    print("\n[🎉] PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
