from flask import Flask ,render_template, url_for,redirect,flash,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin ,LoginManager ,login_user,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField , RadioField  , IntegerField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate
from flask_wtf.file import FileField,FileAllowed
from wtforms.widgets import TextArea
import secrets
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_BINDS']={'two':'sqlite:///maintenance.db',
                                'three':'sqlite:///store.db',
                                'four':'sqlite:///sales.db',
                                'five':'sqlite:///custmer.db'}

app.config['SECRET_KEY']="this is my secret key"

bcrypt=Bcrypt(app)

db=SQLAlchemy(app)
migrate=Migrate(app,db)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    
   
    return users.query.get((user_id))

class custmer(db.Model):
    __bind_key__='five'
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(20),nullable=False)
    secondname=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(80),nullable=False)
    closepoint=db.Column(db.String(80),nullable=False)
    city=db.Column(db.String(20),nullable=False)
    phonenumber=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(20),nullable=False)
    description=db.Column(db.String(20),nullable=False)
    


class sales(db.Model):
    __bind_key__='four'
    id=db.Column(db.Integer,primary_key=True)
    devicename=db.Column(db.String(20),nullable=False)
    shortdesc=db.Column(db.String(100),nullable=False)
    qty=db.Column(db.Integer,default=10 ,nullable=False)
    img_file=db.Column(db.String(80),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    t_price=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
        



class store(db.Model):
    __bind_key__='three'
    id=db.Column(db.Integer,primary_key=True)
    devicename=db.Column(db.String(20),nullable=False)
    shortdesc=db.Column(db.String(100),nullable=False)
    longdesc=db.Column(db.String(255),nullable=False)
    qty=db.Column(db.Integer,default=10 ,nullable=False)
    img_file=db.Column(db.String(80),nullable=False,default='defualt.jpg')
    kind=db.Column(db.String(20),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    

class maintenance(db.Model):
    __bind_key__='two'
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(20),nullable=False)
    secondname=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(80),nullable=False)
    closepoint=db.Column(db.String(80),nullable=False)
    city=db.Column(db.String(20),nullable=False)
    phonenumber=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(20),nullable=False)
    devicename=db.Column(db.String(20),nullable=False)
    description=db.Column(db.String(20),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))


class users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)
    rule=db.Column(db.Boolean(),default=False , nullable=False)
    

class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"الاسم"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"الرمز السري"})
    submit=SubmitField("انشاء حساب")


    def validate_username(self,username):
        existing_users_username=users.query.filter_by(username=username.data).first()

        if existing_users_username:
            raise ValidationError("هذا الاسم موجود بالفعل,اختر اخر")



class storeform(FlaskForm):
    devicename=StringField(validators=[InputRequired(),Length(min=1,max=20)],render_kw={"placeholder":"اسم الجهاز"})
    shortdesc=StringField(widget=TextArea(),render_kw={"placeholder":"نبذة مختصرة"})
    longdesc=StringField(widget=TextArea(),render_kw={"placeholder":"نبذة مطولة"})
    qty=IntegerField(validators=[InputRequired()],render_kw={"placeholder":"الكمية"})
    price=IntegerField(validators=[InputRequired()],render_kw={"placeholder":"السعر"})
    img_file=FileField(validators=[FileAllowed(['jpeg','jfif','jpg','png'])],render_kw={"placeholder":"صورة الجهاز"})
    kind=RadioField('نوع الجهاز', choices=[('الاجهزةالمختبرية','الاجهزةالمختبرية'),('الأجهزةالتشخيصية','الأجهزةالتشخيصية'),('الاجهزةالعلاجية','الاجهزةالعلاجية'),('الاجهزةالمنزلية','الاجهزةالمنزلية')])
    submit=SubmitField("حفظ المعلومات")

class loginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"الاسم"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"الرمز السري"})
    submit=SubmitField("تسجيل الدخول")
    
class custmerform(FlaskForm):
    firstname=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" الاسم الاول"})
    secondname=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" الاسم الثاني"})
    address=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" العنوان"})
    closepoint=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" اقرب نقطة دالة"})
    city=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" المدينة"})
    phonenumber=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":"رقم الهاتف"})
    email=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":"الايميل"})
    description=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" وصف الحالة"})
    submit=SubmitField("اكمال عملية الشراء")



class maintenanceform(FlaskForm):
    firstname=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" الاسم الاول"})
    secondname=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" الاسم الثاني"})
    address=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" العنوان"})
    closepoint=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" اقرب نقطة دالة"})
    city=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" المدينة"})
    phonenumber=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":"رقم الهاتف"})
    email=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":"الايميل"})
    devicename=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" اسم الجهاز"})
    description=StringField(validators=[InputRequired(),Length(min=2,max=20)],render_kw={"placeholder":" وصف الحالة"})
    submit=SubmitField("ارسال")

