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

app = Flask(__name__)

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
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) UNIQUE NOT NULL
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
    ('viandes_poissons', ),('legumes', ),('fruits', ),('feculents', ),('produits_laitiers', )
    ]
c.executemany ('''INSERT INTO Categories (name_cat) VALUES (?)''', classes) 
                    #WHERE NOT EXISTS (VALUES ? FROM Categories WHERE name_cat = ?)''', classes)

#Ajout des lignes de la table Aliment
classes = [('Boeuf', 1),('Canard', 1),('Dinde', 1),('Lapin', 1),('Mouton', 1),('Porc', 1),('Poulet', 1),
('Veau', 1),('Anchois', 1),('Cabillaud', 1),('Daurade', 1),('Lotte', 1),('Sole', 1),('Maquereau', 1),('Sardine', 1),
('Anchois', 1),('Saumon', 1),('Thon', 1),('Truite', 1),('Poulpe', 1),('Crevette', 1),('Moule', 1),('Huître', 1),
('Langoustine', 1),('Bulot', 1),('Oeuf', 1),('Ail', 2),('Aubergine', 2),('Avocat', 2),('Salade', 2),('Betterave', 2),
('Carotte', 2),('Céleri', 2),('Citrouille', 2),('Champignon', 2),('Chou blanc', 2),('Chou rouge', 2),('Chou-fleur', 2),('Chou de Bruxelles', 2),
('Concombre', 2),('Cornichon', 2),('Courgette', 2),('Echalote', 2),('Endive', 2),('Epinard', 2),('Flageolet', 2),
('Haricots verts', 2),('Haricots rouges', 2),('Oignon', 2),('Olives', 2),('Petit pois', 2),('Persil', 2),('Poivron', 2),('Radis', 2),
('Salsifis', 2),('Soja', 2),('Tomate', 2),('Abricot', 3),('Ananas', 3),('Banane', 3),('Cassis', 3),('Cerise', 3),
('Citron', 3),('Citron vert', 3),('Figue', 3),('Fraise', 3),('Framboise', 3),('Fruits de la passion', 3),('Groseille', 3),('Kiwi', 3),
('Maïs', 3),('Mandarine', 3),('Mangue', 3),('Melon', 3),('Mûre', 3),('Myrtille', 3),('Noix de coco', 3),('Orange', 3),
('Pamplemousse', 3),('Pastèque', 3),('Pêche', 3),('Poire', 3),('Pomme', 3),('Prune', 3),('Raisin', 3),('Pâtes', 4),
('Riz', 4),('Pommes de terre', 4),('Quinoa', 4),('Cantal', 5),('Camembert', 5),('Cheddar', 5),('Comté', 5),('Emmental', 5),
('Féta', 5),('Gruyère', 5),('Mascarpone', 5),('Mozzarella', 5),('Parmesan', 5),('Reblochon', 5),('Ricotta', 5),('Roquefort', 5),
('Fromage de chèvre', 5),('Lait', 5),('Fromage blanc', 5),('Yaourt', 5)
]
c.executemany ('''INSERT INTO Foods (name_fo, id_cat) VALUES (?, ?)''', classes) 
                    #WHERE NOT EXISTS (VALUES ? FROM Categories WHERE name_cat = ?)''', classes)

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
    return render_template('index.html')

