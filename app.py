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
        host="serveurmysql",   #localhost sur les machines perso.
        user="lbesson4",
        password="2609",
        database="BDD_lbesson4",
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


# BESSON LUCAS -----------------------------------------------


@app.route('/consomme/show')
def show_consomme():
    mycursor = get_db().cursor()
    sql = "SELECT id_consommation,numMois,quantite,TypedeCharge.LibellerTypeCharge,Consommation.NumImmeuble,Immeuble.Adresse FROM Consommation INNER JOIN TypedeCharge ON Consommation.IdCharge = TypedeCharge.IdCharge INNER JOIN Immeuble ON Consommation.NumImmeuble = Immeuble.NumImmeuble ORDER BY id_consommation;"
    mycursor.execute(sql)
    consomme = mycursor.fetchall()
    return render_template('consomme/show_consomme.html', consomme=consomme)


@app.route('/consomme/add', methods=['GET'])
def add_consomme():
    mycursor = get_db().cursor()
    sql = "SELECT IdCharge,LibellerTypeCharge FROM TypedeCharge ORDER BY LibellerTypeCharge;"
    mycursor.execute(sql)
    typeCharges = mycursor.fetchall()
    sql =" SELECT NumImmeuble,Adresse FROM Immeuble;"
    mycursor.execute(sql)
    immeuble = mycursor.fetchall()
    return render_template('consomme/add_consomme.html', typeCharges=typeCharges, immeuble=immeuble)


@app.route('/consomme/add', methods=['POST'])
def valid_add_consomme():
    mycursor = get_db().cursor()
    numMois = request.form.get('numMois', '')
    quantite = request.form.get('quantite', '')
    IdCharge = request.form.get('IdCharge', '')
    NumImmeuble = request.form.get('NumImmeuble', '')
    tuple_insert = (numMois, quantite, IdCharge, NumImmeuble)
    sql = "INSERT INTO Consommation(numMois, quantite, IdCharge, NumImmeuble) VALUES (%s,%s,%s,%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'Une consommation à été ajouté, Numéro de Mois : ' + numMois + ' - Quantité(s) : ' + quantite + ' - Type de Charge(id) : ' + IdCharge + ' - Numéro Immeuble : ' + NumImmeuble
    flash(message, 'alert-success')
    return redirect('/consomme/show')


@app.route('/consomme/delete', methods=['GET'])
def delete_consomme():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    tuple_delete = (id)
    sql = "DELETE FROM Consommation WHERE id_consommation=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'Une consommation à été supprimé, id : ' + id
    flash(message, 'alert-danger')
    return redirect('/consomme/show')


@app.route('/consomme/edit', methods=['GET'])
def edit_consomme():
    mycursor = get_db().cursor()
    id_consommation = request.args.get('id', '')
    sql = "SELECT id_consommation,numMois,quantite,IdCharge,NumImmeuble FROM Consommation WHERE id_consommation=%s"
    mycursor.execute(sql, (id_consommation))
    consomme = mycursor.fetchone()
    sql = "SELECT IdCharge,LibellerTypeCharge FROM TypedeCharge ORDER BY LibellerTypeCharge;"
    mycursor.execute(sql)
    typeCharges = mycursor.fetchall()
    sql = " SELECT NumImmeuble,Adresse FROM Immeuble;"
    mycursor.execute(sql)
    immeuble = mycursor.fetchall()
    return render_template('consomme/edit_consomme.html', consomme=consomme, typeCharges=typeCharges, immeuble=immeuble)


