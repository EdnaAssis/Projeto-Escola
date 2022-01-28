from PyQt5 import uic, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox

banco = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='escola'
)


def login():
    exibir = tela1.usuario.text() and tela1.senha.text()
    if exibir == '':
        QMessageBox.about(tela1, 'Atenção', 'Insira o usuário e senha')
    else:
        user = tela1.usuario.text()
        senha = tela1.senha.text()
        sql = "select senha from login where usuario = '{}'".format(user)
        conexao = banco.cursor()
        conexao.execute(sql)
        senha_db = conexao.fetchall()

        if senha == senha_db[0][0]:
            tela1.close()
            tela2.show()

        else:
            mensagem = QMessageBox()
            mensagem.setText('Usuário e ou senha incorretos!')
            mensagem.setWindowTitle('Erro')
            mensagem.setIcon(QMessageBox.Information)
            mensagem.exec()


def voltar():
    tela2.close()
    tela1.show()


def cadastrar_user():
    tela1.close()
    tela3.show()


def novo_usuario():
    exibir = tela3.usuario.text() and tela3.senha.text() and tela3.confirm_senha.text()
    if exibir == '':
        QMessageBox.about(tela3, 'Atenção', 'Preencha todos os campos!')
    else:
        usuario = tela3.usuario.text()
        senha = tela3.senha.text()
        confirmar = tela3.confirm_senha.text()
        if senha == confirmar:
            conexao = banco.cursor()
            sql = "insert into login (usuario, senha) values (%s,%s)"
            colunas = (str(usuario), str(senha))
            conexao.execute(sql, colunas)
            banco.commit()
            QMessageBox.about(tela3, 'Salvo', 'Usuário cadastrado')
            tela3.close()
            tela1.show()
        else:
            QMessageBox.about(tela3, 'Erro', 'Senhas não coincidem')
            tela3.senha.setText('')
            tela3.confirm_senha.setText('')

def cadastrar_aluno():
    if tela2.matricula.text() and tela2.nome.text() and tela2.telefone.text() and tela2.email.text() == '':
        QMessageBox.about(tela2, 'Atenção', 'Preencha todos os campos')
    else:
        matricula= tela2.matricula.text()
        nome= tela2.nome.text()
        telefone= tela2.telefone.text()
        email= tela2.email.text()

        if not matricula.isnumeric():
            mensagem = QMessageBox()
            mensagem.setText('O campo Matrícula precisa ser número!')
            mensagem.setWindowTitle('Atenção!!!')
            mensagem.setIcon(QMessageBox.Information)
            mensagem.exec()
        elif not telefone.isnumeric():
            mensagem = QMessageBox()
            mensagem.setText('O campo Telefone precisa ser número!')
            mensagem.setWindowTitle('Atenção!!!')
            mensagem.setIcon(QMessageBox.Information)
            mensagem.exec()
        elif len(telefone) <11:
            mensagem = QMessageBox()
            mensagem.setText('Informe o celular com DDD + os 9 dígitos')
            mensagem.setWindowTitle('Atenção!!!')
            mensagem.setIcon(QMessageBox.Information)
            mensagem.exec()
        else:
            sql= "select email from cadastro_alunos where email = '{}'".format(email)
            conexao= banco.cursor()
            conexao.execute(sql)
            resultado= conexao.fetchall()
            if len(resultado)!=0:
                mensagem = QMessageBox()
                mensagem.setText('E-mail já cadastrado, tente outro!')
                mensagem.setWindowTitle('E-mail existente!!')
                mensagem.setIcon(QMessageBox.Information)
                mensagem.exec()
            else:
                sexo= ''
                if tela2.f.isChecked():
                    sexo= 'feminino'
                elif tela2.m.isChecked():
                    sexo= 'masculino'
                else:
                    sexo= 'não informado'

                conexao = banco.cursor()
                sql = "insert into cadastro_alunos (matricula,nome,telefone,email,sexo) values" \
                      "(%s, %s, %s, %s, %s)"
                colunas = (str(matricula), str(nome), str(telefone), str(email), sexo)
                conexao.execute(sql, colunas)
                banco.commit()
                QMessageBox.about(tela2, 'Sucesso', 'Aluno(a) cadastrado com sucesso!')
                tela2.matricula.setText('')
                tela2.nome.setText('')
                tela2.telefone.setText('')
                tela2.email.setText('')
def sair():
    tela2.close()


app = QtWidgets.QApplication([])
tela1 = uic.loadUi("login.ui")
tela2 = uic.loadUi("Escola.ui")
tela3 = uic.loadUi("cadastrar_user.ui")
tela2.Voltar.triggered.connect(voltar)
tela1.Acessar.clicked.connect(login)
tela1.Cadastrar_login.clicked.connect(cadastrar_user)
tela3.Novo_cadastro.clicked.connect(novo_usuario)
tela2.Cadastrar.clicked.connect(cadastrar_aluno)
tela2.Sair.triggered.connect(sair)
tela1.show()
app.exec()
