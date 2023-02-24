from flask import Flask,render_template,request,session,url_for,flash,redirect
from werkzeug.security import generate_password_hash,check_password_hash
#local imports
from curlsapp import app,db
from curlsapp.models import Admin,Vendors,Styles,Ven_style,Category


@app.route('/admin/register/',methods=["GET","POST"])
def admin_reg():
    if request.method=="GET":
        return render_template('admin/adminreg.html')
    else:
        uname=request.form.get('username')
        pwd=request.form.get('password')
        hashed_pwd = generate_password_hash(pwd)
        #insert into db using ORM, create an instance, assign attributes,add,commit.
        if uname !='' and pwd !='':
            ad=Admin(admin_username=uname,admin_pwd=hashed_pwd)
            db.session.add(ad)
            db.session.commit()
            return redirect(url_for('admin_login'))
        else:
            flash("All fields required")
            return redirect(url_for('admin_reg'))

@app.route('/admin/login/',methods=["POST","GET"])
def admin_login():
    if request.method=="GET":
        return render_template('admin/adminlogin.html')
    else:
        username=request.form.get('username')
        pwd=request.form.get('password')
        #check if user exists in db, then compare passwords and save the session in id. then redirect to dashboard
        udeet = db.session.query(Admin).filter(Admin.admin_username==username).first()
        if udeet !=None:
            pwd_indb=udeet.admin_pwd
            chk = check_password_hash(pwd_indb,pwd)
            if chk:
                id=udeet.admin_id
                session['admin']=id
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid Credentials")
                return redirect(url_for('admin_login'))
        else:
            return redirect(url_for('admin_login'))



@app.route('/admin/dashboard/')
def admin_dashboard():
    if session.get('admin') !=None:
        id = session['admin']
        adeets=db.session.query(Admin).get(id)
        return render_template('admin/admin_dashboard.html',adeets=adeets)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/logout/')
def admin_logout():
    if session.get('admin') !=None:
        session.pop('admin',None)
    return redirect(url_for('admin_login'))

@app.route('/admin/managevendors')
def manage_vendors():
    id = session['admin']
    if id == None:
        return redirect(url_for('admin_login'))
    else:
        vdata=Ven_style.query.all()
        return render_template('admin/manage_vendors.html',vdata=vdata)

@app.route('/admin/vetvendors/<venid>/')
def vet_vendorservices(venid):
    if session.get('admin') !=None:
        vdeet =Ven_style.query.get(venid)
        return render_template('admin/vet_vendorservice.html',vdeet=vdeet)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/deleteven_service/<venid>')
def del_venservice(venid):
    if session.get('admin') !=None:
        vdeet =Ven_style.query.get_or_404(venid)
        db.session.delete(vdeet)
        db.session.commit()
        flash('Vendor service deleted successfully')
        return redirect(url_for('manage_vendors'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/update_venstatus',methods=["POST", "GET"])
def update_venstatus():
    if session.get('admin') !=None:
        newstatus = request.form.get('status')
        styleid = request.form.get('styleid')
        s = db.session.query(Ven_style).get(styleid)
        s.venstyle_status=newstatus
        db.session.commit()
        flash("Vendor style status successfully updated, the vendor can view services now")
        return redirect(url_for('manage_vendors'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/services/',methods=["POST","GET"])
def services():
    if session.get('admin') ==None:
        return redirect(url_for('admin_login'))
    else:
        if request.method=="GET":
            data=db.session.query(Styles).all()
            return render_template('admin/addservices.html',data=data)
        else:
            sname=request.form.get("stylename")
            if sname !="":
                sty=Styles(style_name=sname)
                db.session.add(sty)
                db.session.commit()
                flash("Service added successfully")
                return redirect(url_for('services'))
            else:
                return redirect(url_for('services'))

@app.route('/admin/services/delete/<id>')
def delete_services(id):
    if session.get('admin') ==None:
        return redirect(url_for('admin_login'))
    else:
        #retrieve the style as an object
        styobj=Styles.query.get_or_404(id)
        db.session.delete(styobj)
        db.session.commit()
        flash("Style Deleted Successfully")
        return redirect(url_for('services'))

@app.route('/admin/allcostumers')
def all_customers():
    return render_template('admin/all_customers.html')

@app.route('/admin/product_category',methods=["POST","GET"])
def add_prodcategory():
    if session.get('admin') ==None:
        return redirect(url_for('admin_login'))
    else:
        if request.method=="GET":
            data=db.session.query(Category).all()
            return render_template('admin/add_productcategory.html',data=data)
        else:
            cat=request.form.get("catname")
            if cat != '':
                c=Category(cat_name=cat)
                db.session.add(c)
                db.session.commit()
                flash("Service added successfully")
                return redirect(url_for('add_prodcategory'))
            else:
                return redirect(url_for('add_prodcategory'))

@app.route('/admin/product_category/delete/<id>')
def delete_category(id):
    if session.get('admin') ==None:
        return redirect(url_for('admin_login'))
    else:
        #retrieve the cat as an object
        catobj=Category.query.get_or_404(id)
        db.session.delete(catobj)
        db.session.commit()
        flash("Category Deleted Successfully")
        return redirect(url_for('add_prodcategory'))