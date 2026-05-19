import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Setup Google API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'kunci_api.json'
SPREADSHEET_ID = '1ezPdEt_4Ieh6Sf_kWCTLO5FTTgq0tWjHWQ-8yDFZyco'

def koneksi_sheets():
    try:
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    except Exception as e:
        print(f"\n[!] Gagal koneksi ke Google API: {e}")
        sys.exit()

def tampilkan_menu():
    print("\n" + "="*40)
    print("   🔥 GOOGLE SHEETS UTILITY TOOLS 🔥   ")
    print("="*40)
    print("[1] Tampilkan Seluruh Data Mentah")
    print("[2] Revisi / Edit Data Sel")
    print("[3] Jalankan Data Cleaner (Anti-Duplikat)")
    print("[4] Keluar Aplikasi")
    print("="*40)

def main():
    sheet = koneksi_sheets()
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ").strip()
        
        # MENU 1: TAMPILKAN DATA MENTAH
        if pilihan == '1':
            print("\n[+] Memuat data dari Google Sheets...")
            try:
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A1:B15').execute()
                rows = result.get('values', [])
                if not rows:
                    print("[-] Data kosong, Wir!")
                else:
                    print("\n--- DATA DI GOOGLE SHEETS ---")
                    for i, row in enumerate(rows):
                        print(f"Baris {i+1}: {row}")
            except Exception as e:
                print(f"[!] Error: {e}")
                
        # MENU 2: REVISI / EDIT DATA
        elif pilihan == '2':
            print("\n--- MENU REVISI DATA ---")
            sel = input("Masukkan koordinat sel (Contoh: B3, A5, B11): ").strip().upper()
            if not sel: continue
            
            isi_baru = input(f"Masukkan data baru untuk sel {sel}: ").strip()
            
            range_target = f'Sheet1!{sel}'
            body_revisi = {'values': [[isi_baru]]}
            
            print(f"[+] Mengubah sel {sel} menjadi '{isi_baru}'...")
            try:
                sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=range_target,
                    valueInputOption='USER_ENTERED',
                    body=body_revisi
                ).execute()
                print("[✓] REVISI BERHASIL WIR!")
            except Exception as e:
                print(f"[!] Gagal revisi: {e}")
                
        # MENU 3: DATA CLEANER (ANTI-DUPLIKAT & KOSONG)
        elif pilihan == '3':
            print("\n[+] Menjalankan mesin pembersih otomatis...")
            try:
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A1:B15').execute()
                rows = result.get('values', [])
                
                if not rows:
                    print("[-] Tidak ada data yang bisa dibersihkan.")
                    continue
                
                header = rows[0]
                data_mentah = rows[1:]
                data_bersih = []
                sudah_ada = set()
                
                print(f"[i] Scanning {len(data_mentah)} baris data...")
                
                for r in data_mentah:
                    # Lewati baris kosong total
                    if not r or (len(r) == 1 and r[0].strip() == "") or (len(r) >= 2 and r[0].strip() == "" and r[1].strip() == ""):
                        continue
                    
                    nama_produk = r[0].strip() if len(r) > 0 else ""
                    harga = r[1].strip() if len(r) > 1 else ""
                    
                    # Cek duplikat
                    if nama_produk.lower() in sudah_ada:
                        print(f" -> [CLEANED] Duplikat terdeteksi & dihapus: {nama_produk}")
                        continue
                    
                    if nama_produk:
                        sudah_ada.add(nama_produk.lower())
                    data_bersih.append([nama_produk, harga])
                
                print("\n[✓] HASIL EKSEKUSI CLEANER:")
                print(f"-> {header}")
                for row in data_bersih:
                    print(f"-> {row}")
                    
            except Exception as e:
                print(f"[!] Gagal membersihkan data: {e}")
                
        # MENU 4: KELUAR
        elif pilihan == '4':
            print("\nSampai jumpa lagi, Wir! Tetap kreatif! 🚀")
            break
            
        else:
            print("\n[!] Pilihan kagak ada, Wir. Masukin angka 1 sampai 4 aja.")
            
        input("\nTekan ENTER untuk kembali ke menu utama...")

if __name__ == '__main__':
    main()

