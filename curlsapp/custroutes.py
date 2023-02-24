from flask import Flask,render_template,abort,request,flash,redirect,url_for,session
from sqlalchemy.sql import text
from sqlalchemy import desc
from werkzeug.security import generate_password_hash,check_password_hash
#import local files
from curlsapp import app,db
from curlsapp.models import Customers,Vendors,Lga,State,Messages,Ven_style,Products,Bookings,Cart
from curlsapp.forms import ContactForm

@app.route('/')
def homepage():
    info=db.session.query(Vendors).all()
    prods = Products.query.all()
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    cartdets = Cart.query.filter(Cart.cart_userid==custid).all()
    return render_template('customer/index.html',info=info,prods=prods,custdeets=custdeets,cartdets=cartdets)

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('customer/register.html')
    else:
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        uemail = request.form.get('email')
        phone = request.form.get('phonenumber')
        pwd = request.form.get('password')
        cpwd = request.form.get('confirmpwd')
        hashed_pwd = generate_password_hash(pwd)
        if fname !='' and lname !='' and uemail !='' and pwd!='' and cpwd!='' and phone!='':
            if pwd == cpwd:
                c=Customers(cust_fname=fname,cust_lname=lname,cust_email=uemail,cust_phone=phone,cust_pwd=hashed_pwd)
                db.session.add(c)
                db.session.commit()
                userid=c.cust_id
                session['user']=userid
                return redirect(url_for('login'))
            else:
                flash("Please check input")
                return redirect('/register/')
        else:
            flash("Please complete all fields")
            return redirect('/register/')

@app.route('/index/login',methods=['POST','GET'])
def login():
    if request.method =="GET":
        return render_template('customer/login.html')
    else:
        email=request.form.get('login_email')
        pwd=request.form.get('login_pwd')
        #run query to check if username exists.
        dets=db.session.query(Customers).filter(Customers.cust_email==email).first()
        if dets != None: #meaning there is a cust <cust>
            pwd_indb=dets.cust_pwd
            #check if the pswds match with the one that was inserted into the db.
            chk=check_password_hash(pwd_indb,pwd)
            if chk:
                custid =dets.cust_id
                session['user']=custid
                return redirect(url_for('homepage'))
            else:
                flash('Invalid Credentials')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route('/login/account/')
def account():
    if session.get('user') !=None:
        custid = session.get('user')
        custdeets = db.session.query(Customers).get(custid)
        return render_template('customer/account.html',custdeets=custdeets)
    else:
        return redirect(url_for('homepage'))

@app.route('/logout/')
def cust_logout():
    if session.get('user') !=None:
        session.pop('user',None)
    return redirect(url_for('homepage'))

@app.route('/index/allsalons/')
def all_salons():
    data=db.session.query(Vendors).all()
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    return render_template("customer/allsalons.html",data=data,custdeets=custdeets)

@app.route('/index/salon/<id>')
def view_salon(id):
    data=Vendors.query.get_or_404(id)
    vstyle =db.session.query(Ven_style).filter(Ven_style.venstyle_vendorid==id).all()
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    return render_template('customer/salon.html',data=data,vstyle=vstyle,custdeets=custdeets)

@app.route('/salon/booknow/<vsid>', methods=["GET", "POST"])
def book_salon(vsid):
    custid = session.get('user')
    if custid != None:
        if request.method == "GET":
            custdeets = db.session.query(Customers).get(custid)
            vstyle =db.session.query(Ven_style).get(vsid)
            return render_template('customer/booknow.html',custdeets=custdeets,vstyle=vstyle)
        else:
            date = request.form.get('date')
            time = request.form.get('time')
            booktype = request.form.get('service_type')
            if date != "" and time != "" and booktype != "":
                book = Bookings(booking_date=date,booking_time=time,booking_type=booktype,booking_custid=custid,booking_venstyleid=vsid)
                db.session.add(book)
                db.session.commit()
                return redirect(url_for('addbooking_tocart'))
            else:
                vstyle =db.session.query(Ven_style).get(vsid)
                flash("All fields required")
                return redirect(url_for('book_salon',vsid=vstyle.ven_styleid))         
    else:
        return redirect(url_for('login'))

# intermediary routes
@app.route('/addbooking_tocart')
def addbooking_tocart():
    #fetch booking id and insert into cart 
    custid = session.get('user')
    bookid = Bookings.query.filter(Bookings.booking_custid==custid).order_by(Bookings.booking_id.desc()).first()
    cart = Cart(cartitem_prodid='',cartitem_bookid=bookid.booking_id,cartitem_price=bookid.stylepref.venstyle_amt,cartitem_qty=1,cartitem_total=bookid.stylepref.venstyle_amt,cart_userid=custid)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/addproduct_tocart')
def addproduct_tocart():
    custid = session.get('user')
    if custid == None:
        return redirect('login')
    else:
        #when they click on the product, get the productid and insert into the cart table.
        # product = Products.query.get_or_404(id)
        qty = request.args.get('qty')
        prodid = request.args.get('prodid')
        amt = request.args.get('amount')
        total = request.args.get('total')

        item = Cart.query.filter(Cart.cartitem_prodid==prodid).first()
        if item:
            item.cartitem_price=amt
            item.cartitem_qty=qty
            item.cartitem_total=total
            item.cart_userid=custid
            db.session.commit()
            return redirect(url_for('view_product',id=prodid))
        else:
            cart = Cart(cartitem_prodid=prodid,cartitem_bookid='',cartitem_price=amt,cartitem_qty=qty,cartitem_total=total,cart_userid=custid)
            db.session.add(cart)
            db.session.commit()
            return redirect(url_for('view_product',id=prodid))

