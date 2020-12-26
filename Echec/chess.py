from upemtk import *

"""
Projet d'AP1: Jeu d'échec, par PHAM Hoang-Long et SAVANE Kévin

Fonctionnalités du programme:
- Nom des joueurs (console)
- Annonce du tour (graphique)
- Déplacements (console et graphique)
- Prise en passant
- Promotion

L'amélioration des règles avancées n'est pas complète
"""


taille_case = 100
largeur_plateau = 16  # en nombre de cases
hauteur_plateau = 8  # en nombre de cases


def affiche_echiquier():
	"""
	Fonction qui affiche l'échiquier en créant une liste
	"""
	for i in range(4, 12):
		for j in range(8):
			if (i+j) % 2 == 0:
				remplissage = "#e8da8b"
			elif (i+j) % 2 != 0:
				remplissage = "#7a4c1c"
			rectangle(0+100*i, 0+100*j, 100+100*i, 100+100*j, couleur='black', remplissage=remplissage, epaisseur=1, tag='')


def affichePieces(echiquier):
	"""
	Fonction affichant les pièces de l'échiquier
	"""
	i = 0
	position = 0
	while i < 128:
		img = echiquier[i][0]
		if img == None:
			position += 1
			i += 1
		else:
			image((position%16) * 100, (position//16) * 100, img, ancrage='nw', tag='')
			position += 1
			i += 1


def piece_echiquier(echiquier):
	"""
	Modifie la liste echiquier en une matrice avec des couples correspondant
	à chaque pièce ([nom de l'image de la pièce, couleur de la pièce]), et [None, None] quand une case est vide
	"""
	# Pions
	i = 0
	while i < 128:
		if 20 <= i <= 27:
			echiquier[i] = ["pawnB.png", "Noir", 0]
		elif 100 <= i <= 107:
			echiquier[i] = ["pawnW.png", "Blanc", 0]
		elif i in range(36,44) or i in range(52,60) or i in range(68,76) or i in range(84,92):
			echiquier[i] = [None, None, None]
		else:
			echiquier[i] = ["","",""]
		i += 1

	# Pièces Noires
	echiquier[4] = ["rookB.png", "Noir", ""]
	echiquier[5] = ["knightB.png", "Noir", ""]
	echiquier[6] = ["bishopB.png", "Noir", ""]
	echiquier[7] = ["queenB.png", "Noir", ""]
	echiquier[8] = ["kingB.png", "Noir", ""]
	echiquier[9] = ["bishopB.png", "Noir", ""]
	echiquier[10] = ["knightB.png", "Noir", ""]
	echiquier[11] = ["rookB.png", "Noir", ""]

	# Pièces Blanches
	echiquier[116] = ["rookW.png", "Blanc", ""]
	echiquier[117] = ["knightW.png", "Blanc", ""]
	echiquier[118] = ["bishopW.png", "Blanc", ""]
	echiquier[119] = ["queenW.png", "Blanc", ""]
	echiquier[120] = ["kingW.png", "Blanc", ""]
	echiquier[121] = ["bishopW.png", "Blanc", ""]
	echiquier[122] = ["knightW.png", "Blanc", ""]
	echiquier[123] = ["rookW.png", "Blanc", ""]


def aQuiLeTour(tourDeJouer, joueurB, joueurW):
	if tourDeJouer%2 == 0:
		joueur = "Noir"
		texte(1313, 50, "Au tour de\n{1} ({0})\nde jouer.".format(joueur, joueurB), couleur='black', ancrage='nw', police="Purisa", taille=20, tag='')
	elif tourDeJouer%2 != 0:
		joueur = "Blanc"
		texte(1313, 650, "Au tour de\n{1} ({0})\nde jouer.".format(joueur, joueurW), couleur='black', ancrage='nw', police="Purisa", taille=20, tag='')


def conversionCoordonnees(clicX, clicY):
	"""
	Fonction permettant de convertir les coordonnées du clic en indice de la liste echiquier
	"""
	coord = (clicX//100) + (clicY//100) * 16
	return coord


def deplacementGlobal(clicX, clicY, echiquier, tourDeJouer):
	"""
	Fonction gérant l'intégralité des déplacements, en fonction des coordonnées du clic
	"""
	coord = conversionCoordonnees(clicX, clicY)

	# Déplacement des pions
	if echiquier[coord][0] == "pawnB.png" or echiquier[coord][0] == "pawnW.png":
		tourDeJouer = movePawn(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer
	# Déplacement des cavaliers
	elif echiquier[coord][0] == "knightB.png" or echiquier[coord][0] == "knightW.png":
		tourDeJouer = moveKnight(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer
	# Déplacement des rois
	elif echiquier[coord][0] == "kingB.png" or echiquier[coord][0] == "kingW.png":
		tourDeJouer = moveKing(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer
	# Déplacement des tours
	elif echiquier[coord][0] == "rookB.png" or echiquier[coord][0] == "rookW.png":
		tourDeJouer = moveRook(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer
	# Déplacement des fous
	elif echiquier[coord][0] == "bishopB.png" or echiquier[coord][0] == "bishopW.png":
		tourDeJouer = moveBishop(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer
	# Déplacement des reines
	elif echiquier[coord][0] == "queenB.png" or echiquier[coord][0] == "queenW.png":
		tourDeJouer = moveQueen(clicX, clicY, echiquier, coord, tourDeJouer)
		return tourDeJouer

	return tourDeJouer


def movePawn(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction gérant les déplacements des pions avec la prise en passant
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Pion noir
	if ((echiquier[coord][2] == 0 and (coord + 16 == newCoord or coord + 32 == newCoord) and echiquier[coord][1] == "Noir" and echiquier[newCoord] == [None, None, None])
			or (echiquier[coord][2] > 0 and coord + 16 == newCoord and echiquier[coord][1] == "Noir" and echiquier[newCoord] == [None, None, None])
			or (echiquier[newCoord][1] == "Blanc" and (coord + 15 == newCoord or coord + 17 == newCoord))) and tourDeJouer%2 == 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		echiquier[newCoord][2] += 1
		tourDeJouer += 1

		# Promotion
		if newCoord in range(116,124):
			rook = "rookB.png"
			knight = "knightB.png"
			bishop = "bishopB.png"
			queen = "queenB.png"
			promotion(newCoord, echiquier, rook, knight, bishop, queen)

		return tourDeJouer

	# Pion blanc
	elif ((echiquier[coord][2] == 0 and (coord - 16 == newCoord or coord - 32 == newCoord) and echiquier[coord][1] == "Blanc" and echiquier[newCoord] == [None, None, None])
			or (echiquier[coord][2] > 0 and coord - 16 == newCoord and echiquier[coord][1] == "Blanc" and echiquier[newCoord] == [None, None, None])
			or (echiquier[newCoord][1] == "Noir" and (coord - 15 == newCoord or coord - 17 == newCoord))) and tourDeJouer%2 != 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		echiquier[newCoord][2] += 1
		tourDeJouer += 1

		if newCoord in range(4,12):
			rook = "rookW.png"
			knight = "knightW.png"
			bishop = "bishopW.png"
			queen = "queenW.png"
			promotion(newCoord, echiquier, rook, knight, bishop, queen)


		return tourDeJouer

	# Prise en passant
	elif priseEnPassant(echiquier, coord, newCoord, tourDeJouer):

		# Pion Noir
		if tourDeJouer%2 == 0:
			echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
			echiquier[newCoord-16] = [None, None, None]
			tourDeJouer += 1
			return tourDeJouer

		# Pion Blanc
		elif tourDeJouer%2 != 0:
			echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
			echiquier[newCoord+16] = [None, None, None]
			tourDeJouer += 1
			return tourDeJouer

	# Si la case de déplacement est occupée, on annule le coup
	elif echiquier[newCoord] != [None, None, None]:
		return tourDeJouer

	return tourDeJouer


def moveKnight(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction gérant les déplacements des cavaliers
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Cavalier noir
	if (((coord + 14 == newCoord or coord + 18 == newCoord or coord + 31 == newCoord or coord + 33 == newCoord
			or coord - 14 == newCoord or coord - 18 == newCoord or coord - 31 == newCoord or coord - 33 == newCoord)
			and echiquier[coord][1] == "Noir"
			and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == "Blanc"))) and tourDeJouer%2 == 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		tourDeJouer += 1
		return tourDeJouer

	# Cavalier blanc
	elif (((coord + 14 == newCoord or coord + 18 == newCoord or coord + 31 == newCoord or coord + 33 == newCoord
			or coord - 14 == newCoord or coord - 18 == newCoord or coord - 31 == newCoord or coord - 33 == newCoord)
			and echiquier[coord][1] == "Blanc"
			and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == "Noir"))) and tourDeJouer%2 != 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		tourDeJouer += 1
		return tourDeJouer

	# Si la case de déplacement est occupée, on annule le coup
	elif echiquier[newCoord] != [None, None, None]:
		return tourDeJouer

	return tourDeJouer


def moveKing(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction gérant les déplacements des rois
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Roi noir
	if (((coord + 1 == newCoord or coord + 15 == newCoord or coord + 16 == newCoord or coord + 17 == newCoord
			or coord - 1 == newCoord or coord - 15 == newCoord or coord - 16 == newCoord or coord - 17 == newCoord)
			and echiquier[coord][1] == "Noir"
			and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == "Blanc"))) and tourDeJouer%2 == 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		tourDeJouer += 1
		return tourDeJouer

	# Roi blanc
	elif (((coord + 1 == newCoord or coord + 15 == newCoord or coord + 16 == newCoord or coord + 17 == newCoord
			or coord - 1 == newCoord or coord - 15 == newCoord or coord - 16 == newCoord or coord - 17 == newCoord)
			and echiquier[coord][1] == "Blanc"
			and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == "Noir"))) and tourDeJouer%2 != 0:
		echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
		tourDeJouer += 1
		return tourDeJouer

	# Si la case de déplacement est occupée, on annule le coup
	elif echiquier[newCoord] != [None, None, None]:
		return tourDeJouer

	return tourDeJouer


def moveRook(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction permettant les déplacements des tours
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Tour noir
	if tourDeJouer%2 == 0:
		allie = "Noir"
		ennemi = "Blanc"
		tourDeJouer = deplacementRook(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	# Tour blanc
	elif tourDeJouer%2 != 0:
		allie = "Blanc"
		ennemi = "Noir"
		tourDeJouer = deplacementRook(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	return tourDeJouer


def moveBishop(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction gérant les déplacements des fous
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Fou noir
	if tourDeJouer%2 == 0:
		allie = "Noir"
		ennemi = "Blanc"
		tourDeJouer = deplacementBishop(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	# Fou blanc
	elif tourDeJouer%2 != 0:
		allie = "Blanc"
		ennemi = "Noir"
		tourDeJouer = deplacementBishop(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	return tourDeJouer


def moveQueen(clicX, clicY, echiquier, coord, tourDeJouer):
	"""
	Fonction gérant les déplacements des reines
	"""
	clicX, clicY, evt = attente_clic()
	newCoord = conversionCoordonnees(clicX, clicY)

	# Reine noir
	if tourDeJouer%2 == 0:
		allie = "Noir"
		ennemi = "Blanc"
		tourDeJouer = deplacementQueen(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	# Reine blanc
	elif tourDeJouer%2 != 0:
		allie = "Blanc"
		ennemi = "Noir"
		tourDeJouer = deplacementQueen(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)

	return tourDeJouer


def priseEnPassant(echiquier, coord, newCoord, tourDeJouer):
	"""
	Fonction mettant en oeuvre les conditions de la prise en passant
	"""

	# Pion Noir
	if ((echiquier[coord+1][0] == "pawnW.png" or echiquier[coord-1][0] == "pawnW.png")
			and (echiquier[coord+1][2] == 1 or echiquier[coord-1][2] == 1)
			and (coord + 15 == newCoord or coord + 17 == newCoord)) and coord in range(68,76) and tourDeJouer%2 == 0:
		return True

	# Pion Blanc
	elif ((echiquier[coord+1][0] == "pawnB.png" or echiquier[coord-1][0] == "pawnB.png")
			and (echiquier[coord+1][2] == 1 or echiquier[coord-1][2] == 1)
			and (coord - 15 == newCoord or coord - 17 == newCoord)) and coord in range(52,60) and tourDeJouer%2 != 0:
		return True


def enPassantPossible(tourDeJouer, echiquier):
	"""
	Fonction permettant de vérifier si la prise en passant est possible
	en augmentant le nombre de coups joués après un déplacement double d'un pion
	"""

	# Noir
	if (tourDeJouer - 1)%2 == 0:
		for piece in echiquier:
			if echiquier[piece][0] == "pawnW.png" and echiquier[piece][2] != 0:
				echiquier[piece][2] += 1

	# Blanc
	elif (tourDeJouer - 1)%2 != 0:
		for piece in echiquier:
			if echiquier[piece][0] == "pawnB.png" and echiquier[piece][2] != 0:
				echiquier[piece][2] += 1


def promotion(newCoord, echiquier, rook, knight, bishop, queen):
	"""
	Fonction permettant la promotion d'un pion (Interface graphique)
	"""
	rectangle(600, 350, 1000, 450, couleur='black', remplissage='cyan', epaisseur=1, tag='')
	rectangle(725, 300, 880, 350, couleur='black', remplissage='cyan', epaisseur=1, tag='')
	texte(800, 325, "Promotion", couleur='white', ancrage='center', police="Purisa", taille=20, tag='')
	image(600, 350, rook, ancrage='nw', tag='')
	image(700, 350, knight, ancrage='nw', tag='')
	image(800, 350, bishop, ancrage='nw', tag='')
	image(900, 350, queen, ancrage='nw', tag='')
	clicX, clicY, evt = attente_clic()
	if 600 < clicX < 700 and 350 < clicY < 450:
		echiquier[newCoord][0] = rook
	elif 700 < clicX < 800 and 350 < clicY < 450:
		echiquier[newCoord][0] = knight
	elif 800 < clicX < 900 and 350 < clicY < 450:
		echiquier[newCoord][0] = bishop
	elif 900 < clicX < 1000 and 350 < clicY < 450:
		echiquier[newCoord][0] = queen


def deplacementRook(echiquier, coord, newCoord, tourDeJouer, allie, ennemi):
	"""
	Fonction qui réalise les déplacements des tours
	"""
	deplacementBas = [16,32,48,64,80,96,112]	# Tous les deplacements possibles que peut faire la tour vers le bas
	deplacementHaut = [-16,-32,-48,-64,-80,-96,-112]	# Tous les deplacements possibles que peut faire la tour vers le haut
	deplacementDroite = [1,2,3,4,5,6,7]	# Tous les deplacements possibles que peut faire la tour vers la droite
	deplacementGauche = [-1,-2,-3,-4,-5,-6,-7]	# Tous les deplacements possibles que peut faire la tour vers la gauche

	tourDeJouer = deplacementLonguePortee(deplacementBas, deplacementHaut, deplacementDroite, deplacementGauche, echiquier, coord, newCoord, allie, ennemi, tourDeJouer)
	return tourDeJouer


def deplacementBishop(echiquier, coord, newCoord, tourDeJouer, allie, ennemi):
	"""
	Fonction qui réalise les déplacements des fous
	"""
	deplacementBasDroite = [17,34,51,68,85,102,119]	# Tous les deplacements possibles que peut faire le fou vers en diagonale bas-droite
	deplacementBasGauche = [15,30,45,60,75,90,105]	# Tous les deplacements possibles que peut faire le fou en diagonale bas-gauche
	deplacementHautDroite = [-15,-30,-45,-60,-75,-90,-105]	# Tous les deplacements possibles que peut faire le fou en diagonale haut-droite
	deplacementHautGauche = [-17,-34,-51,-68,-85,-102,-119]	# Tous les deplacements possibles que peut faire le fou en diagonale haut-gauche

	tourDeJouer = deplacementLonguePortee(deplacementBasDroite, deplacementHautDroite, deplacementBasGauche, deplacementHautGauche, echiquier, coord, newCoord, allie, ennemi, tourDeJouer)
	return tourDeJouer


def deplacementQueen(echiquier, coord, newCoord, tourDeJouer, allie, ennemi):
	tourDeJouer = deplacementRook(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)
	tourDeJouer = deplacementBishop(echiquier, coord, newCoord, tourDeJouer, allie, ennemi)
	return tourDeJouer


def deplacementLonguePortee(deplacementListe1, deplacementListe2, deplacementListe3, deplacementListe4, echiquier, coord, newCoord, allie, ennemi, tourDeJouer):
	"""
	Fonction permettant les déplacements à longue portée
	"""
	for i in deplacementListe1:	# On attend une liste de déplacement à valeur positive
		if coord + i < 128:
			if (echiquier[coord+i][1] == allie or echiquier[coord+i][1] == ennemi) and coord + i != newCoord:
				break

			elif (coord + i == newCoord and echiquier[coord][1] == allie and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == ennemi)):
				echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
				tourDeJouer += 1
				return tourDeJouer


	for i in deplacementListe2:	# On attend une liste de déplacement à valeur négative
		if coord + i > 0:
			if (echiquier[coord+i][1] == allie or echiquier[coord+i][1] == ennemi) and coord + i != newCoord:
				break

			elif ((coord + i == newCoord) and echiquier[coord][1] == allie and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == ennemi)):
				echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
				tourDeJouer += 1
				return tourDeJouer


	for i in deplacementListe3:	# On attend une liste de déplacement à valeur positive
		if coord + i < 128:
			if (echiquier[coord+i][1] == allie or echiquier[coord+i][1] == ennemi) and coord + i != newCoord:
				break

			elif ((coord + i == newCoord) and echiquier[coord][1] == allie and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == ennemi)):
				echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
				tourDeJouer += 1
				return tourDeJouer


	for i in deplacementListe4:	# On attend une liste de déplacement à valeur négative
		if coord + i > 0:
			if (echiquier[coord+i][1] == allie or echiquier[coord+i][1] == ennemi) and coord + i != newCoord:
				break

			elif ((coord + i == newCoord) and echiquier[coord][1] == allie and (echiquier[newCoord] == [None, None, None] or echiquier[newCoord][1] == ennemi)):
				echiquier[newCoord], echiquier[coord] = echiquier[coord], [None, None, None]
				tourDeJouer += 1
				return tourDeJouer

	return tourDeJouer




if __name__ == "__main__":

	cree_fenetre(taille_case * largeur_plateau,
				 taille_case * hauteur_plateau)

joueurB = str(input("Joueur noir, entrez votre nom: "))
joueurW = str(input("Joueur blanc, entrez votre nom: "))


tourDeJouer = 0
echiquier = []
for i in range(16):
		for j in range(8):
			echiquier.append([i,j])
piece_echiquier(echiquier)


while True:
	efface_tout()

	affiche_echiquier()
	print(echiquier)
	affichePieces(echiquier)
	aQuiLeTour(tourDeJouer, joueurB, joueurW)
	clicX, clicY, evt = attente_clic()
	tourDeJouer = deplacementGlobal(clicX, clicY, echiquier, tourDeJouer)


attente_clic()
