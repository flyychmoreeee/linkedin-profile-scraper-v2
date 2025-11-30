# Docker Setup untuk LinkedIn Scraper

## Prasyarat

- Docker dan Docker Compose sudah terinstall
- File `.env` dengan `LINKEDIN_LI_AT` sudah dikonfigurasi

## Struktur File

```
.
├── Dockerfile              # Konfigurasi Docker image
├── docker-compose.yml      # Konfigurasi container orchestration
├── .dockerignore           # File yang diabaikan saat build
├── requirements.txt        # Python dependencies
├── main.py                 # FastAPI application
├── linkedin_scraper_v2.py  # LinkedIn scraper logic
└── .env                    # Environment variables (jangan di-commit)
```

## Cara Menjalankan

### 1. Build dan Run dengan Docker Compose (Recommended)

```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# Lihat logs
docker-compose logs -f linkedin-scraper

# Stop container
docker-compose down
```

### 2. Build dan Run Manual dengan Docker

```bash
# Build image
docker build -t linkedin-scraper:latest .

# Run container
docker run -d \
  --name linkedin-scraper \
  -p 8000:8000 \
  --env-file .env \
  linkedin-scraper:latest

# Lihat logs
docker logs -f linkedin-scraper

# Stop container
docker stop linkedin-scraper
docker rm linkedin-scraper
```

## Testing API

### Akses Swagger UI
```
http://localhost:8000/docs
```

### Test dengan curl
```bash
curl "http://localhost:8000/profile?vanity_name=naufal-arga-a5b22b2aa"
```

### Test dengan Python
```python
import requests

response = requests.get(
    "http://localhost:8000/profile",
    params={"vanity_name": "naufal-arga-a5b22b2aa"}
)
print(response.json())
```

## Konfigurasi Environment

Pastikan file `.env` berisi:

```env
LINKEDIN_LI_AT=your_li_at_cookie_here
```

## Troubleshooting

### 1. Chrome tidak ditemukan
```
Error: chrome not found
```
**Solusi:** Pastikan Dockerfile sudah install Chrome. Rebuild image:
```bash
docker-compose build --no-cache
```

### 2. ChromeDriver error
```
Error: chromedriver not found
```
**Solusi:** Dockerfile sudah include ChromeDriver installation. Rebuild:
```bash
docker-compose build --no-cache
```

### 3. Connection refused
```
Error: Connection refused at localhost:8000
```
**Solusi:** Pastikan container sudah running:
```bash
docker-compose ps
docker-compose logs linkedin-scraper
```

### 4. Permission denied
```
Error: Permission denied
```
**Solusi:** Jalankan dengan sudo atau tambahkan user ke docker group:
```bash
sudo usermod -aG docker $USER
```

## Deployment ke VPS

**Untuk deployment lengkap di Ubuntu 24.04 LTS, lihat: `UBUNTU_24_04_DEPLOYMENT.md`**

### Quick Deploy (5 menit)

```bash
# 1. SSH ke VPS
ssh user@your-vps-ip

# 2. Clone project
cd /opt
git clone <repository-url> linkedin-scraper
cd linkedin-scraper

# 3. Setup environment
cp .env.example .env
nano .env  # Edit LINKEDIN_LI_AT

# 4. Build & Run
docker-compose build
docker-compose up -d

# 5. Verify
curl http://localhost:8000/docs
```

### Menggunakan Deploy Script

```bash
# Make script executable
chmod +x deploy.sh

# Build image
./deploy.sh build

# Start container
./deploy.sh start

# View logs
./deploy.sh logs

# Check status
./deploy.sh status
```

### Setup Nginx Reverse Proxy

```bash
# Copy config
sudo cp nginx.conf /etc/nginx/sites-available/linkedin-scraper

# Edit domain
sudo nano /etc/nginx/sites-available/linkedin-scraper
# Ganti "your-domain.com" dengan domain Anda

# Enable
sudo ln -s /etc/nginx/sites-available/linkedin-scraper /etc/nginx/sites-enabled/

# Test & reload
sudo nginx -t
sudo systemctl reload nginx
```

### Setup SSL dengan Certbot

```bash
# Install
sudo apt-get install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Setup Auto-Start dengan Systemd

```bash
# Copy service file
sudo cp linkedin-scraper.service /etc/systemd/system/

# Edit path jika berbeda
sudo nano /etc/systemd/system/linkedin-scraper.service

# Enable & start
sudo systemctl daemon-reload
sudo systemctl enable linkedin-scraper
sudo systemctl start linkedin-scraper

# Check status
sudo systemctl status linkedin-scraper
```

## Resource Management

Container sudah dikonfigurasi dengan resource limits:
- CPU: max 2 cores, reserved 1 core
- Memory: max 2GB, reserved 1GB

Edit `docker-compose.yml` untuk menyesuaikan:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

## Monitoring

### Lihat resource usage
```bash
docker stats linkedin-scraper
```

### Lihat logs real-time
```bash
docker-compose logs -f --tail=100
```

### Health check
```bash
docker-compose ps
# STATUS: Up X seconds (healthy)
```

## Maintenance

### Update dependencies
```bash
# Edit requirements.txt
nano requirements.txt

# Rebuild image
docker-compose build --no-cache

# Restart container
docker-compose up -d
```

### Backup data
```bash
docker-compose exec linkedin-scraper tar czf /app/backup.tar.gz /app/logs
docker cp linkedin-scraper:/app/backup.tar.gz ./backup.tar.gz
```

### Clean up
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune -a
```

## Tips & Best Practices

1. **Selalu gunakan `.env` untuk secrets** - jangan hardcode credentials
2. **Gunakan Docker Compose** - lebih mudah untuk management
3. **Setup health checks** - sudah included di Dockerfile
4. **Monitor logs** - gunakan `docker-compose logs` untuk debugging
5. **Backup regularly** - jika ada data penting
6. **Update images** - rebuild secara berkala untuk security patches

## Support

Jika ada error, cek:
1. Docker logs: `docker-compose logs`
2. Container status: `docker-compose ps`
3. Network: `docker network ls`
4. Resources: `docker stats`
