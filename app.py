from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from models.database import db, Product, Order, OrderItem

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nanas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database and seed products if empty
with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        initial_products = [
            Product(name="Himalayan Timmur & Pink Salt", category="Dark Chocolate", price=450, image="product 1.jpeg", is_featured=True, description="Premium dark chocolate infused with hand-picked Himalayan Timur (Sichuan Pepper) and Pink Himalayan Salt for a unique, tingly sensation."),
            Product(name="Mustang Apple & Roasted Pistachios", category="Premium", price=550, image="product 10.jpeg", is_featured=True, description="A luxury blend featuring dehydrated apples from the orchards of Mustang, paired with crunchy roasted pistachios."),
            Product(name="Semi-Sweet Dark with Orange Peel", category="Dark Chocolate", price=450, image="product 8.jpeg", is_featured=True, description="Traditional semi-sweet dark chocolate with zesty, sun-dried orange peels from Gorkha."),
            Product(name="Artisan Milk Chocolate", category="Milk Chocolate", price=400, image="product 5.jpeg", description="Smooth, creamy milk chocolate handcrafted with the finest Nepali cacao and organic milk."),
            Product(name="Goji Berry Dark Delight", category="Dark Chocolate", price=500, image="product 2.jpeg", description="Rich dark chocolate with antioxidant-filled Himalayan Goji Berries."),
            Product(name="Artisan Gift Bundle", category="Gift Bundles", price=1200, image="product box.jpeg", description="A beautiful selection of our best-selling artisan chocolate bars, elegantly packaged.")
        ]
        db.session.bulk_save_objects(initial_products)
        db.session.commit()

@app.route('/')
def index():
    featured = Product.query.filter_by(is_featured=True).limit(3).all()
    return render_template('index.html', products=featured)

@app.route('/shop')
def shop():
    category = request.args.get('category')
    if category:
        all_products = Product.query.filter_by(category=category).all()
    else:
        all_products = Product.query.all()
    
    # Get unique categories for the filter links
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('shop.html', products=all_products, categories=categories, active_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    # Fetch 3 related products (from same category if possible, or just random)
    related = Product.query.filter(Product.id != product_id).limit(3).all()
    return render_template('product.html', product=product, related=related)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_order = Order(
                customer_name=data['name'],
                phone=data['phone'],
                address=data['address'],
                city=data['city'],
                delivery_date=data.get('delivery_date'),
                total_amount=float(data['total']),
                payment_method=data['payment'],
                status='Pending'
            )
            db.session.add(new_order)
            db.session.flush() # Get order ID before committing

            for item in data['items']:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_name=item['name'],
                    price=float(item['price']),
                    quantity=1 # Simplified for now
                )
                db.session.add(order_item)
            
            db.session.commit()
            return jsonify({"success": True, "order_id": new_order.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 400

    return render_template('checkout.html')

@app.route('/order-success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('success.html', order=order)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Simple placeholder for contact form processing
        return jsonify({"success": True})
    return render_template('contact.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'nanas123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid Access Code.'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    pending_count = Order.query.filter_by(status='Pending').count()
    customer_count = db.session.query(db.func.count(db.func.distinct(Order.phone))).scalar() or 0
    
    return render_template('admin/dashboard.html', 
                         orders=orders, 
                         total_sales=total_sales,
                         pending_count=pending_count,
                         customer_count=customer_count)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