@app.route('/consomme/edit', methods=['POST'])
def valid_edit_consomme():
    mycursor = get_db().cursor()
    id_consommation = request.form.get('id_consommation', '')
    numMois = request.form.get('numMois', '')
    quantite = request.form.get('quantite', '')
    IdCharge = request.form.get('IdCharge', '')
    NumImmeuble = request.form.get('NumImmeuble', '')
    tuple_update = (numMois, quantite, IdCharge, NumImmeuble, id_consommation)
    sql ="UPDATE Consommation SET numMois=%s,quantite=%s,IdCharge=%s,NumImmeuble=%s WHERE id_consommation=%s;"
    print((tuple_update))
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    print(u'Une consommation à été modifié, id : ' + id_consommation + ' - Numéro de Mois : ' + numMois + ' - Quantité(s) : ' + quantite + ' - Type de Charge(id) : ' + IdCharge + ' - Numéro Immeuble : ' +NumImmeuble)
    message=u'Une consommation à été modifié, id : ' + id_consommation + ' - Numéro de Mois : ' + numMois + ' - Quantité(s) : ' + quantite + ' - Type de Charge(id) : ' + IdCharge + ' - Numéro Immeuble : ' +NumImmeuble
    flash(message, 'alert-success')
    return redirect('/consomme/show')


@app.route('/consomme/etat')
def show_etat():
    mycursor = get_db().cursor()
    sql="SELECT id_consommation,numMois,quantite,TypedeCharge.LibellerTypeCharge,Consommation.NumImmeuble,Immeuble.Adresse FROM Consommation INNER JOIN TypedeCharge ON Consommation.IdCharge = TypedeCharge.IdCharge INNER JOIN Immeuble ON Consommation.NumImmeuble = Immeuble.NumImmeuble ORDER BY id_consommation;"
    mycursor.execute(sql)
    consomme = mycursor.fetchall()
    sql = "SELECT IdCharge,LibellerTypeCharge FROM TypedeCharge ORDER BY LibellerTypeCharge;"
    mycursor.execute(sql)
    itemFitre = mycursor.fetchall()
    sql = "SELECT COUNT(*) AS total FROM Consommation WHERE quantite > 5000 AND IdCharge=1 AND numMois=12;"
    mycursor.execute(sql)
    conteur1 = mycursor.fetchone()
    sql = "SELECT id_consommation,numMois,quantite,TypedeCharge.LibellerTypeCharge,Consommation.NumImmeuble,Immeuble.Adresse FROM Consommation INNER JOIN TypedeCharge ON Consommation.IdCharge = TypedeCharge.IdCharge INNER JOIN Immeuble ON Consommation.NumImmeuble = Immeuble.NumImmeuble WHERE quantite > 5000 AND Consommation.IdCharge=1 AND numMois=12 ORDER BY id_consommation ;"
    mycursor.execute(sql)
    resconteur = mycursor.fetchall()
    sql = "SELECT TypedeCharge.LibellerTypeCharge AS Libelle, COUNT(Consommation.quantite) AS Nbr, SUM(Consommation.quantite) AS ConmQte FROM TypedeCharge LEFT JOIN Consommation ON TypedeCharge.IdCharge = Consommation.IdCharge GROUP BY TypedeCharge.LibellerTypeCharge;"
    mycursor.execute(sql)
    analyseCharge = mycursor.fetchall()
    sql = "SELECT COUNT(Consommation.quantite) AS total FROM Consommation;"
    mycursor.execute(sql)
    totalCharge = mycursor.fetchone()
    sql = "SELECT SUM(Consommation.quantite) AS qte FROM Consommation WHERE IdCharge =1;"
    mycursor.execute(sql)
    eau = mycursor.fetchone()
    sql = "SELECT SUM(Consommation.quantite) AS qte  FROM Consommation WHERE IdCharge=2;"
    mycursor.execute(sql)
    elec = mycursor.fetchone()
    sql = "SELECT SUM(Consommation.quantite) AS qte FROM Consommation WHERE IdCharge =3;"
    mycursor.execute(sql)
    gaz = mycursor.fetchone()
    sql = "SELECT SUM(Consommation.quantite) AS qte FROM Consommation WHERE IdCharge =4;"
    mycursor.execute(sql)
    ordure = mycursor.fetchone()
    return render_template('consomme/etat_consomme.html', consomme=consomme, itemFitre=itemFitre, resconteur=resconteur, conteur1=conteur1, analyseCharge=analyseCharge, totalCharge=totalCharge, eau=eau, elec=elec,gaz=gaz,ordure=ordure)


