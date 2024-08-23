
from flask import Flask,render_template,request,url_for,redirect
from flask_wtf import FlaskForm
from app import app
import os
import re

from wtforms import StringField,PasswordField,IntegerField,validators
from wtforms.validators import InputRequired,Length,DataRequired,Email
from flask_wtf.file import FileField, FileAllowed
from application.models import db,func,Cart,users,sections,products,purchases


class User_Login(FlaskForm):
  username=StringField('Username',render_kw={"placeholder": "Enter your username"},validators=[InputRequired()])
  password=PasswordField('Password',render_kw={"placeholder": "Enter your password"},validators=[InputRequired(),Length(min=3, max=12)])
class Admin_Login(FlaskForm):
  username=StringField('Username',render_kw={"placeholder": "Enter your username"},validators=[InputRequired()])
  password=PasswordField('Password',render_kw={"placeholder": "Enter your password"},validators=[InputRequired(), Length(min=3, max=12)])



class new_user(FlaskForm):
  username=StringField('Username',render_kw={"placeholder": "Create your username"},validators=[InputRequired()])
  password=PasswordField('Password',render_kw={"placeholder": "Create your password"},validators=[InputRequired(),Length(min=3, max=12)])
  first_name=StringField('First Name',render_kw={"placeholder": "Enter your first name"},validators=[InputRequired(),Length(max=20)])
  last_name=StringField('Last Name',render_kw={"placeholder": "Enter your last name"},validators=[InputRequired(),Length( max=20)])

  email=StringField('Email',render_kw={"placeholder": "123@example.com"},validators=[Email(),InputRequired()])
  mobile_no=IntegerField('Mobile number',render_kw={"placeholder": "xxxxxxxxxx"},validators=[InputRequired(),Length(10),validators.NumberRange(min=1000000000,max=9999999999)])



class Section(FlaskForm):
  section_name=StringField('Section name',render_kw={"placeholder": "Enter section name"},validators=[InputRequired()])
class product(FlaskForm):
  product_name=StringField('Product name : ',render_kw={"placeholder": "Enter product name"},validators=[InputRequired()]) 
  price=IntegerField('price : ',render_kw={"placeholder": "Enter price per unit"},validators=[InputRequired(),validators.NumberRange(min=0, message="Minimum price is 0")])
  quantity=IntegerField('quantity : ',render_kw={"placeholder": "Enter instock quantity"},validators=[InputRequired(),validators.NumberRange(min=0, message="Minimum instock quantity is 0")])
  unit = StringField( render_kw={"placeholder": "Ex: liter,kg,200g etc.."},validators=[DataRequired()])
  image = FileField('Select an image', validators=[
        FileAllowed(['jpg', 'jpeg'], 'Only JPEG image are allowed.')
    ])


def valid_email(email):
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False
@app.route('/', methods=['GET','POST'])
def user_login():
  f=User_Login()
  if request.method=='GET':
    return render_template('user_login.html',form=f)
  if request.method=='POST':
    
     
      m=f.username.data
      n=f.password.data
      u=users.query.get(m)
     
      if u and u.password==n:
        
        return redirect(url_for('user_dashboard',username=u.username))
  r="Either username or password is incorrect. Please try again."    
  return render_template('user_login.html',form=f,r=r)
@app.route('/admin_login',methods=['GET','POST'])
def admin():
  a=Admin_Login()
  if request.method=='GET':
    return render_template('admin_login.html',form=a)
  if request.method=='POST':
    x=a.username.data
    y=a.password.data
    z=users.query.get(x)
    if z and z.password==y and z.admin=='true':
       return redirect(url_for('admin_dashboard',username=x))
    elif z and z.password==y and z.admin!='true':
      r="You don't have admin access!"
      return render_template('admin_login.html',form=a,r=r)
    else:
      r="Either username or password is incorrect. Please try again."
      return render_template('admin_login.html',form=a,r=r)
@app.route('/new_user',methods=['GET','POST'])
def new():
  n=new_user()
  if request.method=='GET':
    return render_template('new_user.html',form=n) 
  else:
    if not valid_email(n.email.data):
      err="Please enter valid Email address"
      return render_template('new_user.html',form=n,err=err)
    user=db.session.query(users).all()
    flag=False
    r=''
    r1=''
    r2=''
    for i in user:
      if i.username==n.username.data:
        r="username  "
        flag=True
      if i.email==n.email.data:
        r1="Email   "
        flag=True
      if i.mobile_no==n.mobile_no.data:
        r2="Mobile number   "
        flag=True
      if flag:
        err=r+r1+r2+"already exist"
        return render_template('new_user.html',form=n,err=err)
    s=users(username=n.username.data,password=n.password.data,first_name=n.first_name.data,last_name=n.last_name.data,email=n.email.data,mobile_no=n.mobile_no.data,purchase=0)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('user_login'))

