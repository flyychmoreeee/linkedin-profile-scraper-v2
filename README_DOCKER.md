# LinkedIn Scraper - Docker & VPS Deployment Guide

## 🎯 Overview

Setup Docker lengkap untuk LinkedIn Scraper yang siap di-deploy ke VPS Ubuntu 24.04 LTS.

**Status**: ✅ Production Ready

## 📦 What's Included

### Docker Setup
- ✅ Dockerfile optimized untuk Ubuntu 24.04
- ✅ Docker Compose configuration
- ✅ Chromium + ChromeDriver built-in
- ✅ Health checks
- ✅ Resource limits

### Documentation
- ✅ Quick start guide (5 menit)
- ✅ Detailed deployment guide
- ✅ Ubuntu 24.04 specific guide
- ✅ Deployment checklist
- ✅ Troubleshooting guide

### Helper Scripts & Configs
- ✅ `deploy.sh` - Deployment helper
- ✅ `nginx.conf` - Reverse proxy config
- ✅ `linkedin-scraper.service` - Systemd service
- ✅ `.env.example` - Environment template

### Code Optimizations
- ✅ `--headless=new` mode untuk Chrome 120+
- ✅ Linux-specific user-agent
- ✅ Docker-optimized Chrome options
- ✅ Performance tuning

## 🚀 Quick Start (5 Minutes)

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env dan isi LINKEDIN_LI_AT dengan cookie Anda
```

### 2. Build & Run
```bash
docker-compose build
docker-compose up -d
```

### 3. Test
```bash
# Buka di browser: http://localhost:8000/docs
# Atau test dengan curl:
curl "http://localhost:8000/profile?vanity_name=naufal-arga-a5b22b2aa"
```

## 🌐 Deploy ke VPS (Ubuntu 24.04 LTS)

### Step 1: Persiapan VPS (5 menit)
```bash
# SSH ke VPS
ssh user@your-vps-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Deploy Project (5 menit)
```bash
# Clone project
cd /opt
git clone <your-repo-url> linkedin-scraper
cd linkedin-scraper

# Setup environment
cp .env.example .env
nano .env  # Edit LINKEDIN_LI_AT

# Build & Run
docker-compose build
docker-compose up -d

# Verify
curl http://localhost:8000/docs
```

### Step 3: Setup Nginx + SSL (5 menit)
```bash
# Copy Nginx config
sudo cp nginx.conf /etc/nginx/sites-available/linkedin-scraper

# Edit domain
sudo nano /etc/nginx/sites-available/linkedin-scraper
# Ganti "your-domain.com" dengan domain Anda

# Enable
sudo ln -s /etc/nginx/sites-available/linkedin-scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| `DOCKER_QUICKSTART.md` | 5-minute quick start |
| `DOCKER_SETUP.md` | Detailed Docker documentation |
| `UBUNTU_24_04_DEPLOYMENT.md` | Ubuntu 24.04 specific guide |
| `DEPLOYMENT_SUMMARY.md` | Summary & status |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist |

## 🛠️ Useful Commands

```bash
# Build image
docker-compose build --no-cache

# Start container
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Resource usage
docker stats

# Stop container
docker-compose down

# Execute command
docker-compose exec linkedin-scraper bash

# Restart
docker-compose restart
```

## 📋 File Structure

```
linkedin-scraper/
├── Dockerfile                      # Docker image
├── docker-compose.yml              # Container config
├── .dockerignore                   # Build exclusions
├── .env.example                    # Env template
├── requirements.txt                # Python deps
├── main.py                         # FastAPI app
├── linkedin_scraper_v2.py          # Scraper (optimized)
├── deploy.sh                       # Helper script
├── nginx.conf                      # Nginx config
├── linkedin-scraper.service        # Systemd service
├── README_DOCKER.md                # This file
├── DOCKER_QUICKSTART.md            # Quick start
├── DOCKER_SETUP.md                 # Detailed guide
├── UBUNTU_24_04_DEPLOYMENT.md      # Ubuntu guide
├── DEPLOYMENT_SUMMARY.md           # Summary
└── DEPLOYMENT_CHECKLIST.md         # Checklist
```

## 🔧 Docker Image Details

- **Base Image**: Python 3.11-slim (Debian)
- **Browser**: Chromium 142.0.7444.175
- **WebDriver**: ChromeDriver (compatible)
- **Size**: ~1.1GB
- **Python Packages**: FastAPI, Selenium, python-dotenv, google-generativeai

## 💻 System Requirements

### Minimum (Development)
- CPU: 1 core
- Memory: 1GB
- Disk: 5GB

### Recommended (Production)
- CPU: 2 cores
- Memory: 2GB
- Disk: 10GB

## 🔐 Security

- Never commit `.env` file
- Use strong li_at cookie
- Rotate cookie periodically
- Setup firewall on VPS
- Use HTTPS with SSL certificate
- Keep Docker updated

## 🐛 Troubleshooting

### Chrome not found
```bash
docker-compose build --no-cache
```

### Port 8000 already in use
```bash
# Change port in docker-compose.yml
# ports:
#   - "8001:8000"
```

### Permission denied
```bash
sudo usermod -aG docker $USER
# Logout dan login kembali
```

### Out of memory
```bash
# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📊 Monitoring

```bash
# Container status
docker-compose ps

# View logs
docker-compose logs -f --tail=100

# Resource usage
docker stats linkedin-scraper

# Health check
curl http://localhost:8000/docs
```

## 🔄 Maintenance

### Update Dependencies
```bash
nano requirements.txt
docker-compose build --no-cache
docker-compose up -d
```

### Backup
```bash
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup
```

### Clean Up
```bash
docker system prune -a
docker-compose down -v
```

## 📈 Performance Tips

1. **Increase resources** in docker-compose.yml if needed
2. **Monitor logs** regularly for errors
3. **Update** dependencies quarterly
4. **Backup** configuration regularly
5. **Test** endpoints periodically

## ✨ Next Steps

- [ ] Read DOCKER_QUICKSTART.md for 5-minute setup
- [ ] Follow DEPLOYMENT_CHECKLIST.md for VPS deployment
- [ ] Setup monitoring (optional)
- [ ] Setup CI/CD (optional)
- [ ] Setup automated backups (optional)

## 🆘 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs -f`
2. **Verify connectivity**: `curl http://localhost:8000/docs`
3. **Check resources**: `free -h`, `df -h`, `docker stats`
4. **Rebuild**: `docker-compose down -v && docker-compose build --no-cache && docker-compose up -d`

## 📝 Notes

- Build time: ~5-10 minutes (first time)
- Startup time: ~10-15 seconds
- Memory usage: ~500MB-1GB per container
- Image size: ~1.1GB

## 🎉 Ready to Deploy!

Your LinkedIn Scraper is now ready for production deployment on Ubuntu 24.04 LTS VPS.

**Next**: Follow `DEPLOYMENT_CHECKLIST.md` for step-by-step deployment instructions.

---

**Last Updated**: 2025-11-30
**Status**: ✅ Production Ready
**Tested On**: Docker Desktop + Ubuntu 24.04 LTS