@app.route('/consomme/etat', methods=['POST'])
def filtre_etat():

    mycursor = get_db().cursor()
    sql = "SELECT IdCharge,LibellerTypeCharge FROM TypedeCharge ORDER BY LibellerTypeCharge;"
    mycursor.execute(sql)
    itemFitres = mycursor.fetchall()

    filter_items =[]

    for itemFiltre in itemFitres:
        current = request.form.get(str(itemFiltre["IdCharge"]), None)
        if current:
            filter_items.append(current)

    print("filter_items", filter_items)
    if filter_items and filter_items != []:
        if isinstance(filter_items, list):
            chek_filter_item = True
            for number_item in filter_items:
                print('test', number_item)
                if not number_item.isdecimal():
                    chek_filter_item = False
            if chek_filter_item:
                session['filter_items'] = filter_items

    sql = "SELECT id_consommation,numMois,quantite,TypedeCharge.LibellerTypeCharge,Consommation.NumImmeuble,Immeuble.Adresse FROM Consommation INNER JOIN TypedeCharge ON Consommation.IdCharge = TypedeCharge.IdCharge INNER JOIN Immeuble ON Consommation.NumImmeuble = Immeuble.NumImmeuble "
    condition_and = "WHERE"
    list_param = []
    if "filter_items" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_items'][-1]
        for item in session['filter_items']:
            sql = sql + " Consommation.IdCharge = %s "
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    mycursor.execute(sql,tuple_sql)
    consomme = mycursor.fetchall()
    return render_template('consomme/etat_consomme.html', consomme=consomme, itemFitre=itemFitres)


# LADEL AMINE -----------------------------------------------


@app.route('/appartement/show')
def show_appartement():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Appartement ORDER BY CodeAppartement;"
    mycursor.execute(sql)
    appartement = mycursor.fetchall()
    return render_template('appartement/show_appartement.html', appartement=appartement)

@app.route('/appartement/add', methods=['GET'])
def add_appartement():
    mycursor = get_db().cursor()
    sql = "SELECT CodeAppartement FROM Appartement;"
    mycursor.execute(sql)
    appartement = mycursor.fetchall()
    sql =" SELECT NumImmeuble FROM Immeuble;"
    mycursor.execute(sql)
    immeuble = mycursor.fetchall()
    return render_template('appartement/add_appartement.html', appartement=appartement, immeuble=immeuble)


@app.route('/appartement/add', methods=['POST'])
def valid_add_appartement():
    mycursor = get_db().cursor()
    Surface = request.form.get('Surface', '')
    NumEtage = request.form.get('NumEtage', '')
    NumPorte = request.form.get('NumPorte', '')
    IdType = request.form.get('IdType', '')
    NumImmeuble = request.form.get('NumImmeuble', '')
    tuple_insert = (Surface, NumEtage, NumPorte, IdType, NumImmeuble)
    sql = "INSERT INTO Appartement(Surface, NumEtage, NumPorte, IdType, NumImmeuble) VALUES (%s,%s,%s,%s,%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , Surface : '+ Surface + ' NumEtage : '+ NumEtage +' NumPorte : ' + NumPorte + ' IdType : ' + IdType +  ' NumImmeuble : '+NumImmeuble
    flash(message, 'alert-success')
    return redirect('/appartement/show')

@app.route('/appartement/delete', methods=['GET'])
def delete_appartement():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    tuple_delete = (id)
    sql = "DELETE FROM Appartement WHERE CodeAppartement=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'un appartement supprimé, id : ' + id
    flash(message, 'alert-success')
    return redirect('/appartement/show')

@app.route('/appartement/edit', methods=['GET'])
def edit_appartement():
    mycursor = get_db().cursor()
    CodeAppartement= request.args.get('id', '')
    sql = "SELECT * FROM Appartement WHERE CodeAppartement=%s"
    mycursor.execute(sql, CodeAppartement,)
    appartement = mycursor.fetchone()
    sql = " SELECT NumImmeuble FROM Immeuble;"
    mycursor.execute(sql)
    immeuble = mycursor.fetchall()
    return render_template('appartement/edit_appartement.html', appartement=appartement, immeuble=immeuble)

