import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Permet de sélectionner le fichier
def choix_fichier():

    root = tk.Tk()
    root.withdraw()

    fichier_selectionne = filedialog.askopenfilename(
        title="Sélectionner un fichier",
        filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
    )
    if fichier_selectionne:
        print(f"Fichier sélectionné : {fichier_selectionne}")
        return fichier_selectionne
    else:
        print("Aucun fichier sélectionné.")
        return None

# Charge le fichier
def lire_fichier_csv(chemin):
    try:
        data = pd.read_csv(chemin, sep=';', on_bad_lines='skip')
        if 'AAAAMMJJ' in data.columns:
            data['AAAAMMJJ'] = data['AAAAMMJJ'].fillna(0).astype(int)
        return data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

# Calcule la moyenne
def calculer_moyenne_jour(data):
    colonnes_disponibles = proposer_parametres(data)
    choix = input("Sélectionnez un paramètre à analyser par son numéro : ")

    try:
        choix = int(choix)
        if 1 <= choix <= len(colonnes_disponibles):
            parametre = colonnes_disponibles[choix - 1]
            print(f"Calcul de la moyenne journalière pour le paramètre : {parametre}")
            moyennes = data.groupby('AAAAMMJJ')[parametre].mean()
            plt.figure(figsize=(10, 6))
            plt.plot(moyennes.index, moyennes.values, marker='o', linestyle='-', label=parametre)
            plt.title(f"Moyenne journalière du paramètre : {parametre}")
            plt.xlabel("Date (AAAAMMJJ)")
            plt.ylabel(f"Moyenne de {parametre}")
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide. Veuillez entrer un numéro.")

# Filtre
def proposer_parametres(data):
    colonnes_disponibles = [col for col in data.columns if not data[col].isna().all()]
    print("\nParamètres disponibles :")
    for i, col in enumerate(colonnes_disponibles, 1):
        print(f"{i}. {col}")
    return colonnes_disponibles

def afficher_parametres_autres_parametres(data):
    colonnes_disponibles = proposer_parametres(data)
    choix = input("Sélectionnez un paramètre par son numéro : ")

    try:
        choix = int(choix)
        if 1 <= choix <= len(colonnes_disponibles):
            parametre = colonnes_disponibles[choix - 1]
            print(f"\nDonnées pour le paramètre '{parametre}' :")
            print(data[parametre].dropna().head(10))
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide. Veuillez entrer un numéro.")

def afficher_colonnes(fichiers):
    if not fichiers:
        print("La liste des fichiers est vide.")
        return

    print("\nFichiers disponibles :")
    for i, fichier in enumerate(fichiers, 1):
        print(f"{i}. {fichier}")

    try:
        choix = int(input("Sélectionnez un fichier par son numéro : "))
        if 1 <= choix <= len(fichiers):
            fichier_choisi = fichiers[choix - 1]
            data = lire_fichier_csv(fichier_choisi)
            if data is not None:
                if "autres-parametres" in fichier_choisi:
                    calculer_moyenne_jour(data)
                else:
                    print("Ce fichier ne contient pas les paramètres spécifiques.")
            else:
                print("Impossible de lire le fichier sélectionné.")
        else:
            print("Choix de fichier invalide.")
    except ValueError:
        print("Entrée invalide. Veuillez entrer un numéro.")

# Mise en Oeuvre
if __name__ == "__main__":
    fichiers_selectionnes = []

    while True:
        print("\nOptions :")
        print("1. Ajouter un fichier à la liste")
        print("2. Afficher la liste des fichiers sélectionnés")
        print("3. Choisir un fichier, filtrer et afficher la moyenne journalière")
        print("4. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == "1":
            fichier = choix_fichier()
            if fichier:
                fichiers_selectionnes.append(fichier)
        elif choix == "2":
            print("\nFichiers sélectionnés :")
            for i, fichier in enumerate(fichiers_selectionnes, 1):
                print(f"{i}. {fichier}")
        elif choix == "3":
            afficher_colonnes(fichiers_selectionnes)
        elif choix == "4":
            print("Fermeture du programme.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
