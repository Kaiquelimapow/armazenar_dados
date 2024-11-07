from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'imc.db'

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            altura REAL NOT NULL,
                            peso REAL NOT NULL,
                            imc REAL NOT NULL,
                            status TEXT NOT NULL
                        );''')
        print("Banco de dados inicializado e tabela verificada.")


# Função para calcular o IMC
def calcular_imc(peso, altura):
    try:
        imc = peso / (altura ** 2)
        if imc < 18.5:
            status = "Abaixo do peso"
        elif 18.5 <= imc <= 24.9:
            status = "Peso normal"
        else:
            status = "Acima do peso"
        return imc, status
    except ZeroDivisionError:
        return None, "Erro: Altura não pode ser zero."

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            altura = float(request.form['altura'])
            peso = float(request.form['peso'])
            
            imc, status = calcular_imc(peso, altura)
            if imc is None:
                return "Erro: Altura inválida.", 400
            
            # Salvar no banco de dados
            with sqlite3.connect(DATABASE) as conn:
                conn.execute('INSERT INTO usuarios (nome, altura, peso, imc, status) VALUES (?, ?, ?, ?, ?)',
                            (nome, altura, peso, imc, status))
            
            return redirect(url_for('index'))
        except ValueError:
            return "Erro: Altura e peso devem ser números.", 400

    # Listar todos os registros do banco
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT nome, altura, peso, imc, status FROM usuarios')
        registros = cursor.fetchall()

    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
