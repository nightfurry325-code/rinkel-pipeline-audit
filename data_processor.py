import json
import re
from datetime import datetime
import zoneinfo

def clean_text(text):
    """Memastikan teks bersih UTF-8 dan normalisasi enter (Poin 7)"""
    if text is None:
        return None
    # Pastikan tipe data string, encode-decode ke utf-8 untuk bersihkan karakter aneh
    clean_str = str(text).encode('utf-8', errors='ignore').decode('utf-8')
    # Normalisasi semua jenis enter/newline menjadi \n
    return clean_str.replace('\r\n', '\n').replace('\r', '\n')

def format_phone_e164(phone):
    """Memformat nomor telepon ke standar E.164 (Contoh: +34123456789)"""
    if not phone:
        return None
    # Ambil angka saja
    digits = re.sub(r'\D', '', str(phone))
    if not digits:
        return None
    
    # Jika belum ada tanda +, kita tambahkan (Asumsi jika tidak ada kode negara, sesuaikan kebutuhan)
    # Catatan: Klien Spanyol biasanya nomor diawali 34. 
    if not str(phone).startswith('+'):
        return f"+{digits}"
    return f"+{digits}"

def format_timestamp_madrid(dt_str):
    """Mengubah format waktu menjadi ISO 8601 dengan Zona Waktu Europe/Madrid"""
    if not dt_str:
        return None
    try:
        # Asumsi input string waktu universal, kita konversi ke timezone Madrid
        # Jika dt_str berupa format umum 'YYYY-MM-DD HH:MM:SS'
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        # Set zona waktu ke Europe/Madrid
        madrid_tz = zoneinfo.ZoneInfo("Europe/Madrid")
        dt_madrid = dt.replace(tzinfo=madrid_tz)
        return dt_madrid.isoformat()
    except Exception:
        # Jika format berbeda, kembalikan string apa adanya atau sesuaikan
        return dt_str

def process_call_row(raw_data):
    """
    Fungsi utama untuk memproses satu baris data telepon mentah.
    Menjamin aturan: empty fields as null (None di Python), booleans asli, dll.
    """
    processed = {}
    
    # 1. ID Telepon (Wajib untuk filter anti-duplikat nanti)
    processed['call_id'] = raw_data.get('id') if raw_data.get('id') else None
    
    # 2. Text fields (Clean UTF-8 & \n)
    processed['transcript'] = clean_text(raw_data.get('transcript'))
    processed['notes'] = clean_text(raw_data.get('notes'))
    
    # 3. Phone Numbers (E.164)
    processed['customer_phone'] = format_phone_e164(raw_data.get('phone'))
    
    # 4. Timestamps (ISO 8601 Madrid)
    processed['timestamp'] = format_timestamp_madrid(raw_data.get('created_at'))
    
    # 5. Booleans asli (True/False, bukan 1/0 atau yes/no)
    # Mengonversi input apapun ke boolean murni Python
    is_resolved = raw_data.get('resolved')
    if is_resolved in [True, 1, '1', 'yes', 'True', 'true']:
        processed['resolved'] = True
    elif is_resolved in [False, 0, '0', 'no', 'False', 'false']:
        processed['resolved'] = False
    else:
        processed['resolved'] = None # Menjamin empty field as null

    return processed