#****************************USER SIDE********************************************************************


@app.route('/<username>',methods=['POST','GET'])
def user_dashboard(username):
   nammm=users.query.filter_by(username=username).first()
  
   
   if request.method=='POST':
    if request.form.get('search')=="SEARCH":
    
      u=users.query.get(username)
      key=request.form.get('Search')
      sec=None
      prod=None
      pri=None
      l1=[]
      p1=[]
      temp_pid={}
      if key.isalpha():
        sec = sections.query.filter(sections.section_name.like("%" + key + "%")).all()
        prod = products.query.filter(products.product_name.like("%" + key + "%")).all()
        for i in range(len(sec)):
          l1.append([sec[i].section_id,sec[i].section_name])
    
      
        for i in sec:
          pro1=db.session.query(products).filter(products.section_id==i.section_id).all()
          q1=[]
          for j in pro1:
            q1.append([j.product_name,j.price,j.product_id,j.unit])
          p1.append(q1)
      
        for i in prod:
          for j in l1:
            if i.section_id==j[0]:
              break
          else:
            if i.section_id in temp_pid.keys():
              temp_pid[i.section_id].append(i.product_id)
            else:
              temp_pid[i.section_id]=[i.product_id]
      if key.isdigit():
        pri = products.query.filter(products.price <= int(key)).all()
        
      
     
        for i in pri:
          
            if i.section_id in temp_pid.keys():
              temp_pid[i.section_id].append(i.product_id)
            else:
              temp_pid[i.section_id]=[i.product_id]
      
      for key in temp_pid:
        secname=sections.query.get(key)
        l1.append([key,secname.section_name])
        pr=[]
        for val in temp_pid[key]:
          
          pro2=db.session.query(products).filter(products.product_id==val).first()
          pr.append([pro2.product_name,pro2.price,pro2.product_id,pro2.unit])
        p1.append(pr)
      if len(p1)>1:   
        r="Your search result matches with "+str(len(p1))+" sections !"
      elif len(p1)<1:
        r="Sorry. No matched results"
      else:
        r="Your search result matches with "+str(len(p1))+" section !"
      na=db.session.query(users).filter(users.username==username).first()
      namm=nammm.first_name+nammm.last_name
      return render_template('user_dashboard.html',username=username,sections=l1,products=p1,r=r,name=namm)
    if request.form.get('Cart')=="CART":
     return redirect(url_for('cart',username=username))
   
   uu=users.query.get(username)
   s=db.session.query(sections.section_id).all()
   sn=db.session.query(sections.section_name).all()
   l=[]
   for i in range(len(s)):
     l.append([s[i][0],sn[i][0]])
    
   
 
   p=[]
   for i in s:
     pro=db.session.query(products).filter(products.section_id==i[0]).all()
     q=[]
     for j in pro:
      q.append([j.product_name,j.price,j.product_id,j.unit,j.instock_quantity])
     p.append(q)

   if nammm!=None:
    namm=nammm.first_name+nammm.last_name
    return render_template('user_dashboard.html',username=username,sections=l,products=p,name=namm)
   
   return render_template('user_dashboard.html',username=username,sections=l,products=p)
    
  




@app.route('/cart/<username>',methods=['POST','GET'])
def cart(username):
  global pur_id
  c=db.session.query(Cart).filter(Cart.username == username).all()
  length=len(c)
  pur_id=users.query.get(username)
  ca=[]
  amt=0
  for i in c:
      ca.append([i.product_name,i.price,i.quantity])
      amt+=int(i.price)*int(i.quantity)
  
    
    
  if request.method=='POST':
    
    if request.form.get('action')=='checkout':
      pur_id.purchase+=1
      db.session.commit()
      
      id=pur_id.purchase
      for i in c:
        purchases.add_purchase(username,i.product_id,i.product_name,i.section_id,i.price,i.quantity,id,amt)
      Cart.del_cart(username)
      return redirect(url_for('user_dashboard',username=username))
    if request.form.get('action')=='buymore':
      return redirect(url_for('user_dashboard',username=username))
  return render_template('cart.html',username=username,ca=ca,amount=amt,length=length)
