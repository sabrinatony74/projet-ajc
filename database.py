import sqlite3

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
c.executemany ('INSERT INTO Categories (name_cat) VALUES (?)', classes)

#Sauvegarde des changements
conn.commit()

#Fermeture connexion
c= conn.close()