@app.route('/')

def home():
    
    return render_template('home.html')



@app.route('/login',methods=(['POST','GET']))

def login():
    if current_user.is_authenticated:
        flash("لقد قمت بسجيل الدخول بالفعل")
        return redirect(url_for('home'))
    form=loginForm()
    if form.validate_on_submit():
        user=users.query.filter_by(username=form.username.data).first()
        
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                session["card"]=[]
                return redirect(url_for('home'))
            else :
                flash("اسم المستخدم او الرمز السري خاطئ !")
        else :
            flash("اسم المستخدم او الرمز السري خاطئ !")                
    return render_template('login.html',form=form)


@app.route('/register',methods=(['POST','GET']))
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        new_user=users(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("تم انشاء حسابك بنجاح !")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/sale' ,methods=(['POST','GET']))
@login_required

def sale():
    results=session["card"]    
    items=store.query.order_by(store.id)
    return render_template('sales.html',items=items,results=results)


@app.route('/payment',methods=(['GET','POST']))
@login_required

def payment():
    if session["card"] != [] :
        form=custmerform()
        if form.validate_on_submit():
            
            results=session["card"]
                
            for result in results :
                item = store.query.filter_by(id=result["id"]).first()
                s_price=item.price
                new_sale=sales(devicename=item.devicename,shortdesc=item.shortdesc,img_file=item.img_file,qty=result["qty"],price=s_price,t_price=result["qty"]*s_price ,user_id=current_user.id)
                db.session.add(new_sale)
                db.session.commit()
            new_case=custmer(firstname=form.firstname.data,secondname=form.secondname.data,address=form.address.data,closepoint=form.closepoint.data,city=form.city.data,phonenumber=form.phonenumber.data,email=form.email.data,description=form.description.data)
            db.session.add(new_case)
            db.session.commit()
            session["card"]=[]
            return redirect(url_for('sale')) 
    else :
        flash("لم يتم اختيار اي منتج ") 
        return redirect(url_for('home'))   
    return render_template('payment.html',form=form)



@app.route('/logout' ,methods=(['POST','GET']))
@login_required
def logout():
    logout_user()
    session.pop('card',None)
    flash("تم تسجيل الخروج !")
    return redirect (url_for('home'))

   


@app.route('/maintenance' ,methods=(['POST','GET']))
@login_required    
    
def maintenancee():
    
    form=maintenanceform()
    if form.validate_on_submit():
        new_case=maintenance(firstname=form.firstname.data,secondname=form.secondname.data,address=form.address.data,closepoint=form.closepoint.data,city=form.city.data,phonenumber=form.phonenumber.data,email=form.email.data,devicename=form.devicename.data,description=form.description.data)
        db.session.add(new_case)
        db.session.commit()
        flash("تم ارسال حالتك ,سوف يتم التواصل معك في اقرب وقت")
        return redirect (url_for('home'))
    return render_template('maintenance.html',form=form)


@app.route('/proudcts')
def proudcts():
    items=store.query.order_by(store.id)
    
    
    return render_template('proudcts.html',items=items)

@app.route('/pro2')
def pro2():
    items=store.query.order_by(store.id)
    
    
    return render_template('pro2.html',items=items)

@app.route('/pro3')
def pro3():
    items=store.query.order_by(store.id)
    
    
    return render_template('pro3.html',items=items)

@app.route('/pro4')
def pro4():
    items=store.query.order_by(store.id)
    
    
    return render_template('pro4.html',items=items)

@app.route('/info/<int:id>')
def info(id):
    

    items = store.query.filter_by(id=id).first()
    return render_template('info.html',items=items)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')



@app.route('/admin' ,methods=(['POST','GET']))
@login_required
def admin():
    rule=current_user.rule
    if rule==True :
      
        return render_template('admin.html')
    else :    
        flash("يجب ان تكون ادمن للوصول الى هذه الصفحة")
        return redirect(url_for('home'))
    
@app.route('/users' ,methods=(['POST','GET']))
@login_required
def userss():
    rule=current_user.rule
    if rule==True :
         user=users.query.order_by(users.id)
         return render_template('users.html',user=user) 
    else :    
        flash("يجب ان تكون ادمن للوصول الى هذه الصفحة")
       
    user=users.query.order_by(users.id)
    return render_template('users.html',user=user) 



@app.route('/userdelete/<int:id>')
def userdelete(id):
   
    
    user_to_delete=users.query.get_or_404(id)
    try :
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("تم حذف المستخدم ")
        user=users.query.order_by(users.id)
        return render_template('users.html' ,user=user)
    except :
        flash("حدث خطأ اثناء الحذف")
        return render_template('maintenancefb.html',user=user)


@app.route('/makeadmin/<int:id>')
def makeadmin(id):
   
    
    update = users.query.filter_by(id=id).first()
    
    try :
        
        if  update.rule==False :
            update.rule=True
            db.session.commit()
            flash("تم الترقية الى مسؤول ")
            user=users.query.order_by(users.id)
            return render_template('users.html' ,user=user)
        else :
            update.rule=False
            flash("تم سحب الترقية")
            
            db.session.commit()
            user=users.query.order_by(users.id)
            return render_template('users.html' ,user=user)
        
        
        
    except :
    
        flash("حدث خطأ")
        user=users.query.order_by(users.id)
        return render_template('users.html',user=user)

@app.route('/maintenancefb')
@login_required
def maintenancefb():
    rule=current_user.rule
    if rule==True :
        orders=maintenance.query.order_by(maintenance.id)
        return render_template('maintenancefb.html',orders=orders)
    else :    
        flash("يجب ان تكون ادمن للوصول الى هذه الصفحة")
        return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    form=maintenanceform()
    
    user_to_delete=maintenance.query.get_or_404(id)
    try :
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("تم حذف الحالة ")
        orders=maintenance.query.order_by(maintenance.id)
        return render_template('maintenancefb.html' ,orders=orders)
    except :
        flash("حدث خطأ اثناء حذف")
        return render_template('maintenancefb.html',orders=orders)

def save_img(form_img):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_img.filename)
    img_fn=random_hex + f_ext
    img_path=os.path.join(app.root_path,'static/images', img_fn)
    form_img.save(img_path)
    return img_fn
