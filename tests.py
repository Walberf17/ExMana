import time
options = ['R' , 'P' , 'S' , 'T']
player1 = input(f"Player 1, what would you like to choose?: {options}?")
player1 = player1.capitalize()



p1 = options.index(player1)
print("player 1 has chose")
time.sleep(0.5)
print("")

# player 2

print(f"Player 2, what would you like to choose?: {options}? ")

player2 = input("")
player2 = player2.capitalize()

p2 = options.index(player2)
print("Player 2 has chose")
print("")

if p1 == p2:
	print(f'Draw!!! you both took {options[p1]}')
elif (p1-1)%3 >= p2:
	print(f'player1 won with {options[p1]}')
else:
	print(f'player2 won with {options[p2]}')


