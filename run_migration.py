from app import app, get_db, CATEGORY_NAMES, init_db
from bs4 import BeautifulSoup
import os
import sqlite3

def migrate():
    if not os.path.exists('naturita.db'):
        init_db()
        
    with app.app_context():
        db = get_db()
        base_path = os.path.join('static', 'templates', 'catalogo')
        
        count = 0
        for category_slug in CATEGORY_NAMES.keys():
            file_path = os.path.join(base_path, f'{category_slug}.html')
            if not os.path.exists(file_path):
                print(f"Skipping {category_slug}, file not found.")
                continue
                
            print(f"Processing {category_slug}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            cards = soup.find_all('div', class_='card')
            for card in cards:
                name = card.find('h3').text.strip() if card.find('h3') else "Sin nombre"
                description = card.find('p').text.strip() if card.find('p') else ""
                img_tag = card.find('img')
                image_url = img_tag['src'] if img_tag else ""
                
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
        print(f"Migration complete. {count} products added.")

if __name__ == '__main__':
    migrate()
