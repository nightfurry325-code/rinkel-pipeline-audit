import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Bumbu paspor dan izin akses
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # Diubah biar bisa EDIT (bukan readonly)
SERVICE_ACCOUNT_FILE = 'kunci_api.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 2. ID Google Sheets lu (Pastikan isinya ID acak panjang ya, bukan link)
SPREADSHEET_ID = '1ezPdEt_4Ieh6Sf_kWCTLO5FTTgq0tWjHWQ-8yDFZyco'

try:
    # 3. Bangun koneksi kurir (Mendefinisikan variabel 'sheet' yang error tadi)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # 4. Tentukan target lokasi sel yang mau lu revisi/ubah
    # Contoh: Kita mau ngubah isi sel B3 (Baris 3, Kolom Harga)
    RANGE_REVISI = 'Sheet1!B3' 
    
    # Data baru yang pengen lu masukin
    BODY_REVISI = {
        'values': [[7500]] # Mengubah harga di sel B3 jadi 7500
    }
    
    # 5. Eksekusi revisi otomatis ke Google Sheets
    print("Sedang merevisi data ke Google Sheets...")
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_REVISI,
        valueInputOption='USER_ENTERED',
        body=BODY_REVISI
    ).execute()
    
    print("=== ALHAMDULILLAH DATA BERHASIL DIREVISI OLEH PYTHON WIR! ===")

except Exception as e:
    print(f"Waduh ada kendala nih: {e}")
