# -*- coding: utf-8 -*-

# Created on Wed Jul 22 20:15:45 2019

# @authors: T.Barbot, S. Tony, M. Ribeiro
#!/usr/bin/env python3

import flask as fl
import random
import pickle
import hashlib
import sqlite3
import os
from flask import Flask, request, render_template, redirect, url_for
from mailjet_rest import Client

api_key = '4c392ed6313cbe35ff946c4a67bd5698'
api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'

app = Flask(__name__)
app.secret_key='f13bb12fa23f322902df037f05721016ce44d979'

@app.context_processor
def header():
    return dict(existing_email = False,\
                error = False\
                )

def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal.
    """
    b_string=string.encode() #Encodage de la chaine de caractère au format 'bytes'.
    crypted_str=hashlib.sha1(b_string) #Cryptage du mot de passe précédemment encodé au format 'bytes'.
    return crypted_str.hexdigest() #Conversion du mot de passe crypté en un nombre hexadecimal.

# def send_mail(email):
#     api_key = '4c392ed6313cbe35ff946c4a67bd5698'
#     api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
#     mailjet = Client(auth=(api_key, api_secret), version='v3.1') # Envoi du mail de confirmation
#     data = {
#     'Messages': [
#         {
#         "From": {
#             "Email": "food.social.network@gmail.com",
#             "Name": "Food Social Network"
#         },
#         "To": [
#             {
#             "Email": email,
#             "Name": "Users"
#             }
#         ],
#         "Subject": "Inscription",
#         "TextPart": "Création de votre compte",
#         "HTMLPart": "<h3>Félicitation votre compte a bien été créé<a href='profil.html'>Food Social Network</a></h3>", #Pour l'instant, dead link
#         "CustomID": "AppGettingStartedTest"
#         }
#     ]
#     }
#     # result = mailjet.send.create(data=data)
#     # print (result.status_code)
#     # print (result.json())
#     mailjet.send.create(data=data)

def send_mail(tartiflette):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "ribeiromaxance@gmail.com",
            "Name": "Maxance"
        },
        "To": [
            {
            "Email": tartiflette,
            "Name": "Sab"
            }
        ],
        "Subject": "Test envoi email",
        "TextPart": "Mon premier email",
        "HTMLPart": "<h3>Salut ça va ?<a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)

# ----------------------
# BASE DE DONNEES
# ----------------------

#Ouverture connexion
conn = sqlite3.connect('database.db')
c = conn.cursor()
#Création de la base avec les tables
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Relationships (
        id_relationship INTEGER PRIMARY KEY AUTOINCREMENT,
        id_userA INTEGER,
        id_userB INTEGER,
            FOREIGN KEY(id_userA) 
		    REFERENCES Users(id_user),
		    FOREIGN KEY(id_userB) 
		    REFERENCES Users(id_user)
    );
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Events (
        id_event INTEGER PRIMARY KEY AUTOINCREMENT,
        name_ev VARCHAR(255) NOT NULL,
        date_ev DATE NOT NULL,
        hour_ev TIME NOT NULL,
        place_ev VARCHAR(255) NOT NULL
    );
    '''
)   
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Members (
        id_member INTEGER PRIMARY KEY AUTOINCREMENT,
        id_userA INTEGER,
        id_ev INTEGER,
            FOREIGN KEY(id_userA) 
		    REFERENCES Users(id_user),
		    FOREIGN KEY(id_ev) 
		    REFERENCES Events(id_event)
    );
    '''
)
c.execute(
    '''   
    CREATE TABLE IF NOT EXISTS Categories (
        id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
        name_cat VARCHAR(250) NOT NULL
    );
    '''
)
c.execute(
    '''    
    CREATE TABLE IF NOT EXISTS Foods (
        id_food INTEGER PRIMARY KEY AUTOINCREMENT,
        name_fo VARCHAR(255) NOT NULL,
        id_cat INTEGER,
            FOREIGN KEY (id_cat)
            REFERENCES Categories (id_categorie)
    );
    '''
) 
c.execute(
    '''    
    CREATE TABLE IF NOT EXISTS Preferences (
        id_preference INTEGER PRIMARY KEY AUTOINCREMENT,
        id_userA INTEGER NOT NULL,
        id_food_pref INTEGER,
            FOREIGN KEY(id_userA) 
		    REFERENCES Users(id_user),
		    FOREIGN KEY(id_food_pref) 
		    REFERENCES Events(id_food)
    );
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS Restrictions (
        id_restriction INTEGER PRIMARY KEY AUTOINCREMENT,
        id_userA INTEGER NOT NULL,
        id_food_restr INTEGER,
            FOREIGN KEY(id_userA) 
		    REFERENCES Users(id_user),
		    FOREIGN KEY(id_food_restr) 
		    REFERENCES Events(id_food)
    );
    '''
)
#Ajout des lignes de la table Catégories
classes = [
    ('viandes_poissons', 'viandes_poissons', 'viandes_poissons'),('legumes', 'legumes', 'legumes'),('fruits', 'fruits', 'fruits'),('feculents', 'feculents', 'feculents'),('produits_laitiers', 'produits_laitiers', 'produits_laitiers')
    ]
c.executemany ('''INSERT INTO Categories (name_cat) SELECT ? 
                WHERE NOT EXISTS (SELECT ? FROM Categories WHERE name_cat = ?)''', classes)

#Ajout des lignes de la table Aliment


classes = [('Boeuf', 1, 'Boeuf', 'Boeuf'),('Canard', 1, 'Canard', 'Canard'),('Dinde', 1, 'Dinde', 'Dinde'),('Lapin', 1, 'Lapin', 'Lapin'),('Mouton', 1, 'Mouton','Mouton')
# ,('Porc', 1),('Poulet', 1),
# ('Veau', 1),('Anchois', 1),('Cabillaud', 1),('Daurade', 1),('Lotte', 1),('Sole', 1),('Maquereau', 1),('Sardine', 1),
# ('Anchois', 1),('Saumon', 1),('Thon', 1),('Truite', 1),('Poulpe', 1),('Crevette', 1),('Moule', 1),('Huître', 1),
# ('Langoustine', 1),('Bulot', 1),('Oeuf', 1),('Ail', 2),('Aubergine', 2),('Avocat', 2),('Salade', 2),('Betterave', 2),
# ('Carotte', 2),('Céleri', 2),('Citrouille', 2),('Champignon', 2),('Chou blanc', 2),('Chou rouge', 2),('Chou-fleur', 2),('Chou de Bruxelles', 2),
# ('Concombre', 2),('Cornichon', 2),('Courgette', 2),('Echalote', 2),('Endive', 2),('Epinard', 2),('Flageolet', 2),
# ('Haricots verts', 2),('Haricots rouges', 2),('Oignon', 2),('Olives', 2),('Petit pois', 2),('Persil', 2),('Poivron', 2),('Radis', 2),
# ('Salsifis', 2),('Soja', 2),('Tomate', 2),('Abricot', 3),('Ananas', 3),('Banane', 3),('Cassis', 3),('Cerise', 3),
# ('Citron', 3),('Citron vert', 3),('Figue', 3),('Fraise', 3),('Framboise', 3),('Fruits de la passion', 3),('Groseille', 3),('Kiwi', 3),
# ('Maïs', 3),('Mandarine', 3),('Mangue', 3),('Melon', 3),('Mûre', 3),('Myrtille', 3),('Noix de coco', 3),('Orange', 3),
# ('Pamplemousse', 3),('Pastèque', 3),('Pêche', 3),('Poire', 3),('Pomme', 3),('Prune', 3),('Raisin', 3),('Pâtes', 4),
# ('Riz', 4),('Pommes de terre', 4),('Quinoa', 4),('Cantal', 5),('Camembert', 5),('Cheddar', 5),('Comté', 5),('Emmental', 5),
# ('Féta', 5),('Gruyère', 5),('Mascarpone', 5),('Mozzarella', 5),('Parmesan', 5),('Reblochon', 5),('Ricotta', 5),('Roquefort', 5),
# ('Fromage de chèvre', 5),('Lait', 5),('Fromage blanc', 5),('Yaourt', 5)
]
c.executemany ('''INSERT INTO Foods (name_fo, id_cat) SELECT ?, ?
                WHERE NOT EXISTS (SELECT ? FROM Foods WHERE name_fo = ?)''', classes)

c.execute('''INSERT INTO Users (first_name, last_name, email, password) SELECT ?, ?, ? , ? 
            WHERE NOT EXISTS (SELECT ? FROM users WHERE email = ?)'''\
            , ('Admin', 'Admin', 'food.social.network@gmail.com', crypted_string('072330STM'), 'food.social.network@gmail.com', 'food.social.network@gmail.com'))

#Sauvegarde des changements
conn.commit()
#Fermeture connexion
c= conn.close()

#Fonction pour faire les requêtes sql
#Requête SELECT
# def sql_select (texte_select):
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     result_select = c.execute(texte_select)
#     conn.commit()
#     c = conn.close()
#     return result_select
# #Requête INSERT INTO
# def sql_insert (texte_insert):
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     result_insert = c.execute(texte_insert)
#     conn.commit()
#     c = conn.close()
#     return result_insert

# ----------------------
# VUES DU SITE
# ----------------------

@app.route('/')
def accueil():
    if 'logged' in fl.session.keys():
        return fl.redirect('/' + crypted_string(str(fl.session['logged']))+'/')
    else:
        return render_template('index.html')

# Connexion
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Vue de la page de connexion
    """
    if 'logged' in fl.session.keys():
        return fl.redirect('/'+crypted_string(str(fl.session['logged']))+'/')
    else:
        if fl.request.method == 'GET':
            return fl.render_template('index.html')
        
        elif request.method == 'POST':
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            user_mail_list = [a[0] for a in c.execute('SELECT email FROM Users').fetchall()]    # c.execute('SQL_REQUEST).fetchall() renvoie une liste de tuples
                                                                                                # comprenant uniquement un element (car on ne demande que les mails).
                                                                                                # Je fais donc une compréhension de liste par dessus pour récuperer la première
                                                                                                # valeur de chaque tuple.
            if request.form['email'] in user_mail_list:
                pwd = c.execute('SELECT password FROM Users WHERE email = ?', (request.form['email'],)).fetchone()[0]
                if crypted_string(request.form['password']) == pwd:
                    user_id = c.execute('SELECT id_user FROM Users WHERE email = ?', (request.form['email'],)).fetchone()[0]
                    conn.close()
                    fl.session['logged'] = user_id
                    return fl.redirect('/'+crypted_string(str(user_id))+'/')
                else:
                    conn.close()
                    return fl.render_template('index.html', error = True)
            else:
                conn.close()
                return fl.render_template('index.html', error = True)
        else:
            return 'Unknown method'



