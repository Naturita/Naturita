import os
import sqlite3
import json
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='.', static_folder='static')
app.secret_key = 'dev_key_naturita_2025' # Change this in production
DATABASE = 'naturita.db'

CATEGORY_NAMES = {
    'granos_y_semillas': 'Granos y Semillas',
    'frutos_secos': 'Frutos Secos',
    'harina_derivados': 'Harinas y Derivados',
    'snack_cereales': 'Snacks y Cereales',
    'granel': 'Productos a Granel',
    'vegetariano': 'Veganos y Vegetarianos',
    'suplementos': 'Suplementos',
    'organicos': 'Orgánicos',
    'diabetico': 'Diabéticos',
    'celiaco': 'Celíacos',
    'fitness': 'Fitness',
    'endulzante': 'Endulzantes y Naturales',
    'infusiones': 'Infusiones y Hierbas',
    'freezados': 'Freezados'
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        
        # Create default admin if not exists
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                       ('Naturita', generate_password_hash('Lacalera25@')))
            db.commit()
        except sqlite3.IntegrityError:
            pass
        print("Database initialized.")

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/templates/catalogo.html')
def catalogo_index():
    return render_template('static/templates/catalogo.html')

@app.route('/static/templates/catalogo/<category_file>')
def category_page(category_file):
    # This route is for testing the generated pages locally if needed,
    # but normally these are static files.
    return render_template(f'static/templates/catalogo/{category_file}')

@app.route('/imagenes/<path:filename>')
def serve_image(filename):
    return send_from_directory('imagenes', filename)

# --- Admin Routes ---

@app.route('/admin/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('admin_dashboard'))
        
        return render_template('admin/login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

@app.route('/admin')
def admin_dashboard():
    if g.user is None:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    db = get_db()
    
    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    
    if search_query:
        query += ' AND name LIKE ?'
        params.append(f'%{search_query}%')
    
    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)
        
    query += ' ORDER BY category, name'
    
    products = db.execute(query, params).fetchall()
    sales = db.execute('SELECT * FROM sales ORDER BY created_at DESC LIMIT 50').fetchall()
    
    return render_template('admin/dashboard.html', 
                           products=products, 
                           sales=sales, 
                           category_names=CATEGORY_NAMES,
                           current_category=category_filter,
                           current_search=search_query)

@app.route('/admin/add_product', methods=('GET', 'POST'))
def add_product():
    if g.user is None:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity_unit = request.form['quantity_unit']
        extra_info = request.form['extra_info']
        
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join('imagenes', filename))
                # Use relative path compatible with existing structure
                image_url = f'../../../imagenes/{filename}'
        
        # Fallback if no image uploaded (though usually required for new products)
        if not image_url:
             image_url = request.form.get('current_image_url', '')

        db = get_db()
        db.execute(
            'INSERT INTO products (category, name, description, price, quantity_unit, extra_info, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (category, name, description, price, quantity_unit, extra_info, image_url)
        )
        db.commit()
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/product_form.html', action="Agregar", product=None)

@app.route('/admin/edit_product/<int:id>', methods=('GET', 'POST'))
def edit_product(id):
    if g.user is None:
        return redirect(url_for('login'))
    
    db = get_db()
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity_unit = request.form['quantity_unit']
        extra_info = request.form['extra_info']
        
        image_url = request.form.get('current_image_url', '')
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join('imagenes', filename))
                image_url = f'../../../imagenes/{filename}'
        
        db.execute(
            'UPDATE products SET category = ?, name = ?, description = ?, price = ?, quantity_unit = ?, extra_info = ?, image_url = ? WHERE id = ?',
            (category, name, description, price, quantity_unit, extra_info, image_url, id)
        )
        db.commit()
        return redirect(url_for('admin_dashboard'))

    product = db.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    return render_template('admin/product_form.html', product=product, action="Editar")

@app.route('/admin/sync_github')
def sync_github():
    if g.user is None:
        return redirect(url_for('login'))
    
    db = get_db()
    
    # 1. Generate HTML files for each category
    for category_slug, category_name in CATEGORY_NAMES.items():
        products = db.execute('SELECT * FROM products WHERE category = ?', (category_slug,)).fetchall()
        
        # Render template
        html_content = render_template('static/templates/category_base.html', 
                                       category_name=category_name, 
                                       products=products)
        
        # Write to file
        file_path = os.path.join('static', 'templates', 'catalogo', f'{category_slug}.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    # 2. Git commands
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Update products from Admin Panel'], check=True)
        subprocess.run(['git', 'push'], check=True)
        flash_message = "Sincronización completada con éxito."
    except Exception as e:
        flash_message = f"Error al sincronizar: {str(e)}"
        print(flash_message)

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/migrate_data')
def migrate_data():
    # Helper to populate DB from existing HTML files
    if g.user is None:
        return redirect(url_for('login'))
        
    db = get_db()
    base_path = os.path.join('static', 'templates', 'catalogo')
    
    count = 0
    for category_slug in CATEGORY_NAMES.keys():
        file_path = os.path.join(base_path, f'{category_slug}.html')
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        cards = soup.find_all('div', class_='card')
        for card in cards:
            name = card.find('h3').text.strip() if card.find('h3') else "Sin nombre"
            # Remove emoji from name if present (simple heuristic)
            # name = name.encode('ascii', 'ignore').decode('ascii').strip() 
            
            description = card.find('p').text.strip() if card.find('p') else ""
            img_tag = card.find('img')
            image_url = img_tag['src'] if img_tag else ""
            
            # Fix relative paths if needed. In HTML they are like "../../../imagenes/..."
            # We keep them as is because the template uses them.
            
            price = card.get('data-precio', '')
            quantity_unit = card.get('data-cantidad', '')
            extra_info = card.get('data-extra', '')
            
            # Check if exists
            exists = db.execute('SELECT id FROM products WHERE name = ?', (name,)).fetchone()
            if not exists:
                db.execute(
                    'INSERT INTO products (category, name, description, price, quantity_unit, extra_info, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (category_slug, name, description, price, quantity_unit, extra_info, image_url)
                )
                count += 1
    
    db.commit()
    return f"Migración completada. {count} productos agregados."

@app.route('/api/record_sale', methods=['POST'])
def record_sale():
    data = request.get_json()
    total = data.get('total')
    items = json.dumps(data.get('items'))
    customer_info = data.get('customer_info', '')
    
    db = get_db()
    db.execute('INSERT INTO sales (total, items, customer_info) VALUES (?, ?, ?)',
               (total, items, customer_info))
    db.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, port=5000)
