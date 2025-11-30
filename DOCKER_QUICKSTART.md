# Docker Quick Start Guide

## 5 Menit Setup

### Step 1: Persiapan
```bash
# Pastikan Docker sudah terinstall
docker --version
docker-compose --version
```

### Step 2: Setup Environment
```bash
# Copy template .env
cp .env.example .env

# Edit .env dengan LinkedIn li_at cookie Anda
# Gunakan text editor favorit Anda
```

### Step 3: Build & Run
```bash
# Build image (pertama kali saja, ~5-10 menit)
docker-compose build

# Run container
docker-compose up -d

# Tunggu ~30 detik sampai container fully started
sleep 30

# Check status
docker-compose ps
```

### Step 4: Test
```bash
# Buka di browser
# http://localhost:8000/docs

# Atau test dengan curl
curl "http://localhost:8000/profile?vanity_name=naufal-arga-a5b22b2aa"
```

## Perintah Penting

```bash
# Lihat logs
docker-compose logs -f

# Stop container
docker-compose down

# Restart container
docker-compose restart

# Remove everything
docker-compose down -v
```

## Deployment ke VPS (1 Command)

```bash
# 1. SSH ke VPS
ssh user@your-vps-ip

# 2. Clone project
git clone <your-repo-url> linkedin-scraper
cd linkedin-scraper

# 3. Setup & Run
cp .env.example .env
nano .env  # Edit LINKEDIN_LI_AT

# 4. Start
docker-compose up -d

# 5. Verify
curl http://localhost:8000/docs
```

## Troubleshooting Cepat

| Problem | Solution |
|---------|----------|
| Port 8000 sudah dipakai | `docker-compose down` atau ubah port di `docker-compose.yml` |
| Chrome error | `docker-compose build --no-cache` |
| Connection refused | `docker-compose ps` - pastikan status `Up` |
| Permission denied | `sudo docker-compose up -d` |

## Next Steps

- Baca `DOCKER_SETUP.md` untuk konfigurasi lebih detail
- Setup Nginx reverse proxy untuk domain
- Setup SSL dengan Certbot
- Monitor dengan `docker stats`
