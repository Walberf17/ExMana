


# deck_list_cards_battle = list(x + 1 for x in range(11))

# Cards

EFFECTS_KINDS = [
	'Interact',
	'Get',
	'Fire',
	'Ice',
	'Poison',
	'Move',
	'Smell' ,
	'Taste' ,
	'Sight' ,
	'Search' ,
	'Thoughtful Search' ,
]


CARDS_DICT = {
	# 1:{
	# 'name': 'cool name for the card',
	# 'active_effects': [['Fire' , 'fire_damage(-2)' , 0 , [4,4]]], # index , action , duration , size
	# 'map_effect':[[index , 'fire_damage(-2)' , 0 , [4,4]]], # index , action , duration , size
	# 'cost': 15 | (2,15) # time cost | time cost , mana cost,
	# 'melee': False,
	# 'kind': from kinds list
	# }
	# index: dict{name:str, active_effects:list , map_effect:list , cost: list of float , melee:boolean
	# effects: [[effect1 , duration1 , size1] , [effect2 , duration2 , size2]]
	# size: list if max_rect , int if circle
	1: {
		"name": 'Descanse em Paz' ,
		'active_effects': [['Get' , "get_item(size)" , 0 , .5]] ,
		'map_effect': [['Fire' , 'fire_damage(-5)' , 1 , [2 , 2]]] ,
		'cost': 15 ,
		'melee': False ,
		'kind': 'Physic'
	} ,
	2: {
		'name': 'Cafungada Monstra' ,
		'active_effects': [['Smell' , 'feel_world(size , kind)' , 0, 5]] ,
		'cost': 5 ,
		'melee': True ,
		'kind': 'feel',
	} ,
	3: {
		'name': 'Assadura Grave' ,
		'active_effects': [['Fire' , 'fire_damage(-10)' , 0 , [1 , 1]] , ['Fire' , 'fire_damage(-5)' , 5 , [1 , 1]]] ,
		'map_effect': [['Fire' , 'fire_damage(-5)' , 1 , [2 , 2]]] ,
		'cost': 15 ,
		'melee': False ,
		'kind': 'Magic',
	} ,
	4: {
		'name': '22º em Moc' ,
		'active_effects': [['Ice' , 'ice_damage(-10)' , 0 , [1 , 1]] , ['Ice' , 'ice_damage(-5)' , 4 , [2 , 2]]] ,
		'map_effect': [['Ice' , 'ice_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 15 ,
		'melee': False ,
		'kind': 'Magic',
	} ,
	5: {
		'name': 'Movimento - 2pixel' ,
		'active_effects': [['Move' , 'move_card(2)' , 0 , .1]] ,
		'cost': 5 ,
		'melee': True ,
		'kind': 'movement',
	} ,

	6: {
		'name': 'Artigo de Luxo' ,
		'active_effects': [["Oil" , 'oil_damage(-10)' , 0 , [1 , 1]] , ['Poison' , 'poison_damage(-5)' , 5 , [3 , 3]]] ,
		'map_effect': [['Oil' , 'oil_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 7 ,
		'melee': False ,
		'kind': 'Physic',
	} ,
	7: {
		'name': 'Água Oxigenada 40 Volumes' ,
		'active_effects': [["Poison" , 'poison_damage(-2)' , 0 , .5] , ] ,
		'map_effect': [['Poison' , 'poison_damage(-5)' , 0 , [2 , 2]]] ,
		'cost': 1 ,
		'melee': True ,
		'kind': 'Physic',
	} ,
	8: {
		'name': 'Demo com Espada' ,
		'active_effects': [["Poison" , 'poison_damage(-4)' , 0 , .5] , ["Poison" , 'stress_damage(-4)' , 0 , .5] ,
		                   ["Poison" , 'physic_damage(-2)' , 5 , .5]] ,
		'cost': 1 ,
		'melee': True ,
		'kind': 'Physic',
	} ,
	9: {
		'name': 'Interagir' ,
		'active_effects': [["Interact" , 'interact(pos , size)' , 0 , .5]] ,
		'cost': 1 ,
		'melee': True ,
		'kind': 'Interact',
	} ,
}
