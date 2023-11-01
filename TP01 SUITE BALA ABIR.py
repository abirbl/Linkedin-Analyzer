import random

frequences = {
  'a': 12,
  'b': 8,
  'c': 6,
  'd': 10,
  'e': 20,
  'f': 4,
  'g': 2
}

total = len(frequences)

def generer_tableau_substitution():

  # Générer une liste de nombres de 0 à 99
  plage_nombres = list(range(100))

  # Initialiser le tableau
  table = {}

  for symbole, frequence in frequences.items():

    # Calculer le nombre de nombres à attribuer
    nb_nombres = int(frequence / total * 100)

    # Tirer aléatoirement les nombres
    nombres = random.sample(plage_nombres, nb_nombres)

    # Ajouter l'entrée au tableau
    table[symbole] = nombres

    # Supprimer les nombres utilisés
    plage_nombres = [n for n in plage_nombres if n not in nombres]

  return table

  def verifier_repetition(table):

    for valeurs1 in table.values():
       for valeurs2 in table.values():
          if set(valeurs1) & set(valeurs2):
           return True

  return False

# Exemple d'utilisation
tab = generer_tableau_substitution()

"""2)"""

#une fonction qui crypte un texte par un chiffre homophone en se basant sur la table Tab.
import random

def chiffrer_homophone(message, tab):

  crypte = ""
  dernier_choix = None

  for symbole in message.lower():

    if symbole in tab:

      homophones = tab[symbole]

      # Tirer les homophones dans un ordre aléatoire
      random.shuffle(homophones)

      for h in homophones:

        if h != dernier_choix:

          crypte += h + " "
          dernier_choix = h
          break

      # Si tous ont déjà été choisis
      else:

        crypte += random.choice(homophones) + " "

    else:

      crypte += symbole + " "

  return crypte.strip()

"""3)"""

import random
import string

def generer_carre_polybe():
    alphabet = string.ascii_lowercase
    carre_polybe = {}

    # Créer un carré de Polybe avec des lettres de l'alphabet
    for i in range(5):
        for j in range(5):
            carre_polybe[alphabet[i * 5 + j]] = (i + 1, j + 1)

    return carre_polybe


def chiffrer_polybe(texte, carre_polybe):
    texte_chiffre = ""
    for char in texte.lower():
        if char in carre_polybe:
            coord = carre_polybe[char]
            texte_chiffre += str(coord[0]) + str(coord[1]) + " "
        else:
            texte_chiffre += char + " "
    return texte_chiffre.strip()

# Générer un carré de Polybe
carre_polybe = generer_carre_polybe()

# Exemple d'utilisation du chiffrement avec un carré de Polybe
texte_a_chiffrer = "BONJOUR"
texte_chiffre_polybe = chiffrer_polybe(texte_a_chiffrer, carre_polybe)

def chiffrer_alternative_2(texte):
  texte_chiffre = ""
  for char in texte:
    if char.isalpha():
      if char.isupper():
        code = "A" # Majuscule
      char = char.lower()
    else:
        code = "a" # Minuscule
    index = ord(char) - ord('a') + 1
    texte_chiffre += str(index) + code + " "
  else:
      texte_chiffre += char + " "
  return texte_chiffre.strip()

# Exemple d'utilisation
texte_a_chiffrer = "HEEY"
texte_chiffre_alternative_2 = chiffrer_alternative_2(texte_a_chiffrer)

"""Exercice 5:"""

def inverse(n):
  if n==0:
    return 0
  for i in range(1,27):
    if (n*i) % 26 == 1:
      return i
  return 0
# Exemple d'utilisation de la fonction
inverse(5) # Remplacez cela par le nombre pour lequel vous souhaitez trouver l'inverse

nombre = int(input("Entrez un nombre: "))

inverse = inverse(nombre)

if inverse != 0:
  print(f"L'inverse de {nombre} dans Z/26Z est {inverse}.")
else:
  print(f"{nombre} n'a pas d'inverse dans Z/26Z.")

import numpy as np

def texte_vers_nombres(texte):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    nombres = [alphabet.index(char) for char in texte.lower() if char in alphabet]
    return np.array(nombres)

def trouver_inverse_modulo(Q):
    # Calculer l'inverse de la matrice Q modulo 26 en utilisant la fonction numpy 'inv'
    Q_inverse = np.linalg.inv(Q).astype(int) % 26
    return Q_inverse

def chiffrement_hill(texte, matrice_cle):
    # Convertir le texte en une séquence de nombres
    nombres = texte_vers_nombres(texte)

    # Ajouter des zéros pour obtenir un nombre pair d'éléments (pour les matrices 2x2)
    if len(nombres) % 2 != 0:
        nombres = np.append(nombres, [0])

    # Former des paires de nombres pour constituer la matrice P
    P = nombres.reshape(-1, 2)

    # Chiffrer le texte en utilisant la formule C = P * matrice_cle mod 26
    C = np.dot(P, matrice_cle) % 26

    # Retourner le texte chiffré sous forme de chaîne de caractères
    texte_chiffre = ''.join([chr(num + ord('a')) for row in C for num in row])
    return texte_chiffre

def dechiffrement_hill(texte_chiffre, matrice_cle):
    # Calculer l'inverse de la matrice de clé modulo 26
    matrice_inverse = trouver_inverse_modulo(matrice_cle)

    # Convertir le texte chiffré en une séquence de nombres
    nombres_chiffres = texte_vers_nombres(texte_chiffre)

    # Ajouter des éléments nuls pour obtenir un nombre pair d'éléments
    if len(nombres_chiffres) % 2 != 0:
        nombres_chiffres = np.append(nombres_chiffres, [0])

    # Former des paires de nombres pour constituer la matrice C
    C = nombres_chiffres.reshape(-1, 2)

    # Déchiffrer le texte en utilisant la formule P = C * matrice_inverse mod 26
    P = np.dot(C, matrice_inverse) % 26

    # Retourner le texte déchiffré sous forme de chaîne de caractères
    texte_dechiffre = ''.join([chr(num + ord('a')) for row in P for num in row])
    return texte_dechiffre

# Exemple d'utilisation du chiffrement et du déchiffrement de Hill
matrice_cle = np.array([[6, 24], [1, 13]])  # Remplacez cela par votre matrice de clé
texte_a_chiffrer = "chiffragematriciel"  # Remplacez cela par le texte à chiffrer

texte_chiffre_hill = chiffrement_hill(texte_a_chiffrer, matrice_cle)
print(f"Texte chiffre : {texte_chiffre_hill}")

texte_dechiffre_hill = dechiffrement_hill(texte_chiffre_hill, matrice_cle)
print(f"Texte déchiffré : {texte_dechiffre_hill}")