@app.route('/signup/', methods=['GET', 'POST'])        
def sign_up(): #page inscription

    #Vue affichée quand on entre l'url dans la barre d'adresse (en gros, affichage du formulaire à renseigner)
    if fl.request.method == 'GET':
        return fl.render_template('inscription.html') 
    
    #remplissage du formaulaire et incrémentation de la base de données
    elif fl.request.method == 'POST': #méthode post
        
        conn = sqlite3.connect('database.db') #ouverture de la connection à la base de données
        c = conn.cursor() #création du curseur
 
        # On vérifie si l'email existe ou non
        email_list = c.execute('SELECT email FROM Users').fetchone() # On parcours la liste des emails de la base de données
        if fl.request.form['email'] in email_list : # Test pour savoir si l'email existe ou non
            return fl.render_template('inscription.html', existing_email = True) # Réponse du site si condition 'email déja utilisé' est vraie.
        else:
            first_name = request.form['first_name'] # Méthode de flask pour récupérer un élément du formulaire (ex : input name='first_name')
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            c.executemany('''INSERT INTO Users (first_name, last_name, email, password)
                            VALUES (?, ?, ?, ?)''', first_name, last_name, email, password) # On insère les données dans la base de donnée
            
            # first_name = request.form['first_name'] # Méthode de flask pour récupérer un élément du formulaire (input name="prénom")
            #     c.execute('INSERT INTO Users (first_name) VALUES (?)', first_name) # On insère le nom dans la base de donnée
            # last_name = request.form['last_name'] 
            #     c.execute('INSERT INTO Users (last_name) VALUES (?)', last_name) 
            # email = request.form['email'] 
            #     c.execute('INSERT INTO Users (email) VALUES (?)', email) 
            # password = request.form['password']
            #     c.execute('INSERT INTO Users (password) VALUES (?)', password)
             
            api_key = '4c392ed6313cbe35ff946c4a67bd5698'
            api_secret = 'ff1d1fd6e23e34400d6b95abe8822706'
            mailjet = Client(auth=(api_key, api_secret), version='v3.1') # Envoi du mail de confirmation
            email = request.form['email']
            data = {
            'Messages': [
                {
                "From": {
                    "Email": "food.social.network@gmail.com",
                    "Name": "Food Social Network"
                },
                "To": [
                    {
                    "Email": email,
                    "Name": "Users"
                    }
                ],
                "Subject": "Inscription",
                "TextPart": "Création de votre compte",
                "HTMLPart": "<h3>Félicitation votre compte a bien été créé<a href='profil.html'>Food Social Network</a></h3>",
                "CustomID": "AppGettingStartedTest"
                }
            ]
            }
            result = mailjet.send.create(data=data)
            print (result.status_code)
            print (result.json())
        
            conn.commit #enregistrement des modifications
            c = conn.close #fermeture de la connection avec la base de données

            return fl.redirect(fl.url_for('profil')) # Après stockage des données, envoie vers la vue profil
    
    else:
        return "Méthode non gérée"


#si on veut faire une redirection vers une page il faut d'abord créer une vue comme ci-dessous:
@app.route('/profil/', methods=['GET', 'POST']) #vue vers laquelle on veut rediriger 
def profil(): #ici mettre le nom de la fonction 
    return fl.render_template('profil.html')

@app.route('/profil-ami/')
def friend(): 
    return fl.render_template('profil-ami.html')

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

# Connexion
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Vue de la page de connexion
    """
    if request.method == 'POST':
        x = "sabrinatony@gmail.com"
        y = "test"
        if request.form['username'] != x: #for request.form['password'] != y: x et y seront remplacés par les id de la BD
            return fl.render_template('index.html', error = True)
        else:
            return fl.redirect(fl.url_for('profil'))#bien mettre le nom de la fonction 
    return render_template('index.html')


#Redirection vers une ancre
@app.route("/myredirect")
def my_redirect():
    return redirect(url_for("profil",_anchor="amis"))


"""
Partie temporaire nécessaire au fonctionnement du code en absence de dataBase
"""
email_list=list()

def userDict():
    with open('DB/userdict.pickle', 'rb') as file:
        data = pickle.Unpickler(file)
        dico = data.load()
        return dico

def id_list(user_dict):
    return list(user_dict.keys())

def emailList(dico):
    for key in dico.keys():
        email_list.append(dico[key]['email'])
    return email_list
"""
Fin de la partie temporaire
"""

def id_gen(id_list):
    """
    Génération d'un chiffre aléatoire compris entre 1 et 2000. Deviendra obsolète avec la DataBase
    """
    for _ in range (2000):
        x = random.randint(1,2000)
        if x not in id_list:
            return x
        else:
            continue

def crypted_pswd(password):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal.
    """
    b_password=password.encode() #Encodage de la chaine de caractère au format 'bytes'.
    crypted_pswd=hashlib.sha1(b_password) #Cryptage du mot de passe précédemment encodé au format 'bytes'.
    return crypted_pswd.hexdigest() #Conversion du mot de passe crypté en un nombre hexadecimal.

@app.context_processor
def header():
    return dict(existing_email = False)


if __name__ == "__main__":                     
    app.run(host = 'localhost', debug = True)  