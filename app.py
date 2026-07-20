from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os


app = Flask(__name__)

BANCO = "database.db"



def conectar():

    conexao = sqlite3.connect(BANCO)

    conexao.row_factory = sqlite3.Row

    return conexao





def criar_banco():

    conexao = conectar()

    cursor = conexao.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixas (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            numero TEXT NOT NULL,

            unidade TEXT NOT NULL,

            mes TEXT NOT NULL,

            status TEXT NOT NULL,

            data_cadastro TEXT NOT NULL,

            data_envio TEXT

        )
    """)


    conexao.commit()

    conexao.close()







@app.route("/")
def index():

    conexao = conectar()


    caixas = conexao.execute(
        """
        SELECT * FROM caixas
        WHERE status != 'Enviada'
        ORDER BY id DESC
        """
    ).fetchall()


    conexao.close()


    return render_template(
        "index.html",
        caixas=caixas
    )









@app.route("/cadastrar", methods=["POST"])
def cadastrar():


    c = request.form["c"]
    p = request.form["p"]
    numero = request.form["numero"]
    d = request.form["d"]
    s = request.form["s"]


    codigo_completo = f"C{c} P{p} {numero} D{d} S{s}"



    unidade = request.form["unidade"]

    mes = request.form["mes"]



    data = datetime.now().strftime("%d/%m/%Y")



    conexao = conectar()



    conexao.execute(
        """
        INSERT INTO caixas
        (
            numero,
            unidade,
            mes,
            status,
            data_cadastro
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            codigo_completo,
            unidade,
            mes,
            "Em Produção",
            data
        )
    )



    conexao.commit()

    conexao.close()



    return redirect("/")











@app.route("/pronta/<int:id>")
def marcar_pronta(id):

    conexao = conectar()


    conexao.execute(
        """
        UPDATE caixas

        SET status = 'Pronta'

        WHERE id = ?
        """,

        (id,)
    )


    conexao.commit()

    conexao.close()


    return redirect("/")









@app.route("/relatorio", methods=["POST"])
def relatorio():


    caixas = request.form.getlist("caixas")


    data_envio = datetime.now().strftime("%d/%m/%Y")



    conexao = conectar()



    for codigo in caixas:


        conexao.execute(
            """
            UPDATE caixas

            SET status = 'Enviada',
                data_envio = ?

            WHERE numero = ?

            """,

            (
                data_envio,
                codigo
            )
        )



    conexao.commit()

    conexao.close()



    return render_template(
        "relatorio.html",
        caixas=caixas
    )









@app.route("/enviadas")
def enviadas():

    conexao = conectar()

    caixas = conexao.execute(
        """
        SELECT *
        FROM caixas
        """
    ).fetchall()

    conexao.close()

    return render_template(
        "enviadas.html",
        caixas=caixas
    )










@app.route("/excluir/<int:id>")
def excluir(id):


    conexao = conectar()



    conexao.execute(
        """
        DELETE FROM caixas

        WHERE id = ?
        """,

        (id,)
    )



    conexao.commit()

    conexao.close()



    return redirect("/")









if __name__ == "__main__":


    criar_banco()


    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )