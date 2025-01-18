from flask import Flask, render_template, redirect, request, url_for, flash
from db import db
from models.Task import Task
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash




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
@login_required
def index():
    tasks = Task.query.all()  # Carrega todas as tarefas do banco
    return render_template('index.html', tasks=tasks)




# Rota para adicionar uma nova tarefa
@app.route('/add_task', methods=['POST'])
@login_required
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
@login_required
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
            return redirect(url_for('index'))
        else:
         flash('Login inválido. Tente novamente.')
    return render_template('login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # Obtém os dados do formulário
        name = request.form['name']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # Verificar se as senhas coincidem
        if password != password_confirm:
            flash('As senhas não coincidem.', 'error')
            return redirect(url_for('register'))
        
        # Gerar o hash da senha
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Criar e adicionar o usuário ao banco de dados
        new_user = User(username=login, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
