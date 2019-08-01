# -*- coding: utf-8 -*-

# Created on Wed Jul 22 20:15:45 2019

# @authors: T.Barbot, S. Tony, M. Ribeiro
#!/usr/bin/env python3

import flask as fl
import random
import pickle
import hashlib
import sqlite3
from flask import Flask, request, render_template, redirect, url_for

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
    ('viandes_poissons', ), 
    ('legumes', ),
    ('fruits', ),
    ('feculents', ),
    ('produits_laitiers', )
    ]
c.executemany ('''INSERT INTO Categories (name_cat) VALUES (?)''', classes) 
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
        email_list = c.execute('SELECT email FROM Users') # On parcours la liste des emails de la base de données
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
            
            return fl.redirect(fl.url_for('profil')) # Après stockage des données, envoie vers la vue profil
        
        conn.commit #enregistrement des modifications
        c = conn.close #fermeture de la connection avec la base de données
    
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