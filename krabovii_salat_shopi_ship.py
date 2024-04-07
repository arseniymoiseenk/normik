from flask import Flask,render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///company.db"
db = SQLAlchemy(app)

project_worker_association = db.Table(
    "project_worker",
    db.Column("project_id", db.Integer, db.ForeignKey("project.id")),
    db.Column("worker_id", db.Integer, db.ForeignKey("worker.id"))
)
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    projects = db.relationship("Project", backref="company", lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    workers = db.relationship("Worker",
                               secondary=project_worker_association,
                               backref="projects")
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/workers_by_company/<int:company_id>")
def workers_by_company(company_id):
    company = Company.query.get(company_id)
    if company:
        workers = [worker.name for project in company.projects for worker in project.workers]
        return jsonify(workers)
    else:
        return "Company not found"

@app.route("/projects_by_worker/<int:worker_id>")
def projects_by_worker(worker_id):
    worker = Worker.query.get(worker_id)
    if worker:
        projects = [project.name for project in worker.projects]
        return jsonify(projects)
    else:
        return "Worker not found"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)