@app.route('/appartement/edit', methods=['POST'])
def valid_edit_appartement():
    mycursor = get_db().cursor()
    CodeAppartement = request.form.get('CodeAppartement', '')
    Surface = request.form.get('Surface', '')
    NumEtage = request.form.get('NumEtage', '')
    NumPorte = request.form.get('NumPorte', '')
    IdType = request.form.get('IdType', '')
    NumImmeuble = request.form.get('NumImmeuble', '')
    tuple_update = (Surface, NumEtage, NumPorte, IdType, NumImmeuble,CodeAppartement)
    sql ="UPDATE Appartement SET Surface=%s,NumEtage=%s,NumPorte=%s,Idtype=%s,NumImmeuble=%s WHERE CodeAppartement=%s;"
    print((tuple_update))
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    print(u'appartement modifié, code:  : ' + Surface + ' NumEtage :'+ NumEtage +' NumPorte :' + NumPorte + ' IdType :' + IdType +  ' NumImmeuble'+NumImmeuble)
    message=u' appartement modifié, code: ' + CodeAppartement + ' Surface : ' +Surface + ' NumEtage :'+ NumEtage +' NumPorte :' + NumPorte + ' IdType :' + IdType +  ' NumImmeuble :'+NumImmeuble
    flash(message, 'alert-success')
    return redirect('/appartement/show')


# MARECHAL NATHAN -----------------------------------------------

@app.route('/contrat/show')
def show_contrat():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Contrat ORDER BY NumContrat;"
    mycursor.execute(sql)
    contrat = mycursor.fetchall()
    return render_template('contrat/showcontrat.html', contrat=contrat)

@app.route('/contrat/delete', methods=['GET'])
def delete_contrat():
    mycursor = get_db().cursor()
    NumContrat = request.args.get('NumContrat', '')
    tuple_delete = (NumContrat)
    sql = "DELETE FROM Contrat WHERE NumContrat=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    print(sql + tuple_delete)
    message=u'un contrat supprimé, id : ' + NumContrat
    flash(message, 'alert-success')
    return redirect('/contrat/show')

@app.route('/contrat/edit', methods=['GET'])
def edit_contrat():
    mycursor = get_db().cursor()
    NumContrat = request.args.get('NumContrat', '')
    sql = "SELECT * FROM Contrat WHERE NumContrat=%s;"
    mycursor.execute(sql,(NumContrat))
    Contrat = mycursor.fetchall()
    sql = "SELECT CodeAppartement FROM Appartement;"
    mycursor.execute(sql)
    Appartement = mycursor.fetchall()
    sql = " SELECT IdLocataire FROM Locataire;"
    mycursor.execute(sql)
    Locataire = mycursor.fetchall()
    print(Contrat)
    return render_template('contrat/edit_contrat.html', Contrat=Contrat[0], Appartement=Appartement, Locataire=Locataire)

@app.route('/contrat/edit', methods=['POST'])
def valid_edit_contrat():
    NumContrat = request.form.get('NumContrat','')
    Date_debut = request.form.get('Date_debut', '')
    Date_fin = request.form.get('Date_fin', '')
    CodeAppartement = request.form.get('CodeAppartement', '')
    PrixLoyer = request.form.get('PrixLoyer', '')
    IdLocataire = request.form.get('IdLocataire', '')
    mycursor = get_db().cursor()
    tuple_update = (Date_debut, Date_fin, CodeAppartement, PrixLoyer, IdLocataire, NumContrat)
    print(tuple_update)
    sql ="UPDATE Contrat SET Date_debut=%s,Date_fin=%s,CodeAppartement=%s,PrixLoyer=%s, IdLocataire=%s WHERE NumContrat=%s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    print(u'contrat modifié, id:  : ' + NumContrat)
    message=u'  contrat modifié, id: : ' + NumContrat
    flash(message, 'alert-success')
    return redirect('/contrat/show')

