from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_session import Session
import bcrypt
from queries import QUERIES
from datetime import datetime  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperMarketSecret2025'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'SuperMarket'
}
# Home (splash) page displays the welcome screen
@app.route('/')
def splash():
    return render_template('splash.html')

# Main index page
@app.route('/index')
def index():
    return render_template('index.html')

# Route for handling the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from the login form
        username = request.form['username']
        password = request.form['password']

        try:
            # Connect to MySQL database
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("SELECT user_id, username, password, role, customer_id, employee_id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            # Check if user exists and password matches
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[3]
                session['customer_id'] = user[4]
                session['employee_id'] = user[5]
                flash('تم تسجيل الدخول بنجاح!')
                if user[3] == 'manager':
                    return redirect(url_for('owner'))
                else:
                    return redirect(url_for('index'))
            else:
                # If user not found or password doesn't match
                flash('مستخدم غير موجود أو كلمة المرور غير صحيحة.')
                return render_template('login.html')
        except mysql.connector.Error as err:
            flash(f'خطأ في الاتصال بقاعدة البيانات: {err}')
            return render_template('login.html')

    return render_template('login.html')

# Route for displaying dairy products
@app.route('/dairy_products')
def dairy_products():
    try:
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
         # Execute SQL query to get products that belong to the 'منتجات الألبان' (Dairy Products) category
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name = 'منتجات الألبان'
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('dairy_products.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('dairy_products.html', products=[])

# Route for displaying fruits and vegetables
@app.route('/fruits_and_vegetables')
def fruits_and_vegetables():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name IN ('فواكه', 'خضروات')
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('fruits_and_vegetables.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('fruits_and_vegetables.html', products=[])

# Route for displaying breads
@app.route('/breads')
def breads():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name = 'خبز'
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('breads.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('breads.html', products=[])

# Route for displaying meats and frozen products
@app.route('/meats_frozen')
def meats_frozen():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name IN ('لحوم', 'متجمدات')
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('meats_frozen.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('meats_frozen.html', products=[])

# Route for displaying beverages
@app.route('/beverages')
def beverages():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name = 'مشروبات'
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('beverages.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('beverages.html', products=[])

# Route for displaying snacks
@app.route('/snacks')
def snacks():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, c.name AS category
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            WHERE c.name = 'سناكس'
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('snacks.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return render_template('snacks.html', products=[])

# Route for handling user logout
@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح.')
    return redirect(url_for('login'))

# Route for the owner dashboard
@app.route('/owner')
def owner():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير للوصول إلى لوحة التحكم.')
        return redirect(url_for('login'))
    return render_template('owner.html')

# Route for displaying the owner dashboard with queries
@app.route('/search_products', methods=['GET', 'POST'])
def search_products():
    if 'username' not in session or session.get('role') != 'customer':
        flash('يجب تسجيل الدخول كمشتري للبحث عن المنتجات.')
        return redirect(url_for('login'))

    products = []
    if request.method == 'POST':
        search_query = request.form['search_query']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.product_id, p.name, p.price, c.name AS category
                FROM product p
                JOIN category c ON p.category_id = c.category_id
                WHERE p.name LIKE %s OR c.name LIKE %s
            """, (f'%{search_query}%', f'%{search_query}%'))
            products = cursor.fetchall()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            flash(f'خطأ في البحث: {err}')

    return render_template('search_products.html', products=products)

# Route for adding a product to the cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Check if user is logged in and has the role of customer
    if 'username' not in session or session.get('role') != 'customer':
        flash('يجب تسجيل الدخول كمشتري لإضافة المنتجات إلى السلة.')
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = {}

    try:
        # Connect to the database and fetch product details
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT product_id, name, price FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        db.close()

        if product:
            product_id, name, price = product
            # If product already exists in cart, increment its quantity
            if product_id in session['cart']:
                session['cart'][product_id]['quantity'] += 1
            else:
                session['cart'][product_id] = {'name': name, 'price': float(price), 'quantity': 1}
            flash('تم إضافة المنتج إلى السلة!')
    except mysql.connector.Error as err:
        flash(f'خطأ في إضافة المنتج: {err}')

    return redirect(request.referrer or url_for('index'))

# Route for displaying the shopping cart
@app.route('/cart')
def cart():
    if 'username' not in session or session.get('role') != 'customer':
        flash('يجب تسجيل الدخول كمشتري لعرض السلة.')
        return redirect(url_for('login'))

    # Retrieve the cart from session, or use empty cart if not found
    cart = session.get('cart', {})
    category = request.args.get('category')
    products = []
    categories = []

    total = 0
     # Calculate total price of items in the cart
    if cart:
        try:
            total = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
        except Exception as e:
            flash('خطأ في حساب الإجمالي.')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        cursor.execute("SELECT DISTINCT c.name FROM category c JOIN product p ON c.category_id = p.category_id")
        categories = [row[0] for row in cursor.fetchall()]

        if category:
            cursor.execute("""
                SELECT p.product_id, p.name, p.price 
                FROM product p 
                JOIN category c ON p.category_id = c.category_id 
                WHERE c.name = %s
            """, (category,))
            products = cursor.fetchall()

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        flash(f'خطأ في تحميل المنتجات: {err}')

    return render_template('cart.html', cart=cart, products=products, category=category, categories=categories, total=total)

# Route for removing a product from the cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})

    if product_id in cart:
        if cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
            flash('تم تقليل الكمية بمقدار 1.')
        else:
            del cart[product_id]
            flash('تم حذف المنتج من السلة.')

    session['cart'] = cart
    return redirect(request.referrer or url_for('cart'))

# Route for updating the quantity of a product in the cart
@app.route('/update_quantity/<int:product_id>/<int:quantity>')
def update_quantity(product_id, quantity):
    if 'cart' in session and product_id in session['cart'] and quantity > 0:
        session['cart'][product_id]['quantity'] = quantity
        flash('تم تحديث الكمية!')
    return redirect(url_for('cart'))

# Route for confirming the purchase
@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
     # Ensure the user is logged in and has the 'customer' role
    if 'username' not in session or session.get('role') != 'customer':
        flash('يجب تسجيل الدخول كمشتري لتأكيد الشراء.')
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    if not cart:
        flash('السلة فارغة!')
        return redirect(url_for('cart'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Check availability of all products in the cart
        for product_id, item in cart.items():
            cursor.execute("SELECT stock_level FROM product WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if not result:
                flash(f"المنتج برقم {product_id} غير موجود.")
                return redirect(url_for('cart'))
            stock = result[0]
            if stock < item['quantity']:
                flash(f"الكمية غير كافية للمنتج برقم {product_id}. المتوفر: {stock}")
                return redirect(url_for('cart'))

        # Insert a new order(assign to any manager employee)
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, OrderDate)
            SELECT %s, e.employee_id, CURDATE()
            FROM employee e
            WHERE e.role = 'مدير' LIMIT 1
        """, (session['customer_id'],))
        db.commit()
        order_id = cursor.lastrowid

        total = 0
        for product_id, item in cart.items():
            #  Insert order details and update stock levels for each product
            cursor.execute("""
                INSERT INTO order_details (product_id, order_id, unitprice, quantity)
                VALUES (%s, %s, %s, %s)
            """, (product_id, order_id, item['price'], item['quantity']))

             # Update stock level in product table
            cursor.execute("""
                UPDATE product
                SET stock_level = stock_level - %s
                WHERE product_id = %s
            """, (item['quantity'], product_id))

            total += item['price'] * item['quantity']

        db.commit()
        session['cart'] = {}
        flash(f'تم تأكيد الشراء! الحساب الكلي: {total} شيقل')

    except mysql.connector.Error as err:
        db.rollback()
        flash(f'خطأ في تأكيد الشراء: {err}')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('order_history'))

# Route for displaying order history
@app.route('/order_history')
def order_history():
    if 'username' not in session or session.get('role') != 'customer':
        flash('يجب تسجيل الدخول كمشتري لعرض تاريخ الطلبات.')
        return redirect(url_for('login'))

    orders = []
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT o.order_id, o.OrderDate, SUM(od.unitprice * od.quantity) AS total
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            WHERE o.customer_id = %s
            GROUP BY o.order_id, o.OrderDate
        """, (session['customer_id'],))
        orders = cursor.fetchall()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب تاريخ الطلبات: {err}')

    return render_template('order_history.html', orders=orders)

# Route for managing orders (only accessible by manager)
@app.route('/orders')
def orders():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الطلبات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT o.order_id, c.name AS customer, o.OrderDate
            FROM orders o
            JOIN customer c ON o.customer_id = c.customer_id
        """)
        orders = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('orders.html', orders=orders)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الطلبات: {err}')
        return redirect(url_for('index'))

# Route for adding a new order (only accessible by manager)
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة طلب.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        order_date = request.form['order_date']

        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO orders (customer_id, employee_id, OrderDate)
                VALUES (%s, %s, %s)
            """, (customer_id, session['employee_id'], order_date))
            db.commit()
            cursor.close()
            db.close()
            flash('تم إضافة الطلب بنجاح!')
            return redirect(url_for('orders'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة الطلب: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT customer_id, name FROM customer")
        customers = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('add_order.html', customers=customers)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب العملاء: {err}')
        return redirect(url_for('orders'))

# Route for editing an existing order (only accessible by manager)
@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل الطلبات.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        order_date = request.form.get('order_date')

        if not customer_id or not order_date:
            flash("جميع الحقول مطلوبة.")
            return redirect(url_for('edit_order', order_id=order_id))

        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                UPDATE orders
                SET customer_id = %s, OrderDate = %s
                WHERE order_id = %s
            """, (customer_id, order_date, order_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل الطلب بنجاح!')
            return redirect(url_for('orders'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل الطلب: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT order_id, customer_id, OrderDate FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            flash("الطلب غير موجود.")
            return redirect(url_for('orders'))

        cursor.execute("SELECT customer_id, name FROM customer")
        customers = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template('edit_order.html', order=order, customers=customers)

    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الطلب: {err}')
        return redirect(url_for('orders'))

# Route for deleting an order (only accessible by manager)
@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف الطلبات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف الطلب بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف الطلب: {err}')

    return redirect(url_for('orders'))

# Route for handling user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456',
                database='SuperMarket'
            )
            cursor = conn.cursor()

            # Add customer first
            cursor.execute("INSERT INTO customer (name, phone_number, email) VALUES (%s, %s, %s)", (name, phone, email))
            customer_id = cursor.lastrowid

            # Then add user
            cursor.execute("INSERT INTO users (username, password, role, customer_id) VALUES (%s, %s, 'customer', %s)",
                           (username, hashed_pw, customer_id))

            conn.commit()
            flash("تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول الآن.")
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            flash(f"خطأ في التسجيل: {err}")
            return redirect(url_for('register'))

        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

# Route for managing employees (only accessible by manager)
@app.route('/employees')
def employees():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الموظفين.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT e.employee_id, e.name, e.salary, e.role, s.name AS store_name
            FROM employee e
            LEFT JOIN store s ON e.store_id = s.store_id
        """)
        employees = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('employees.html', employees=employees)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الموظفين: {err}')
        return redirect(url_for('index'))

# Route for adding a new employee (only accessible by manager)
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة موظف.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        role = request.form['role']
        store_id = request.form['store_id'] if request.form['store_id'] else None

        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO employee (name, salary, hire_date, role, store_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, salary, hire_date, role, store_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم إضافة الموظف بنجاح!')
            return redirect(url_for('employees'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة الموظف: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT store_id, name FROM store")
        stores = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('add_employee.html', stores=stores)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الفروع: {err}')
        return redirect(url_for('employees'))

# Route for editing an employee (only accessible by manager)
@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل الموظفين.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        role = request.form['role']
        store_id = request.form['store_id'] if request.form['store_id'] else None

        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                UPDATE employee
                SET name = %s, salary = %s, hire_date = %s, role = %s, store_id = %s
                WHERE employee_id = %s
            """, (name, salary, hire_date, role, store_id, employee_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل الموظف بنجاح!')
            return redirect(url_for('employees'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل الموظف: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT employee_id, name, salary, hire_date, role, store_id FROM employee WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()
        cursor.execute("SELECT store_id, name FROM store")
        stores = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('edit_employee.html', employee=employee, stores=stores)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الموظف: {err}')
        return redirect(url_for('employees'))

# Route for deleting an employee (only accessible by manager)
@app.route('/delete_employee/<int:employee_id>')
def delete_employee(employee_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف الموظفين.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف الموظف بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف الموظف: {err}')

    return redirect(url_for('employees'))

# Route for managing categories (only accessible by manager)
@app.route('/categories')
def categories():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الفئات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('categories.html', categories=categories)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الفئات: {err}')
        return redirect(url_for('index'))

# Route for adding a new category (only accessible by manager)
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة فئة.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO category (name) VALUES (%s)", (name,))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة الفئة بنجاح!')
            return redirect(url_for('categories'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة الفئة: {err}')

    return render_template('add_category.html')

# Route for editing a category (only accessible by manager)
@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل الفئات.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("UPDATE category SET name = %s WHERE category_id = %s", (name, category_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل الفئة بنجاح!')
            return redirect(url_for('categories'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل الفئة: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT category_id, name FROM category WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('edit_category.html', category=category)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الفئة: {err}')
        return redirect(url_for('categories'))

# Route for deleting a category (only accessible by manager)  
@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف الفئات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف الفئة بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف الفئة: {err}')

    return redirect(url_for('categories'))

# Route for managing warehouses (only accessible by manager)
@app.route('/warehouses')
def warehouses():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة المستودعات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT warehouse_id, location FROM warehouse")
        warehouses = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('warehouses.html', warehouses=warehouses)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المستودعات: {err}')
        return redirect(url_for('index'))

# Route for adding a new warehouse (only accessible by manager)
@app.route('/add_warehouse', methods=['GET', 'POST'])
def add_warehouse():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة مستودع.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form['location']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO warehouse (location) VALUES (%s)", (location,))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة المستودع بنجاح!')
            return redirect(url_for('warehouses'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة المستودع: {err}')

    return render_template('add_warehouse.html')

# Route for editing a warehouse (only accessible by manager)
@app.route('/edit_warehouse/<int:warehouse_id>', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل المستودعات.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form['location']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("UPDATE warehouse SET location = %s WHERE warehouse_id = %s", (location, warehouse_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل المستودع بنجاح!')
            return redirect(url_for('warehouses'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل المستودع: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT warehouse_id, location FROM warehouse WHERE warehouse_id = %s", (warehouse_id,))
        warehouse = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('edit_warehouse.html', warehouse=warehouse)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المستودع: {err}')
        return redirect(url_for('warehouses'))

# Route for deleting a warehouse (only accessible by manager)    
@app.route('/delete_warehouse/<int:warehouse_id>')
def delete_warehouse(warehouse_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف المستودعات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM warehouse WHERE warehouse_id = %s", (warehouse_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف المستودع بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف المستودع: {err}')
    return redirect(url_for('warehouses'))

# Route for managing suppliers (only accessible by manager)
@app.route('/suppliers')
def suppliers():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الموردين.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT supplier_id, name, contact_info FROM supplier")
        suppliers = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('suppliers.html', suppliers=suppliers)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الموردين: {err}')
        return redirect(url_for('index'))

# Route for adding a new supplier (only accessible by manager)
@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة مورد.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO supplier (name, contact_info) VALUES (%s, %s)", (name, contact_info))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة المورد بنجاح!')
            return redirect(url_for('suppliers'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة المورد: {err}')

    return render_template('add_supplier.html')

# Route for editing a supplier (only accessible by manager)
@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل الموردين.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("UPDATE supplier SET name = %s, contact_info = %s WHERE supplier_id = %s", (name, contact_info, supplier_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل المورد بنجاح!')
            return redirect(url_for('suppliers'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل المورد: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT supplier_id, name, contact_info FROM supplier WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('edit_supplier.html', supplier=supplier)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المورد: {err}')
        return redirect(url_for('suppliers'))

# Route for deleting a supplier (only accessible by manager)
@app.route('/delete_supplier/<int:supplier_id>')
def delete_supplier(supplier_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف الموردين.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM supplier WHERE supplier_id = %s", (supplier_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف المورد بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف المورد: {err}')
    return redirect(url_for('suppliers'))

# Route for managing users (only accessible by manager)
@app.route('/users')
def users():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الفروع.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT user_id , username, role, customer_id, employee_id FROM users")
        users = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('users.html', users=users)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المستخدمين: {err}')
        return redirect(url_for('index'))

# Route for managing stores (only accessible by manager)
@app.route('/stores')
def stores():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة الفروع.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT store_id, name FROM store")
        stores = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('stores.html', stores=stores)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب الفروع: {err}')
        return redirect(url_for('index'))

# Route for adding a new store (only accessible by manager)
@app.route('/add_store', methods=['GET', 'POST'])
def add_store():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة فرع.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO store (name) VALUES (%s)", (name,))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة الفرع بنجاح!')
            return redirect(url_for('stores'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة الفرع: {err}')

    return render_template('add_store.html')

# Route for editing a store (only accessible by manager)
@app.route('/edit_store/<int:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل الفروع.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("UPDATE store SET name = %s WHERE store_id = %s", (name, store_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل اسم الفرع بنجاح!')
            return redirect(url_for('stores'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل الفرع: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT store_id, name FROM store WHERE store_id = %s", (store_id,))
        store = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('edit_store.html', store=store)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب بيانات الفرع: {err}')
        return redirect(url_for('stores'))
    
# Route for deleting a store (only accessible by manager)
@app.route('/delete_store/<int:store_id>')
def delete_store(store_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف الفروع.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM store WHERE store_id = %s", (store_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف الفرع بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف الفرع: {err}')

    return redirect(url_for('stores'))

# Route for managing customers (only accessible by manager)
@app.route('/customers')
def customers():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة العملاء.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT customer_id, name, phone_number, email FROM customer")
        customers = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('customers.html', customers=customers)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب العملاء: {err}')
        return redirect(url_for('index'))

# Route for adding a new customer (only accessible by manager)
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة عميل.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO customer (name, phone_number, email) VALUES (%s, %s, %s)", (name, phone_number, email))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة العميل بنجاح!')
            return redirect(url_for('customers'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة العميل: {err}')

    return render_template('add_customer.html')

# Route for editing a customer (only accessible by manager)
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل العملاء.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("UPDATE customer SET name = %s, phone_number = %s, email = %s WHERE customer_id = %s", (name, phone_number, email, customer_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل بيانات العميل بنجاح!')
            return redirect(url_for('customers'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل بيانات العميل: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT customer_id, name, phone_number, email FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('edit_customer.html', customer=customer)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب بيانات العميل: {err}')
        return redirect(url_for('customers'))

# Route for deleting a customer (only accessible by manager)
@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف العملاء.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف العميل بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف العميل: {err}')

    return redirect(url_for('customers'))

# Route for managing products (only accessible by manager)
@app.route('/products')
def products():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإدارة المنتجات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.stock_level, p.expiration_date,
                   c.name AS category, s.name AS supplier, w.location AS warehouse
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            JOIN supplier s ON p.supplier_id = s.supplier_id
            JOIN warehouse w ON p.warehouse_id = w.warehouse_id
        """)
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('products.html', products=products)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب المنتجات: {err}')
        return redirect(url_for('index'))
    
# Route for adding a new product (only accessible by manager)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لإضافة منتج.')
        return redirect(url_for('login'))
    
    # add the product to the database
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock_level']
        expiration_str = request.form['expiration_date']
        category_id = request.form['category_id']
        supplier_id = request.form['supplier_id']
        warehouse_id = request.form['warehouse_id']

        # Validate the expiration date format and ensure it is not in the past
        if expiration_str:
            try:
                expiration_date = datetime.strptime(expiration_str, '%Y-%m-%d').date()
                today = datetime.today().date()
                if expiration_date < today:
                    flash('لا يمكن إضافة منتج بصلاحية منتهية. الرجاء تعديل تاريخ الصلاحية.')
                    return redirect(url_for('add_product'))
            except ValueError:
                flash('صيغة تاريخ غير صحيحة.')
                return redirect(url_for('add_product'))
        else:
            expiration_date = None  # Allow products without an expiration date

        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
             # Insert the new product into the database
            cursor.execute("""
                INSERT INTO product (name, price, stock_level, expiration_date, category_id, supplier_id, warehouse_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, price, stock, expiration_date, category_id, supplier_id, warehouse_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تمت إضافة المنتج بنجاح!')
            return redirect(url_for('products'))
        except mysql.connector.Error as err:
            flash(f'خطأ في إضافة المنتج: {err}')
            return redirect(url_for('add_product'))

    # Fetch categories, suppliers, and warehouses for the form
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT supplier_id, name FROM supplier")
        suppliers = cursor.fetchall()
        cursor.execute("SELECT warehouse_id, location FROM warehouse")
        warehouses = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('add_product.html', categories=categories, suppliers=suppliers, warehouses=warehouses)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب البيانات المساعدة: {err}')
        return redirect(url_for('products'))

# Route for editing a product (only accessible by manager)
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لتعديل المنتجات.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock_level']
        expiration = request.form['expiration_date'] or None
        category_id = request.form['category_id']
        supplier_id = request.form['supplier_id']
        warehouse_id = request.form['warehouse_id']
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("""
                UPDATE product
                SET name=%s, price=%s, stock_level=%s, expiration_date=%s,
                    category_id=%s, supplier_id=%s, warehouse_id=%s
                WHERE product_id = %s
            """, (name, price, stock, expiration, category_id, supplier_id, warehouse_id, product_id))
            db.commit()
            cursor.close()
            db.close()
            flash('تم تعديل المنتج بنجاح!')
            return redirect(url_for('products'))
        except mysql.connector.Error as err:
            flash(f'خطأ في تعديل المنتج: {err}')

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT product_id, name, price, stock_level, expiration_date, category_id, supplier_id, warehouse_id FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.execute("SELECT category_id, name FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT supplier_id, name FROM supplier")
        suppliers = cursor.fetchall()
        cursor.execute("SELECT warehouse_id, location FROM warehouse")
        warehouses = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('edit_product.html', product=product, categories=categories, suppliers=suppliers, warehouses=warehouses)
    except mysql.connector.Error as err:
        flash(f'خطأ في جلب بيانات المنتج: {err}')
        return redirect(url_for('products'))

# Route for deleting a product (only accessible by manager)
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير لحذف المنتجات.')
        return redirect(url_for('login'))

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('تم حذف المنتج بنجاح!')
    except mysql.connector.Error as err:
        flash(f'خطأ في حذف المنتج: {err}')

    return redirect(url_for('products'))

# Route for managing reports (only accessible by manager)
@app.route('/reports')
def reports():
    if 'username' not in session or session.get('role') != 'manager':
        flash('يجب تسجيل الدخول كمدير للوصول إلى التقارير.')
        return redirect(url_for('login'))

    query_key = request.args.get('query')  
    results = {}

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        if query_key and query_key in QUERIES:
            cursor.execute(QUERIES[query_key])
            columns = [desc[0] for desc in cursor.description]  
            rows = cursor.fetchall()
            results[query_key] = {
                'columns': columns,
                'rows': rows
            }
        else:
            query_key = None

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        flash(f'خطأ في تنفيذ التقارير: {err}')

    return render_template('reports.html', results=results, selected_query=query_key, query_keys=list(QUERIES.keys()))

if __name__ == '__main__':
    app.run(debug=True)