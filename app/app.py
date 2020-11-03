from flask import Flask, render_template,redirect, url_for, request, flash
import flask_login
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'super secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
@flask_login.login_required
def home():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions t order by t.date desc limit 5')
    col_names = [description[0] for description in cursor.description]
    latest_transactions = cursor.fetchall()
    conn.close()
    return render_template('index.html', rows=latest_transactions, columns=col_names)

@app.route('/transactions_input', methods=['POST'])
@flask_login.login_required
def transactions_input():

    date = request.form['date']
    total = request.form['total']
    buyername = request.form['buyername']
    via = request.form['via']
    shippingcost = request.form['shippingcost']
    packingcost = request.form['packingcost']
    insurance = request.form['insurance']
    freeshippingadmin = request.form['freeshippingadmin']
    pmstaradmin = request.form['pmstaradmin']
    giftcost = request.form['giftcost']
    paymentvia = request.form['paymentvia']
    transactiontype = request.form['transactiontype']
    totalprofit = request.form['totalprofit']

    conn = get_db_connection()

    userid = conn.execute('SELECT u.user_id FROM users u where username = "{}"'.format(flask_login.current_user.username)).fetchall()
    userid = userid[0]['user_id']
    sql = '''insert into transactions(date,total,buyer_name,via,
    shipping_cost,packing_cost,insurance,free_shipping_admin,pmstar_admin,
    gift_cost,payment_via,transaction_type,total_profit,user_id) 
    values ("{}",{},"{}","{}",{},{},{},{},{},{},"{}","{}",{},{})'''.format(date,total,buyername,via,shippingcost,packingcost,
                                                                        insurance,freeshippingadmin,pmstaradmin,giftcost,
                                                                        paymentvia,transactiontype,totalprofit,userid)

    print(sql)
    conn.execute(sql)
    conn.commit()

    cursor = conn.execute('SELECT * FROM transactions t order by t.date desc limit 5')
    col_names = [description[0] for description in cursor.description]
    latest_transactions = cursor.fetchall()

    conn.close()

    return render_template('index.html', rows=latest_transactions, columns=col_names)

@login_manager.user_loader
def user_loader(email):
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users where email = "{}" limit 1'.format(email)).fetchall()
    if not users:
        return
    username = users[0]['username']
    user = User()
    user.id = email
    user.username = username
    conn.close()
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    conn = get_db_connection()
    users = conn.execute('SELECT email FROM users where email = "{}" limit 1'.format(email)).fetchall()
    if not users:
        return

    username = users[0]['username']

    user = User()
    user.id = email
    user.username = username
    user.is_authenticated = check_password_hash(user[0]['password'], request.form['password'] )
    conn.close()
    return user

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():


    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users where email = "{}" limit 1'.format(email)).fetchall()


    if not check_password_hash(users[0]['password'], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    username = users[0]['username']
    user = User()
    user.id = email
    user.username = username
    flask_login.login_user(user)
    conn.close()
    return redirect(url_for('home'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    conn = get_db_connection()
    result = conn.execute('SELECT * FROM users where email = "{}"'.format(email)).fetchall()

    if result:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    sql = 'insert into users(email,username,password) values ("{}","{}","{}")'.format(email,name,generate_password_hash(password, method='sha256'))

    conn.execute(sql)
    conn.commit()
    conn.close()

    return redirect(url_for('login'))


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.username

# session['user_id'] = form.user.id
@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))