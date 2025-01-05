from flask import Flask, render_template, redirect,request,url_for, flash
from database import db
from models.Task import Task
    


app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chavesecreta1'

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()



@app.route('/') #Rota principal para exibir tarefas
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods = ['POST'])
def add_task():
    title = request.form.get('title')
    if not title:
        flash('O titulo da tarefa é obrigatório!', 'error')
        return redirect(url_for('index'))

    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    flash('Tarefa adicionada com sucesso', 'success')
    return redirect(url_for('index'))    



if __name__ == '__main__':
    app.run (debug=True)

