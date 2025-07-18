import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin

def scrape_cart_from_file(html_path):
    """Scrape cart data from a local HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"Error: File {html_path} not found.")
        print("Please save the cart page HTML manually:")
        print("1. Go to https://www.waveshare.com/checkout/cart/")
        print("2. Right-click -> 'Save As' -> Save as 'data.html'")
        print("3. Place the file in the same directory as this script")
        return None
    
    return parse_cart_html(html_content)

def scrape_cart_from_url(url):
    """Scrape cart data directly from URL (may not work due to session requirements)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return parse_cart_html(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        print("Cart pages usually require session cookies. Please use the manual HTML save method.")
        return None

def parse_cart_html(html_content):
    """Parse HTML content and extract cart data"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize lists to store table data
    data = {
        'Product Name': [],
        'SKU': [],
        'Part No.': [],
        'Unit Price': [],
        'Quantity': [],
        'Subtotal': []
    }
    
    # Method 1: Look for cart items in typical e-commerce structures
    cart_items = soup.find_all('tr', class_=['cart-item', 'item-row']) or \
                 soup.find_all('div', class_=['cart-item', 'product-item']) or \
                 soup.find_all('li', class_=['cart-item', 'product-item'])
    
    if not cart_items:
        # Method 2: Look for table rows in cart tables
        cart_table = soup.find('table', class_=['cart', 'shopping-cart', 'data-table'])
        if cart_table:
            cart_items = cart_table.find_all('tr')[1:]  # Skip header row
    
    if not cart_items:
        # Method 3: Your original approach - look for SKU divs
        cart_items = soup.find_all('div', string=lambda t: t and 'SKU:' in t)
    
    print(f"Found {len(cart_items)} potential cart items")
    
    for i, item in enumerate(cart_items):
        try:
            # Initialize default values
            product_name = ""
            sku = ""
            part_no = ""
            unit_price = ""
            quantity = 1
            subtotal = ""
            
            if item.name == 'tr':  # Table row approach
                cells = item.find_all(['td', 'th'])
                if len(cells) >= 4:
                    product_name = cells[0].get_text(strip=True)
                    sku = extract_sku_from_text(cells[1].get_text(strip=True))
                    unit_price = extract_price_from_text(cells[2].get_text(strip=True))
                    quantity = extract_quantity_from_text(cells[3].get_text(strip=True))
                    subtotal = extract_price_from_text(cells[4].get_text(strip=True)) if len(cells) > 4 else ""
            
            else:  # Div-based approach (your original)
                parent = item.find_parent('div')
                if not parent:
                    continue
                
                # Extract product name
                product_name_elem = parent.find_previous_sibling('div')
                product_name = product_name_elem.get_text(strip=True) if product_name_elem else f"Product {i+1}"
                
                # Extract SKU
                sku = item.get_text(strip=True).replace('SKU:', '').strip()
                
                # Extract Part No.
                part_no_elem = item.find_next('div', string=lambda t: t and 'Part No.:' in t)
                part_no = part_no_elem.get_text(strip=True).replace('Part No.:', '').strip() if part_no_elem else ""
                
                # Extract Unit Price
                unit_price_elem = item.find_next('div', string=lambda t: t and 'Unit Price:' in t)
                if unit_price_elem:
                    price_span = unit_price_elem.find_next('span')
                    unit_price = price_span.get_text(strip=True) if price_span else ""
                
                # Extract Quantity
                quantity_elem = parent.find_previous('div', string=lambda t: t and 'x' in t)
                if quantity_elem and 'x' in quantity_elem.get_text():
                    try:
                        quantity_text = quantity_elem.get_text(strip=True).split('x')[0].strip()
                        quantity = int(quantity_text)
                    except (ValueError, IndexError):
                        quantity = 1
                
                # Extract Subtotal
                subtotal_elem = item.find_next('div', string=lambda t: t and 'Subtotal:' in t)
                if subtotal_elem:
                    subtotal_span = subtotal_elem.find_next('span')
                    subtotal = subtotal_span.get_text(strip=True) if subtotal_span else ""
            
            # Only append if we have at least product name and some other info
            if product_name and (sku or unit_price or subtotal):
                data['Product Name'].append(product_name)
                data['SKU'].append(sku)
                data['Part No.'].append(part_no)
                data['Unit Price'].append(unit_price)
                data['Quantity'].append(quantity)
                data['Subtotal'].append(subtotal)
                
        except Exception as e:
            print(f"Error processing item {i+1}: {e}")
            continue
    
    return data

def extract_sku_from_text(text):
    """Extract SKU from text"""
    if 'SKU:' in text:
        return text.split('SKU:')[1].strip()
    return text.strip()

def extract_price_from_text(text):
    """Extract price from text"""
    import re
    price_match = re.search(r'[\$€£¥]?[\d,]+\.?\d*', text)
    return price_match.group() if price_match else text.strip()

def extract_quantity_from_text(text):
    """Extract quantity from text"""
    import re
    qty_match = re.search(r'\d+', text)
    return int(qty_match.group()) if qty_match else 1

def add_power_calculations(df):
    """Add power calculation columns and Raspberry Pi 5 data"""
    # Add Raspberry Pi 5 if not already present
    pi5_present = any('raspberry pi 5' in name.lower() for name in df['Product Name'])
    
    if not pi5_present:
        # Add Raspberry Pi 5 16GB data
        new_row = {
            'Product Name': 'Raspberry Pi 5 (16GB)',
            'SKU': 'RPI5-16GB',
            'Part No.': 'RPI5-16GB',
            'Unit Price': '$80.00',
            'Quantity': 1,
            'Subtotal': '$80.00'
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Add power consumption columns
    power_data = {
        'Voltage (V)': [],
        'Current (A)': [],
        'Power (W)': [],
        'Notes': []
    }
    
    for _, row in df.iterrows():
        product_name = row['Product Name'].lower()
        
        if 'raspberry pi 5' in product_name:
            power_data['Voltage (V)'].append(5.0)
            power_data['Current (A)'].append('0.6 - 2.4')
            power_data['Power (W)'].append('3.0 - 12.0')
            power_data['Notes'].append('Idle: ~2.7W, Peak: ~12W')
        elif 'can' in product_name or 'mcp2515' in product_name:
            power_data['Voltage (V)'].append(5.0)
            power_data['Current (A)'].append('0.05 - 0.1')
            power_data['Power (W)'].append('0.25 - 0.5')
            power_data['Notes'].append('CAN interface module')
        elif 'display' in product_name or 'lcd' in product_name or 'screen' in product_name:
            power_data['Voltage (V)'].append(5.0)
            power_data['Current (A)'].append('0.1 - 0.5')
            power_data['Power (W)'].append('0.5 - 2.5')
            power_data['Notes'].append('Display module')
        elif 'sensor' in product_name:
            power_data['Voltage (V)'].append(3.3)
            power_data['Current (A)'].append('0.001 - 0.05')
            power_data['Power (W)'].append('0.003 - 0.165')
            power_data['Notes'].append('Sensor module')
        elif 'hat' in product_name or 'expansion' in product_name:
            power_data['Voltage (V)'].append(5.0)
            power_data['Current (A)'].append('0.05 - 0.2')
            power_data['Power (W)'].append('0.25 - 1.0')
            power_data['Notes'].append('HAT/Expansion board')
        else:
            power_data['Voltage (V)'].append(5.0)
            power_data['Current (A)'].append('0.05 - 0.1')
            power_data['Power (W)'].append('0.25 - 0.5')
            power_data['Notes'].append('Generic accessory')
    
    # Add power columns to dataframe
    for col, values in power_data.items():
        df[col] = values
    
    return df

def main():
    html_path = "./app_modules/assets/data/data.html"
    cart_url = "https://www.waveshare.com/checkout/cart/"
    
    print("Waveshare Cart Scraper")
    print("=" * 50)
    
    # Try to scrape from local file first
    if os.path.exists(html_path):
        print(f"Found {html_path}, scraping from local file...")
        data = scrape_cart_from_file(html_path)
    else:
        print(f"Local file {html_path} not found.")
        print("Attempting to scrape from URL (may not work due to session requirements)...")
        data = scrape_cart_from_url(cart_url)
    
    if data is None:
        print("\nTo manually save the cart page:")
        print("1. Go to https://www.waveshare.com/checkout/cart/")
        print("2. Right-click on the page -> 'Save As' -> 'Webpage, Complete'")
        print("3. Save as 'data.html' in this directory")
        print("4. Run this script again")
        return
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        print("No cart data found. Please check the HTML structure.")
        return
    
    # Add power calculations
    df = add_power_calculations(df)
    
    # Display results
    print(f"\nExtracted {len(df)} items:")
    print("=" * 50)
    print(df.to_string(index=False))
    
    # Calculate total power requirements
    total_power_min = 0
    total_power_max = 0
    
    for _, row in df.iterrows():
        power_str = str(row['Power (W)'])
        if ' - ' in power_str:
            min_power, max_power = power_str.split(' - ')
            total_power_min += float(min_power)
            total_power_max += float(max_power)
        else:
            try:
                power_val = float(power_str)
                total_power_min += power_val
                total_power_max += power_val
            except ValueError:
                pass  # Skip if can't parse
    
    print(f"\nPower Summary:")
    print("=" * 50)
    print(f"Total Power Consumption: {total_power_min:.2f}W - {total_power_max:.2f}W")
    print(f"Recommended Power Supply: 5V @ {max(3, int(total_power_max/5) + 1)}A ({max(15, int(total_power_max) + 5)}W)")
    
    # Save to CSV
    output_file = './app_modules/assets/data/waveshare_cart_with_power.csv'
    df.to_csv(output_file, index=False)
    print(f"\nTable saved to '{output_file}'")

if __name__ == "__main__":
    main()