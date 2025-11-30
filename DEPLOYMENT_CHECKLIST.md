# LinkedIn Scraper - Deployment Checklist

## Pre-Deployment (Local)

- [ ] **Environment Setup**
  - [ ] Copy `.env.example` ke `.env`
  - [ ] Isi `LINKEDIN_LI_AT` dengan cookie yang valid
  - [ ] Test cookie di browser (pastikan bisa login)

- [ ] **Docker Build**
  - [ ] Run `docker-compose build --no-cache`
  - [ ] Verify build success (check image size ~1.1GB)
  - [ ] Run `docker images | grep linkedin-scraper`

- [ ] **Local Testing**
  - [ ] Run `docker-compose up -d`
  - [ ] Wait 10-15 seconds untuk startup
  - [ ] Test API: `curl http://localhost:8000/docs`
  - [ ] Test endpoint: `curl "http://localhost:8000/profile?vanity_name=test-profile"`
  - [ ] Check logs: `docker-compose logs -f`
  - [ ] Stop container: `docker-compose down`

- [ ] **Code Review**
  - [ ] Review `linkedin_scraper_v2.py` optimizations
  - [ ] Verify `--headless=new` argument
  - [ ] Check Chrome options untuk Docker
  - [ ] Verify user-agent untuk Linux

## VPS Preparation (Ubuntu 24.04 LTS)

- [ ] **System Setup**
  - [ ] SSH ke VPS
  - [ ] Run `sudo apt-get update && sudo apt-get upgrade -y`
  - [ ] Install curl: `sudo apt-get install -y curl`
  - [ ] Check disk space: `df -h` (minimal 10GB free)
  - [ ] Check memory: `free -h` (minimal 2GB)

- [ ] **Docker Installation**
  - [ ] Install Docker: `curl -fsSL https://get.docker.com | sudo sh`
  - [ ] Verify: `docker --version`
  - [ ] Test: `sudo docker run hello-world`
  - [ ] Add user to docker group: `sudo usermod -aG docker $USER`
  - [ ] Logout dan login kembali

- [ ] **Docker Compose Installation**
  - [ ] Download: `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
  - [ ] Make executable: `sudo chmod +x /usr/local/bin/docker-compose`
  - [ ] Verify: `docker-compose --version`

- [ ] **Project Setup**
  - [ ] Create directory: `mkdir -p /opt/linkedin-scraper`
  - [ ] Clone project: `git clone <repo-url> /opt/linkedin-scraper`
  - [ ] Navigate: `cd /opt/linkedin-scraper`
  - [ ] Copy env: `cp .env.example .env`
  - [ ] Edit env: `nano .env` (set LINKEDIN_LI_AT)
  - [ ] Verify permissions: `ls -la .env`

## Deployment (VPS)

- [ ] **Build Docker Image**
  - [ ] Run: `docker-compose build --no-cache`
  - [ ] Monitor build progress
  - [ ] Verify build success
  - [ ] Check image: `docker images | grep linkedin-scraper`

- [ ] **Start Container**
  - [ ] Run: `docker-compose up -d`
  - [ ] Wait 15-20 seconds
  - [ ] Check status: `docker-compose ps`
  - [ ] View logs: `docker-compose logs -f`
  - [ ] Verify running: `docker ps | grep linkedin-scraper`

- [ ] **Test API**
  - [ ] Test health: `curl http://localhost:8000/docs`
  - [ ] Test endpoint: `curl "http://localhost:8000/profile?vanity_name=test"`
  - [ ] Check response format
  - [ ] Verify no errors in logs

- [ ] **Nginx Setup** (if using domain)
  - [ ] Install Nginx: `sudo apt-get install -y nginx`
  - [ ] Copy config: `sudo cp nginx.conf /etc/nginx/sites-available/linkedin-scraper`
  - [ ] Edit domain: `sudo nano /etc/nginx/sites-available/linkedin-scraper`
  - [ ] Create symlink: `sudo ln -s /etc/nginx/sites-available/linkedin-scraper /etc/nginx/sites-enabled/`
  - [ ] Test config: `sudo nginx -t`
  - [ ] Reload: `sudo systemctl reload nginx`
  - [ ] Test: `curl http://your-domain.com`

