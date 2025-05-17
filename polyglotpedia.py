from game import Game

def quit():
    print()
    print('Thanks for playing!')
    exit()

game = Game()

print('Would you like to play a game with 10 questions, or see who long you can surive with 3 lives?')
response = ''
exit_code = -1
while True:
    response = input('Please type "10" or "I": ').lower()
    match response:
        case '10':
            print()
            exit_code = game.compare_two_10()
            break
        case 'i':
            print()
            exit_code = game.compare_two_inf()
            break
        case 'q':
            exit_code = 1
        case 'quit':
            exit_code = 1

if exit_code == 1:
    quit()
