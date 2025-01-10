from flask import Flask, render_template, redirect, request, url_for, flash
from database import db
from models.Task import Task
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Certifique-se de que o nome do arquivo do banco de dados é 'tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chavesecreta1'

db.init_app(app)




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Criação das tabelas ao rodar a aplicação
with app.app_context():
    db.create_all()

# Rota principal para exibir tarefas
@app.route('/')
def index():
    tasks = Task.query.all()  # Carrega todas as tarefas do banco
    return render_template('index.html', tasks=tasks)

# Rota para adicionar uma nova tarefa
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')  # Obtém o título da tarefa
    if not title:
        flash('O título da tarefa é obrigatório!', 'error')  # Exibe um erro se o título não for fornecido
        return redirect(url_for('index'))

    new_task = Task(title=title)  # Cria uma nova tarefa
    db.session.add(new_task)  # Adiciona a nova tarefa ao banco
    db.session.commit()  # Confirma a transação
    flash('Tarefa adicionada com sucesso!', 'success')  # Exibe uma mensagem de sucesso
    return redirect(url_for('index'))  # Redireciona para a página principal

# Rota para excluir uma tarefa
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)  # Encontra a tarefa pelo ID
    if task:
        db.session.delete(task)  # Deleta a tarefa
        db.session.commit()  # Confirma a transação
        flash('Tarefa excluída com sucesso!', 'success')  # Exibe mensagem de sucesso
    else:
        flash('Tarefa não encontrada.', 'error')  # Caso não encontre a tarefa
    return redirect(url_for('index'))  # Redireciona para a página principal


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido. Tente novamente.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Olá, {current_user.username}! Bem-vindo ao painel.'






if __name__ == '__main__':
    app.run(debug=True)
