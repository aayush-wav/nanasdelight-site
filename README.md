# Nana's Delight E-commerce Site

A premium, artisan e-commerce website for "Nana's Delight" chocolates and bakery, handcrafted in Patan Dhoka, Nepal.

## Features
- **Luxury UI/UX**: Parallax scroll, smooth transitions, and organic "paper-like" design.
- **Full Shop Flow**: Product catalog, detail pages, shopping cart, and secure checkout.
- **Admin Panel**: Role-based staff access to manage orders, products, and sales.
- **Payment Simulation**: Integration ready for eSewa, Khalti, and COD.
- **Responsive Design**: Mobile-first approach for chocolate lovers on the go.

## Tech Stack
- **Backend**: Python / Flask
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, GSAP
- **Animations**: GSAP (GreenSock)

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```
   The site will be available at `http://127.0.0.1:5000`.

3. **Admin Access**:
   - URL: `http://127.0.0.1:5000/admin`
   - Access Code: `nanas123` (Change this in `app.py`)

## Directory Structure
- `/static`: CSS, JS, and Images (Product photos provided by user).
- `/templates`: HTML templates using Jinja2 inheritance.
- `/models`: Database schema and models.
- `app.py`: Main logic and routing.

## Brand Identity
- **Colors**: Cream (#F5ECD7), Dark Chocolate (#1D0D07), Gold (#C9A84C), Terracotta (#D87D4A).
- **Fonts**: Playfair Display (Luxury Serif), Montserrat (Clean Sans-serif), Sacramento (Handwritten).

---
*Handcrafted in Nepal, Made with Love.*
