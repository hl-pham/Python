from upemtk import *
from time import sleep
from random import randint

# Mini-projet 3: Snake - Kévin SAVANE, TP2

"""
Ce programme permet de créer le jeu du snake.
Il existe 3 niveaux de difficultés, Débutant, Intermédiaire et Expert
Débutant: Ecran torique, sans obstacles, sans accélération
Intermédiaire: Ecran torique, avec accélération (+3 toutes les 5 pommes), 18 obstacles
Expert: Ecran non torique, avec accélération (+ la moitié de la vitesse précédente toutes les 3 pommes), 25 obstacles
On peut bien sur changer le corps principal du jeu dans Débutant, Intermédiaire et Expert par une fonction au lieu de réécrire 3 fois
le corps avec seulement quelques valeurs qui changent et des fonctions ajoutées/supprimées
"""


# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
	"""
	Fonction recevant les coordonnées d'une case du plateau sous la forme
	d'un couple d'entiers (ligne, colonne) et renvoyant les coordonnées du
	pixel se trouvant au centre de cette case. Ce calcul prend en compte la
	taille de chaque case, donnée par la variable globale taille_case.
	"""
	i, j = case
	return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
	"""
	Fonction permettant l'affichage des pommes
	"""
	x, y = case_vers_pixel(pommes)

	cercle(x, y, taille_case/2,
		   couleur='darkred', remplissage='red')
	rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
			  couleur='darkgreen', remplissage='darkgreen')


def affiche_obstacles(obstacles):
	"""
	Fonction permettant l'affichage des obstacles.
	"""
	i = 0
	while i < len(obstacles):
		x, y = case_vers_pixel([obstacles[i][0], obstacles[i][1]])

		rectangle(x-taille_case*.5, y-taille_case*.5, x+taille_case*.5, y+taille_case*.5,
			couleur='black', remplissage='black')
		i += 1


def affiche_serpent(serpent):
	"""
	Fonction permettant l'affichage du serpent.
	"""
	i = 0
	while i < len(serpent):
		x, y = case_vers_pixel([serpent[i][0], serpent[i][1]])

		cercle(x, y, taille_case/2 + 1,
		   	couleur='darkgreen', remplissage='green')
		i += 1


def change_direction(direction, touche):
	"""
	Fonction renvoyant la direction prise par le serpent.
	"""
	(x, y) = direction
	if touche == 'Up':
		# flèche haut pressée	
		if direction == (0, 1):
			x = 0
			y = 1
		else:
			x = 0
			y = -1
		direction = (x, y)
		return direction
	elif touche == 'Down':
		# flèche bas pressée
		if direction == (0, -1):
			x = 0
			y = -1
		else:
			x = 0
			y = 1
		direction = (x, y)
		return direction
	elif touche == 'Right':
		# flèche droite pressée
		if direction == (-1, 0):
			x = -1
			y = 0
		else:
			x = 1
			y = 0
		direction = (x, y)
		return direction
	elif touche == 'Left':
		# flèche gauche pressée
		if direction == (1, 0):
			x = 1
			y = 0
		else:
			x = -1
			y = 0
		direction = (x, y)
		return direction
	else:
		# pas de changement !
		return direction


def deplacement(direction, serpent):
	"""
	Permet le déplacement du serpent en
	retirant la queue (dernier élément de la liste)
	et en ajoutant une nouvelle tête (premier élément de la liste).
	"""
	new_head = [serpent[0][0]+direction[0], serpent[0][1]+direction[1]]
	serpent.insert(0, new_head)
	serpent.pop()


def ecran_pacman(serpent):
	"""
	Permet de transformer l'arène en arène torique (PacMan).
	"""
	i = 0
	while i < len(serpent):
		if serpent[i][0] < 0:
			serpent[i][0] = 39

		if serpent[i][0] > 39:
			serpent[i][0] = 0

		if serpent[i][1] < 0:
			serpent[i][1] = 29

		if serpent[i][1] > 29:
			serpent[i][1] = 0
		i += 1


def vitesse(nbPommes, framerate, acceleration, pommesMangees):
	"""
	Augmente la vitesse du jeu toutes les pommesMangees pommes,
	en renvoyant le taux de rafraichissement.
	"""
	if nbPommes % pommesMangees == 0:
		framerate += acceleration
	return framerate


def creer_obstacles(nbObstacle, obstacle, totalObstacle):
	"""
	Creer totalObstacle obstacles de manière aléatoire
	sur le terrain de jeu en renvoyant la liste obstacle.
	"""
	while nbObstacle != totalObstacle:
		obstacle.append([randint(0, 39), randint(0, 29)])
		if [0, 0] in obstacle:
			obstacle.remove([0,0])
			nbObstacle -= 1
		nbObstacle += 1
	return obstacle


def contact_obstacle(serpent, obstacle):
	"""
	Renvoie False si le serpent rentre dans un obstacle.
	False permettra de sortir de la boucle principale.
	"""
	indiceObstacle = 0
	while indiceObstacle < len(obstacle):
		if serpent[0] == obstacle[indiceObstacle]:
			return False
		indiceObstacle += 1
	return True


