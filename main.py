from flask import Flask, render_template, redirect, request, session
import mysql.connector
#pip install mysql-connector-python BAIXAR - AJUDA A CONETAR MYSQL COM O PYTHON

#REDIRECT manda o user pra ROTA
#RENDER_TEMPLATE manda o user pra HTML CSS

conexaoDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="trabalheconosco"
)

app = Flask(__name__)
app.secret_key = "siteemprego" #session  nescessita da secret_key

#FUNÇÃO PARA VERIFICAR LOGIN
def verifica_sessao():
    if "login" in session and session ['login']: #verifica se a página está rodando com um login 
        return True
    else:
        return False #faz o controle de usuario/ para ele não acessar páginas pelo link 


#HOMEPAGE
@app.route('/')
def home():
    comandoSQL = 'SELECT * FROM vaga' #comando sql
    cursorDB = conexaoDB.cursor() #deixa conexao estavel
    cursorDB.execute(comandoSQL) #executa comando sql
    vagas = cursorDB.fetchall()#faz uma lista com os dados
    cursorDB.close()#fecha banco de dados

    return render_template("home.html", vagas=vagas)

#ROTA PARA ABRIR O FORMULÁRIO DE CADASTRO
@app.route("/cadvaga")
def novavaga():

    if not verifica_sessao(): #verificação se tem sessao / um acesso login na pagina 
        return render_template('login.html')
    
    return render_template("formvaga.html")

#ROTA PARA RECEBER A POSTAGEM DO FORMULÁRIO 
@app.route("/cadastrar", methods=['POST'])
def cadvaga():

    cargo = request.form['cargo']
    descricao = request.form['descricao']
    local = request.form['local']
    salario = request.form['salario']
    comandoSQL = f'INSERT INTO Vaga VALUES (null, "{cargo}","{descricao}","{local}","{salario}")'
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL)
    conexaoDB.commit()
    cursorDB.close()
    return redirect('/adm')

#ROTA PARA PREVINIR QUE USER TENTE ENTRAR NA /CADASTRAR 
@app.route("/cadastrar", methods=['GET', 'PUT', 'DELETE', 'PATCH']) #POST grava info, GET pega info, PUT atualiza info, DELETE exclusão info, PATCH faz mudança parcial na info
def handle_wrong_methods():
    return redirect('/') # Trata todos os outros métodos, redirecionando para a página inicial (/).

#ROTA PARA ABRIR DETALHES DA VAGA
@app.route('/detalhes/<int:id>', methods=['GET']) #Pega a vaga que o user escolheu 
def detalhes(id):
    comandoSQL = f'SELECT * FROM Vaga WHERE idVaga = {id}' #Seleciona o vagas em idvagas / funciona como filtros de paginas, trazendo só oque foi selecionado 
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL)
    vaga = cursorDB.fetchone() # fetchone apenas 1 valor
    cursorDB.close()
    return render_template("detalhes.html",vaga=vaga)

#ROTA DA PÁGINA ADMINISTRATIVA
@app.route('/adm')
def adm():

    if not verifica_sessao(): #verificação se tem sessao / um acesso login na pagina 
        return render_template('/login.html')

    comandoSQL = 'SELECT * FROM Vaga ORDER BY idVaga DESC'
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL)
    vagas = cursorDB.fetchall()
    cursorDB.close()
    return render_template("adm.html",vagas=vagas)

#ROTA DA PÁGINA DE LOGIN
@app.route('/login')
def login():

    if not verifica_sessao(): #verificação se tem sessao / um acesso login na pagina 
        return render_template('/login.html')
    else: 
        return redirect("/adm") #SE JÁ TIVER SESSÃO ATIVA NO SERVER, ELE MANDA PRA ADM

#ACESSO PAGINA ADMIN
@app.route("/acesso", methods=['POST'])
def acesso():
    usuario_informado = request.form['usuario']
    senha_informado = request.form['senha']

    if usuario_informado == 'admin' and senha_informado =='1234': #USER E SENHA PRE SETADOS
        session['login'] = True #Autoriza a entrada 
        return redirect('/adm')
    else:
        return render_template('login.html', msg="Usuário e senha estão incorretos")
    
#LOGOUT PAGINA ADMIN
@app.route('/logout')
def logout():
    if verifica_sessao():
        session.clear() #limpa a sessão 
    
    return redirect('/') #retorno pra home


@app.route('/deletar/<int:id>')
def excluir(id):
    if not verifica_sessao(): #verificação se tem sessao / um acesso login na pagina 
        return render_template('/login.html')
    
    comandoSQL = f'DELETE FROM Vaga WHERE idVaga = {id}'
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL)
    conexaoDB.commit()
    cursorDB.close()
    return redirect('/adm')
    
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')




#SE USER TENTAR ACESSAR UMA ROTA NÃO AUTORIZADA 
@app.errorhandler(405)
def erro405(error):
    return redirect("/")

#SE USER TENTAR ACESSAR UMA ROTA QUE NÃO EXISTE 
@app.errorhandler(404)
def erro404(error):
    return redirect("/")


#FINAL - RODAR O APP BONITINHO 
app.run(debug = True) #ACESSAR ACESSO NO AR - liberação endereço publico no ar