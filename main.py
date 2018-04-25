from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'password'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

  

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'GET':
        if 'id' in request.args:
            blog_id = request.args.get('id')
            blogpost = Blog.query.filter_by(id = blog_id)
            return render_template('blog.html', blog_id=blog_id, blogpost=blogpost)
             
        else:     
            blogposts = Blog.query.all()
        return render_template('mainblog.html', blogposts=blogposts)


    
    else:
        title_error = ''
        body_error = ''
        authorchangethis = 'change this' #change this and in the Blog call below
        title_name = request.form['title']
        body_content = request.form['body']
        if title_name == '':
                title_error = "Please enter a title"
        if body_content == '':
            body_error = "Please enter content"
        
        rules = (body_error == '', title_error == '')

        if all(rules):
            new_blog = Blog(title_name, body_content, authorchangethis)
            db.session.add(new_blog)
            db.session.commit()
            blogposts = Blog.query.all()
            id = new_blog.id
            return redirect('/?id=' + str(id))
        

    return render_template('newpost.html', title_error=title_error, body_error=body_error) 

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    
    return render_template('newpost.html')
    
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect("/")
            #remember user
        else:
            #tell them why it failed
            return '<h1>Error: No user exists</h1>'
    return render_template("login.html")

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        username_error = ''
        password_error = ''
        confirm_error = ''
        existing_error = ''

        if username == '':
            username_error = "This is not a valid username"
        if ' ' in username:
            username_error = "This is not a valid username"
        if password == '':
            password_error = "This is not a valid password"
        if ' ' in password:
            password_error = "This password is invalid"
        if len(username) < 3:
            username_error = "This is not a valid username"
        if len(password) < 3:
            password_error = "This is not a valid password"
        if password != confirmpassword:
            confirm_error = "Your passwords don't match"
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            existing_error = ''
        if not existing_user == False:
            existing_error = 'This user already exists'
        
        rules = (username_error == "", password_error == "", 
        confirm_error == "", existing_error == '')
        if all(rules):
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        
        return render_template('signup.html', username_error=username_error, 
        password_error=password_error, confirm_error=confirm_error,
        username=username, existing_error=existing_error)
        #need to verify the passwords match. Check user signup assignment.

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO - remember this user
            return redirect ('/')
        else: 
            #return message that they already exist
            return '<h1>Duplicate User</h1>'

    return render_template('signup.html')

if __name__ == '__main__':
    app.run()