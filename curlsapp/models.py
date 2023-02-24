from datetime import datetime
from curlsapp import db

class Customers(db.Model):
    cust_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    cust_fname = db.Column(db.String(100),nullable=False)
    cust_lname = db.Column(db.String(100),nullable=False)
    cust_email = db.Column(db.String(120)) 
    cust_pwd = db.Column(db.String(120),nullable=True)
    cust_phone = db.Column(db.String(25),nullable=True)
    cust_dob =db.Column(db.Date(),nullable=True)
    cust_address=db.Column(db.String(255),nullable=True)
    #foreign keys
    cust_lgaid =db.Column(db.Integer,db.ForeignKey('lga.lga_id'))
    cust_stateid=db.Column(db.Integer,db.ForeignKey('state.state_id'))
    #set relationships with Lga, State, Bookings,Customer_orders,Cart
    lgadeets = db.relationship('Lga', back_populates="custlga" )
    thestates = db.relationship('State',back_populates='custstate')
    bookdeets=db.relationship('Bookings',back_populates='custbook',cascade="all, delete-orphan")
    myorders=db.relationship('Customer_orders',back_populates='thecustorder')
    mycart = db.relationship('Cart',back_populates='custcart')

class Vendors(db.Model):
    ven_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    ven_name = db.Column(db.String(100),nullable=False)
    ven_salonpix=db.Column(db.String(120),nullable=True)
    ven_workdesc =db.Column(db.Text(),nullable=True)
    ven_email =db.Column(db.String(120))
    ven_pwd=db.Column(db.String(120),nullable=True)
    ven_address=db.Column(db.String(255),nullable=True)
    #foreign keys
    ven_lgaid=db.Column(db.Integer,db.ForeignKey('lga.lga_id'))
    ven_stateid=db.Column(db.Integer,db.ForeignKey('state.state_id'))
    #set relationship with Lga, State, Ven_style,Products
    thelgas = db.relationship('Lga', back_populates='venlgas')
    allstates=db.relationship('State',back_populates='venstates')
    services=db.relationship('Ven_style', back_populates='vendeets')
    prods=db.relationship('Products',back_populates='thevendor')

    ven_socialmedia=db.Column(db.String(120),nullable=True)
    ven_socialmedia2=db.Column(db.String(120),nullable=True)
    ven_phone=db.Column(db.String(25),nullable=True)
    ven_regdate=db.Column(db.DateTime(),default=datetime.utcnow)

class Styles(db.Model):
    style_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    style_name=db.Column(db.String(100),nullable=False)
    #set relationship with Ven_style
    ven_stylesdeets=db.relationship('Ven_style',back_populates='allstyles')

class Ven_style(db.Model):
    ven_styleid=db.Column(db.Integer, autoincrement=True,primary_key=True)
    venstyle_styleid=db.Column(db.Integer,db.ForeignKey('styles.style_id'),nullable=False)
    venstyle_amt=db.Column(db.Float,nullable=True)
    venstyle_pic=db.Column(db.String(120),nullable=True)
    venstyle_vid=db.Column(db.String(120),nullable=True)
    venstyle_desc =db.Column(db.String(255),nullable=True)
    venstyle_vendorid=db.Column(db.Integer,db.ForeignKey('vendors.ven_id'))
    venstyle_status=db.Column(db.Enum('1','0'),nullable=False,server_default=("0"))
    #set relationship with Vendors, Styles,Bookings
    vendeets = db.relationship('Vendors', back_populates='services')
    allstyles = db.relationship('Styles',back_populates='ven_stylesdeets')
    bookservice=db.relationship('Bookings',back_populates='stylepref')

class Bookings(db.Model):
    booking_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    booking_date=db.Column(db.Date(),nullable=True)
    booking_time=db.Column(db.Time(),nullable=True)
    booking_status=db.Column(db.Enum('1','0'),nullable=False,server_default=("0"))
    #confirmed = 1, cancelled = 0
    booking_type=db.Column(db.Enum('home service','salon visit'),nullable=False,server_default=("salon"))
    #foreign keys
    booking_custid=db.Column(db.Integer,db.ForeignKey('customers.cust_id'))
    booking_venstyleid=db.Column(db.Integer,db.ForeignKey('ven_style.ven_styleid'))
    #set relationship with Customers, Ven_style
    custbook = db.relationship('Customers', back_populates='bookdeets')
    stylepref = db.relationship('Ven_style',back_populates='bookservice')
    theorderdet=db.relationship('Order_details',back_populates='bookinglink')
    cartbook=db.relationship('Cart',back_populates='itembook')

