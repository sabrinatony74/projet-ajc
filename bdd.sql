Create Database db_project;
Use db_project;
Create TABLE Users (
    id_user INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    pwd VARCHAR(100) UNIQUE NOT NULL
);
Create TABLE Relationships (
    id_relationship INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_userA INTEGER, 
    id_userB INTEGER, 
		FOREIGN KEY(id_userA) 
		REFERENCES Users(id_user),
		FOREIGN KEY(id_userB) 
		REFERENCES Users(id_user)
);
Create TABLE Events (
    id_event INTEGER PRIMARY KEY AUTO_INCREMENT,
    name_ev VARCHAR(100) NOT NULL,
    date_ev DATE NOT NULL, 
    hour_ev TIME NOT NULL,
    place_ev VARCHAR(200) NOT NULL
);
Create TABLE Members (
    id_member INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_userA INTEGER NOT NULL,
    id_ev INTEGER NOT NULL,
		FOREIGN KEY(id_userA) 
		REFERENCES Users(id_user),
		FOREIGN KEY(id_ev) 
		REFERENCES Events(id_event)
);
Create TABLE Categories (
    id_categorie INTEGER PRIMARY KEY AUTO_INCREMENT,
    name_cat VARCHAR(100) NOT NULL
);
Create TABLE Foods (
    id_food INTEGER PRIMARY KEY AUTO_INCREMENT,
    name_fo VARCHAR(100) NOT NULL,
    id_cat INTEGER NOT NULL,
		FOREIGN KEY(id_cat) 
		REFERENCES Categories(id_categorie)
);
Create TABLE Preferences (
    id_preference INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_userA INTEGER NOT NULL,
    id_food_pref INTEGER,
		FOREIGN KEY(id_userA) 
		REFERENCES Users(id_user),
		FOREIGN KEY(id_food_pref) 
		REFERENCES Foods(id_food)
);
Create TABLE Restrictions (
    id_restriction INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_userA INTEGER NOT NULL,
    id_food_restr INTEGER,
		FOREIGN KEY(id_userA) 
		REFERENCES Users(id_user),
		FOREIGN KEY(id_food_restr) 
		REFERENCES Foods(id_food)
);