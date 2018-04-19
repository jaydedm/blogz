from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'password'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
  

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
        title_name = request.form['title']
        body_content = request.form['body']
        if title_name == '':
                title_error = "Please enter a title"
        if body_content == '':
            body_error = "Please enter content"
        
        rules = (body_error == '', title_error == '')

        if all(rules):
            new_blog = Blog(title_name, body_content)
            db.session.add(new_blog)
            db.session.commit()
            blogposts = Blog.query.all()
            id = new_blog.id
            return redirect('/?id=' + str(id))
        

    return render_template('newpost.html', title_error=title_error, body_error=body_error) 

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    
    return render_template('newpost.html')
    


if __name__ == '__main__':
    app.run()