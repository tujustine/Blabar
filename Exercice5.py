#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 5 : Ajout des droits utilisateurs

import sqlite3

if __name__ == "__main__":
    # Connexion à la bdd
    bdd = sqlite3.connect("blabar.db")
    bdd.text_factory = str
    curseur = bdd.cursor()

liste_manager = []
liste_bar = []
liste_g = []

manager = curseur.execute('SELECT Id_manager FROM ETABLISSEMENT;')
for man in manager:
    liste_manager.append(*man)

nom_bar = curseur.execute('SELECT Nom FROM ETABLISSEMENT;')
for bar in nom_bar:
    liste_bar.append(*bar)

man_and_bar = curseur.execute('SELECT Id_manager, Nom FROM ETABLISSEMENT;')
for el in man_and_bar:
    liste_g.append(el)

user_rights = True
while user_rights:
    user_id = input("Entrez votre identifiant: ")
    user_id = user_id.capitalize()  # dans le cas où le matricule n'est pas rentré en majuscules
    if user_id in liste_manager:
        print("Id correct")
        bar_name = input("Quel est le bar que vous gérez ? : ")
        if bar_name in liste_bar:
            print("Nom bar correct")
            id_and_bar = user_id, bar_name
            # print(id_and_bar)
            if id_and_bar in liste_g:
                print("accès autorisé")
                # Nombre total de boissons vendues pour chaque employé.e et montant total associé à ces ventes 
                curseur.execute("SELECT Id_employe, COUNT(V.Id_boisson), ROUND(SUM(Prix)) \
                FROM VENTE AS V JOIN CARTE AS C \
                ON V.Id_boisson=C.Id_boisson \
                JOIN EMPLOYE AS EM \
                ON Id_employe = EM.Matricule \
                GROUP BY Id_employe \
                HAVING Nom_bar = ? ;", (bar_name,))
                
                print("Matricule    Nombre total de\tTotal (€) ")
                print("\t    boissons vendues")
                # Affichage de tous les résultats 
                for res in curseur.fetchall():
                    print(f"{res[0]} \t\t {res[1]} \t\t{res[2]}")

                other = input("Voulez-vous consulter autre chose ? (O/N) ")
                if other == "N":
                    user_rights = False
            else:
                print("L'accès ne vous est pas autorisé")
                user_rights = False
        else:
            print("L'accès ne vous est pas autorisé")
            user_rights = False
    else:
        print("L'accès ne vous est pas autorisé")
        user_rights = False
bdd.close()
