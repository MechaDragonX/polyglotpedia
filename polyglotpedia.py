from game import Game

VALID_RESPONSES = [
    '10',
    'i',
    'q',
    'quit'
]

def quit():
    print()
    print('Thanks for playing!')
    exit()

game = Game()

print('Would you like to play a game with 10 questions, or see who long you can surive with 3 lives?')
response = ''
exit_code = -1
while response not in VALID_RESPONSES:
    response = input('Please type "10" or "I": ').lower()
    match response:
        case '10':
            print()
            exit_code = game.compare_two_10()
        case 'i':
            print()
            exit_code = game.compare_two_inf()
        case 'q':
            exit_code = 1
        case 'quit':
            exit_code = 1

if exit_code == 1:
    quit()
