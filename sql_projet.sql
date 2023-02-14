DROP TABLE IF EXISTS Consommation ;
DROP TABLE IF EXISTS Dispose ;
DROP TABLE IF EXISTS Contrat ;
DROP TABLE IF EXISTS Appartement ;
DROP TABLE IF EXISTS Mois ;
DROP TABLE IF EXISTS TypedeCharge ;
DROP TABLE IF EXISTS TypeAppartement ;
DROP TABLE IF EXISTS Amenagement ;
DROP TABLE IF EXISTS Locataire ;
DROP TABLE IF EXISTS Immeuble ;

CREATE TABLE Immeuble(
   NumImmeuble INT AUTO_INCREMENT,
   Adresse VARCHAR(100),
   NbAppartement INT NOT NULL,
   PRIMARY KEY(NumImmeuble)
);

CREATE TABLE Locataire(
   IdLocataire INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Prenom VARCHAR(50),
   Coordonnee VARCHAR(10),
   PRIMARY KEY(IdLocataire)
);

CREATE TABLE Amenagement(
   IdAmenagement INT AUTO_INCREMENT,
   TypeAmenagement VARCHAR(50),
   PRIMARY KEY(IdAmenagement)
);

CREATE TABLE TypedeCharge(
   IdCharge INT AUTO_INCREMENT,
   LibellerTypeCharge VARCHAR(50),
   PRIMARY KEY(IdCharge)
);


CREATE TABLE TypeAppartement(
   IdType INT AUTO_INCREMENT,
   CategorieAppartement VARCHAR(2),
   PRIMARY KEY(IdType)
);

CREATE TABLE Appartement(
   CodeAppartement INT AUTO_INCREMENT,
   Surface INT,
   NumEtage INT,
   NumPorte INT,
   IdType INT NOT NULL,
   NumImmeuble INT NOT NULL,
   PRIMARY KEY(CodeAppartement),
   FOREIGN KEY(IdType) REFERENCES TypeAppartement(IdType),
   FOREIGN KEY(NumImmeuble) REFERENCES Immeuble(NumImmeuble)
);

CREATE TABLE Contrat(
   NumContrat INT AUTO_INCREMENT,
   Date_debut DATE,
   Date_fin DATE,
   PrixLoyer DECIMAL(7,2),
   IdLocataire INT NOT NULL,
   CodeAppartement INT NOT NULL,
   PRIMARY KEY(NumContrat),
   UNIQUE(CodeAppartement),
   FOREIGN KEY(IdLocataire) REFERENCES Locataire(IdLocataire),
   FOREIGN KEY(CodeAppartement) REFERENCES Appartement(CodeAppartement)
);


CREATE TABLE Dispose(
   id_dispose INT AUTO_INCREMENT,
   quantite VARCHAR(50),
   IdAmenagement INT NOT NULL,
   CodeAppartement INT NOT NULL,
   PRIMARY KEY(id_dispose),
   FOREIGN KEY(IdAmenagement) REFERENCES Amenagement(IdAmenagement),
   FOREIGN KEY(CodeAppartement) REFERENCES Appartement(CodeAppartement)
);

CREATE TABLE Consommation(
   id_consommation INT AUTO_INCREMENT,
   numMois INT,
   quantite VARCHAR(50),
   IdCharge INT NOT NULL,
   NumImmeuble INT NOT NULL,
   PRIMARY KEY(id_consommation),
   FOREIGN KEY(IdCharge) REFERENCES TypedeCharge(IdCharge),
   FOREIGN KEY(NumImmeuble) REFERENCES Immeuble(NumImmeuble)
);

INSERT INTO Immeuble VALUES
    (NULL, '10 Rue Aristide Briand 90000 Belfort', 3),
    (NULL, '16 Rue Auguste Scheurer-Kestner 90000 Belfort', 3),
    (NULL, '5 bis Rue François Heim 90000 Belfort', 2),
    (NULL, '10 bis Rue François Heim 90000 Belfort', 5),
    (NULL, '23 Rue Auguste Scheurer-Kestner 90000 Belfort', 3),
    (NULL, '29 Rue François-Severin Marceau 90000 Belfort', 4);

INSERT INTO Locataire VALUES
    (NULL,'Emerick', 'Michael ', '0161246538'),
    (NULL, 'Derek','Schaefer', '0315206091'),
    (NULL, 'Dearmond','Julia', '0106675601'),
    (NULL, 'Aletha ', 'Taylor', '0437856510'),
    (NULL, 'Freeman', 'Myrtle', '0309083381' ),
    (NULL, 'Guernon', 'Amarante', '0586568658'),
    (NULL, 'Leroux', 'Gueri', '0202539299'),
    (NULL, 'Lemieux', 'Galatee', '0408303396'),
    (NULL, 'Henrichon', 'Mayhew', '0273313191');

INSERT INTO Amenagement VALUES
    (NULL, 'Garage'),
    (NULL, 'Place de Parking'),
    (NULL, 'Cave'),
    (NULL, 'Jardin'),
    (NULL, 'Balcon');

