from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

# application WSGI
# (interface de serveur web python)
# comportements et methodes d'un serveur web

app = Flask(__name__)    # instance de classe Flask (en parametre le nom du module)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


# mysql --user=votreLogin  --password=votreMotDePasse --host=serveurmysql --database=BDD_votreLogin

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(    #pymysql.connect remplace mysql.connector
        host="localhost",   #localhost sur les machines perso.
        user="lbesson4",
        password="2609",
        database="BDD_SAE",
        port=8889,
        charset='utf8mb4',                      # 2 attributs à ajouter
        cursorclass=pymysql.cursors.DictCursor  # 2 attributs à ajouter
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

@app.route('/consomme/show')
def show_consomme():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Consommation ORDER BY id_consommation;"
    mycursor.execute(sql)
    consomme = mycursor.fetchall()
    return render_template('consomme/show_consomme.html', consomme=consomme)