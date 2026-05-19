import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Tentukan bahan kunci dan ruang lingkup izinnya
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'kunci_api.json'

# 2. Proses validasi paspor/surat izin ke Google
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 3. Ganti ID ini dengan ID Google Sheets lu sendiri
# (ID itu karakter panjang yang ada di URL Google Sheets lu)
SPREADSHEET_ID = '1ezPdEt_4Ieh6Sf_kWCTLO5FTTgq0tWjHWQ-8yDFZyco'
RANGE_NAME = 'Sheet1!A1:B5' # Mengambil data dari Sheet1 kolom A baris 1 sampai B baris 5

try:
    # 4. Panggil kurir buat hubungin layanan Sheets
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # 5. Eksekusi penarikan data
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    rows = result.get('values', [])

    if not rows:
        print('Waduh, datanya kosong, Wir!')
    else:
        print('=== ALHAMDULILLAH DATA MASUK WIR ===')
        for row in rows:
            # Nampilin kolom data di terminal
            print(row)
            
except Exception as e:
    print(f"Ada yang error nih, Wir! Cek kesalahannya: {e}")