@app.route('/<username>/<int:section_id>/<product_id>', methods=['POST','GET'])
def buy(username,section_id,product_id):
  s=sections.query.get(section_id)
  p=db.session.query(products).filter(products.product_id==product_id).first()
  if request.method=='GET':
    
    return render_template('buy.html',sname=s.section_name,pname=p.product_name,price=p.price,unit=p.unit,username=username,sid=section_id,pid=product_id,v=1)
  else:
     quan=request.form.get('quantity')
     
     if int(quan)<=p.instock_quantity:
        amoun=(int(quan))*(int(p.price))
        amount="Total amount : Rs."+str(amoun)
     else:
        amount="The required quantity is not available"
     if request.form.get('action')=="amount":
      
      return render_template('buy.html',sname=s.section_name,pname=p.product_name,price=p.price,unit=p.unit,username=username,sid=section_id,v=quan,amount=amount)
     if request.form.get('action')=="cart":
       p1=p.product_name
       p2=p.price
       Cart.insert_cart(username,product_id,p1,section_id,p2,quan)
   
       return redirect(url_for('user_dashboard',username=username))
@app.route('/profile/<username>')
def profile(username):
  u=db.session.query(purchases).filter(purchases.username == username).all()
  length=len(u)

  
  dict={}
  for i in u:
    
    
    if i.purchase_id in dict.keys():
      dict[i.purchase_id][1].append((i.product_name,i.quantity,i.price*i.quantity))
    else:
      dict[i.purchase_id]=[i.amount,[(i.product_name,i.quantity,i.price*i.quantity)]]
  return render_template('profile.html',username=username,purchase=dict,length=length)  


# ********************************ADMIN SIDE ********************************************************

@app.route('/admin_login/<username>',methods=['GET','POST'])  
def admin_dashboard(username):
   nam=users.query.get(username)
   na=nam.first_name+nam.last_name
   uu=users.query.get(username)
   s=db.session.query(sections.section_id).all()
   sn=db.session.query(sections.section_name).all()
   l=[]
   for i in range(len(s)):
     l.append([s[i][0],sn[i][0]])
    
   
 
   p=[]
   for i in s:
     pro=db.session.query(products).filter(products.section_id==i[0]).all()
     q=[]
     for j in pro:
      q.append([j.product_name,j.price,j.product_id,j.unit,j.instock_quantity])
     p.append(q)  
   
   return render_template('admin_dashboard.html',username=username,sections=l,products=p,name=na)

@app.route('/admin_login/<username>/add_section',methods=['GET','POST'])
def add_section(username):
  s=Section()
  section=db.session.query(sections.section_name).all()
  if request.method=='GET':
    return render_template('add_section.html',username=username,form=s)
  else:
    
    sec_name=s.section_name.data
    for i in section:
      if i[0].lower()==sec_name.lower():
        err="Section already exist. Try using a different name."
        return render_template('add_section.html',username=username,form=s,err=err)
    sections.add_sec(sec_name)
    
    
    return redirect(url_for('admin_dashboard',username=username))
  
@app.route('/admin_login/<username>/edit_section/<sec_id>',methods=['GET','POST'])
def edit_section(username,sec_id):
  namm=sections.query.filter_by(section_id=sec_id).first()
  section=db.session.query(sections.section_name).all()

  
  if request.method=='GET':
    
    return render_template('edit_section.html',username=username,sec_name=namm.section_name)
  else:
    new=request.form.get('edit_sectio')
    for i in section:
      if i[0].lower()==new.lower():
        err="Section already exist. Try changing to a different name."
        return render_template('edit_section.html',username=username,sec_name=namm.section_name,err=err)
    sections.edit_sec(new,sec_id)
    return redirect(url_for('admin_dashboard',username=username))
  
@app.route('/admin_login/<username>/del_section/<sec_id>',methods=['GET','POST'])
def del_section(username,sec_id):
  
  p=db.session.query(products).filter(products.section_id == sec_id).all()
  
  for i in p:
    pid=str(i.product_id)+".jpg"
    path=os.path.join('static', pid)
    
    if os.path.isfile(path):
      
      os.remove(path)
  sections.del_sec(sec_id)

  return redirect(url_for('admin_dashboard',username=username))
  

