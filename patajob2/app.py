import os
from flask import Flask,render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm,LoginForm,UpdateAccount
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin





basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

bcrypt = Bcrypt(app)


bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "patajob.sqlite")# Connection to the DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = False
app.config['SECRET_KEY'] = 'topsecret'
login_manager = LoginManager(app)

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    image = db.Column(db.String(20),unique=False,nullable=True, default="default.jpg")
    file_data = db.Column(db.String(20))
    linkedin = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    fb = db.Column(db.String(100))


def _repr_(self):
    return 'User {},{}'.format(self.username,self.image_file,self.password)




@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', title='home Page',users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        #fetching data from the signup form
        full_names =  form.full_names.data
        email = form.email.data
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        #handle database
        new_user = User(full_names=full_names,email=email,password=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        #if successful return the user to login page
        return redirect(url_for('login'))
    return render_template('register.html', form=form , title='Register Page')


@app.route('/login',methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html',form=form)


def save_image(form_picture):
    _,_ext = os.path.splitext(form_picture.filename)
    picture_name = _ + _ext
    picture_path = os.path.join(app.root_path + "/static/images/profile_images", picture_name)
    form_picture.save(picture_path)
    return picture_name


@app.route('/account',methods=['GET','POST'])
def account():
    #get the form from  the front end
    form = UpdateAccount()

    #if the form has data from the user
    if form.validate_on_submit():

        #check the form if it has an image file
        if form.image.data:
            image = save_image(form.image.data)
            current_user.image = image

        # if the form has no image file
        current_user.full_names = form.full_names.data
        current_user.email = form.email.data
        current_user.linkedin = form.linkedin.data
        current_user.twitter = form.twitter.data
        current_user.fb = form.fb.data

        db.session.commit()
        return redirect(url_for('account'))

    form.full_names.data = current_user.full_names
    form.email.data = current_user.email
    print(current_user.image)
    image_file = url_for('static',filename='images/profile_images/'+ current_user.image)
    return render_template('account.html',title ='Account',form=form,image_file=image_file)





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))









if __name__ == '__main__':
    app.run(debug=True,port=3000)