#cart will be dynamic. empty at sometimes and not at other times
@app.route('/cart/')
def cart():
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    #fetch from the cart table and use the id to display the items in the cart.
    cartdets = Cart.query.filter(Cart.cart_userid==custid).all()
    # totalAmt = db.session.query(db.func.sum(Cart.cartitem_total)).filter(Cart.cart_userid==custid).first()
    query = f"SELECT SUM(cartitem_total) FROM cart WHERE cart_userid={custid}"
    result = db.session.execute(text(query))
    total = result.fetchone()
    # totalAmt = Cart.query.filter(Cart.cart_userid==custid).first()
    return render_template('/customer/cart.html',custdeets=custdeets,cartdets=cartdets,total=total)


@app.route('/cart/removeitem/<id>')
def removeitem(id):
    custid = session.get('user')
    if custid == None:
        return redirect(url_for('login'))
    else:
        #retrieve cart and delete cart id
        cartobj = Cart.query.get_or_404(id)
        db.session.delete(cartobj)
        db.session.commit()
        flash("Item has been removed from cart")
        return redirect(url_for('cart'))

@app.route('/cart/clearcart')
def clearcart():
    custid = session.get('user')
    if custid == None:
        return redirect(url_for('login'))
    else:
        Cart.query.filter_by(cart_userid=custid).delete()
        # db.session.delete(clearcart)
        db.session.commit()
        return redirect(url_for('cart'))


@app.route('/index/allproducts')
def all_products():
    allprods = Products.query.all()
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    return render_template('customer/allproducts.html',allprods=allprods,custdeets=custdeets)

@app.route('/index/product/<id>')
def view_product(id):
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    prod = Products.query.get_or_404(id)
    vprods = db.session.query(Products).filter(Products.prod_venid==prod.thevendor.ven_id).all()
    cartdets = Cart.query.filter(Cart.cart_userid==custid).all()
    cartitem = Cart.query.filter(Cart.cartitem_prodid==id).first()
    return render_template('customer/product.html',prod=prod, vprods=vprods,custdeets=custdeets,cartdets=cartdets,cartitem=cartitem)





#while customers are logged in
@app.route('/load_lga/<stateid>')
def load_lga(stateid):
    lgas = db.session.query(Lga).filter(Lga.lga_stateid==stateid).all()
    data2send = "<select class='form-select border-info' name='lga'>"
    for s in lgas:
        data2send = data2send+f"<option value='{s.lga_id}'>"+s.lga_name +"</option>"
    
    data2send = data2send + "</select>"

    return data2send

@app.route('/myprofile',methods=["GET","POST"])
def cust_profile():
    id=session.get('user')
    if id ==None:
        return redirect(url_for('login'))
    else:
        if request.method=="GET":
            cust=db.session.query(Customers).filter(Customers.cust_id==id).first()
            ldata=db.session.query(Lga).all()
            sdata=db.session.query(State).all()
            custdeets = db.session.query(Customers).get(id)
            return render_template('customer/myprofile.html',cust=cust,ldata=ldata,sdata=sdata,custdeets=custdeets)
        else:
            dob=request.form.get('dob')
            address=request.form.get('address')
            lga=request.form.get('lga')
            state=request.form.get('state')
            if dob != '' and address !='' and lga !='' and state !='':
                #query an object of Customers,get id, assign attributes, commit
                custobj=db.session.query(Customers).get(id)
                custobj.cust_dob=dob
                custobj.cust_address=address
                custobj.cust_lgaid=lga
                custobj.cust_stateid=state
                db.session.commit()
                flash('Profile updated successfully')
                return redirect(url_for('cust_profile'))
            else:
                flash('Please supply information')
                return redirect(url_for('cust_profile'))

@app.route('/myorders')
def cust_orders():
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    return render_template('customer/myorders.html',custdeets=custdeets)

@app.route('/mybookings')
def cust_bookings():
    custid = session.get('user')
    custdeets = db.session.query(Customers).get(custid)
    return render_template('customer/mybookings.html',custdeets=custdeets)

@app.route('/contactus/', methods=["POST","GET"])
def contactus():
    contact=ContactForm()
    if request.method=="GET":
        custid = session.get('user')
        if custid != None:
            custdeets = db.session.query(Customers).get(custid)
        else:
            custdeets=None
        return render_template('customer/contactus.html',contact=contact,custdeets=custdeets)
    else:
        if contact.validate_on_submit():
            email=contact.email.data
            msg=contact.message.data
            m = Messages(msg_email=email,msg_content=msg)
            db.session.add(m)
            db.session.commit()
            flash('Thank you for contacting us, we will revert.')
            return redirect(url_for('contactus'))
        else:
            return render_template('customer/contactus.html',contact=contact)




#layouts
# @app.route('/base')
# def basepage():
#     return render_template('baselayout.html')

# @app.route('/dashlayout')
# def dashboard():
#     return render_template('dash_layout.html')

# @app.route('/homelayout')
# def layout():
#     if session.get('user') == None:
#         return redirect(url_for('homepage'))
#     else:
#         return render_template('homelayout.html')

# @app.route('/homelayout')
# def layout():
#     if session.get('user') !=None:
#         return render_template('homelayout.html')

#test
# @app.route('/temp')
# def test():
#     return render_template('temp.html')

