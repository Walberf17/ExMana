# Quests info

QUEST_KIND = [ # kind # exemple of goal
	'Place', # get to a place map001
	'NPC', # talk to a NPC  npc-h-2
	'Retrieve' , # Give something to a NPC [npc-h-2 , [[item_idx , quantity] , [item_idx , quantity]]]
	'Collect', # Collect something [[item_idx , quantity] , [2,4]]
	'Kill', # kill the monsters [[monter001 , 5] , [monter002 , 5]]
]

QUEST_DICT = {
	#   'Name': the name of the quest
	# 	'Description': a little text of what the player have to do
	# 	'Card_reward': the index or list of indexes of the card the player will get when completing the quest
	#   'Item_reward': the index or list of indexes of the items the player will get when completing the quest
	# 	'Kind': from QUEST_KIND, will tell how this quest will work.
	# 	'Goals': the goal, or a list of goal needed for complete the quest
	# 	'Chain_quest': it will reward a next quest, so that, when this is over, generates another
	# 	'Marks_reward': list of marks the player will get when the quest is over
	#   'Requirements': list of marks to get the quest
	#   'Talk_text': the text in the begining of the quest
	#   'Ending_text': the talk at the end of the quest

	1:{
		'Name': 'Tutorial',
		'Description': 'Find the NPC who talked to you and talk again',
		'Card_reward': 2,
		'Kind': 'NPC',
		'Goals': 1,
		'Chain_quest': False,
		'Marks_reward': [1],
		'Talk_text': 'Então, essa é a quest, vc vai ter de se virar pra fazer isso',
		'Ending_text': 'Você finalmente chegou ao final da bagaça, então é isso.'

	},


	1.1: {
		'name': 'Tutorial2',
		'Description': 'Find the door and exit',
		'Card_reward': 2,
		'Kind': 'Collect',
		'Goals': [[2 , 3] , [1,5]],

	},
}


QUEST_MARKS = {
	1: 'TUTORIAL COMPLETE',
}
