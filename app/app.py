from flask import Flask, render_template,redirect, url_for, request, flash, jsonify
import flask_login
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'super secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

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

# @app.route('/test')
# def test():
#     conn = get_db_connection()
#     # sql = '''
#     # select b.brand_id,b.brand_name,p.product_id,p.product_name from products p join brands b on b.brand_id = p.brand_id
#     # '''
#     sql = '''
#     select b.brand_name from brands b
#     '''
#     cursor = conn.execute(sql)
#     brand_result = cursor.fetchall()
#     brand_result = [x[0] for x in brand_result]
#     conn.close()
#     # print(brand_result)
#     # data = ['a','b','c']
#     return render_template('test.html', brand_result=brand_result)
#
# @app.route('/test_post', methods=['POST'])
# def test_post():
#     print("okeee")
#     print(request)
#     name = request.form.getlist('name[]')
#     print(name)
#     return redirect(url_for('test.html'))


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
@flask_login.login_required
def home():
    conn = get_db_connection()
    cursor = conn.execute('''SELECT t.transaction_id,t.date,t.buyer_name,t.via,t.total,t.transaction_type,
                            t.payment_via,t.shipping_cost,t.packing_cost,t.insurance ,t.free_shipping_admin,
                            t.pmstar_admin,t.gift_cost,t.total_profit  FROM transactions t order by t.date desc limit 5''')
    col_names = [description[0] for description in cursor.description]
    latest_transactions = cursor.fetchall()
    conn.close()
    return render_template('home.html', rows=latest_transactions, columns=col_names)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():


    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users where email = "{}" limit 1'.format(email)).fetchall()


    if not users or not check_password_hash(users[0]['password'], password):
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

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


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

    try:
        transaction_id = request.form['transactionid']
    except:
        transaction_id = None

    print(transaction_id)
    conn = get_db_connection()

    userid = conn.execute('SELECT u.user_id FROM users u where username = "{}"'.format(flask_login.current_user.username)).fetchall()
    userid = userid[0]['user_id']

    if not transaction_id:
        sql = '''insert into transactions(date,total,buyer_name,via,
        shipping_cost,packing_cost,insurance,free_shipping_admin,pmstar_admin,
        gift_cost,payment_via,transaction_type,total_profit,user_id) 
        values ("{}",{},"{}","{}",{},{},{},{},{},{},"{}","{}",{},{})'''.format(date,total,buyername,via,shippingcost,packingcost,
                                                                            insurance,freeshippingadmin,pmstaradmin,giftcost,
                                                                            paymentvia,transactiontype,totalprofit,userid)
    else:
        sql = ''' UPDATE transactions
            SET 
            date = "{}",
            total = {},
            buyer_name = "{}",
            via = "{}",
            shipping_cost = {},
            packing_cost = {},
            insurance = {},
            free_shipping_admin = {},
            pmstar_admin = {},
            gift_cost = {},
            payment_via = "{}",
            transaction_type = "{}",
            total_profit = {},
            user_id = {}
            WHERE transaction_id = {}
        '''.format(date,total,buyername,via,shippingcost,packingcost,
                    insurance,freeshippingadmin,pmstaradmin,giftcost,
                    paymentvia,transactiontype,totalprofit,userid,transaction_id)

    print(sql)
    conn.execute(sql)
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/transactions_search', methods=['POST'])
@flask_login.login_required
def transactions_search():
    from_date = request.form['from_date']
    to_date = request.form['to_date']

    conn = get_db_connection()
    sql = '''SELECT t.transaction_id,t.date,t.buyer_name,t.via,t.total,t.transaction_type,
                                        t.payment_via,t.shipping_cost,t.packing_cost,t.insurance ,
                                        t.free_shipping_admin,t.pmstar_admin,,t.gift_cost,t.total_profit  
                                        FROM transactions t where t.date >= "{}" and t.date <= "{}"
                                        order by t.date desc'''.format(str(from_date),str(to_date))

    cursor = conn.execute(sql)
    col_names = [description[0] for description in cursor.description]
    latest_transactions = cursor.fetchall()

    conn.close()
    return render_template('home.html', rows=latest_transactions, columns=col_names)


@app.route('/transactions_edit')
@flask_login.login_required
def transactions_edit():
    return render_template('transactions_edit.html', col_names=None, data=None)

@app.route('/transactions_delete' ,methods=['POST'])
@flask_login.login_required
def transactions_delete():
    transaction_id = request.form['deleteid']

    conn = get_db_connection()
    conn.execute('DELETE FROM transactions as t where t.transaction_id = {}'.format(transaction_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/transactions_update', methods=['POST'])
@flask_login.login_required
def transactions_update():
    transaction_id = request.form['updateid']

    conn = get_db_connection()
    sql = '''SELECT t.transaction_id,t.date,t.buyer_name,t.via,t.total,t.transaction_type,
                                        t.payment_via,t.shipping_cost,t.packing_cost,t.insurance,
                                        t.free_shipping_admin,t.pmstar_admin,t.gift_cost,t.total_profit  
                                        FROM transactions t where t.transaction_id = {}
                                        order by t.date desc limit 1'''.format(transaction_id)

    cursor = conn.execute(sql)
    col_names = [description[0] for description in cursor.description]
    data = cursor.fetchall()[0]
    conn.close()
    return render_template('transactions_edit.html', col_names=col_names, data=data)

@app.route('/product_detail_edit')
@flask_login.login_required
def product_detail_edit():
    conn = get_db_connection()
    sql = '''
    select b.brand_name from brands b
    '''
    cursor = conn.execute(sql)
    brand_result = cursor.fetchall()
    brand_result = [x[0] for x in brand_result]
    conn.close()

    return render_template('product_detail_edit.html',data=None,brand_result=brand_result)

@app.route('/get_product/<brand>', methods=['GET'])
@flask_login.login_required
def get_product(brand):
    conn = get_db_connection()

    sql = '''
        select p.product_name from products p where p.brand_id = (select b.brand_id from brands b where b.brand_name = '{}')
        '''.format(brand)
    cursor = conn.execute(sql)
    product_result = cursor.fetchall()
    product_result = [x[0] for x in product_result]
    conn.close()
    if not product_result:
        return jsonify([])
    else:
        return jsonify(product_result)

