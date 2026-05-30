import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def main():
    print("==================================================")
    print(" Mulai Scraper Data TKA (Tabel Tüm Provinsi & Jenjang) ")
    print("==================================================")
    
    # Menampilkan daftar Jenjang kepada pengguna berdasarkan opsi yang ada di web
    print("\n=== Pilihan Jenjang ===")
    print("1. SEMUA")
    print("2. SMA")
    print("3. SMK")
    print("4. PAKET C")
    print("5. SLB")
    print("=======================\n")
    
    # Meminta input dari pengguna (Jenjang)
    print("Masukkan nomor jenjang yang ingin di-scrape (contoh: 2 untuk SMA).")
    print("Catatan: Website TKA ini spesifik hanya merilis data untuk SMA/SMK sederajat (bukan SD/SMP).")
    pilihan_jenjang = input("Pilihan Anda (1-5): ").strip()
    
    jenjang_map = {
        '1': 'SEMUA',
        '2': 'SMA',
        '3': 'SMK',
        '4': 'PAKET C',
        '5': 'SLB'
    }
    
    if pilihan_jenjang not in jenjang_map:
        print("[-] Pilihan tidak valid, menggunakan default: SEMUA")
        target_jenjang = 'SEMUA'
    else:
        target_jenjang = jenjang_map[pilihan_jenjang]

    # Menampilkan daftar Provinsi
    provinsi_list = [
        "DKI JAKARTA", "JAWA BARAT", "JAWA TENGAH", "DI YOGYAKARTA", "JAWA TIMUR", 
        "ACEH", "SUMATERA UTARA", "SUMATERA BARAT", "RIAU", "JAMBI", 
        "SUMATERA SELATAN", "LAMPUNG", "KALIMANTAN BARAT", "KALIMANTAN TENGAH", "KALIMANTAN SELATAN", 
        "KALIMANTAN TIMUR", "SULAWESI UTARA", "SULAWESI TENGAH", "SULAWESI SELATAN", "SULAWESI TENGGARA", 
        "MALUKU", "BALI", "NUSA TENGGARA BARAT", "NUSA TENGGARA TIMUR", "PAPUA", 
        "BENGKULU", "MALUKU UTARA", "BANGKA BELITUNG", "GORONTALO", "BANTEN", 
        "KEPULAUAN RIAU", "SULAWESI BARAT", "PAPUA BARAT", "KALIMANTAN UTARA", "PAPUA SELATAN", 
        "PAPUA TENGAH", "PAPUA PEGUNUNGAN", "PAPUA BARAT DAYA", "SEKOLAH INDONESIA"
    ]
    
    print("\n=== Pilihan Provinsi ===")
    for idx, prov in enumerate(provinsi_list, start=1):
        print(f"{idx}. {prov}")
    print("========================\n")
    print("Masukkan nomor provinsi (pisahkan dg koma, misal: 1,2,3).")
    print("Atau ketik 'semua' jika ingin data 39 provinsi se-Indonesia.")
    pilihan_prov = input("Pilihan Anda: ").strip().lower()
    
    filter_provinsi = []
    if pilihan_prov != 'semua':
        try:
            indeks = [int(x.strip()) for x in pilihan_prov.split(',') if x.strip()]
            for x in indeks:
                if 1 <= x <= len(provinsi_list):
                    filter_provinsi.append(provinsi_list[x-1].upper())
        except ValueError:
            print("[-] Input provinsi tidak valid, akan menggunakan 'semua' provinsi.")
        
    namaprov_file = "semuaprov" if not filter_provinsi else "CustomProv"
    output_file = f"hasil_tka_{namaprov_file}_{target_jenjang.replace(' ', '')}.xlsx"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        url = 'https://tka.kemendikdasmen.go.id/hasiltka/'
        print(f"\n[+] Mengakses website: {url}")
        
        try:
            page.goto(url, wait_until='networkidle', timeout=60000)
        except PlaywrightTimeoutError:
            print("[-] Gagal memuat halaman web: Waktu tunggu habis (Timeout).")
            browser.close()
            return
            
        print("[+] Mengatur filter Wilayah menjadi 'Provinsi'...")
        try:
            # Biasanya Select pertama adalah filter Wilayah
            page.locator('select').nth(0).select_option(label='Provinsi')
            time.sleep(1)
        except Exception as e:
            print(f"[-] Gagal set dropdown Wilayah: {e}")
            
        print(f"[+] Mengatur filter Jenjang menjadi '{target_jenjang}'...")
        try:
            # Mencari radio label dengan text sesuai lalu klik
            # Di Playwright kita bisa menggunakan text locator untuk label
            radio_label = page.locator(f"label:has-text('{target_jenjang}')").nth(0)
            if radio_label.count() > 0:
                radio_label.click()
            time.sleep(1)
        except Exception as e:
            print(f"[-] Gagal klik Jenjang: {e}")

        # Pastikan Provinsi adalah "Semua Provinsi" (Secara default begitu)
        try:
            page.locator('select').nth(1).select_option(label='Semua Provinsi')
            time.sleep(1)
        except Exception:
            pass
            
        print("[+] Mengklik tombol Refresh...")
        refresh_btn = page.locator("button:has-text('Refresh')")
        if refresh_btn.count() == 0:
            refresh_btn = page.locator('button.bg-gradient-to-r.from-blue-500')
            
        if refresh_btn.count() > 0:
            refresh_btn.click()
        else:
            print("[-] Tidak menenukan tombol Refresh, mencoba melanjutkan saja...")
            
        print("[+] Menunggu tabel termuat (Bisa memakan waktu 3-5 detik)...")
        time.sleep(4)
        
        try:
            # Memastikan tabel ada
            page.wait_for_selector('table', state='visible', timeout=15000)
        except Exception:
            print("[-] Tabel tidak langsung terlihat. Mencoba tombol view tabel...")
            # Jika tabel tertutup tab grafik, klik icon view table
            try:
                page.locator('button i.fa-table').last.click()
                time.sleep(2)
            except Exception:
                pass
        
        print(f"[+] Melakukan scraping tabel untuk jenjang {target_jenjang}...")
        try:
            # Kita grab isi array 2D via Javascript
            table_data = page.evaluate('''() => {
                let thead = document.querySelector('table thead');
                let tbody = document.querySelector('table tbody');
                if(!thead || !tbody) return null;
                
                let cols = [];
                let headers = thead.querySelectorAll('th');
                headers.forEach(th => {
                    cols.push(th.innerText.trim().replace(/\\n/g, ' '));
                });
                
                let rows = [];
                let trs = tbody.querySelectorAll('tr');
                trs.forEach(tr => {
                    let cells = tr.querySelectorAll('td, th');
                    let rowData = [];
                    cells.forEach(c => rowData.push(c.innerText.trim()));
                    rows.push(rowData);
                });
                return {columns: cols, rows: rows};
            }''')
        except Exception as e:
            print(f"[-] Terjadi error saat evaluate JS: {e}")
            browser.close()
            return
            
        browser.close()
        
        if not table_data or not table_data.get('columns'):
            print("[-] Gagal mengekstrak data dari tabel. Pastikan website sedang tidak mainatenance.")
            return
            
        cols = table_data['columns']
        rows = table_data['rows']
        
        # Preprocessing baris jika ada yang panjang kolomnya tidak sama
        valid_rows = []
        for r in rows:
             if len(r) == len(cols):
                 valid_rows.append(r)
             elif len(r) == len(cols) - 1 and r[0] == '-':
                 # Baris 'Rerata Nasional' biasanya kehilangan 1 kolom
                 valid_rows.append([''] + r)
             elif len(r) > 0 and r[0] not in ['', '-', 'No'] and len(r) >= 3:
                # Handle fallback if length mismatch
                pass
                 
        print(f"[+] Berhasil mencuplik {len(cols)} kolom dan {len(valid_rows)} total baris provinsi (termasuk Nasional).")
        
        # Jadikan Dataframe Pandas
        df = pd.DataFrame(valid_rows, columns=cols)
        
        # Menerapkan filter / penyaringan berdasarkan provinsi yang dipilih (jika ada)
        if filter_provinsi and 'PROVINSI' in df.columns:
            print(f"[+] Membuang data provinsi yang tidak dipilih, menyisakan {len(filter_provinsi)} provinsi...")
            # Kita simpan teks aslinya karena terkadang web menuliskannya berbeda sedikit, kita pakai str.contains atau upper
            kondisi_filter = df['PROVINSI'].str.upper().isin(filter_provinsi) | df['PROVINSI'].str.upper().str.contains("RERATA NASIONAL")
            df = df[kondisi_filter]
        
        # Deteksi otomatis kolom nilai (selain NO, KODE PROV, PROVINSI)
        non_value_cols = ['NO', 'KODE PROV', 'PROVINSI']
        
        # Bersihkan string nilai ke float (10.05 -> kadang ditulis 10,05)
        subject_cols = [c for c in cols if c.upper() not in non_value_cols]
        for sub in subject_cols:
            df[sub] = df[sub].str.replace(',', '.').astype(float, errors='ignore')
            
        # Kalkulasi kolom rata-rata total di paling kanan
        df_num = df[subject_cols].apply(pd.to_numeric, errors='coerce')
        df['Rata-rata Keseluruhan TKA'] = df_num.mean(axis=1).round(2)
        
        # Bersihkan jika ada kolom kosong (opsional)
        if 'NO' in df.columns:
            df = df.drop(columns=['NO']) # NO tidak berguna di Excel karena sudah ada nomor baris
            
        print("\n==================================================")
        try:
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"SUKSES: Seluruh data (Semua mapel) berhasil disimpan ke file HTML/Excel:\n-> {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"GAGAL: Terjadi masalah lokal saat menyimpan file: {e}")
        print("==================================================")

if __name__ == '__main__':
    main()
