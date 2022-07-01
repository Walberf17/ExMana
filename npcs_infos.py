"""
this is a list of speeches for the NPC to use in game.
"""


# default speeches for each kind of NPC

YOUNG_WOMEN = [
	"Oi, senhor?",
	"Como vai?",
	"Você vem muito por aqui?",
	"Você é um belo exemplar... ;)",
	"XD",
	"Muito quente aqui!",
]

YOUNG_MEN = [
	'Nossa!',
	'Calor!',
	'Cara, deu fome...',
	'Ah...',
]

CHILDREN = [
	"Oi, senhor!",
	"Mim dá isso?",
	"Você é velho?",
	"Quer bricar?",
	"O Jorge não mandou o video lá?",
	"Ontem a mulher das vacinas falou que eu vou ficar forte se eu tomar as vacinas!",
	"Bom dia!",
]



# Default NPC dict
NPCS_KIND_DICT = { # NPC_idx : the kinds it gets
	1: [CHILDREN , YOUNG_MEN],
	2: [YOUNG_WOMEN],
	3: [YOUNG_MEN]
}