@app.route('/contrat/add', methods=['GET'])
def add_contrat():
    mycursor = get_db().cursor()
    sql = "SELECT NumContrat FROM Contrat;"
    mycursor.execute(sql)
    Contrat = mycursor.fetchall()
    sql = "SELECT CodeAppartement FROM Appartement ;"
    mycursor.execute(sql)
    Appartement = mycursor.fetchall()
    sql = " SELECT IdLocataire FROM Locataire;"
    mycursor.execute(sql)
    Locataire = mycursor.fetchall()
    return render_template('contrat/add_contrat.html', Contrat=Contrat, Appartement=Appartement,Locataire=Locataire)


@app.route('/contrat/add', methods=['POST'])
def valid_add_contrat():
    mycursor = get_db().cursor()
    NumContrat = request.form.get('NumContrat', '')
    Date_debut = request.form.get('Date_debut', '')
    Date_fin = request.form.get('Date_fin', '')
    PrixLoyer = request.form.get('PrixLoyer', '')
    IdLocataire = request.form.get('IdLocataire', '')
    CodeAppartement = request.form.get('CodeAppartement', '')
    tuple_insert = ( Date_debut, Date_fin, PrixLoyer, IdLocataire, CodeAppartement, NumContrat )
    sql = "INSERT INTO Contrat( Date_debut, Date_fin, PrixLoyer, IdLocataire, CodeAppartement, NumContrat) VALUES (%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'contrat ajouté , NumContrat :'+ NumContrat + 'Date_début :'+ Date_debut +'Date_fin :' + Date_fin + 'PrixLoyer :'+PrixLoyer + 'IdLocataire :' + IdLocataire + 'CodeAppartement :' + CodeAppartement
    flash(message, 'alert-success')
    return redirect('/contrat/show')

# PETERSCHMITT MATHIEU -----------------------------------------------


@app.route('/immeuble/show')
def show_immeubles():
    cursor = get_db().cursor()
    sql = "SELECT NumImmeuble, Adresse, NbAppartement FROM Immeuble ORDER BY NumImmeuble;"
    cursor.execute(sql)
    immeubles = cursor.fetchall()
    return render_template('immeuble/show.html', immeubles=immeubles)

@app.route('/immeuble/add', methods=['GET'])
def add_immeuble_get():
    return render_template('immeuble/add.html')

@app.route('/immeuble/add', methods=['POST'])
def add_immeuble_post():
    cursor = get_db().cursor()
    adresse = request.form.get('adresse', '')
    nbAppart = request.form.get('nbAppart', '')
    print(f'immeuble ajouté , adresse : {adresse}, nbAppart : {nbAppart}')
    sql = "INSERT INTO Immeuble(Adresse, NbAppartement) VALUES (%s,%s);"
    cursor.execute(sql, (adresse, nbAppart))
    get_db().commit()
    message = u'immeuble ajouté , nombre d\'appartement :'+ nbAppart + ' adresse de l\'apparement :'+ adresse
    flash(message, 'alert-success')
    return redirect('/immeuble/show')

@app.route('/immeuble/delete', methods=['GET'])
def delete_immeuble():
    cursor = get_db().cursor()
    id_immeuble = request.args.get('id', '')
    tuple_delete = (id_immeuble)
    sql = "DELETE FROM Immeuble WHERE NumImmeuble=%s;"
    cursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'un immeuble supprimé supprimé, id : ' + id_immeuble
    flash(message, 'alert-success')
    return redirect('/immeuble/show')

@app.route('/immeuble/edit', methods=['GET'])
def edit_immeuble_get():
    cursor = get_db().cursor()
    id_immeuble = request.args.get('id', '')
    sql = "SELECT * FROM Immeuble WHERE NumImmeuble=%s"
    cursor.execute(sql, (id_immeuble))
    immeuble = cursor.fetchone()
    return render_template('immeuble/edit.html', immeuble=immeuble)

