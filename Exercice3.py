#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 3 : Consulter le nombre total de boissons vendues pour chaque
# employé.e ainsi que le montant total associé à ces ventes 

import sqlite3

if __name__ == "__main__":
    # Connexion à la bdd
    bdd = sqlite3.connect("blabar.db")
    bdd.text_factory = str
    curseur = bdd.cursor()

requete = "SELECT Id_employe, COUNT(V.Id_boisson), ROUND(SUM(Prix)) \
            FROM VENTE AS V JOIN CARTE AS C \
            ON V.Id_boisson=C.Id_boisson \
            GROUP BY Id_employe;"
curseur.execute(requete)
total = curseur.fetchall()
print("Matricule    Nombre total de\tTotal (€) ")
print("\t    boissons vendues")

# Affichage de tous les résultats 
for t in total:
    print(f"{t[0]} \t\t {t[1]} \t\t{t[2]}")

bdd.close()
