from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

# application WSGI
# (interface de serveur web python)
# comportements et methodes d'un serveur web

app = Flask(__name__)    # instance de classe Flask (en parametre le nom du module)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


# mysql --user=votreLogin  --password=votreMotDePasse --host=serveurmysql --database=BDD_votreLogin






# Connexion ---------------------------------------------------------

# def get_db():
#     if 'db' not in g:
#         g.db =  pymysql.connect(    #pymysql.connect remplace mysql.connector
#         host="localhost",   #localhost sur les machines perso.
#         user="lbesson4",
#         password="2609",
#         database="BDD_SAE",
#         port=8889,
#         charset='utf8mb4',                      # 2 attributs à ajouter
#         cursorclass=pymysql.cursors.DictCursor  # 2 attributs à ajouter
# )
#     return g.db


def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            # host="localhost",                 # à modifier
            # user="login",                     # à modifier
            # password="secret",                # à modifier
            # database="BDD_votrelogin",        # à modifier
            # charset='utf8mb4',
            # cursorclass=pymysql.cursors.DictCursor

            host="localhost",                 # à modifier
            user="nmarech6",                     # à modifier
            password="0609",                # à modifier
            database="BDD_nmarech6",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db











@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('layout.html')


# Amine -----------------------------------------------

@app.route('/appartement/show')
def show_appartement():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Appartement ORDER BY CodeAppartement"
    mycursor.execute(sql)
    appartement = mycursor.fetchall()
    return render_template('appartement/show_appartement.html', appartement=appartement)

# Lucas -----------------------------------------------

@app.route('/consomme/show')
def show_consomme():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Consommation ORDER BY id_consommation;"
    mycursor.execute(sql)
    consomme = mycursor.fetchall()
    return render_template('consomme/show_consomme.html', consomme=consomme)

# Nathan -----------------------------------------------

@app.route('/contrat/show')
def show_contrat():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Contrat ORDER BY NumContrat;"
    mycursor.execute(sql)
    contrat = mycursor.fetchall()
    return render_template('contrat/showcontrat.html', contrat=contrat)

@app.route('/contrat/delete', methods=['GET'])
def delete_ville():
    num_contrat = request.args.get('NumContrat', '')
    mycursor = get_db().cursor()
    sql = "DELETE FROM Contrat WHERE NumContrat=%s"
    mycursor.execute(sql, (num_contrat))
    get_db().commit()
    return redirect('/contrat/show')

# Matthieu -----------------------------------------------

# Benjamin -----------------------------------------------