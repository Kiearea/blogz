from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz4me@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'h394gILnoPyzie'


class Blogz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogz = db.relationship('Blogz', backref = 'owner') #ties the task to an owner

    def __init__(self, name, password):
        self.namme = name
        self.password = password


@app.route('/')
def index():
    return render_template('index.html')

#Login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def validate_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        username_error = ""
        password_error = ""

    # Do checks
        if username == username_error:
            username_error = "This field cannot be left blank"
        else:
            if len(username) < 3 or len(username) > 20:
                username_error = "Usernames must be between 3 and 20 characters"
            else:
                if username.isspace():
                    username_error = "Usernames cannot contain spaces"

        #password verification
        if password == password_error:
            password_error = "This field cannot be left blank"
        else:
            if len(password) < 3 or len(password) > 20:
                password_error = "Passwords must be between 3 and 20 character"
            else:
                if password.isspace():
                    password_error = "Password cannot contain spaces"

        if not username_error and not password_error:
            return render_template('newpost.html')

    # redirect if errors
        return render_template("login.html",
            username_error=username_error,
            password_error=password_error,
            username=username)

    else:
        return redirect('/login')


#signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def validate_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify_password']

        username_error = ""
        password_error = ""
        verify_error = ""

    # Do checks
        if username == username_error:
            username_error = "This field cannot be left blank"
        else:
            if len(username) < 3 or len(username) > 20:
                username_error = "Usernames must be between 3 and 20 characters"
            else:
                if username.isspace():
                    username_error = "Usernames cannot contain spaces"

        #password verification
        if password == password_error:
            password_error = "This field cannot be left blank"
        else:
            if len(password) < 3 or len(password) > 20:
                password_error = "Passwords must be between 3 and 20 character"
            else:
                if password.isspace():
                    password_error = "Password cannot contain spaces"

        if verify == verify_error:
            verify_error = "This field cannot be left blank"
        else:
            if verify != password:
                verify_error = "Passwords don't match. Please try again"

        if not username_error and not password_error and not verify_error:
            return render_template('newpost.html')

    # redirect if errors
        return render_template("signup.html",
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error,
            username=username)

    else:
        return redirect('/signup')


#New posts
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(name=session['name']).first()
    return render_template('newpost.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        add_entry = Blogz(title, body)
        db.session.add(add_entry)
        db.session.commit()

        title_error = ""
        body_error = ""

        if title == title_error:
            title_error = "This field cannot be left blank"

        if body == body_error:
            body_error = "This field cannot be left blank"

    if not title_error and not body_error:
        return render_template('add_entry.html', title=title, body=body)

    return render_template('newpost.html', title_error=title_error, body_error=body_error)

@app.route('/blogz', methods=['GET', 'POST'])
def blogz():
    if request.method == 'GET':
        blogz_id = request.args.get('id')
        blogz_entries = Blogz.query.all()
        single_entry = Blogz.query.filter_by(id=blogz_id).first()

    return render_template('blogz.html', blogz=blogz_entries, single_entry=single_entry)

@app.route('/logout')
def logout():
    del session['name']
    return redirect('/')

if __name__ == '__main__':
    app.run()
