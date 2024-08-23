from sqlalchemy import Table,Column,String,Integer,select,func

from datetime import datetime
import pytz

from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
indian_time = pytz.timezone('Asia/Kolkata')
class users(db.Model):
    __tablename__='users'
    

    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True, nullable=False)
    mobile_no=db.Column(db.Integer,unique=True, nullable=False)
    purchase=db.Column(db.Integer)
    admin=db.Column(db.String)
    
    created_on = db.Column(db.String, default=datetime.now(indian_time))

class sections(db.Model):
    __tablename__='sections'
    section_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    section_name=db.Column(db.String,nullable=False,unique=True)
    def add_sec(name):
        s=sections(section_name=name)
        db.session.add(s)
        db.session.commit()
    def edit_sec(new,sid):
        n=sections.query.get(sid)
        n.section_name=new
        db.session.commit()
    def del_sec(sid):
        d=sections.query.get(sid)
        db.session.delete(d)
        p=db.session.query(products).filter(products.section_id == sid).all()
        for i in p:
            #t=i.product_id
            #t1=products.query.get(t)
            db.session.delete(i)
        db.session.commit()

class products(db.Model):
    __tablename__='products'
    product_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    product_name=db.Column(db.String,nullable=False,unique=True)
    price=db.Column(db.Integer)
    instock_quantity=db.Column(db.Integer)
    section_id=db.Column(db.Integer,db.ForeignKey('sections.section_id'))
    unit=db.Column(db.String,nullable=False)
    section=db.relationship('sections')
    def add_pro(name,p,q,u,sid):
        pro=products(product_name=name,price=p,instock_quantity=q,section_id=sid,unit=u)
        db.session.add(pro)
        db.session.commit()
        pid = db.session.query(products).order_by(products.product_id.desc()).first()
        return pid.product_id
    def del_pro(pid):
        d=products.query.filter_by(product_id=pid).first()
        db.session.delete(d)
        db.session.commit()
    def edit_pro(name,price,q,u,sid,pid):
        p=products.query.get(pid)
        p.product_name=name
        p.price=price
        p.instock_quantity=q
        p.unit=u
        p.section_id=sid
        db.session.commit()

class Cart(db.Model):
    __tablename__='Cart'
    cart_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,db.ForeignKey('users.username'))
    product_id=db.Column(db.Integer,db.ForeignKey('products.product_id'))
    product_name=db.Column(db.String,db.ForeignKey('products.product_name'))
    section_id=db.Column(db.Integer,db.ForeignKey('sections.section_id'))
    price=db.Column(db.Integer,db.ForeignKey('products.price'))
    quantity=db.Column(db.Integer)
    @classmethod
    def insert_cart(s,user,pid,pname,sid,p,q):
        check_exist=Cart.query.filter_by(product_id=pid).first()
        if check_exist!=None:
            check_exist.quantity=int(check_exist.quantity)+int(q)
        else:
            c=Cart(username=user,product_id=pid,product_name=pname,section_id=sid,price=p,quantity=q)
            db.session.add(c)
            db.session.commit()

        i=products.query.filter_by(product_id=pid).first()
        i.instock_quantity=int(i.instock_quantity)-int(q)
        db.session.commit()
    def del_cart(username):
        car=Cart.query.filter_by(username=username).all()
        for i in car:
            db.session.delete(i)
        db.session.commit()
class purchases(db.Model):
    __tablename__='purchases'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    purchase_id=db.Column(db.Integer,nullable=False)
    username=db.Column(db.String,db.ForeignKey('users.username'))
    product_id=db.Column(db.Integer,db.ForeignKey('products.product_id'))
    product_name=db.Column(db.String,db.ForeignKey('products.product_name'))
    section_id=db.Column(db.Integer,db.ForeignKey('sections.section_id'))
    price=db.Column(db.Integer,db.ForeignKey('products.price'))
    quantity=db.Column(db.Integer)
    amount=db.Column(db.Integer)

    def add_purchase(username,pid,pname,sid,price,quantity,purid,amt):
        u=purchases(purchase_id=purid,username=username,product_id=pid,product_name=pname,section_id=sid,price=price,quantity=quantity,amount=amt)
        db.session.add(u)
        
        db.session.commit()
class role(db.Model):
    id=db.Column(db.String,primary_key=True)
    name=db.column(db.String)
    desc=db.column(db.string)
