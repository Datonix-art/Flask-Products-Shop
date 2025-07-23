# E-Commerce Web App
Final project for TBC education / Geolab

# Description Of Project
This project is a fully functional e-commerce web application built with Flask. It allows users to browse, search, and purchase products, with features such as:

- User authentication (sign up, login, logout)
- Multilingual support (English & Georgian)
- Product listings with filtering by category, brand, etc.
- Shopping cart and payment system integration (Stripe)
- Admin dashboard to manage users, orders, and products
- Email verification and security measures
- Responsive frontend with templates and static assets
- Docker support for easy deployment

# Getting Started
## Prerequesities
- Python 3.8+ (for local installation)
- Docker and Docker Compose (for Docker installation)
## Installation
## Option 1: Local Installation
1. Clone the repository
```bash
git clone https://github.com/Datonix-art/E-Commerce-Web-App.git
cd E-Commerce-Web-App
```
2. Create environment
```bash
python -m venv venv
```
3. Activate environment
```bash
venv/Scripts/activate
```
4. install dependencies
```
pip install -r requirements.txt
```
## Option 2: Docker Installation
1. Clone the repository
```bash
git clone https://github.com/Datonix-art/E-Commerce-Web-App.git
cd E-Commerce-Web-App
```
2. Build image
```bash
docker build -t Commerce-App .
```
# Environment Variables
This project uses environment variables to manage sensitive data and configuration. Create a ```.env``` file in the project root directory and add the following variables:
## Required Environment Variables
## Flask Configuration
```bash
SECRET_KEY='your_secret_key'
```
**Description** : random string (32+ characters recommended).
## Database configuration
```bash
SQLALCHEMY_DATABASE_URI='database.db'
```
**Description** : database name
## Security & Authentication
```bash
SECURITY_PASSWORD_SALT='your_password_salt'
```
**Description** : Should be unique, random string
## Stripe Payment Integration
```bash
STRIPE_SECRET_KEY='your_stripe_secret_key'
STRIPE_PUBLISHABLE_KEY='your_stripe_publishable_key'
```
**Description** : Stripe API keys for payment processing. Use test keys for development and live keys for production.
#### how to obtain:
1. Create a Stripe account at [stripe.com](https://stripe.com/)
2. Navigate to Dashboard → Developers → API keys
3. Copy your publishable and secret keys 
4. Assing those keys to variables
## reCAPTCHA Configuration
```bash
RECAPTCHA_PUBLIC_KEY='your_recaptcha_site_key'
RECAPTCHA_PRIVATE_KEY='your_recaptcha_secret_key'
```
**Description** : Google reCAPTCHA keys for bot protection
#### how to obtain:
1. Visit [Google reCaptcha Admin Console](https://www.google.com/recaptcha/admin/site/730650979)
2. Register your site
3. Select reCAPTCHA v2
4. add your domain(s)
5. Copy the site Key (public) and secret_key (secret)
6. Assing those keys to variables
## Email Configuration
```bash
MAIL_USERNAME='your_email'
MAIL_PASSWORD='your_app_password'
```
**Description** :  Email credentials for sending verification emails
####  Setup:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. Use the generated app password (not your regular Gmail password)
4. Assing generated password and email to variables
# Usage
# option 1: Run locally
``` bash
python app.py
```
The application will be avaiable at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
# option 2: Run with Docker
``` 
docker run -d -p 5000:5000 Commerce-App 
```
The application will be avaiable at [http://localhost:5000](http://localhost:5000)
# Branding Notice
This project was created as part of the TBC education / Geolab Bootcamp.
The TBC logo and related branding are owned by their respective entities and may not be reused, modified, or redistributed without permission.

Feel free to fork or use the code under the terms of the MIT license — but do not use the TBC logo or project branding in your own versions or hosted apps.

# License

see [MIT License](LICENSE) for details.