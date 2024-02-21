# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 7 : afficher le nombre de ventes effectuées ce mois-ci par ses employé.e.s
# et le montant que cela représente, ainsi que le bénéfice généré pour chaque employé du bar
# pour une date donnée.

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
            print("Nom de bar correct")
            id_and_bar = user_id, bar_name
            # print(id_and_bar)
            if id_and_bar in liste_g:
                print("accès autorisé")
                choice = input("Que voulez-vous faire ?\nTapez 1 pour consulter le nombre total de boissons vendues et le CA associé pour votre bar.\
                                 \nTapez 2 pour consulter le nombre total de boissons vendues, le CA associé et le montant des bénéfices de chaque employé de votre bar.\
                                 \nTapez 3 pour consulter le nombre total de boissons vendues, le CA associé et le montant des bénéfices de chaque employé de votre bar à une date précise.\n ")
                if int(choice) == 1:
                    # Nombre total de boissons vendues pour chaque employé.e et montant total associé à ces ventes 
                    curseur.execute("SELECT Id_employe, COUNT(V.Id_boisson), ROUND(SUM(Prix)) \
                                    FROM VENTE AS V JOIN CARTE AS C \
                                    ON V.Id_boisson=C.Id_boisson \
                                    JOIN EMPLOYE AS EM \
                                    ON Id_employe = EM.Matricule \
                                    GROUP BY Id_employe \
                                    HAVING Nom_bar = ? ;", (bar_name,))
                    print(f"Nombre total de boissons vendues et le CA associé pour f'{bar_name} :")
                    for res in curseur.fetchall():
                        print(res)

                elif int(choice) == 2:
                    # Nombre et montant des ventes 
                    curseur.execute("SELECT Nom_bar, COUNT(V.Id_Boisson), ROUND(SUM(Prix)) \
                                    FROM VENTE AS V \
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? ;", (bar_name,))

                    for res in curseur.fetchall():
                        print("\nNom du bar :", res[0], "\nNombre de vente :", res[1], "\nMontant des ventes :", res[2],
                              "€\n")

                    # Bénéfice par employé
                    curseur.execute("SELECT Id_employe, ROUND(SUM(Prix)) \
                                    FROM VENTE AS V \
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? \
                                    GROUP BY Id_employe;", (bar_name,))
                    print("\nBénéfice par employé :")
                    for res in curseur.fetchall():
                        print(*res)

                elif int(choice) == 3:
                    date = input("Saisissez une date au format jj/mm/aaaa : ")
                    # Nombre et montant des ventes à une date donnée
                    curseur.execute("SELECT Nom_bar, COUNT(VENTE.Id_Boisson), ROUND(SUM(Prix)) \
                                    FROM VENTE \
                                    JOIN CARTE AS C ON VENTE.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON VENTE.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? \
                                    AND VENTE.Date = ? ;", (bar_name, date,))

                    res = curseur.fetchone()
                    print("\nNom du bar :", res[0], "\nLe :", f'{date}', "\nNombre de vente :", res[1], "\nMontant des ventes :", res[2], "€\n")
                    
                    # Bénéfice par employé à une date donnée
                    curseur.execute("SELECT Id_employe, ROUND(SUM(Prix)) \
                                    FROM VENTE AS V \
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? AND V.Date = ? \
                                    GROUP BY Id_employe;", (bar_name, date,))
                    print("\nBénéfice par employé, le", f'{date}', ":")
                    for res in curseur.fetchall():
                        print(*res)

                else :
                    print("Fin de la session")
                    user_rights = False

                other = input("\nVoulez-vous consulter autre chose ? (O/N) ")
                if other == "N":
                    print("Fin de la session, à bientôt.")
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
