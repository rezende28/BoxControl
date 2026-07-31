from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def horario_brasilia():
    return datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%d/%m/%Y às %H:%M")



def conectar():

    conexao = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )

    return conexao





def criar_banco():

    conexao = conectar()

    cursor = conexao.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixas (

            id SERIAL PRIMARY KEY,

            numero TEXT NOT NULL,

            unidade TEXT NOT NULL,

            mes TEXT NOT NULL,

            responsavel TEXT NOT NULL,
            
            observacoes TEXT,

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


    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM caixas
        WHERE status != 'Enviada'
        ORDER BY id DESC
        """
    )

    caixas = cursor.fetchall()


    conexao.close()


    return render_template(
        "index.html",
        caixas=caixas
    )







@app.route("/cadastrar", methods=["POST"])
def cadastrar():


    c = request.form["c"]
    p = request.form["p"]
    d = request.form["d"]
    s = request.form["s"]


    codigo_completo = f"C{c} P{p} D{d} S{s}"



    unidade = request.form["unidade"]

    mes = request.form["mes"]

    responsavel = request.form["responsavel"]

    observacoes = request.form.get("observacoes", "")

    data = horario_brasilia()


    conexao = conectar()
    
    cursor = conexao.cursor()



    cursor.execute(
        """
        INSERT INTO caixas
(
    numero,
    unidade,
    mes,
    responsavel,
    observacoes,
    status,
    data_cadastro
)

VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,

        (
    codigo_completo,
    unidade,
    mes,
    responsavel,
    observacoes,
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

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE caixas

        SET status = 'Pronta'

        WHERE id = %s
        """,

        (id,)
    )


    conexao.commit()

    conexao.close()


    return redirect("/")









@app.route("/relatorio", methods=["POST"])
def relatorio():


    caixas = request.form.getlist("caixas")


    data_envio = horario_brasilia() 



    conexao = conectar()

    cursor = conexao.cursor()

    for codigo in caixas:


        cursor.execute(
            """
            UPDATE caixas

            SET status = 'Enviada',
                data_envio = %s

            WHERE numero = %s

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

    cursor = conectar

    cursor.execute(
        """
        SELECT *
        FROM caixas
        WHERE status = 'Enviada'
        ORDER BY id DESC
        """
    )
    
    caixas = cursor.fetchall()


    conexao.close()


    return render_template(
        "enviadas.html",
        caixas=caixas
    )





@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM caixas

        WHERE id = %s
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