def contact_serpent(serpent):
	"""
	Renvoie False si le serpent rentre dans lui-meme.
	False permettra de sortir de la boucle principale.
	"""
	indiceSerpent = 1
	while indiceSerpent < len(serpent):
		if serpent[0] == serpent[indiceSerpent]:
			return False
		indiceSerpent += 1
	return True




# programme principal
if __name__ == "__main__":

	# initialisation du jeu
	direction = (0, 0)  						# direction initiale du serpent
	cree_fenetre(taille_case * largeur_plateau,
				 taille_case * hauteur_plateau)
	nbPommes = 0								# Nombre initial de pommes
	serpent = [[0, 0]]							# Coordonnées initiales du serpent
	pommes = [randint(0, 39), randint(0, 29)]	# Coordonnées de la première pomme
	tailleSerpent = 1							# Taille du serpent
	nbObstacle = 0								# Nombre d'obstacles
	obstacle = []								# Liste des coordonnées des obstacles
	difficulte = ""								# Difficulté du jeu: debutant, intermediaire ou expert


	# Corps principale du programme
	
	# Initialisation des variables msgPosX et msgPosY, pour définir le centre de la fenêtre. Variables utilisées pour afficher certaines messages
	msgPosX, msgPosY = case_vers_pixel((20, 13))

	texte(306, 141, "Cliquez sur une difficulté:", "blue","center","Purisa","20","")
	texte(306, 186, "Débutant", "green", "center", "Purisa", "20", "")
	texte(306, 216, "Intermédiaire", "green", "center", "Purisa", "20", "")
	texte(306, 246, "Expert", "green", "center", "Purisa", "20", "")


	# Choix de la difficulté en cliquant sur le nom de la difficulté
	while difficulte == "":
		clicX, clicY, evt = attente_clic()
		if (253 <= clicX <= 362) and (177 <= clicY <= 196):		# Difficulté Débutant
			difficulte = "debutant"
		elif (229 <= clicX <= 385) and (206 <= clicY <= 226):	# Difficulté Intermédiaire
			difficulte = "intermediaire"
		elif (270 <= clicX <= 347) and (236 <= clicY <= 262):	# Difficulté Expert
			difficulte = "expert"

	efface_tout()



	# Difficulté Débutant
	if difficulte == "debutant":
		framerate = 10   # taux de rafraîchissement du jeu en images/s
		texte(msgPosX, msgPosY, "Vous avez choisi la difficulté Débutant.", "blue","center","Purisa","18","")
		texte(msgPosX, msgPosY+30, "Mangez les pommes, pas le serpent !", "blue","center","Purisa","17","")
		texte(msgPosX, msgPosY+60, "Appuyez sur une touche pour lancer la partie.", "blue","center","Purisa","17","")
		attente_touche()

		while True:
			# affichage des objets
			efface_tout()
			texte(0, 0, "Score: {0}".format(nbPommes), "black","nw","Purisa","10","")
			affiche_pommes(pommes)
			affiche_serpent(serpent)
			mise_a_jour()

			# gestion des événements
			ev = donne_evenement()
			ty = type_evenement(ev)
			if ty == 'Quitte':
				break
			elif ty == 'Touche':
				direction = change_direction(direction, touche(ev))
			deplacement(direction, serpent)
			ecran_pacman(serpent)

			# Augmentation de la taille du serpent après ingestion d'une pomme
			if pommes in serpent:
				nbPommes += 1
				pommes = [randint(0, 39), randint(0, 29)]
				serpent.append([serpent[tailleSerpent-1][0]-direction[0], (serpent[tailleSerpent-1][1])-direction[1]])	# On ajoute un élément à la liste serpent
				tailleSerpent += 1

				# Test si la nouvelle pomme est créée sur le serpent. Si c'est le cas, on change les coordonnées de la pomme
				while pommes in serpent or (pommes in obstacle):
					pommes = [randint(0, 39), randint(0, 29)]
				affiche_pommes(pommes)

			# Affecte True ou False à continuer pour continuer ou sortir de la boucle principale
			continuer = contact_serpent(serpent)
			if continuer == False:
				break

			# attente avant rafraîchissement
			sleep(1/framerate)

		# fermeture et sortie
		efface_tout()

		# Affichage du message de fin de partie
		texte(msgPosX, msgPosY, "Perdu ! Vous avez mangé {0} pomme(s).".format(nbPommes), "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+30, "Vous ferez mieux la prochaine fois  ¯\\_(ツ)_/¯", "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+60, "Cliquez pour quitter le jeu.", "blue","center","Purisa","15","")
		attente_clic()
		ferme_fenetre()



	# Difficulte Intermédiaire
	elif difficulte == "intermediaire":
		framerate = 13   # taux de rafraîchissement du jeu en images/s
		texte(307, 173, "Vous avez choisi la difficulté Intermédiaire.", "blue","center","Purisa","18","")
		texte(307, 207, "Mangez les pommes, mais évitez les obstacles !", "blue","center","Purisa","17","")
		texte(307, 239, "Le jeu s'accélère !", "blue","center","Purisa","17","")
		texte(307, 271, "Appuyez sur une touche pour lancer la partie.", "blue", "center", "Purisa", "17", "")
		attente_touche()
		creer_obstacles(nbObstacle, obstacle, 18)


		while True:
			# affichage des objets
			efface_tout()
			texte(0, 0, "Score: {0}".format(nbPommes), "black","nw","Purisa","10","")
			affiche_obstacles(obstacle)
			affiche_pommes(pommes)
			affiche_serpent(serpent)
			mise_a_jour()

			# gestion des événements
			ev = donne_evenement()
			ty = type_evenement(ev)
			if ty == 'Quitte':
				break
			elif ty == 'Touche':
				direction = change_direction(direction, touche(ev))
			deplacement(direction, serpent)
			ecran_pacman(serpent)

			# Augmentation de la taille du serpent après ingestion d'une pomme
			if pommes in serpent:
				nbPommes += 1
				pommes = [randint(0, 39), randint(0, 29)]
				serpent.append([serpent[tailleSerpent-1][0]-direction[0], (serpent[tailleSerpent-1][1])-direction[1]])
				tailleSerpent += 1

				# Test si la nouvelle pomme est créée sur le serpent. Si c'est le cas, on change les coordonnées de la pomme
				while pommes in serpent or (pommes in obstacle):
					pommes = [randint(0, 39), randint(0, 29)]
				affiche_pommes(pommes)

				# Modifie le taux de rafraichissement du jeu pour l'accélérer
				framerate = vitesse(nbPommes, framerate, 3, 5)

			# Affecte True ou False à continuer pour continuer ou sortir de la boucle principale
			continuer = contact_obstacle(serpent, obstacle)
			if continuer == False:
				break

			continuer = contact_serpent(serpent)
			if continuer == False:
				break

			# attente avant rafraîchissement
			sleep(1/framerate)

		# fermeture et sortie
		efface_tout()

		# Affichage du message de fin de partie
		texte(msgPosX, msgPosY, "Perdu ! Vous avez mangé {0} pomme(s).".format(nbPommes), "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+30, "Vous ferez mieux la prochaine fois  ¯\\_(ツ)_/¯", "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+60, "Cliquez pour quitter le jeu.", "blue","center","Purisa","15","")
		attente_clic()
		ferme_fenetre()



	# Difficulte Expert
	elif difficulte == "expert":
		framerate = 10   # taux de rafraîchissement du jeu en images/s
		texte(307, 173, "Vous avez choisi la difficulté Expert.", "blue","center","Purisa","18","")
		texte(307, 207, "Mangez les pommes, mais évitez les obstacles !", "blue","center","Purisa","17","")
		texte(307, 239, "Le jeu s'accélère et l'écran n'est plus torique !", "blue","center","Purisa","17","")
		texte(307, 271, "Appuyez sur une touche pour lancer la partie.", "blue", "center", "Purisa", "17", "")
		attente_touche()
		creer_obstacles(nbObstacle, obstacle, 25)

		while True:
			# affichage des objets
			efface_tout()
			texte(0, 0, "Score: {0}".format(nbPommes), "black","nw","Purisa","10","")
			affiche_obstacles(obstacle)
			affiche_pommes(pommes)
			affiche_serpent(serpent)
			mise_a_jour()

			# gestion des événements
			ev = donne_evenement()
			ty = type_evenement(ev)
			if ty == 'Quitte':
				break
			elif ty == 'Touche':
				direction = change_direction(direction, touche(ev))
			deplacement(direction, serpent)

			# Ecran non torique. On regarde si les coordonnées du serpent dépassent de l'écran de jeu
			if serpent[0][0] not in range(0,40) or serpent[0][1] not in range(0,30):
				break

			# Augmentation de la taille du serpent après ingestion d'une pomme
			if pommes in serpent:
				nbPommes += 1
				pommes = [randint(0, 39), randint(0, 29)]
				serpent.append([serpent[tailleSerpent-1][0]-direction[0], (serpent[tailleSerpent-1][1])-direction[1]])
				tailleSerpent += 1

				while pommes in serpent or (pommes in obstacle):
					pommes = [randint(0, 39), randint(0, 29)]
				affiche_pommes(pommes)

				# Modifie le taux de rafraichissement du jeu pour l'accélérer
				framerate = vitesse(nbPommes, framerate, framerate//2, 3)

			# Affecte True ou False à continuer pour continuer ou sortir de la boucle principale
			continuer = contact_obstacle(serpent, obstacle)
			if continuer == False:
				break

			continuer = contact_serpent(serpent)
			if continuer == False:
				break

			# attente avant rafraîchissement
			sleep(1/framerate)

		# fermeture et sortie
		efface_tout()

		# Affichage du message de fin de partie
		texte(msgPosX, msgPosY, "Perdu ! Vous avez mangé {0} pomme(s).".format(nbPommes), "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+30, "Vous ferez mieux la prochaine fois  ¯\\_(ツ)_/¯", "blue","center","Purisa","15","")
		texte(msgPosX, msgPosY+60, "Cliquez pour quitter le jeu.", "blue","center","Purisa","15","")
		attente_clic()
		ferme_fenetre()

# Fin du programme