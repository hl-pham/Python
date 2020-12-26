from upemtk import *

taille_case = 100
largeur_plateau = 8
hauteur_plateau = 8



def creer_plateau_position():
	"""
	Fonction créant le plateau des positions
	"""
	plateauPosition = []
	for i in range(largeur_plateau):
		for j in range(hauteur_plateau):
			plateauPosition.append((i, j))
	return plateauPosition



def creer_echiquier(plateauPosition):
	"""
	Fonction créant le plateau avec les pièces
	"""
	echiquier = []
	for i in range(len(plateauPosition)):
		if plateauPosition[i][0] == 1:
			echiquier.append(["pawn", "Black"])
		elif plateauPosition[i][0] == 6:
			echiquier.append(["pawn", "White"])
		else:
			echiquier.append([None])


	echiquier[0] = echiquier[7] = ["rook", "Black"]
	echiquier[1] = echiquier[6] = ["knight", "Black"]
	echiquier[2] = echiquier[5] = ["bishop", "Black"]
	echiquier[3] = ["queen", "Black"]
	echiquier[4] = ["king", "Black"]

	echiquier[56] = echiquier[63] = ["rook", "White"]
	echiquier[57] = echiquier[62] = ["knight", "White"]
	echiquier[58] = echiquier[61] = ["bishop", "White"]
	echiquier[59] = ["queen", "White"]
	echiquier[60] = ["king", "White"]

	return echiquier



def affiche_echiquier():
	"""
	Fonction qui affiche l'échiquier en créant une liste
	"""
	for i in range(hauteur_plateau):
		for j in range(largeur_plateau):
			if (i+j) % 2 == 0:
				remplissage = "#e8da8b"
			elif (i+j) % 2 != 0:
				remplissage = "#7a4c1c"
			rectangle(0+100*i, 0+100*j, 100+100*i, 100+100*j, couleur='black', remplissage=remplissage, epaisseur=1, tag='')



def affiche_pieces(echiquier):
	"""
	Fonction affichant les pièces de l'échiquier
	"""
	for i in range(len(echiquier)):
		if echiquier[i] != [None]:
			img = echiquier[i][0] + echiquier[i][1][0] + ".png"
			image((i%8) * 100, (i//8) * 100, img, ancrage='nw', tag='')



def aQuiLeTour(tourDeJouer, joueurB, joueurW):
	"""
	Fonction affichant le tour des joueurs
	"""
	rectangle(200, 350, 600, 450, couleur='black', remplissage='cyan', epaisseur=1, tag='')
	rectangle(350, 450, 450, 500, couleur='black', remplissage='cyan', epaisseur=1, tag='')
	texte(400, 475, "Ok", couleur='black', ancrage='center', police="Purisa", taille=20, tag='')

	if tourDeJouer % 2 == 0:
		texte(400, 400, "Au tour de {0} de jouer.".format(joueurB), couleur='black', ancrage='center', police="Purisa", taille=20, tag='')
	elif tourDeJouer % 2 != 0:
		texte(400, 400, "Au tour de {0} de jouer.".format(joueurW), couleur='black', ancrage='center', police="Purisa", taille=20, tag='')

	clicX, clicY, evt = attente_clic()

	if 350 < clicX < 450 and 450 < clicY < 500:
		return



def conversionCoordonnees(clicX, clicY):
	"""
	Fonction permettant de convertir les coordonnées du clic en indice de la liste echiquier
	"""
	coord = (clicX//100) + (clicY//100) * 16
	return coord



def allMovements(clicX, clicY, echiquier, tourDeJouer):
	"""
	Fonction gérant l'intégralité des déplacements
	"""
	coord = conversionCoordonnees(clicX, clicY)
	













if __name__ == "__main__":

	cree_fenetre(taille_case * largeur_plateau,
				 taille_case * hauteur_plateau)

joueurB = str(input("Joueur noir, entrez votre nom: "))
joueurW = str(input("Joueur blanc, entrez votre nom: "))

tourDeJouer = 0
plateauPosition = creer_plateau_position()
echiquier = creer_echiquier(plateauPosition)
print(plateauPosition)



while True:
	efface_tout()
	affiche_echiquier()
	print(echiquier)
	affiche_pieces(echiquier)
	aQuiLeTour(tourDeJouer, joueurB, joueurW)
	clicX, clicY, evt = attente_clic()
	print(clicX, clicY)

attente_clic()