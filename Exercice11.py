# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 10 : Afficher les employé.e.s qui ont vendu le plus de cocktails du jour
# et de bières en pression.

import sqlite3

if __name__ == "__main__":
    # Connexion à la BDD
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
                                 \nTapez 3 pour consulter le nombre total de boissons vendues, le CA associé et le montant des bénéfices de chaque employé de votre bar à une date précise.\
                                 \nTapez 4 pour consulter une liste des boissons les moins vendues et des employé.e.s ayant fait le moins de vente ce mois-ci.\
                                 \nTapez 5 pour consulter une liste des boissons et des employé.e.s ayant rapporté le plus d’argent ce mois-ci.\
                                 \nTapez 6 pour consulter la liste des employé.e.s ayant vendu le plus de cocktails du jour et de bières en pression.\
                                 \nTapez 7 pour consulter le degré d'alcool consommé en moyenne et la quantité de d'alcool vendu ce mois-ci.\n")

                if int(choice) == 1:
                    curseur.execute("SELECT COUNT(V.Id_boisson), Id_employe, ROUND(SUM(Prix)) \
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
                    curseur.execute("SELECT Nom_bar, COUNT(V.Id_Boisson), ROUND(SUM(Prix)) \
                                                    FROM VENTE AS V \
                                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson \
                                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                                    WHERE Nom_bar = ? ;", (bar_name,))

                    for res in curseur.fetchall():
                        print("\nNom du bar :", res[0], "\nNombre de vente :", res[1], "\nMontant des ventes :", res[2],
                              "\n")

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
                    curseur.execute("SELECT Nom_bar, COUNT(VENTE.Id_Boisson), ROUND(SUM(Prix)) \
                                    FROM VENTE \
                                    JOIN CARTE AS C ON VENTE.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON VENTE.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? \
                                    AND VENTE.Date = ? ;", (bar_name, date,))

                    res = curseur.fetchone()
                    print("\nBar :", res[0], "\nLe :", f'{date}', "\nNombre de vente :", res[1],
                          "\nMontant des ventes :", res[2], "\n")

                    curseur.execute("SELECT Id_employe, ROUND(SUM(Prix)) \
                                    FROM VENTE AS V \
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    WHERE Nom_bar = ? AND V.Date = ? \
                                    GROUP BY Id_employe;", (bar_name, date,))
                    print("\nBénéfice par employé, le", f'{date}', ":")
                    for res in curseur.fetchall():
                        print(*res)

                elif int(choice) == 4:
                    nb_res = input("Combien de résultats voulez-vous afficher ? ")
                    # Les x boissons les moins vendues dans l'établissement
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Ventes, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    GROUP BY V.Id_boisson\
                                    ORDER BY Ventes ASC\
                                    LIMIT ? ;", (bar_name, nb_res,))

                    print(f"\nLes {nb_res} boissons les moins vendues ce mois :")
                    for res in curseur.fetchall():
                        print(*res)

                    # Les x employé.e.s ayant vendu le moins de boissons
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Ventes, EM.Matricule, EM.Nom, EM.Prenom \
                                    FROM VENTE AS V \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom = EM.Nom_bar \
                                    WHERE Nom_bar = ? \
                                    GROUP BY EM.Matricule\
                                    ORDER BY Ventes ASC\
                                    LIMIT ? ;", (bar_name, nb_res,))
                    print(f"\nLes {nb_res} employé.e.s ayant vendu le moins de boissons ce mois :")
                    for res in curseur.fetchall():
                        print(*res)

                elif int(choice) == 5:
                    nb_res = input("Combien de résultats voulez-vous afficher ? ")
                    # Les x boissons ayant rapporté le plus d’argent
                    curseur.execute("SELECT ROUND(SUM(Prix)) AS Total, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    GROUP BY C.Nom\
                                    ORDER BY Total DESC\
                                    LIMIT ? ;", (bar_name,))

                    print(f"\nLes {nb_res} boissons ayant rapporté le plus d'argent sont :")
                    print(f"Total \t Boisson")
                    for res in curseur.fetchall():
                        # print(*res)
                        print(f"{res[0]} \t {res[1]}")

                    # Les x employé.e.s ayant rapporté le plus d’argent
                    curseur.execute("SELECT ROUND(SUM(Prix)) AS Total, EM.Matricule, EM.Nom, EM.Prenom \
                                    FROM VENTE AS V \
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule \
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom = EM.Nom_bar \
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    WHERE Nom_bar = ? \
                                    GROUP BY V.Id_employe\
                                    ORDER BY Total DESC\
                                    LIMIT ? ;", (bar_name, nb_res))
                    print(f"\nLes {nb_res} employé.e.s ayant rapporté le plus d'argent sont :")
                    print(f"Total \t Matricule \tNom Prénom")
                    for res in curseur.fetchall():
                        # print(*res)
                        print(f"{res[0]} \t {res[1]} \t{res[2]} {res[3]}")

                elif int(choice) == 6:
                    nb_res = input("Combien de résultats voulez-vous afficher ? ")
                    cocktail = "Cocktail du moment"
                    biere = "Blonde pression"
                    # Les x employé.e.s ayant vendu le plus de cocktails du jour
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Total, EM.Matricule, EM.Nom, EM.Prenom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    AND C.Nom = ?\
                                    GROUP BY V.Id_employe\
                                    ORDER BY Total DESC\
                                    LIMIT ? ;", (bar_name, cocktail, nb_res,))

                    print("\nLes employé.e.s ayant vendu le plus de cocktails du jour sont :")
                    print(f"Total \t Matricule \tNom Prénom")
                    for res in curseur.fetchall():
                        #print(*res)
                        print(f"{res[0]} \t {res[1]} \t{res[2]} {res[3]}")

                    # Les x employé.e.s ayant vendu le plus de bières pression
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Total, EM.Matricule, EM.Nom, EM.Prenom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    AND C.Nom = ?\
                                    GROUP BY V.Id_employe\
                                    ORDER BY Total DESC\
                                    LIMIT ? ;", (bar_name, biere, nb_res,))
                    print("\nLes employé.e.s ayant vendu le plus de bières pression sont :")
                    print(f"Total \t Matricule \tNom Prénom")
                    for res in curseur.fetchall():
                        #print(*res)
                        print(f"{res[0]} \t {res[1]} \t{res[2]} {res[3]}")

                elif int(choice) == 7:
                    #degré d'alcool moyen et quantité vendu dans un bar
                    curseur.execute("SELECT Nom_bar, ROUND(AVG(Degre), 2), SUM(Quantite) \
                                    FROM CARTE AS C \
                                    JOIN VENTE AS V ON V.Id_boisson = C.Id_boisson \
                                    JOIN EMPLOYE AS EM ON Matricule = V.Id_employe \
                                    WHERE EM.Nom_bar = ? \
                                    AND Degre IS NOT NULL;", (bar_name,))
                    res = curseur.fetchone()
                    print("Le degré moyen d'alcool consommé au", res[0], "est", str(res[1])+"°.",
                          "\nLa quantité d'alcool vendu dans ce bar ce mois-ci est de", str(res[2])+"cL")

                else:
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