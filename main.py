import json
from random import randint
from unicodedata import normalize
from threading import Thread


def currentUserSession(session):
    with open('members.json') as members:
        users = json.load(members)

    for user in users:
        if (user['login'] == session['login']):
            user.get(session['game'])['hasPlayed'] = True
            user.get(session['game'])['pontuation'] += session['pontuation']

            with open('members.json', 'w') as members:
                json.dump(users, members)


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


def hangmanGame(session):
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

    encryptedWord = []

    for letter in treatedHangmanWord:
        if (letter != ' '):
            encryptedWord.append('_')
        else:
            encryptedWord.append(' ')

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

    guesses = set()
    userMissesCounter = 0
    isARightGuess = False

    print('\nLetras já usadas: ', {})
    print('Tema: ', wordTheme)
    print(hangmanEvolution[0])
    print(''.join(encryptedWord))
    userGuess = input('Insira uma letra: ').lower()

    while (userMissesCounter < 6):
        isARightGuess = False

        if (not(userGuess.isalpha()) or userGuess == 'ç' or len(userGuess) != 1):
            print('\n!!! Jogada inválida!\n')
            userGuess = input('Insira APENAS uma letra: ').lower()
            continue

        if (userGuess in guesses):
            print('!!! Você já usou esta letra!\n')
            userGuess = input('Insira uma letra não usada: ').lower()
            continue

        guesses.add(userGuess)

        for i in range(0, len(treatedHangmanWord)):
            if (userGuess == treatedHangmanWord[i]):
                encryptedWord[i] = userGuess
                isARightGuess = True

        if (not(isARightGuess)):
            session['pontuation'] -= 1
            userMissesCounter += 1

        print('\nLetras já usadas: ', guesses)
        print('Tema: ', wordTheme)
        print(hangmanEvolution[userMissesCounter])
        print(''.join(encryptedWord))

        if (''.join(encryptedWord) == treatedHangmanWord):
            break

        if (userMissesCounter < 6):
            userGuess = input('\nInsira uma letra: ').lower()

    if (userMissesCounter == 6):
        print(''.join(encryptedWord) + ' --> ' + treatedHangmanWord)

    currentUserSession(session)


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


def gamesMenu(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    chooseOption = input(
        '***************************************\nHora da diversão (ou não)!\n 1 - Jogo da Forca \n 2 - Labirinto InFEInal \n 3 - Placar dos Jogos\n Escolha uma opção: ')

    if (chooseOption == '1'):
        HANGMAN_GAME_START_PONTUATION = 6

        session['game'] = 'game1'
        session['pontuation'] = HANGMAN_GAME_START_PONTUATION
        hangmanGame(session)
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
            session = {
                'login': user,
                'password': password,
                'game': None,
                'pontuation': 0
            }
            gamesMenu(session)
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
        gamesMenu()
    else:
        print('Até mais! =)')


main()
