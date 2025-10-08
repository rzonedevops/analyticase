# ZA Judiciary Integration - Deployment Guide

This guide provides comprehensive instructions for deploying the ZA Judiciary Integration system in production environments.

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04+ / CentOS 8+ / Red Hat 8+
- **Python**: 3.11 or higher
- **Database**: PostgreSQL 13+ (or Supabase)
- **Memory**: Minimum 2GB RAM, Recommended 4GB+
- **Storage**: Minimum 10GB free space
- **Network**: HTTPS/SSL certificate for production

### External Dependencies
- **Court Online API**: Official credentials from Office of the Chief Justice
- **CaseLines API**: Integration credentials (when available)
- **SMTP Server**: For email notifications (optional)

## Production Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 1. Prepare Environment
```bash
# Clone repository
git clone https://github.com/rzonedevops/analyticase.git
cd analyticase

# Set up environment variables
cp .env.example .env
nano .env  # Configure your settings
```

#### 2. Configure Environment Variables
```bash
# Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
NEON_CONNECTION_STRING=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-production-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars

# Court Online Integration (when available)
COURT_ONLINE_API_URL=https://api.courtonline.org.za
COURT_ONLINE_API_KEY=your_court_online_api_key

# CaseLines Integration (when available)
CASELINES_API_URL=https://api.caselines.org.za
CASELINES_API_KEY=your_caselines_api_key

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=false
```

#### 3. Deploy with Docker Compose
```bash
# Build and start services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs za-judiciary-api
```

#### 4. Initialize Database
```bash
# Run database initialization
docker-compose exec za-judiciary-api python scripts/init_database.py
```

#### 5. Verify Deployment
```bash
# Test health endpoint
curl http://localhost/api/health

# Run comprehensive tests
docker-compose exec za-judiciary-api python /app/run_tests.py
```

### Option 2: Manual Deployment

#### 1. System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-pip python3.11-venv nginx postgresql-client -y

# Create application user
sudo useradd -m -s /bin/bash zaintegration
sudo su - zaintegration
```

#### 2. Application Setup
```bash
# Clone and setup application
git clone https://github.com/rzonedevops/analyticase.git
cd analyticase

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Configure your settings
```

#### 3. Database Initialization
```bash
# Initialize database schema and data
python za_judiciary_integration/scripts/init_database.py
```

#### 4. Service Configuration
Create systemd service file:
```bash
sudo nano /etc/systemd/system/za-judiciary-api.service
```

```ini
[Unit]
Description=ZA Judiciary Integration API
After=network.target

[Service>
Type=simple
User=zaintegration
WorkingDirectory=/home/zaintegration/analyticase/za_judiciary_integration/api
Environment=PATH=/home/zaintegration/analyticase/venv/bin
ExecStart=/home/zaintegration/analyticase/venv/bin/python main_za_enhanced.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### 5. Start Services
```bash
# Enable and start service
sudo systemctl enable za-judiciary-api
sudo systemctl start za-judiciary-api

# Check status
sudo systemctl status za-judiciary-api
```

#### 6. Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/za-judiciary-api
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/api/health;
        access_log off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/za-judiciary-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/TLS Configuration

### Using Let's Encrypt (Recommended)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Verify auto-renewal
sudo certbot renew --dry-run
```

## Monitoring and Logging

### Application Logs
```bash
# View application logs
sudo journalctl -u za-judiciary-api -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Monitoring
Set up monitoring for these endpoints:
- `GET /api/health` - Application health
- `GET /api/status` - System status
- `GET /api/za-judiciary/integration-status` - Integration status

### Log Rotation
```bash
sudo nano /etc/logrotate.d/za-judiciary-api
```

```
/var/log/za-judiciary-api/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 zaintegration zaintegration
    postrotate
        systemctl reload za-judiciary-api
    endscript
}
```

## Security Considerations

### 1. Network Security
- Use HTTPS/SSL for all communications
- Implement proper firewall rules
- Use VPN for database connections
- Enable fail2ban for brute force protection

### 2. Application Security
- Use strong, unique secret keys
- Implement rate limiting
- Validate all input data
- Use parameterized database queries
- Regular security updates

### 3. Database Security
- Use SSL connections to database
- Implement proper access controls
- Regular backups with encryption
- Monitor for suspicious activities

### 4. API Security
- Implement JWT authentication
- Use API key rotation
- Monitor API usage patterns
- Implement proper CORS policies

## Backup and Recovery

### Database Backup
```bash
# Create backup script
cat > /home/zaintegration/backup_db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $NEON_CONNECTION_STRING > /home/zaintegration/backups/za_judiciary_$DATE.sql
find /home/zaintegration/backups -name "za_judiciary_*.sql" -mtime +7 -delete
EOF

chmod +x /home/zaintegration/backup_db.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /home/zaintegration/backup_db.sh
```

### Application Backup
```bash
# Backup application and configuration
tar -czf za_judiciary_backup_$(date +%Y%m%d).tar.gz \
    /home/zaintegration/analyticase \
    /etc/systemd/system/za-judiciary-api.service \
    /etc/nginx/sites-available/za-judiciary-api
```

## Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check service status
sudo systemctl status za-judiciary-api

# Check logs
sudo journalctl -u za-judiciary-api -n 50

# Verify environment variables
sudo systemctl show za-judiciary-api -p Environment
```

#### 2. Database Connection Issues
```bash
# Test database connection
python -c "
import os
import psycopg2
conn = psycopg2.connect(os.getenv('NEON_CONNECTION_STRING'))
print('Database connection successful')
conn.close()
"
```

#### 3. API Not Responding
```bash
# Check if port is listening
sudo netstat -tlnp | grep :5000

# Test local connection
curl http://localhost:5000/api/health

# Check nginx configuration
sudo nginx -t
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head

# Restart services if needed
sudo systemctl restart za-judiciary-api
```

### Performance Tuning

#### Database Optimization
- Enable connection pooling
- Optimize query performance
- Regular VACUUM and ANALYZE
- Monitor slow queries

#### Application Optimization
- Use production WSGI server (Gunicorn)
- Enable caching where appropriate
- Optimize JSON responses
- Monitor response times

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Database read replicas
- Container orchestration (Kubernetes)
- Microservices architecture

### Vertical Scaling
- Increase server resources
- Optimize database configuration
- Use faster storage (SSD)
- Increase connection limits

## Compliance and Legal

### Data Protection
- Implement POPIA compliance measures
- Regular security audits
- Data encryption at rest and in transit
- Proper access logging

### Legal Requirements
- Electronic Filing Act compliance
- Court Rules adherence
- Audit trail maintenance
- Document retention policies

## Support and Maintenance

### Regular Maintenance Tasks
- Security updates (monthly)
- Database maintenance (weekly)
- Log review (daily)
- Backup verification (weekly)

### Emergency Procedures
- Service restart procedures
- Database recovery steps
- Emergency contact information
- Escalation procedures

For additional support, please contact the development team or refer to the documentation in the `docs/` directory.