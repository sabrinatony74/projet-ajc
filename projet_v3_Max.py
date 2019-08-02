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

def send_mail(mail):
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
            "Email": mail,
            "Name": "Users"
            }
        ],
        "Subject": "Inscription",
        "TextPart": "Mon premier email",
        "HTMLPart": "<h3>Félicitations votre compte a été créé</h3>",
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
    ('viandes_poissons', 'viandes_poissons', 'viandes_poissons'),
    ('legumes', 'legumes', 'legumes'),
    ('fruits', 'fruits', 'fruits'),
    ('feculents', 'feculents', 'feculents'),
    ('produits_laitiers', 'produits_laitiers', 'produits_laitiers')
    ]
c.executemany ('''INSERT INTO Categories (name_cat) SELECT ? 
                WHERE NOT EXISTS (SELECT ? FROM Categories WHERE name_cat = ?)''', classes)

#Ajout des lignes de la table Aliment
classes = [('Boeuf', 1, 'Boeuf', 'Boeuf'),('Canard', 1, 'Canard', 'Canard'),('Dinde', 1, 'Dinde', 'Dinde'),
('Lapin', 1, 'Lapin', 'Lapin'),('Mouton', 1, 'Mouton','Mouton'),('Porc', 1, 'Porc', 'Porc'),
('Poulet', 1, 'Poulet', 'Poulet'),('Veau', 1,'Veau', 'Veau'),('Anchois', 1, 'Anchois', 'Anchois'),
('Cabillaud', 1, 'Cabillaud', 'Cabillaud'),('Daurade', 1, 'Daurade', 'Daurade'),('Lotte', 1, 'Lotte', 'Lotte'),
('Sole', 1, 'Sole', 'Sole'),('Maquereau', 1, 'Maquereau', 'Maquereau'),('Sardine', 1, 'Sardine', 'Sardine'),
('Anchois', 1, 'Anchois', 'Anchois'),('Saumon', 1, 'Saumon', 'Saumon'),('Thon', 1, 'Thon', 'Thon'),
('Truite', 1, 'Truite', 'Truite'),('Poulpe', 1, 'Poulpe', 'Poulpe'),('Crevette', 1, 'Crevette', 'Crevette'),
('Moule', 1, 'Moule', 'Moule'),('Huître', 1, 'Huître', 'Huître'),('Langoustine', 1, 'Langoustine', 'Langoustine'),
('Bulot', 1, 'Bulot', 'Bulot'),('Oeuf', 1, 'Oeuf', 'Oeuf'),('Ail', 2, 'Ail', 'Ail'),
('Aubergine', 2, 'Aubergine', 'Aubergine'),('Avocat', 2, 'Avocat', 'Avocat'),('Salade', 2, 'Salade', 'Salade'),
('Betterave', 2, 'Betterave', 'Betterave'),('Carotte', 2, 'Carotte', 'Carotte'),('Céleri', 2, 'Céleri', 'Céleri'),
('Citrouille', 2, 'Citrouille', 'Citrouille'),('Champignon', 2, 'Champignon', 'Champignon'),('Chou blanc', 2, 'Chou blanc', 'Chou blanc'),
('Chou rouge', 2, 'Chou rouge', 'Chou rouge'),('Chou-fleur', 2, 'Chou-fleur', 'Chou-fleur'),('Chou de Bruxelles', 2, 'Chou de Bruxelles', 'Chou de Bruxelles'),
('Concombre', 2, 'Concombre', 'Concombre'),('Cornichon', 2, 'Cornichon', 'Cornichon'),('Courgette', 2, 'Courgette', 'Courgette'),
('Echalote', 2, 'Echalote', 'Echalote'),('Endive', 2, 'Endive', 'Endive'),('Epinard', 2, 'Epinard', 'Epinard'),
('Flageolet', 2, 'Flageolet', 'Flageolet'),('Haricots verts', 2, 'Haricots verts', 'Haricots verts'),('Haricots rouges', 2, 'Haricots rouges', 'Haricots rouges'),
('Oignon', 2, 'Oignon', 'Oignon'),('Olives', 2, 'Olives', 'Olives'),('Petit pois', 2, 'Petits pois', 'Petits pois'),
('Persil', 2, 'Persil', 'Persil'),('Poivron', 2, 'Poivron', 'Poivron'),('Radis', 2, 'Radis', 'Radis'),
('Salsifis', 2, 'Salsifis', 'Salsifis'),('Soja', 2, 'Soja', 'Soja'),('Tomate', 2, 'Tomate', 'Tomate'),
('Abricot', 3, 'Abricot', 'Abricot'),('Ananas', 3, 'Ananas', 'Ananas'),('Banane', 3, 'Banane', 'Banane'),
('Cassis', 3, 'Cassis', 'Cassis'),('Cerise', 3, 'Cerise', 'Cerise'),('Citron', 3, 'Citron', 'Citron'),
('Citron vert', 3, 'Citron vert', 'Citron vert'),('Figue', 3, 'Figue', 'Figue'),('Fraise', 3, 'Fraise', 'Fraise'),
('Framboise', 3, 'Framboise', 'Framboise'),('Fruits de la passion', 3, 'Fruits de la passion', 'Fruits de la passion'),('Groseille', 3, 'Groseille', 'Groseille'),
('Kiwi', 3, 'Kiwi', 'Kiwi'),('Maïs', 3, 'Maïs', 'Maïs'),('Mandarine', 3, 'Mandarine', 'Mandarine'),
('Mangue', 3, 'Mangue', 'Mangue'),('Melon', 3, 'Melon', 'Melon'),('Mûre', 3, 'Mûre', 'Mûre'),
('Myrtille', 3, 'Myrtille', 'Myrtille'),('Noix de coco', 3, 'Noix de coco', 'Noix de coco'),('Orange', 3, 'Orange', 'Orange'),
('Pamplemousse', 3, 'Pamplemousse', 'Pamplemousse'),('Pastèque', 3, 'Pastèque', 'Pastèque'),('Pêche', 3, 'Pêche', 'Pêche'),
('Poire', 3, 'Poire', 'Poire'),('Pomme', 3, 'Pomme', 'Pomme'),('Prune', 3, 'Prune', 'Prune'),
('Raisin', 3, 'Raisin', 'Raisin'),('Pâtes', 4, 'Pâtes', 'Pâtes'),('Riz', 4, 'Riz', 'Riz'),
('Pommes de terre', 4, 'Pommes de terre', 'Pommes de terre'),('Quinoa', 4, 'Quinoa', 'Quinoa'),('Cantal', 5, 'Cantal', 'Cantal'),
('Camembert', 5, 'Camembert', 'Camembert'),('Cheddar', 5, 'Cheddar', 'Cheddar'),('Comté', 5, 'Comté', 'Comté'),
('Emmental', 5, 'Emmental', 'Emmental'),('Féta', 5, 'Féta', 'Féta'),('Gruyère', 5, 'Gruyère', 'Gruyère'),
('Mozzarella', 5, 'Mozzarella', 'Mozzarella'),('Parmesan', 5, 'Parmesan', 'Parmesan'),('Reblochon', 5, 'Reblochon', 'Reblochon'),
('Ricotta', 5, 'Ricotta', 'Ricotta'),('Roquefort', 5, 'Roquefort', 'Roquefort'),('Fromage de chèvre', 5, 'Fromage de chèvre', 'Fromage de chèvre'),
('Lait', 5, 'Lait', 'Lait'),('Fromage blanc', 5, 'Fromage blanc', 'Fromage blanc'),('Yaourt', 5, 'Yaourt', 'Yaourt')
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