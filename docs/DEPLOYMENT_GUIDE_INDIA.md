# Deployment Guide - Commercial Web Servers in India

## 🇮🇳 Best Options for India (Cheapest to Most Expensive)

### 1. **Railway.app** ⭐ RECOMMENDED for India
**Cost:** FREE tier available, Paid from $5/month (~₹415/month)

**Why Best for India:**
- ✅ Free tier with 500 hours/month
- ✅ Global CDN (fast in India)
- ✅ Easy deployment (GitHub integration)
- ✅ Automatic HTTPS
- ✅ No credit card for free tier
- ✅ Great for Flask apps

**Deployment Steps:**

1. **Create Account**
   - Visit: https://railway.app
   - Sign up with GitHub

2. **Prepare Your Code**
   ```bash
   cd c:\TGDemo\webapp
   
   # Create Procfile
   echo "web: python app.py" > Procfile
   
   # Create runtime.txt
   echo "python-3.11" > runtime.txt
   ```

3. **Create requirements.txt** (already exists)
   ```
   flask>=3.0.0
   flask-cors>=4.0.0
   flask-socketio>=5.3.0
   python-socketio>=5.10.0
   opencv-python-headless>=4.8.0  # Use headless for server
   deepface>=0.0.79
   tf-keras>=2.15.0
   tensorflow>=2.15.0
   numpy>=1.24.0
   pillow>=10.0.0
   gunicorn>=21.2.0  # Production server
   ```

4. **Update app.py for Production**
   ```python
   # At the end of app.py, change:
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       socketio.run(app, host='0.0.0.0', port=port)
   ```

5. **Deploy**
   - Push code to GitHub
   - In Railway: "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Flask and deploys

6. **Get Your URL**
   - Railway provides: `https://your-app.railway.app`
   - Update Android app SERVER_URL to this

**Pricing:**
- Free: 500 hours/month, 512MB RAM
- Paid: $5/month (~₹415) for unlimited

---

### 2. **Render.com**
**Cost:** FREE tier, Paid from $7/month (~₹580/month)

**Why Good for India:**
- ✅ Free tier (spins down after inactivity)
- ✅ Easy deployment
- ✅ Automatic HTTPS
- ✅ Good performance in Asia

**Deployment Steps:**

1. **Create Account**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --worker-class eventlet -w 1 app:app`
     - **Environment:** Python 3

3. **Add Environment Variables**
   - `PYTHON_VERSION`: 3.11

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes

**Pricing:**
- Free: Spins down after 15 min inactivity
- Paid: $7/month (~₹580) for always-on

---

### 3. **PythonAnywhere**
**Cost:** FREE tier, Paid from $5/month (~₹415/month)

**Why Good for India:**
- ✅ Python-specific hosting
- ✅ Easy setup (no Docker/Git required)
- ✅ Web-based file editor
- ✅ Good for beginners

**Deployment Steps:**

1. **Create Account**
   - Visit: https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Go to "Files" tab
   - Upload your `webapp` folder
   - Or use Git: `git clone https://github.com/your-repo.git`

3. **Create Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Set source code path: `/home/yourusername/webapp`
   - Set WSGI file to point to `app.py`

5. **Reload**
   - Click "Reload" button
   - Access at: `https://yourusername.pythonanywhere.com`

**Pricing:**
- Free: 1 web app, limited CPU
- Paid: $5/month (~₹415) for custom domain

---

### 4. **Heroku** (Now Paid Only)
**Cost:** $5-7/month (~₹415-580/month)

**Why Still Popular:**
- ✅ Mature platform
- ✅ Good documentation
- ✅ Many add-ons

**Deployment Steps:**

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd c:\TGDemo\webapp
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

**Pricing:**
- Eco: $5/month (~₹415)
- Basic: $7/month (~₹580)

---

### 5. **Indian Hosting Providers**

#### A. **DigitalOcean Bangalore** ⭐ Best for India
**Cost:** $4/month (~₹330/month) for basic droplet

**Why Best for Indian Traffic:**
- ✅ Bangalore datacenter (lowest latency)
- ✅ Full control (VPS)
- ✅ Scalable
- ✅ Good support

**Deployment Steps:**

1. **Create Droplet**
   - Visit: https://www.digitalocean.com
   - Choose: Ubuntu 22.04, Bangalore region
   - Size: Basic $4/month

2. **SSH into Server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Dependencies**
   ```bash
   apt update
   apt install python3-pip python3-venv nginx
   ```

4. **Upload Code**
   ```bash
   # On your PC:
   scp -r webapp root@your-server-ip:/var/www/
   ```

5. **Setup Application**
   ```bash
   cd /var/www/webapp
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Create Systemd Service**
   ```bash
   nano /etc/systemd/system/facerecognition.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Face Recognition Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/webapp
   Environment="PATH=/var/www/webapp/venv/bin"
   ExecStart=/var/www/webapp/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   systemctl start facerecognition
   systemctl enable facerecognition
   ```

8. **Configure Nginx**
   ```bash
   nano /etc/nginx/sites-available/facerecognition
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. **Enable Site**
   ```bash
   ln -s /etc/nginx/sites-available/facerecognition /etc/nginx/sites-enabled/
   systemctl restart nginx
   ```

