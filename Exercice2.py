#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 2 : Affichage des statistiques globales 

import sqlite3

def requete_to_dict(requete):
    """""
        Cette fonction prend une requête en entrée et permet de récupérer un dictionnaire
    """""
    dictionnaire = {} 
    curseur.execute(requete)
    for resultat in curseur.fetchall():
        dictionnaire[resultat[0]] = resultat[1] 
    return dictionnaire

if __name__ == "__main__":
    # Connexion à la bdd
    bdd = sqlite3.connect("blabar.db")
    bdd.text_factory = str
    curseur = bdd.cursor()

# Nombre total de bars
requete = "SELECT COUNT(Id_etablissement) \
            FROM ETABLISSEMENT;"
curseur.execute(requete)
total_bar = curseur.fetchone()[0]

# Nombre total d'employé.e.s
requete = "SELECT COUNT(Matricule) \
           FROM EMPLOYE;"
curseur.execute(requete)
total_employe = curseur.fetchone()[0]

# Nombre d'employé.e.s pour chaque profession
requete = "SELECT COUNT(Matricule), Profession \
           FROM EMPLOYE \
           GROUP BY Profession;"
nb_profession = requete_to_dict(requete)

# Revenu total du groupe
requete = "SELECT ROUND(SUM(Prix)) \
            FROM CARTE AS C JOIN VENTE AS V \
            ON C.Id_boisson=V.Id_boisson;"
curseur.execute(requete)
revenu = round(curseur.fetchone()[0])

statistiques = {"Nombre total de bars" : total_bar,
"Nombre total d'employé.e.s" : total_employe, 
"Nombre d'employé.e.s pour chaque profession": nb_profession,
"Revenu total du groupe": revenu}

print(statistiques)

bdd.close()