@app.route('/signup/', methods=['GET', 'POST'])        
def sign_up(): #page inscription

    #Vue affichée quand on entre l'url dans la barre d'adresse (en gros, affichage du formulaire à renseigner)
    if fl.request.method == 'GET':
        return fl.render_template('inscription.html') 
    
    #remplissage du formulaire et incrémentation de la base de données
    elif fl.request.method == 'POST': #méthode post
        
        conn = sqlite3.connect('database.db') #ouverture de la connection à la base de données
        c = conn.cursor() #création du curseur
 
        # On vérifie si l'email existe ou non
        email_list = c.execute('SELECT email FROM Users').fetchone() # On parcours la liste des emails de la base de données
        if fl.request.form['email'] in email_list : # Test pour savoir si l'email existe ou non
            conn.close() #Fermeture database avant de quitter la fonction (sinon database locked)
            return fl.render_template('inscription.html', existing_email = True) # Réponse du site si condition 'email déja utilisé' est vraie.
        else:
            first_name = fl.request.form['first_name'] # Méthode de flask pour récupérer un élément du formulaire (ex : input name='first_name')
            last_name = fl.request.form['last_name']
            email = fl.request.form['email']
            password = fl.request.form['password']
            c.execute('''INSERT INTO Users (first_name, last_name, email, password)
                            VALUES (?, ?, ?, ?)''', (first_name, last_name, email, crypted_string(password))) # On insère les données dans la base de donnée
        
            conn.commit()#enregistrement des modifications
            user_id = c.execute('SELECT id_user FROM Users WHERE email = ?', (email,)).fetchone()[0]
            fl.session['logged'] = user_id
            c = conn.close() #fermeture de la connection avec la base de données
            send_mail(str(email))
            return fl.redirect('/'+ crypted_string(str(user_id)) +'/') # Revenir dessus. Après stockage des données, envoie vers la vue profil
    
    else:
        return "Unknown method"


