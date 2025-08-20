from flask import Blueprint, render_template, redirect, url_for, request
from .models import Task
from .database import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@main.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        if title.strip():
            new_task = Task(title=title)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add_task.html")

@main.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("main.index"))
