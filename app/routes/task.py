from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Tasks  

tasks_bp = Blueprint('tasks', __name__)

#Route to show all tasks
@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    tasks = Tasks.query.all()
    return render_template("tasks.html", tasks=tasks)

#Route to add a new task
@tasks_bp.route('/add', methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get("title")

    if title:
        new_task = Tasks(title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", "success")

    return redirect(url_for('tasks.view_tasks'))

#Route to change task status (cycle: Pending -> Working -> Done -> Pending)
@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"]) 
def toggle_status(task_id):
    task = Tasks.query.get(task_id)

    if task:
        if task.status == 'Pending':
            task.status = 'Working'  
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))  

# 🔹 Route to clear all tasks
@tasks_bp.route('/clear', methods=["POST"])
def clear_tasks():
    Tasks.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))