- [ ] **SSL Setup** (if using domain)
  - [ ] Install Certbot: `sudo apt-get install -y certbot python3-certbot-nginx`
  - [ ] Generate cert: `sudo certbot --nginx -d your-domain.com`
  - [ ] Follow prompts (accept terms, choose redirect)
  - [ ] Verify: `curl https://your-domain.com`
  - [ ] Check auto-renewal: `sudo systemctl status certbot.timer`

- [ ] **Systemd Service** (optional, for auto-start)
  - [ ] Copy service: `sudo cp linkedin-scraper.service /etc/systemd/system/`
  - [ ] Edit path: `sudo nano /etc/systemd/system/linkedin-scraper.service`
  - [ ] Reload: `sudo systemctl daemon-reload`
  - [ ] Enable: `sudo systemctl enable linkedin-scraper`
  - [ ] Start: `sudo systemctl start linkedin-scraper`
  - [ ] Verify: `sudo systemctl status linkedin-scraper`

## Post-Deployment

- [ ] **Monitoring**
  - [ ] Check container status: `docker-compose ps`
  - [ ] Monitor resource: `docker stats`
  - [ ] View logs: `docker-compose logs -f`
  - [ ] Test health endpoint regularly

- [ ] **Backup**
  - [ ] Backup .env: `cp .env .env.backup`
  - [ ] Backup config: `cp docker-compose.yml docker-compose.yml.backup`
  - [ ] Store backups safely

- [ ] **Security**
  - [ ] Setup firewall: `sudo ufw enable`
  - [ ] Allow SSH: `sudo ufw allow 22/tcp`
  - [ ] Allow HTTP: `sudo ufw allow 80/tcp`
  - [ ] Allow HTTPS: `sudo ufw allow 443/tcp`
  - [ ] Verify: `sudo ufw status`

- [ ] **Documentation**
  - [ ] Document VPS IP/Domain
  - [ ] Document admin credentials
  - [ ] Document backup location
  - [ ] Create runbook untuk common tasks

## Maintenance Schedule

### Daily
- [ ] Check container status: `docker-compose ps`
- [ ] Monitor logs for errors: `docker-compose logs`

### Weekly
- [ ] Check disk space: `df -h`
- [ ] Check memory usage: `free -h`
- [ ] Review error logs
- [ ] Test API endpoints

### Monthly
- [ ] Update system: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] Rebuild image: `docker-compose build --no-cache`
- [ ] Restart container: `docker-compose restart`
- [ ] Backup configuration

### Quarterly
- [ ] Review security settings
- [ ] Update dependencies
- [ ] Performance tuning
- [ ] Disaster recovery test

## Rollback Procedure

If something goes wrong:

```bash
# 1. Stop current container
docker-compose down

# 2. Restore backup
cp .env.backup .env
cp docker-compose.yml.backup docker-compose.yml

# 3. Rebuild
docker-compose build --no-cache

# 4. Restart
docker-compose up -d

# 5. Verify
docker-compose ps
curl http://localhost:8000/docs
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change port in docker-compose.yml |
| Chrome not found | Rebuild: `docker-compose build --no-cache` |
| Permission denied | Add user to docker group |
| Out of memory | Increase swap or upgrade VPS |
| SSL certificate error | Run certbot again: `sudo certbot --nginx -d domain.com` |
| Container won't start | Check logs: `docker-compose logs` |

## Success Criteria

- [ ] Container running: `docker-compose ps` shows "Up"
- [ ] API responding: `curl http://localhost:8000/docs` returns 200
- [ ] Scraper working: Test endpoint returns valid data
- [ ] Logs clean: No errors in `docker-compose logs`
- [ ] Resources healthy: `docker stats` shows reasonable usage
- [ ] SSL working: HTTPS accessible (if using domain)
- [ ] Auto-start working: Container restarts after reboot (if using systemd)

## Sign-Off

- [ ] Deployment completed successfully
- [ ] All tests passed
- [ ] Documentation updated
- [ ] Team notified
- [ ] Monitoring enabled

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Approved By**: _______________
**Notes**: _______________________________________________
