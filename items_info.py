EQUIPAMENTS_DICT = {  # name:str , description:str , place:str , modifiers: dict of status to modify and number
	1: {"name": "small sword of wood" ,
	    "description": "Is it a toy?!" ,
	    "place": "hand" ,
	    "modifiers": {"attack": 2 ,
	                  "velocity": 3 ,
	                  "mana": 5
	                  }
	    } ,
}

POSSIBLE_CLUES = [
	"sight",
	"smell",
	"search",
	"taste",
	"touch",
	"listen",
]

ITEMS_INFO_DICT = {
	'bread1' : {'size':[.5,.5] , 'clues' : ['sight'] , 'card_idx':2},

}