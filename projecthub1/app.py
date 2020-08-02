from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_desc = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.Integer, primary_key=True)
    project_status = db.Column(db.String(100), nullable=False)
    project_stack = db.Column(db.String(100), nullable=False)
    max_members = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Project %r>' % self.id


@app.route('/')
def index():
    return "Home"


@app.route('/post-project', methods=['POST','GET'])
def post_project():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        client_email = request.form['client_email']

        project = Project(title=title, text=text, client_email=client_email)

        try:
            db.session.add(project)
            return render_template("all-projects.html")
            db.session.commit()
            return redirect('/projects')
        except:
            return "Nothing here. Try add the project again."
    else:
        return render_template("post_project.html")


@app.route('/projects')
def all_projects():
    projects = Project.query.order_by(Project.project_id).all()
    return render_template("all-projects.html", projects=projects)


if __name__ == "__main__":
    app.run(debug=True)

