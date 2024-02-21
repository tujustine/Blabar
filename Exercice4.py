#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 4 : Récupérer la date où il y a eu le moins de vente enregistrée
# et la date où les bénéfices ont été les moins importants

import sqlite3

if __name__ == "__main__":
    # Connexion à la bdd
    bdd = sqlite3.connect("blabar.db")
    bdd.text_factory = str
    curseur = bdd.cursor()

# Date à laquelle le moins de vente a été enregistré
requete = "SELECT VENTE.Date, COUNT(VENTE.Id_boisson) AS NbVente \
            FROM VENTE \
            GROUP BY Date \
            ORDER BY NbVente ASC;"
curseur.execute(requete)

# On récupère seulement le 1er résultat
date_vente = curseur.fetchone()

# Date à laquelle les bénéfices ont été les moins importants
requete = "SELECT V.Date, ROUND(SUM(Prix)) AS Benefice \
            FROM CARTE AS C JOIN VENTE AS V \
            ON C.Id_boisson=V.Id_boisson \
            GROUP BY Date \
            ORDER BY Benefice ASC;"
curseur.execute(requete)

# On récupère seulement le 1er résultat
date_benefice = curseur.fetchone()

resultat = {"Date avec le moins de ventes": date_vente,
"Date avec le moins de bénéfices": date_benefice}

print(resultat)

bdd.close()