INSERT INTO TypedeCharge VALUES
    (NULL, 'Eau'),
    (NULL, 'Electricite'),
    (NULL, 'Gaz'),
    (NULL, 'Ordure');

INSERT INTO TypeAppartement VALUES
    (NULL, 'F2'),
    (NULL, 'F3');

INSERT INTO Appartement VALUE
    (NULL, 34, 2, 6, 1, 2),
    (NULL, 40, 1, 4, 2, 3),
    (NULL, 43, 2, 8, 1, 1);

INSERT INTO Contrat VALUE
    (NULL, '2021-09-12', '2023-09-12', 1200, 4, 3),
    (NULL, '2021-09-12', '2023-09-12', 1500, 2, 2),
    (NULL, '2021-09-12', '2023-09-13', 1000, 1, 1);

INSERT INTO Consommation VALUE
    (NULL,12,'5500 L',1,1),
    (NULL,12,'5700 L',1,5),
    (NULL,12,'30 L',1,3),
    (NULL,12,'5300 KWH',2,4),
    (NULL,12,'1000 m3',3,1),
    (NULL,12,'1100 kG',4,1),
    (NULL,12,'100 kG',4,1),
    (NULL,12,'30 L',1,3),
    (NULL,12,'4300 KWH',2,4);


INSERT INTO Dispose VALUE
    (NULL,2,1,1),
    (NULL,2,3,2);

SELECT * FROM Consomme;

SELECT DISTINCT CodeAppartement
FROM Appartement
WHERE
    Surface BETWEEN 40 AND 50;

SELECT COUNT(CodeAppartement) AS NB_APPARTEMENT
FROM Appartement
WHERE
    Surface BETWEEN 40 AND 50;

SELECT DISTINCT NumContrat, PrixLoyer
FROM Contrat
WHERE
    PrixLoyer < 1300
GROUP BY NumContrat;

SELECT DISTINCT NumContrat, Date_fin
FROM Contrat
WHERE
    Date_fin<= '2023-09-12'
GROUP BY NumContrat;

SELECT Nom, Prenom
FROM Locataire
WHERE  (Nom LIKE 'L%' OR Nom LIKE 'D%' )
AND  Prenom LIKE  '%g%'
ORDER BY nom;

SELECT CodeAppartement,Adresse,NumEtage,NumPorte,CategorieAppartement
FROM Appartement
INNER JOIN Immeuble
ON Appartement.NumImmeuble = Immeuble.NumImmeuble
INNER JOIN TypeAppartement
ON Appartement.IdType = TypeAppartement.IdType
ORDER BY CodeAppartement ASC;

SELECT CodeAppartement,CategorieAppartement
FROM Appartement
INNER JOIN TypeAppartement
ON Appartement.IdType = TypeAppartement.IdType
ORDER BY CodeAppartement ASC;

SELECT Consomme.NumImmeuble,Adresse, Quantite, LibellerTypeCharge,Mois
FROM Consomme
INNER JOIN TypedeCharge
ON Consomme.IdCharge = TypedeCharge.IdCharge AND TypedeCharge.LibellerTypeCharge = 'Eau'
INNER JOIN Immeuble
ON Consomme.NumImmeuble = Immeuble.NumImmeuble
INNER JOIN Mois
ON Consomme.IdMois = Mois.IdMois
ORDER BY NumImmeuble ASC;

SELECT Consomme.NumImmeuble,Adresse, Quantite, LibellerTypeCharge,Mois
FROM Consomme
INNER JOIN TypedeCharge
ON Consomme.IdCharge = TypedeCharge.IdCharge AND TypedeCharge.LibellerTypeCharge = 'Electriciter'
INNER JOIN Immeuble
ON Consomme.NumImmeuble = Immeuble.NumImmeuble
INNER JOIN Mois
ON Consomme.IdMois = Mois.IdMois
ORDER BY NumImmeuble ASC, Mois.IdMois ASC;

SELECT NumContrat,Nom,Prenom, Adresse, Immeuble.NumImmeuble, NumPorte, Appartement.CodeAppartement
FROM Contrat
INNER JOIN Appartement
ON Contrat.CodeAppartement = Appartement.CodeAppartement
INNER JOIN Immeuble
ON Appartement.NumImmeuble = Immeuble.NumImmeuble
INNER JOIN Locataire
ON Contrat.IdLocataire = Locataire.IdLocataire
ORDER BY NumContrat ASC ;

SELECT CodeAppartement,Surface
FROM Appartement
WHERE
    Surface >= 40
GROUP BY CodeAppartement;

SELECT CodeAppartement, TypeAmenagement # Dispose.IdAmenagement
FROM Dispose
INNER JOIN Amenagement
    ON Dispose.IdAmenagement = Amenagement.IdAmenagement
ORDER BY CodeAppartement ASC ;

SELECT CodeAppartement,IdAmenagement
FROM Dispose
WHERE
    IdAmenagement=3
GROUP BY CodeAppartement