@app.route('/immeuble/edit', methods=['POST'])
def edit_immeuble_post():
    cursor = get_db().cursor()
    id_immeuble = request.form.get('id', '')
    adresse = request.form.get('adresse', '')
    nbAppart = request.form.get('nbAppart', '')
    tuple_update = (adresse, nbAppart, id_immeuble)
    sql ="UPDATE Immeuble SET Adresse=%s,NbAppartement=%s WHERE NumImmeuble=%s;"
    print((tuple_update))
    cursor.execute(sql, (adresse, nbAppart, id_immeuble))
    get_db().commit()
    print(u'immeuble modifié, id:  : ' + id_immeuble)
    message=u'immeuble modifié, id: : ' + id_immeuble
    flash(message, 'alert-success')
    return redirect('/immeuble/show')

@app.route('/immeuble/etat', methods=['GET'])
def etat_immeuble():
    cursor = get_db().cursor()
    id_immeuble = request.args.get('id', '')
    sql = "SELECT * FROM Immeuble WHERE NumImmeuble=%s"
    cursor.execute(sql, (id_immeuble))
    immeuble = cursor.fetchone()
    sql = "SELECT * FROM Appartement LEFT JOIN Immeuble ON Appartement.NumImmeuble = Immeuble.NumImmeuble;"
    cursor.execute(sql)
    appartements = cursor.fetchall()
    sql = "SELECT * FROM TypeAppartement"
    cursor.execute(sql)
    type_apparts = cursor.fetchall()
    return render_template('immeuble/etat.html', immeuble=immeuble, appartements=appartements, type_apparts=type_apparts)

# BERKROUBER Benjamin ----------------------------------------------------------------------------------

@app.route('/amenagement/show')
def show_amenagement():
    #print(amenagement)
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Amenagement;"
    mycursor.execute(sql)
    amenagement = mycursor.fetchall()
    return render_template('amenagement/show_amenagement.html', amenagement=amenagement)

@app.route('/amenagement/add', methods=['GET'])
def add_amenagement():
    mycursor = get_db().cursor()
    sql1 = "SELECT * FROM Amenagement;"
    mycursor.execute(sql1)
    amenagement = mycursor.fetchall()
    return render_template('amenagement/add_amenagement.html', amenagement=amenagement)

@app.route('/amenagement/add', methods=['POST'])
def valid_add_amenagement():
    mycursor = get_db().cursor()
    TypeAmenagement = request.form['TypeAmenagement']
    tuple_insert = (TypeAmenagement,)
    sql = "INSERT INTO Amenagement(TypeAmenagement) VALUES (%s);"
    mycursor.execute(sql,tuple_insert)
    get_db().commit()
    message = u'type ajouté , TypeAmenagement :'+TypeAmenagement
    flash(message, 'alert-success')
    return redirect('/amenagement/show')

@app.route('/amenagement/delete', methods=['GET'])
def delete_amenagement():
    mycursor = get_db().cursor()
    IdAmenagement = request.args.get('IdAmenagement', ' ')
    tuple_delete = (IdAmenagement,)
    sql = "DELETE FROM Amenagement WHERE IdAmenagement=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    flash(message, 'alert-warning')
    return redirect('/amenagement/show')

@app.route('/amenagement/edit', methods=['GET'])
def edit_amenagement():
    mycursor = get_db().cursor()
    IdAmenagement = request.args.get('IdAmenagement', '')
    sql = "SELECT * FROM Amenagement WHERE IdAmenagement=%s;"
    mycursor.execute(sql, (IdAmenagement,))
    amenagements = mycursor.fetchone()
    sql1 = "SELECT * FROM Amenagement;"
    mycursor.execute(sql1)
    amenagement = mycursor.fetchall()
    return render_template('amenagement/edit_amenagement.html', amenagement=amenagement,amenagements=amenagements)

@app.route('/amenagement/edit', methods=['POST'])
def valid_edit_amenagement():
    mycursor = get_db().cursor()
    TypeAmenagement = request.form['TypeAmenagement']
    IdAmenagement = request.form.get('IdAmenagement', '')
    tuple_update = (TypeAmenagement, IdAmenagement,)
    sql = "UPDATE Amenagement SET TypeAmenagement=%s WHERE IdAmenagement=%s;"
    mycursor.execute(sql,tuple_update)
    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/amenagement/show')

if __name__ == '__main__':
    app.run()