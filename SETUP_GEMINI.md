# Setup Gemini API untuk Skills Generation

## Langkah-langkah Setup

### 1. Dapatkan Gemini API Key
- Kunjungi: https://makersuite.google.com/app/apikeys
- Login dengan Google account Anda
- Klik "Create API Key"
- Copy API key yang sudah di-generate

### 2. Install Google Generative AI Library
```bash
pip install google-generativeai
```

### 3. Update file `.env`
Buka file `.env` dan update `GEMINI_API_KEY`:
```
LINKEDIN_LI_AT=your_li_at_cookie
GEMINI_API_KEY=your_gemini_api_key_here
```

## Cara Kerja

Ketika ekstraksi skills dari LinkedIn gagal, sistem akan:

1. **Mengumpulkan data** - Headline, About, dan Experience dari profil
2. **Generate dengan AI** - Mengirim data ke Gemini untuk generate skills yang relevan
3. **Format output** - Skills di-return dalam format: `skill1|skill2|skill3|...`

## Contoh Output

**Input:**
- Headline: "Senior Software Engineer at Tech Company"
- About: "Passionate about building scalable web applications..."
- Experience: "Lead Backend Developer", "Full Stack Engineer", etc.

**Output (dari Gemini):**
```
Python|JavaScript|React|Node.js|AWS|Docker|PostgreSQL|REST APIs|Microservices|System Design
```

## Troubleshooting

### Error: "GEMINI_API_KEY tidak diset"
- Pastikan `.env` file sudah di-update dengan API key yang valid
- Restart aplikasi setelah update `.env`

### Error: "Invalid API key"
- Verifikasi API key di https://makersuite.google.com/app/apikeys
- Pastikan API key tidak ada spasi atau karakter tambahan

### Error: "Quota exceeded"
- Gemini API memiliki rate limit gratis
- Tunggu beberapa saat sebelum mencoba lagi
- Atau upgrade ke plan berbayar

## Biaya

Gemini API menawarkan:
- **Free tier**: 60 requests per menit
- **Paid tier**: Mulai dari $0.075 per 1000 input tokens

Untuk informasi lebih lanjut: https://ai.google.dev/pricing
