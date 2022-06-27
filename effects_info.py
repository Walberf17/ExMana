

EFFECT_INFO = {
	'Fire': 'fire_damage(5)'
}

# for maps
MAP_EFFECTS = {
	"Fire": {"color": "red" , "effect": ["fire_effect()"]} ,
	"Ice": {"color": "red" , "effect": ["ice_effect()"]} ,
	"Oil": {"color": "dark gray" , "effect": ["oil_effect()"]} ,
	"Firaga": {"color": "green" , "effect": ["firaga_effect()"]} ,
	"Oxigen": {"color": "pink" , "effect": []} ,
	"Poison": {"color": "dark green" , "effect": ["poison_effect()"]} ,
	"Explosion": {"color": "black" , "effect": ["explosion_effect()"]} ,
	"Light": {"color": "yellow" , "effect": []} ,
	"Smell": {"color": "green" , "effect": []} ,
	"Taste" : {"color": "green" , "effect": []},
	"Sight" : {"color": "green" , "effect": []},
	"Search" : {"color": "green" , "effect": []},
	"Throughtful Search": {"color": "green" , "effect": []},


}

EFFECT_INTERACTIONS = [
	["Oil" , "Fire" , "Firaga"] ,
	["Fire" , "Ice" , None] ,
	["Poison" , "Oxigen" , None] ,
	["Oxigen" , "Fire" , "Explosion"] ,
	["Oxigen" , "Firaga" , "Explosion"] ,
]

EFFECTS_AND_DAMAGE_INFO = [
	"fire_damage" ,  # usual args = (value)
	"ice_damage" , # usual args = (value)
	"poison_damage" , # usual args = (value)
	"ground_damage" , # usual args = (value)
	"wind_damage" , # usual args = (value)
	"electric_damage" , # usual args = (value)
	"dark_damage" , # usual args = (value)
	"light_damage" , # usual args = (value)
	"time_damage" , # usual args = (value)
	"oil_damage" , # usual args = (value)
	"gravity_damage" , # usual args = (value)
	"space_damage" , # usual args = (value)
	"pure_damage" , # usual args = (value)
	"stress_damage" , # usual args = (value)
	"physical_damage" , # usual args = (value)
	"feel_smell" , # usual args = (pos , area)
	"feel_taste" , # usual args = (pos , area)
	"feel_sight" , # usual args = (pos , area)
	"search" , # usual args = (pos , area)
	"throughtful_search" , # usual args = (pos , area)
	"move_card" , # usual args = (value)
	"get_item", # usual args = (self.rect , size)

]