class State(db.Model):
    state_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name=db.Column(db.String(100),nullable=False)
    #set relationship with Lga, Customer, Vendor
    lgas = db.relationship('Lga',back_populates='statedeets')
    custstate=db.relationship('Customers',back_populates='thestates')
    venstates=db.relationship('Vendors',back_populates='allstates')

class Lga(db.Model):
    lga_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    lga_name = db.Column(db.String(100),nullable=False)
    lga_stateid = db.Column(db.Integer, db.ForeignKey('state.state_id'))
    #set relationship with state
    statedeets = db.relationship('State', back_populates='lgas')
    #set relationship with customers
    custlga = db.relationship('Customers',back_populates="lgadeets")
    #set relationship with vendors
    venlgas =db.relationship('Vendors',back_populates='thelgas')

class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)

class Messages(db.Model):
    msg_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    msg_email=db.Column(db.String(100),nullable=False)
    msg_content=db.Column(db.Text(),nullable=False)
    msg_date=db.Column(db.DateTime(),default=datetime.utcnow)

class Category(db.Model):
    cat_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_name=db.Column(db.String(50), nullable=True)
    thecat=db.relationship('Products',back_populates="catdeets")

class Products(db.Model):
    prod_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    prod_name=db.Column(db.String(100),nullable=True)
    prod_desc=db.Column(db.Text(),nullable=True)
    prod_catid=db.Column(db.Integer(),db.ForeignKey('category.cat_id'), nullable=False)
    prod_amt=db.Column(db.Float,nullable=True)
    prod_pic=db.Column(db.String(120),nullable=True)
    prod_qty=db.Column(db.Integer(),nullable=False)
    prod_venid=db.Column(db.Integer(),db.ForeignKey('vendors.ven_id'), nullable=False)
    #set relationships
    catdeets = db.relationship('Category',back_populates="thecat")
    thevendor=db.relationship('Vendors',back_populates='prods')
    orderlink=db.relationship('Order_details',back_populates='prodets')
    custprod=db.relationship('Cart',back_populates='itemprod')

class Order_details(db.Model):
    order_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_prodid=db.Column(db.Integer(),db.ForeignKey('products.prod_id'), nullable=False)
    order_prodqty=db.Column(db.Integer(),nullable=True)
    order_bookid=db.Column(db.Integer(),db.ForeignKey('bookings.booking_id'), nullable=False)
    order_amt=db.Column(db.Float,nullable=True)
    #set relationships
    prodets=db.relationship('Products',back_populates='orderlink')
    bookinglink=db.relationship('Bookings',back_populates='theorderdet')


class Customer_orders(db.Model):
    custorder_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    custorder_date=db.Column(db.DateTime(),default=datetime.utcnow)
    custorder_totalamt=db.Column(db.Float,nullable=True)
    custorder_status=db.Column(db.Enum('1','0'),nullable=False,server_default=("0"))
    order_custid=db.Column(db.Integer(),db.ForeignKey('customers.cust_id'), nullable=False)
    #the relationship
    thecustorder=db.relationship('Customers',back_populates='myorders')
    paydeets=db.relationship('Payment',back_populates='odetails')

class Payment(db.Model):
    pay_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pay_ref=db.Column(db.String(255),nullable=True)
    pay_amt=db.Column(db.Float,nullable=True)
    pay_status=db.Column(db.Enum('success','pending','failed'),nullable=False,server_default=("pending"))
    pay_date=db.Column(db.DateTime(),default=datetime.utcnow)
    pay_custorderid=db.Column(db.Integer(),db.ForeignKey('customer_orders.custorder_id'), nullable=False)
    #the relationship
    odetails = db.relationship('Customer_orders',back_populates='paydeets')

class Cart(db.Model):
    cart_id =db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # cartitem_img = db.Column(db.String(120),nullable=True)
    cartitem_prodid =db.Column(db.Integer(),db.ForeignKey('products.prod_id'), nullable=True)
    cartitem_bookid=db.Column(db.Integer(),db.ForeignKey('bookings.booking_id'), nullable=True)
    # cartitem should be either booking id or product id. 
    #cart dets will only dislpay the booking info or the product info
    cartitem_price=db.Column(db.Float,nullable=True)
    cartitem_qty=db.Column(db.Integer(),nullable=False)
    cartitem_total=db.Column(db.Float,nullable=True)
    cart_userid=db.Column(db.Integer,db.ForeignKey('customers.cust_id'))
    #relationships
    custcart = db.relationship('Customers',back_populates='mycart')
    itemprod = db.relationship('Products',back_populates='custprod')
    itembook = db.relationship('Bookings',back_populates='cartbook')
    