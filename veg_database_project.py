# ---------------- DATABASE CONNECTION ----------------
import mysql.connector
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Rohini@2005',
    database='vegetable'
)
cursor = db.cursor()
# ---------------- OWNER FUNCTIONS ----------------
def add_vegetable():
    name = input('Vegetable name: ').lower()
    cursor.execute(
        'SELECT id FROM vegetables WHERE name=%s',
        (name,)
    )
    data = cursor.fetchone()
    if data:
        print('Vegetable already exists')
        return
    qty = float(input('Quantity: '))
    cp = float(input('Cost price: '))
    sp = float(input('Selling price: '))
    cursor.execute(
        '''
        INSERT INTO vegetables
        (name, quantity, cost_price, selling_price)
        VALUES(%s,%s,%s,%s)
        ''',
        (name, qty, cp, sp)
    )
    db.commit()
    print('Vegetable added successfully')
def remove_vegetable():
    name = input('Vegetable to remove: ').lower()
    cursor.execute(
        'SELECT id FROM vegetables WHERE name=%s',
        (name,)
    )
    data = cursor.fetchone()
    if not data:
        print('Vegetable not found')
        return
    vid = data[0]
    cursor.execute(
        'SELECT COUNT(*) FROM sales WHERE veg_id=%s',
        (vid,)
    )
    count = cursor.fetchone()[0]
    if count > 0:
        print('Cannot delete vegetable. Sales history exists.')
        return
    cursor.execute(
        'DELETE FROM vegetables WHERE id=%s',
        (vid,)
    )
    db.commit()
    print('Vegetable removed successfully')
def update_vegetable():
    name = input('Vegetable to update: ').lower()
    cursor.execute(
        'SELECT id FROM vegetables WHERE name=%s',
        (name,)
    )
    data = cursor.fetchone()
    if not data:
        print('Vegetable not found')
        return
    qty = float(input('New quantity: '))
    cp = float(input('New cost price: '))
    sp = float(input('New selling price: '))
    cursor.execute(
        '''
        UPDATE vegetables
        SET quantity=%s,
            cost_price=%s,
            selling_price=%s
        WHERE name=%s
        ''',
        (qty, cp, sp, name)
    )
    db.commit()
    print('Vegetable updated successfully')
def view_inventory():
    cursor.execute(
        'SELECT name, quantity, selling_price FROM vegetables'
    )
    rows = cursor.fetchall()
    print(f"\n{'ITEM':<12}{'QTY':<10}{'PRICE':<10}")
    print('-' * 32)
    for name, qty, price in rows:
        print(f"{name:<12}{qty:<10}{price:<10}")
def customer_report():
    date = input('Enter date (YYYY-MM-DD): ')
    cursor.execute(
        '''
        SELECT c.id,
               c.name,
               c.phone,
               SUM(s.total),
               s.sale_date
        FROM customers c
        JOIN sales s
        ON c.id = s.customer_id
        WHERE s.sale_date=%s
        GROUP BY c.id, s.sale_date
        ''',
        (date,)
    )
    rows = cursor.fetchall()
    if not rows:
        print('No customer records found')
        return
    print(f"\n{'ID':<5}{'NAME':<15}{'PHONE':<15}{'TOTAL':<10}")
    print('-' * 45)
    for cid, name, phone, total, sdate in rows:
        print(f"{cid:<5}{name:<15}{phone:<15}{total:<10}")
def profit_report():
    date = input('Enter date (YYYY-MM-DD): ')
    cursor.execute(
        '''
        SELECT v.name,
               s.sale_date,
               SUM((v.selling_price - v.cost_price) * s.qty)
        FROM sales s
        JOIN vegetables v
        ON s.veg_id = v.id
        WHERE s.sale_date=%s
        GROUP BY v.name, s.sale_date
        ''',
        (date,)
    )
    rows = cursor.fetchall()
    if not rows:
        print('No sales found')
        return
    total_profit = 0
    print(f"\n{'VEGETABLE':<15}{'PROFIT':<10}")
    print('-' * 30)
    for name, sdate, profit in rows:
        total_profit += profit
        print(f"{name:<15}{profit:<10}")
    print('-' * 30)
    print(f"{'TOTAL PROFIT':<15}{total_profit}")
# ---------------- CUSTOMER FUNCTIONS ----------------
def add_to_cart(cart):
    cursor.execute(
        'SELECT name, quantity, selling_price FROM vegetables'
    )
    rows = cursor.fetchall()
    print(f"\n{'ITEM':<12}{'QTY':<10}{'PRICE':<10}")
    print('-' * 32)
    for name, qty, price in rows:
        print(f"{name:<12}{qty:<10}{price:<10}")
    while True:
        item = input('\nVegetable name(done): ').lower()
        if item == 'done':
            break
        qty = float(input('Quantity: '))
        cursor.execute(
            '''
            SELECT id, quantity
            FROM vegetables
            WHERE name=%s
            ''',
            (item,)
        )
        data = cursor.fetchone()
        if not data:
            print('Vegetable not found')
            continue
        vid, stock = data
        if qty > stock:
            print('not enough stock')
            continue
        cart[item] = cart.get(item, 0) + qty
        cursor.execute(
            '''
            UPDATE vegetables
            SET quantity = quantity - %s
            WHERE id=%s
            ''',
            (qty, vid)
        )
        db.commit()
        print('Added to cart')
