# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exercice 12 : Afficher un nombre à déterminer de boissons les moins vendues ou les
# moins consommer.

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

print("Souhaitez vous consulter les résultats à l'échelle d'un bar ou de la chaine ?")
choice = input("Tapez 1 pour consulter les résultats à l'échelle d'un bar"
               "\nTapez 2 pour consulter les résultats à l'échelle de la chaine\n")
nb_drink = input("Combien de boissons voulez-vous afficher ? ")

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
                if int(choice) == 1:
                    #les x boissons les moins vendues
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Ventes, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    GROUP BY V.Id_boisson\
                                    ORDER BY Ventes ASC\
                                    LIMIT ? ;", (bar_name, nb_drink,))

                    print(f'Les {nb_drink} boissons ayant été le moins consommé au {bar_name}.')
                    for res in curseur.fetchall():
                        print(*res)


                    #les x boissons qui ont rapporté le moins
                    curseur.execute("SELECT ROUND(SUM(Prix)) AS Total, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    JOIN ETABLISSEMENT AS ET ON ET.Nom=EM.Nom_Bar\
                                    AND EM.Nom_bar = ?\
                                    GROUP BY C.Nom\
                                    ORDER BY Total ASC\
                                    LIMIT ? ;", (bar_name, nb_drink,))

                    print(f"Les {nb_drink} boissons ayant le moins rapportées au {bar_name}.")
                    for res2 in curseur.fetchall():
                        print(*res2)

                elif int(choice) == 2:
                    curseur.execute("SELECT COUNT(V.Id_boisson) AS Ventes, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    GROUP BY V.Id_boisson\
                                    ORDER BY Ventes ASC\
                                    LIMIT ? ;", (nb_drink,))

                    print(f'Les {nb_drink} ayant été le moins consommé.')
                    for res in curseur.fetchall():
                        print(*res)

                    # les x boissons qui ont rapporté le moins
                    curseur.execute("SELECT ROUND(SUM(Prix)) AS Total, C.Nom\
                                    FROM VENTE AS V\
                                    JOIN CARTE AS C ON V.Id_boisson = C.Id_boisson\
                                    JOIN EMPLOYE AS EM ON V.Id_employe = EM.Matricule\
                                    GROUP BY C.Nom\
                                    ORDER BY Total ASC\
                                    LIMIT ? ;", (nb_drink,))

                    print(f"Les {nb_drink} ayant le moins rapportées.")
                    for res2 in curseur.fetchall():
                        print(*res2)

            other = input("\nVoulez-vous consulter autre chose ? (O/N) ")
            if other == "N":
                print("Fin de la session, à bientôt.")
                user_rights = False

    else:
        print("L'accès ne vous est pas autorisé")
        user_rights = False
bdd.close()