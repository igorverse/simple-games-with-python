import json
from random import randint
from unicodedata import normalize


def isLoginCorrect(login, password):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json', encoding='utf-8') as members:
        users = json.load(members)

    for user in users:
        if (user['login'] == login and user['password'] == password):
            return True

    return False


def isUserAlreadyRegistered(login):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json', encoding='utf-8') as members:
        users = json.load(members)

    for user in users:
        if (user['login'] == login):
            return True

    return False


def registerUser(newUser, password):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json') as members:
        users = json.load(members)

    users.append({"login": newUser,
                  "password": password,
                  "game1": {
                      "pontuation": 0
                  },
                  "game2": {
                      "pontuation": 0
                  }
                  })

    with open('members.json', 'w') as members:
        json.dump(users, members)


def hangmanGame():
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """

    with open('hangmanWords.json') as file:
        words = json.load(file)

    chooseTheme = input(
        '1 - Heróis\n 2 - Vilões\n 3 - Nomes\n 4 - Animais\n 5 - Países\n Escolha uma opção de tema: ')
    wordTheme = ''

    if (chooseTheme == '1'):
        wordTheme = 'heroes'
    elif (chooseTheme == '2'):
        wordTheme = 'vilains'
    elif (chooseTheme == '3'):
        wordTheme = 'names'
    elif (chooseTheme == '4'):
        wordTheme = 'animals'
    elif (chooseTheme == '5'):
        wordTheme = 'countries'
    else:
        raise Exception('Not implemented')

    hangmanWord = (words[wordTheme][randint(
        0, len(words[wordTheme]) - 1)]).lower()

    treatedHangmanWord = normalize('NFKD', hangmanWord).encode(
        'ascii', 'ignore').decode('ascii')

    encryptedWord = ''

    for letter in treatedHangmanWord:
        if (letter != ' '):
            encryptedWord += '_'
        else:
            encryptedWord += ' '

    hangmanEvolution = ['''
  *---*
  |   |
      |
      |
      |
      |
=========''', '''
  *---*
  |   |
  O   |
      |
      |
      |
=========''', '''
  *---*
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  *---*
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  *---*
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  *---*
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

    userMissesCounter = 0
    userGuess = input('Insira uma letra: ')
    while(not(userGuess.isalpha()) or len(userGuess) != 1):
        print('\nJogada inválida!\n')
        userGuess = input('Insira APENAS uma letra: ')

    # while (userMissesCounter < 6 or encryptedWord != hangmanWord):


def mazeGame():
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    raise Exception('Not implemented!')


def scoreboard():
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    raise Exception('Not implemented!')


def gamesMenu():
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    chooseOption = input(
        '***************************************\nHora da diversão (ou não)!\n 1 - Jogo da Forca \n 2 - Labirinto InFEInal \n 3 - Placar dos Jogos\n Escolha uma opção: ')

    if (chooseOption == '1'):
        hangmanGame()
    elif (chooseOption == '2'):
        mazeGame()
    elif (chooseOption == '3'):
        scoreboard()
    else:
        print('Ops! Opção inválida!')


def main():
    loginMenu = input(
        'Bem-vindo! \n 1 - Login \n 2 - Registrar-se no sistema \n tecla qualquer - Sair\n Digite: ')

    if (loginMenu == '1'):
        user = input('usuário: ')
        password = input('senha: ')

        if (isLoginCorrect(user, password)):
            gamesMenu()
        else:
            print('\nUsuário ou senha inválida')
            print('------------------------')
            main()
    elif (loginMenu == '2'):
        newUser = input('nome de usuário: ')
        password = input('senha: ')

        while (isUserAlreadyRegistered(newUser)):
            print('Este nome de usuário já foi registrado. Tente um outro...')
            newUser = input('nome de usuário: ')

        registerUser(newUser, password)
        print('Seja bem-vindo, %s!' % (newUser))
    else:
        print('Até mais! =)')


main()