def remove_from_cart(cart):
    if not cart:
        print('Cart empty')
        return
    item = input('Vegetable to remove: ').lower()
    if item not in cart:
        print('Item not in cart')
        return
    qty = cart[item]
    cursor.execute(
        '''
        UPDATE vegetables
        SET quantity = quantity + %s
        WHERE name=%s
        ''',
        (qty, item)
    )
    del cart[item]
    db.commit()
    print('Item removed from cart')
def update_cart(cart):
    if not cart:
        print('Cart empty')
        return
    item = input('Vegetable to update: ').lower()
    if item not in cart:
        print('Item not in cart')
        return
    new_qty = float(input('New quantity: '))
    old_qty = cart[item]
    diff = new_qty - old_qty
    cursor.execute(
        '''
        SELECT id, quantity
        FROM vegetables
        WHERE name=%s
        ''',
        (item,)
    )
    data = cursor.fetchone()
    if not data:
        print('Vegetable not found')
        return
    vid, stock = data
    if diff > stock:
        print('Not enough stock')
        return
    cursor.execute(
        '''
        UPDATE vegetables
        SET quantity = quantity - %s
        WHERE id=%s
        ''',
        (diff, vid)
    )
    if new_qty == 0:
        del cart[item]
    else:
        cart[item] = new_qty
    db.commit()
    print('Cart updated')
def view_cart(cart):
    if not cart:
        print('Cart empty')
        return
    total = 0
    print(f"\n{'ITEM':<12}{'QTY':<10}{'PRICE':<10}{'SUBTOTAL':<10}")
    print('-' * 45)
    for item, qty in cart.items():
        cursor.execute(
            '''
            SELECT selling_price
            FROM vegetables
            WHERE name=%s
            ''',
            (item,)
        )
        price = float(cursor.fetchone()[0])
        subtotal = price * qty
        total += subtotal
        print(f"{item:<12}{qty:<10}{price:<10}{subtotal:<10}")
    print('-' * 45)
    print(f"{'TOTAL':<32}{total}")
def bill(cart):
    if not cart:
        print('Cart empty')
        return
    name = input('Customer name: ')
    while True:
        phone = input('Phone number: ')
        if phone.isdigit() and len(phone) == 10:
            break
        print('Invalid phone number')
    cursor.execute(
        '''
        INSERT INTO customers(name, phone)
        VALUES(%s,%s)
        ''',
        (name, phone)
    )
    db.commit()
    cust_id = cursor.lastrowid
    total = 0
    print(f"\n{'ITEM':<12}{'QTY':<10}{'PRICE':<10}{'SUBTOTAL':<10}")
    print('-' * 45)
    for item, qty in cart.items():
        cursor.execute(
            '''
            SELECT id, selling_price
            FROM vegetables
            WHERE name=%s
            ''',
            (item,)
        )
        data = cursor.fetchone()
        vid, price = data
        price=float(price)
        subtotal = qty * price
        total += subtotal
        cursor.execute(
            '''
            INSERT INTO sales
            (customer_id, veg_id, qty, total)
            VALUES(%s,%s,%s,%s)
            ''',
            (cust_id, vid, qty, subtotal)
        )
        print(f"{item:<12}{qty:<10}{price:<10}{subtotal:<10}")
    print('-' * 45)
    print(f"{'TOTAL':<32}{total}")
    print('\nBilling successful')
    db.commit()
    cart.clear()
# ---------------- MAIN PROGRAM ----------------
while True:
    print('\n' + '=' * 50)
    print('      WELCOME TO VEGETABLE STORE')
    print('=' * 50)
    role = input('Role(owner/customer/exit): ').lower()
    # ---------------- OWNER ----------------
    if role == 'owner':
        password = input('Password: ')
        if password != 'admin':
            print('Wrong password')
            continue
        while True:
            print('''
===== OWNER MENU =====
1.Add Vegetable
2.Remove Vegetable
3.Update Vegetable
4.View Inventory
5.Customer Report
6.Profit Report
7.Back
''')
            ch = input('Enter choice: ')
            if ch == '1':
                add_vegetable()
            elif ch == '2':
                remove_vegetable()
            elif ch == '3':
                update_vegetable()
            elif ch == '4':
                view_inventory()
            elif ch == '5':
                customer_report()
            elif ch == '6':
                profit_report()
            elif ch == '7':
                break
            else:
                print('Invalid choice')
    # ---------------- CUSTOMER ----------------
    elif role == 'customer':
        cart = {}
        while True:
            print('''
===== CUSTOMER MENU =====
1.Add To Cart
2.Remove From Cart
3.Update Cart
4.View Cart
5.Bill
6.Back
''')
            ch = input('Enter choice: ')
            if ch == '1':
                add_to_cart(cart)
            elif ch == '2':
                remove_from_cart(cart)
            elif ch == '3':
                update_cart(cart)
            elif ch == '4':
                view_cart(cart)
            elif ch == '5':
                bill(cart)
            elif ch == '6':
                break
            else:
                print('Invalid choice')
    # ---------------- EXIT ----------------
    elif role == 'exit':
        print('Shop Closed')
        break
    else:
        print('Invalid role')