@app.route('/stoage' , methods=(['POST','GET']))
def storage():
    return render_template('storage.html')



@app.route('/additem' ,methods=(['POST','GET']))
@login_required
def additem():
    form=storeform()
    rule=current_user.rule
    
    if rule==True :
        if form.validate_on_submit():
            if form.img_file.data:
                pic_file=save_img(form.img_file.data)
                new_proudct=store(devicename=form.devicename.data,shortdesc=form.shortdesc.data,longdesc=form.longdesc.data,img_file=pic_file,price=form.price.data,qty=form.qty.data,kind=form.kind.data)    
                db.session.add(new_proudct)
                db.session.commit()
                return redirect (url_for('additem'))
            
         
            
            
        return render_template('additem.html',form=form)
         
    else :    
        flash("يجب ان تكون ادمن للوصول الى هذه الصفحة")
        return redirect(url_for('home'))

@app.route('/updateitem/<int:id>' ,methods=(['POST','GET']))
def updateitem(id):
    form=storeform()
    item=store.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.img_file.data:
                pic_file=save_img(form.img_file.data)
                item.devicename=form.devicename.data
                item.shortdesc=form.shortdesc.data
                item.longdesc=form.longdesc.data
                item.qty=form.qty.data
                item.price=form.price.data
                item.kind=form.kind.data
                item.img_file=pic_file
                db.session.commit()
                flash("تم تعديل المعلومات")
                return redirect(url_for('update'))
    form.devicename.data=item.devicename
    form.shortdesc.data= item.shortdesc
    form.longdesc.data=item.longdesc
    form.qty.data=item.qty
    form.price.data=item.price
    form.kind.data=item.kind
    form.img_file.data=item.img_file
    return render_template('updateitem.html',form=form)


@app.route('/update' ,methods=(['POST','GET'])) 
 
def update():
    items=store.query.order_by(store.id)
    return render_template('update.html' ,items=items)


@app.route('/addtocard/<int:id>/<int:qty>' )
def addtocard(id,qty):
    items=session["card"]
    li=[]
    
    for item in items:

        if item.get("id",None)!=id :
            li.append(item)
            print(item)
           
        else :
            item["qty"] =item["qty"]+ qty
            li.append(item) 
    
    if len(items)==0 :
        li.append({"id":id ,"qty":qty})
    elif id not in [obj['id'] for obj in li ] :
        
        li.append({"id":id ,"qty":qty})


    session["card"]=li
   
    print(session["card"])
    return redirect(url_for('proudcts'))



@app.route('/updatecard/<int:id>' , methods=["POST"] )
def updatecard(id):
    qty=int(request.form.get("quantity"))
    print(qty)
    items=session["card"]
    li=[]
    
    for item in items:

        if item.get("id",None)!=id :
            li.append(item)
            print(item)
           
        else :
            item["qty"] =int(item.get("qty",0))+ qty
            li.append(item) 
    
    if len(items)==0 :
        li.append({"id":id ,"qty":qty})
    elif id not in [obj['id'] for obj in li ] :
        
        li.append({"id":id ,"qty":qty})


    session["card"]=li
   
    print(session["card"])
    return redirect(url_for('proudcts'))

if __name__=="__main__":

   app.run(debug=True) 