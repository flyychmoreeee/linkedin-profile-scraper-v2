# LinkedIn Profile Scraper - Setup Guide

## Cara Mendapatkan `li_at` Cookie

### Langkah 1: Login ke LinkedIn
1. Buka https://www.linkedin.com
2. Login dengan akun Anda

### Langkah 2: Buka Developer Tools
1. Tekan `F12` atau `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
2. Pergi ke tab **Application** atau **Storage**

### Langkah 3: Cari Cookie `li_at`
1. Di sidebar, pilih **Cookies** → **https://www.linkedin.com**
2. Cari cookie dengan nama `li_at`
3. Copy value-nya (panjang string yang panjang)

### Langkah 4: Set Environment Variable
**Windows (PowerShell):**
```powershell
$env:LINKEDIN_LI_AT = "paste_your_li_at_value_here"
```

**Windows (Command Prompt):**
```cmd
set LINKEDIN_LI_AT=paste_your_li_at_value_here
```

**Linux/Mac:**
```bash
export LINKEDIN_LI_AT="paste_your_li_at_value_here"
```

Atau buat file `.env`:
```
LINKEDIN_LI_AT=paste_your_li_at_value_here
```

## Instalasi Dependencies

```bash
pip install -r requirements.txt
```

Anda juga perlu download **ChromeDriver** dari https://chromedriver.chromium.org/ yang sesuai dengan versi Chrome Anda.

## Menjalankan Server

```bash
uvicorn main:app --reload
```

Server akan berjalan di `http://localhost:8000`

## Testing API

### Endpoint: GET /profile

**URL:**
```
http://localhost:8000/profile?vanity_name=rasya-zildan-19588b2a4
```

**Response (Success):**
```json
{
  "name": "Rasya Zildan",
  "headline": "Software Engineer at Company XYZ",
  "summary": "Passionate about coding...",
  "profile_picture": "https://...",
  "location": "Jakarta, Indonesia",
  "experiences": [
    {
      "title": "Software Engineer",
      "company": "Company XYZ"
    }
  ],
  "education": [
    {
      "school": "University Name"
    }
  ],
  "skills": ["Python", "JavaScript", "React"]
}
```

**Response (Error):**
```json
{
  "error": "Profil tidak ditemukan"
}
```

## Troubleshooting

### 1. "ChromeDriver not found"
- Download ChromeDriver dari https://chromedriver.chromium.org/
- Pastikan versi sesuai dengan Chrome Anda
- Letakkan di folder yang sama dengan script atau tambahkan ke PATH

### 2. "li_at cookie expired"
- Cookie `li_at` memiliki masa berlaku
- Jika error, ambil cookie baru dari LinkedIn

### 3. "Profile not found" padahal profil ada
- Pastikan profil public (bisa diakses tanpa login)
- Tunggu beberapa saat sebelum scrape ulang

### 4. Selenium timeout
- Tingkatkan `time.sleep()` di `linkedin_scraper.py`
- Atau gunakan `--headless` mode untuk performa lebih baik

## Notes

- Scraper ini menggunakan Selenium untuk membuka browser real
- Lebih reliable daripada API karena bisa scrape profil private (dengan akun Anda)
- Gunakan dengan bijak dan sesuai Terms of Service LinkedIn
- Jangan share `li_at` cookie Anda dengan orang lain
