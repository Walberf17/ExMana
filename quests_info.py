# Quests info

QUEST_KIND = [ # kind # exemple of goal
	'Place', # get to a place map001
	'NPC', # talk to a NPC  npc-h-2
	'Retrieve' , # Give something to a NPC [npc-h-2 , [[item_idx , quantity] , [item_idx , quantity]]]
	'Collect', # Collect something [[item_idx , quantity] , [2,4]]
	'Kill', # kill the monsters [[monter001 , 5] , [monter002 , 5]]
]

QUEST_DICT = {
	1:{
		'name': 'Tutorial',
		'Description': 'Find the door and exit',
		'Card_reward': 2,
		'Kind': 'Collect',
		'Goals': [[1,3]]*5,
		'Chain_quest': True
	},
	1.1: {
		'name': 'Tutorial2',
		'Description': 'Find the door and exit',
		'Card_reward': 2,
		'Kind': 'Collect',
		'Goals': [[2 , 3] , [1,5]],

	},
}
