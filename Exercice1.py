#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 1 : Création de la BDD

import sqlite3
import csv

# Connexion à la bdd
bdd = sqlite3.connect("blabar.db")
bdd.text_factory = str
curseur = bdd.cursor()

# Création des tables de la bdd
curseur.execute("CREATE TABLE IF NOT EXISTS EMPLOYE (Matricule TEXT PRIMARY KEY, \
                Nom TEXT NOT NULL, Prenom TEXT NOT NULL, Profession TEXT NOT NULL, Nom_bar TEXT NOT NULL);")
curseur.execute("CREATE TABLE IF NOT EXISTS ETABLISSEMENT (Id_etablissement INTEGER PRIMARY KEY AUTOINCREMENT, \
                Nom TEXT NOT NULL, Adresse TEXT NOT NULL, Numtel INTEGER NOT NULL, Id_manager TEXT NOT NULL, \
                FOREIGN KEY(Id_manager) REFERENCES EMPLOYE(Matricule) );")
curseur.execute("CREATE TABLE IF NOT EXISTS CARTE (Id_boisson INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT NOT NULL, \
                Type TEXT NOT NULL, Prix FLOAT NOT NULL, Degre FLOAT, Quantite FLOAT NOT NULL);")
curseur.execute("CREATE TABLE IF NOT EXISTS VENTE (Id_employe TEXT NOT NULL, Id_boisson INTEGER NOT NULL, Date TEXT NOT NULL, \
                FOREIGN KEY(Id_employe) REFERENCES EMPLOYE(Matricule), \
                FOREIGN KEY(Id_boisson) REFERENCES CARTE(Id_boisson));")

PATH = "./data/"

# Remplissage de notre bdd
fichier = open(PATH+"employes.csv", "r")
csv_reader = csv.DictReader(fichier, delimiter="\t")
for ligne in csv_reader:
    curseur.execute("INSERT INTO EMPLOYE (Prenom, Nom, Matricule, Profession, Nom_bar) \
                    VALUES (:Prenom, :Nom, :Matricule, :Profession, :Nom_Bar)", ligne)
fichier.close()

fichier = open(PATH+"etablissements.csv", "r")
csv_reader = csv.DictReader(fichier, delimiter="\t")
for ligne in csv_reader:
    curseur.execute("INSERT INTO ETABLISSEMENT (Nom, Adresse, Numtel, Id_manager) \
                    VALUES (:Name, :Adresse, :NumTel, :Manager_Id)", ligne)
fichier.close()

fichier = open(PATH+"carte.csv", "r")
csv_reader = csv.DictReader(fichier, delimiter="\t")
for ligne in csv_reader:
    curseur.execute("INSERT INTO CARTE (Id_boisson, Nom, Type, Prix, Degre, Quantite) \
                    VALUES (:Id_Boisson, :Nom, :Type, :Prix, :Degre, :Quantite)", ligne)
fichier.close()

fichier = open(PATH+"ventes.csv", "r")
csv_reader = csv.DictReader(fichier, delimiter="\t")
for ligne in csv_reader:
    curseur.execute("INSERT INTO VENTE (Id_employe, Id_boisson, Date) \
                    VALUES (:Employe_Id, :Boisson_Id, :Date)", ligne)
fichier.close()

bdd.commit()
bdd.close()