@app.route('/admin_login/<username>/add_product/<sec_id>',methods=['GET','POST'])
def add_product(username,sec_id):
  p=product()
  if request.method=='GET':
    return render_template('add_product.html',username=username,form=p)
  else:
    p=product()
    PRODUCT=db.session.query(products.product_name).all()
    
    pname=p.product_name.data
    for i in PRODUCT:
      if i[0].lower()==pname.lower():
        err="Product already exist. Try using a different name."
        return render_template('add_product.html',username=username,form=p,err=err)
    price=p.price.data
    q=p.quantity.data
    u=p.unit.data
    pid=products.add_pro(pname,price,q,u,sec_id)
    pid1=str(pid)+'.jpg'
    img=p.image.data
    if img != None:
      img.save(os.path.join('static',pid1))
    return redirect(url_for('admin_dashboard',username=username))
  



@app.route('/admin_login/<username>/edit/<section_id>/<product_id>', methods=['GET','POST'])
def edit_product(username,section_id,product_id):
  p=products.query.get(product_id)
  if request.method=='GET':
    
    return render_template('edit_product.html',name=p.product_name,price=p.price,quantity=p.instock_quantity,unit=p.unit,sid=p.section_id)
  if request.method=='POST':
    pro_name=request.form.get('product_name')
    price=request.form.get('price')
    q=request.form.get('quantity')
    sid=request.form.get('sid')
    u=request.form.get('unit')

    if sid!=section_id:
      
      SECTION=db.session.query(sections.section_id).all()
      
      for i in SECTION:
        
        if i[0]==int(sid):
          break  
          
      else:
        err="Section ID doesn't exist. Try moving to different section"
        return render_template('edit_product.html',err=err,name=p.product_name,price=p.price,quantity=p.instock_quantity,unit=p.unit,sid=p.section_id)


      

    if pro_name!=p.product_name:
      PRODUCT=db.session.query(products.product_name).all()
      for i in PRODUCT:
        if i[0].lower()==pro_name.lower():
          err="Product already exist. Try changing to a different name."
          return render_template('edit_product.html',err=err,name=p.product_name,price=p.price,quantity=p.instock_quantity,unit=p.unit,sid=p.section_id)
    
    products.edit_pro(pro_name,price,q,u,sid,product_id)
    pid=str(product_id)+'.jpg'
    img=request.files['image']
    if img.filename !='':
      
      if os.path.isfile(os.path.join('static', pid)):
        os.remove(os.path.join('static', pid))
      img.save(os.path.join('static',pid))
    
    return redirect(url_for('admin_dashboard',username=username))
  



    

@app.route('/admin_login/<username>/delete/<sec_id>/<product_id>',methods=['GET','POST'])
def del_product(username,sec_id,product_id):
  if request.method=='GET':
    products.del_pro(product_id)
    p=str(product_id)+'.jpg'
    path=os.path.join('static', p)
    if os.path.isfile(path):
      os.remove(path)
    return redirect(url_for('admin_dashboard',username=username))
@app.route('/admin_login/<username>/statistics')
def statistics(username):
  dict={'Top users':[],'Demanded sections':[],'Frequently Bought products':[]}
  max_value = db.session.query(func.max(users.purchase)).scalar()

  
  rows = db.session.query(users).filter_by(purchase=max_value).all()
  for i in rows:
    dict['Top users'].append(i.username)
  sid = db.session.query(purchases.section_id, func.count(purchases.section_id)) .group_by(purchases.section_id).order_by(func.count(purchases.section_id).desc()).all()
  for i in sid:
    sname=sections.query.get(i[0])
    dict['Demanded sections'].append(sname.section_name)
    t=sid.index(i)+1
    if t<len(sid) and i[1]==sid[t][1]:
      continue
    else:
      break
  pid = db.session.query(purchases.product_id, func.count(purchases.product_id)) .group_by(purchases.product_id).order_by(func.count(purchases.product_id).desc()).all()
  for i in pid:
    pname=products.query.get(i[0])
    dict['Frequently Bought products'].append(pname.product_name)
    t=pid.index(i)+1
    if t<len(pid) and i[1]==pid[t][1]:
      continue
    else:
      break
  
  return render_template('statistics.html',dict=dict)
@app.route('/admin_login/<username>/delall')
def delall(username):
  s=sections.query.all()
  s1=db.session.query(sections).all()
  print(s1)
  for i in s:
    sections.del_sec(i.section_id)
  return redirect(url_for('admin_dashboard',username=username))






