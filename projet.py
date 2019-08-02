# -*- coding: utf-8 -*-

# Created on Wed Jul 22 20:15:45 2019

# @authors: T.Barbot, S. Tony
#!/usr/bin/env python3

import flask as fl
import random
import pickle
import hashlib
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)

# ----------------------
# VUES DU SITE
# ----------------------

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/inscription/')
def inscription(): 
    return render_template('inscription.html')

@app.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    """
    Vue de la page d'inscription.
    """
    if fl.request.method == 'POST': # methode 'POST' -> Pour résumer, la methode 'POST' concerne les formulaires. Si on remplit un formulaire, on envoie une requete 'POST' au serveur. Sinon, c'est du 'GET'.
        user_dict=userDict() # Dictionnaire comprenant les infos utilisateurs. Deviendra inutile avec la dataBase
        if fl.request.form['email'] in emailList(user_dict): # Vérifie que l'adresse mail renseignée par l'utilisateur n'est pas déja associée à un compte
            return fl.render_template('inscription.html', existing_email = True) #Réponse du site si condition 'email déja utilisé' est vraie.
        else:
            user_dict.update({id_gen(id_list(user_dict)):{'last_name':fl.request.form['last_name'], 'first_name':fl.request.form['first_name'], 'email':fl.request.form['email'], 'password':crypted_pswd(fl.request.form['password'])}}) # Si email non utilisé (i.e. nouveau profil), récupération des données du formulaire et stockage (dans dico pour l'instant, dans dataBase à terme).
            with open('DB/userdict.pickle', 'wb') as file: # Ces trois lignes sont vouées à disparaitre.
                data = pickle.Pickler(file, protocol=2)    # Elles permettent de stocker les données du
                data.dump(user_dict)                       # dictionnaire 'user_dict' dans un fichier via le module 'pickle'.
            return fl.redirect(fl.url_for('index')) # Après stockage des données, envoie vers une autre vue
    return fl.render_template('inscription.html') # methode 'GET' -> vue affichée quand on entre l'url dans la barre d'adresse (en gros, affichage du formulaire à renseigner)

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