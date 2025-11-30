# LinkedIn Scraper - Quick Reference Card

## 🚀 Start Here

```bash
# 1. Setup environment
cp .env.example .env
nano .env  # Edit LINKEDIN_LI_AT

# 2. Build & Run
docker-compose build
docker-compose up -d

# 3. Test
curl http://localhost:8000/docs
```

## 📋 Essential Commands

### Build & Run
```bash
docker-compose build              # Build image
docker-compose up -d              # Start container
docker-compose down               # Stop container
docker-compose restart            # Restart container
```

### Monitoring
```bash
docker-compose ps                 # Check status
docker-compose logs -f            # View logs
docker stats                      # Resource usage
curl http://localhost:8000/docs   # Health check
```

### Maintenance
```bash
docker-compose build --no-cache   # Force rebuild
docker system prune -a            # Clean up
docker-compose exec bash          # Shell access
```

## 🌐 VPS Deployment (Ubuntu 24.04)

### 1. Install Docker (5 min)
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Deploy Project (5 min)
```bash
cd /opt
git clone <repo-url> linkedin-scraper
cd linkedin-scraper
cp .env.example .env
nano .env  # Edit LINKEDIN_LI_AT
docker-compose build
docker-compose up -d
```

### 3. Setup Nginx + SSL (5 min)
```bash
sudo cp nginx.conf /etc/nginx/sites-available/linkedin-scraper
sudo nano /etc/nginx/sites-available/linkedin-scraper  # Edit domain
sudo ln -s /etc/nginx/sites-available/linkedin-scraper /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | `docker-compose build --no-cache` |
| Port in use | Change port in `docker-compose.yml` |
| Chrome error | Rebuild image |
| Permission denied | `sudo usermod -aG docker $USER` |
| Out of memory | Increase swap or upgrade VPS |

## 📚 Documentation Map

| Need | File |
|------|------|
| 5-min setup | `DOCKER_QUICKSTART.md` |
| Full Docker guide | `DOCKER_SETUP.md` |
| Ubuntu 24.04 guide | `UBUNTU_24_04_DEPLOYMENT.md` |
| Step-by-step checklist | `DEPLOYMENT_CHECKLIST.md` |
| Overview & status | `DEPLOYMENT_SUMMARY.md` |
| This quick ref | `QUICK_REFERENCE.md` |

## 🎯 Common Tasks

### View Logs
```bash
docker-compose logs -f              # Real-time
docker-compose logs --tail=100      # Last 100 lines
docker-compose logs linkedin-scraper # Specific service
```

### Update Dependencies
```bash
nano requirements.txt
docker-compose build --no-cache
docker-compose up -d
```

### Backup Configuration
```bash
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup
```

### Execute Command in Container
```bash
docker-compose exec linkedin-scraper bash
docker-compose exec linkedin-scraper python -c "import sys; print(sys.version)"
```

### Check Resource Usage
```bash
docker stats linkedin-scraper
free -h
df -h
```

## 🔐 Security Checklist

- [ ] `.env` file not committed to git
- [ ] Strong li_at cookie
- [ ] Firewall enabled on VPS
- [ ] SSL certificate installed
- [ ] Regular backups
- [ ] Update system regularly

## 📊 Resource Limits

Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

## 🆘 Emergency Commands

```bash
# Stop everything
docker-compose down -v

# Force rebuild
docker-compose build --no-cache

# Full restart
docker-compose up -d

# Check health
docker-compose ps
curl http://localhost:8000/docs
```

## 📞 Getting Help

1. Check logs: `docker-compose logs -f`
2. Read docs: See Documentation Map above
3. Verify setup: `docker-compose ps`
4. Test API: `curl http://localhost:8000/docs`

## ✅ Success Indicators

- [ ] `docker-compose ps` shows "Up"
- [ ] `curl http://localhost:8000/docs` returns 200
- [ ] No errors in logs
- [ ] API responds to requests
- [ ] Resource usage reasonable

## 🚀 Next Steps

1. Read `DOCKER_QUICKSTART.md` (5 min)
2. Follow `DEPLOYMENT_CHECKLIST.md` (VPS)
3. Setup monitoring (optional)
4. Setup backups (optional)

---

**Quick Links**
- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Ubuntu 24.04: https://ubuntu.com/
- Nginx: https://nginx.org/
- Let's Encrypt: https://letsencrypt.org/

**Last Updated**: 2025-11-30
