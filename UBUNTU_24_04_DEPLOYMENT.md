# Deployment Guide: Ubuntu 24.04 LTS + Docker

Panduan lengkap untuk deploy LinkedIn Scraper di VPS dengan Ubuntu 24.04 LTS.

## Prerequisites

- VPS dengan Ubuntu 24.04 LTS
- Akses SSH ke VPS
- Minimal 2GB RAM, 10GB disk space
- Domain (optional, untuk production)

## Step 1: Persiapan VPS

### 1.1 Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl wget git
```

### 1.2 Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
docker run hello-world

# Add user ke docker group (opsional, agar tidak perlu sudo)
sudo usermod -aG docker $USER
# Logout dan login kembali untuk apply
```

### 1.3 Install Docker Compose

```bash
# Download latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

## Step 2: Clone & Setup Project

### 2.1 Clone Repository
```bash
cd /opt
sudo git clone <your-repo-url> linkedin-scraper
cd linkedin-scraper
sudo chown -R $USER:$USER .
```

### 2.2 Setup Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit dengan text editor favorit
nano .env

# Isi LINKEDIN_LI_AT dengan cookie Anda
# LINKEDIN_LI_AT=your_cookie_here
```

## Step 3: Build & Deploy

### 3.1 Build Docker Image
```bash
# Build image (first time, ~10-15 minutes)
docker-compose build

# Verify build success
docker images | grep linkedin-scraper
```

### 3.2 Run Container
```bash
# Start container
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test API
curl http://localhost:8000/docs
```

### 3.3 Test API Endpoint
```bash
# Test dengan curl
curl "http://localhost:8000/profile?vanity_name=naufal-arga-a5b22b2aa"

# Atau buka di browser
# http://your-vps-ip:8000/docs
```

## Step 4: Setup Reverse Proxy (Nginx)

### 4.1 Install Nginx
```bash
sudo apt-get install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4.2 Configure Nginx
```bash
# Create config file
sudo nano /etc/nginx/sites-available/linkedin-scraper

# Paste config berikut:
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Ganti dengan domain Anda

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 4.3 Enable Config
```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/linkedin-scraper /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Step 5: Setup SSL (Let's Encrypt)

### 5.1 Install Certbot
```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

### 5.2 Generate Certificate
```bash
# Generate SSL certificate
sudo certbot --nginx -d your-domain.com

# Follow prompts:
# - Enter email
# - Accept terms
# - Choose redirect option (2 untuk redirect HTTP ke HTTPS)
```

### 5.3 Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Verify auto-renewal is enabled
sudo systemctl status certbot.timer
```

## Step 6: Monitoring & Maintenance

### 6.1 Check Container Status
```bash
# View all containers
docker-compose ps

# View resource usage
docker stats linkedin-scraper

# View logs
docker-compose logs -f --tail=100
```

### 6.2 Restart Container
```bash
# Restart
docker-compose restart

# Restart specific service
docker-compose restart linkedin-scraper

# Full restart
docker-compose down
docker-compose up -d
```

### 6.3 Update Dependencies
```bash
# Edit requirements.txt
nano requirements.txt

# Rebuild image
docker-compose build --no-cache

# Restart container
docker-compose up -d
```

### 6.4 View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Logs dari specific service
docker-compose logs linkedin-scraper
```

## Step 7: Backup & Recovery

### 7.1 Backup Configuration
```bash
# Backup .env file
cp .env .env.backup

# Backup docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup
```

### 7.2 Backup Data
```bash
# Backup logs (jika ada)
tar czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Upload ke cloud storage
# scp logs-backup-*.tar.gz user@backup-server:/backups/
```

## Troubleshooting

### Problem: Port 8000 sudah dipakai
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# Atau ubah port di docker-compose.yml
# ports:
#   - "8001:8000"
```

### Problem: Chrome/Chromium tidak ditemukan
```bash
# Rebuild image
docker-compose build --no-cache

# Check logs
docker-compose logs
```

### Problem: Permission denied
```bash
# Add user ke docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Atau gunakan sudo
sudo docker-compose up -d
```

### Problem: Out of memory
```bash
# Check memory usage
free -h

# Increase swap (optional)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Problem: Disk space penuh
```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a

# Remove old logs
docker-compose logs --tail=0 > /dev/null
```

## Performance Tuning

### Increase Resource Limits
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 4G
    reservations:
      cpus: '2'
      memory: 2G
```

### Optimize Nginx
Edit `/etc/nginx/nginx.conf`:
```nginx
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
```

## Security Best Practices

### 1. Firewall Configuration
```bash
# Install UFW
sudo apt-get install -y ufw

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### 2. Fail2Ban (Optional)
```bash
# Install
sudo apt-get install -y fail2ban

# Start service
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 3. Environment Variables
```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use strong li_at cookie
# Rotate cookie periodically
```

## Useful Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec linkedin-scraper bash

# Rebuild image
docker-compose build --no-cache

# Remove all containers/images
docker-compose down -v
docker system prune -a

# Check container health
docker-compose ps

# View resource usage
docker stats

# Restart service
docker-compose restart linkedin-scraper
```

## Support & Debugging

Jika ada masalah:

1. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

2. **Verify connectivity:**
   ```bash
   curl http://localhost:8000/docs
   ```

3. **Check system resources:**
   ```bash
   free -h
   df -h
   docker stats
   ```

4. **Rebuild everything:**
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

## Next Steps

- Setup monitoring dengan Prometheus/Grafana (optional)
- Setup CI/CD dengan GitHub Actions (optional)
- Setup automated backups (optional)
- Setup email alerts untuk errors (optional)