@app.route('/<crypted_id>/', methods=['GET', 'POST']) 
def profil(crypted_id):                                     #Gerer la liste des amis a afficher sur la page profil (avec id crypté dans url du lien)
    if 'logged' not in fl.session.keys():
        return fl.redirect(fl.url_for('login'))
    else:
        if fl.request.method == 'GET':
            if crypted_string(str(fl.session['logged'])) == crypted_id: # Permet de vérifier si le profil affiché (determiné par crypted_id) est son propre profil (fl.session['logged'])
                return fl.render_template('profil.html', own_profile = True) # Ajouter partie dynamiques a la page HTML
            else:
                return fl.render_template('profil.html') # Faire le cas profil ami

# @app.route('/profil-ami/')
# def friend(): 
#     return fl.render_template('profil-ami.html')

@app.route('/new/') 
def new(): 
    return fl.render_template('new.html')

@app.route('/recette/') 
def recette():
    return fl.render_template('recette.html')

@app.route('/resultat/') 
def resultat(): 
    return fl.render_template('resultat.html')
 
@app.route('/suivre-event/') 
def suivre(): 
    return fl.render_template('suivre-event.html')

# Renvoi du lien retour de la page inscription vers la page d'accueil
@app.route('/index/', methods=['GET', 'POST']) #vue vers laquelle on veut rediriger 
def index():
    return fl.render_template('index.html')

# Deconnexion
@app.route('/index/', methods=['GET', 'POST']) #vue vers laquelle on veut rediriger 
def out():
    return fl.render_template('index.html')

#Redirection vers une ancre
@app.route("/myredirect")
def my_redirect():
    return redirect(url_for("profil",_anchor="amis"))

if __name__ == "__main__":                     
    app.run(host = 'localhost', debug = True)  