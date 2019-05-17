from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildme@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blog.html',title="Build-A-Blog")

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        add_entry = Blog(title, body)
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

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        blog_id = request.args.get(add_entry)
        blog_entries = Blog.query.all()

    return render_template('blog.html', blog=blog_entries)

if __name__ == '__main__':
    app.run()