**Pricing:**
- Basic: $4/month (~₹330)
- Standard: $12/month (~₹1000)

#### B. **AWS Mumbai (Amazon EC2)**
**Cost:** Free tier 1 year, then ~$10/month (~₹830/month)

**Why Consider:**
- ✅ Mumbai datacenter
- ✅ Free tier (12 months)
- ✅ Enterprise-grade
- ✅ Many services

**Pricing:**
- Free: t2.micro for 12 months
- Paid: ~$10/month (~₹830)

---

## 📊 Cost Comparison (India)

| Provider | Free Tier | Paid (Monthly) | INR | Best For |
|----------|-----------|----------------|-----|----------|
| **Railway** ⭐ | ✅ 500 hrs | $5 | ₹415 | Easiest deployment |
| **Render** | ✅ Limited | $7 | ₹580 | Auto-scaling |
| **PythonAnywhere** | ✅ 1 app | $5 | ₹415 | Beginners |
| **Heroku** | ❌ | $5-7 | ₹415-580 | Mature platform |
| **DigitalOcean BLR** ⭐ | ❌ | $4 | ₹330 | **Cheapest, India** |
| **AWS Mumbai** | ✅ 12 mo | $10 | ₹830 | Enterprise |

---

## 🎯 My Recommendation for India

### **For Beginners: Railway.app**
- Free tier to start
- Easy deployment
- No server management
- Good performance globally

### **For Production: DigitalOcean Bangalore**
- Lowest latency in India
- Cheapest ($4/month = ₹330)
- Full control
- Scalable

### **Quick Start: PythonAnywhere**
- Easiest setup
- No command line needed
- Free tier available

---

## 🚀 Quick Deployment (Railway - Recommended)

### Step-by-Step:

1. **Prepare Code**
   ```bash
   cd c:\TGDemo\webapp
   
   # Create Procfile
   echo web: gunicorn --worker-class eventlet -w 1 app:app > Procfile
   
   # Update requirements.txt (add gunicorn)
   echo gunicorn==21.2.0 >> requirements.txt
   echo eventlet==0.33.3 >> requirements.txt
   ```

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Railway"
   git remote add origin https://github.com/yourusername/face-recognition.git
   git push -u origin main
   ```

3. **Deploy on Railway**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Wait 3-5 minutes
   - Get URL: `https://your-app.railway.app`

4. **Update Android App**
   ```kotlin
   // In MainActivity.kt
   private val SERVER_URL = "https://your-app.railway.app"
   ```

5. **Test**
   - Open URL in browser
   - Test face recognition
   - Install Android app

---

## 🔒 Production Checklist

Before deploying:

- [ ] Change Flask secret key
- [ ] Enable HTTPS (automatic on Railway/Render)
- [ ] Set environment variables
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Add error logging
- [ ] Test on mobile devices
- [ ] Optimize images/assets

---

## 💰 Cost Optimization Tips

1. **Use Free Tiers**
   - Railway: 500 hours/month free
   - Render: Free with sleep
   - AWS: 12 months free

2. **Optimize Resources**
   - Use `opencv-python-headless` (smaller)
   - Enable caching
   - Compress images
   - Use CDN for static files

3. **Monitor Usage**
   - Set up alerts
   - Track bandwidth
   - Monitor CPU usage

4. **Scale Gradually**
   - Start with free tier
   - Upgrade when needed
   - Use auto-scaling

---

## 📱 Update Android App for Production

```kotlin
// MainActivity.kt
class MainActivity : AppCompatActivity() {
    
    // Production URL
    private val SERVER_URL = "https://your-app.railway.app"
    
    // Or use BuildConfig for different environments
    private val SERVER_URL = if (BuildConfig.DEBUG) {
        "http://10.0.2.2:5000"  // Development
    } else {
        "https://your-app.railway.app"  // Production
    }
}
```

---

## 🆘 Troubleshooting

### App not loading
- Check server logs
- Verify URL is correct
- Check CORS settings
- Test in browser first

### Slow performance
- Use DigitalOcean Bangalore for India
- Enable caching
- Optimize model (use Facenet)
- Reduce image size

### High costs
- Use free tiers
- Optimize resource usage
- Set spending limits
- Monitor usage

---

## 📞 Support

For deployment issues:
- Railway: https://railway.app/help
- Render: https://render.com/docs
- DigitalOcean: https://www.digitalocean.com/community

---

## ✅ Summary

**Best Choice for India:**

1. **Free/Testing**: Railway.app (₹0)
2. **Production**: DigitalOcean Bangalore (₹330/month)
3. **Easiest**: PythonAnywhere (₹415/month)

**Recommended Path:**
1. Start with Railway free tier
2. Test and validate
3. Move to DigitalOcean Bangalore for production
4. Scale as needed

Total cost: **₹0-330/month** for most use cases! 🎉
