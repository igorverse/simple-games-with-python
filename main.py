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


def mazeGame(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    print('Como o Naruto, este jogo pode ser duro às vezes...')
    hat = '^'
    hole = 'O'
    fieldCharacter = '░'
    pathCharacter = '*'

    playerPosition = [0, 0]
    isFinished = False

    def _generateField(height, width):
        field = []
        elementsOfTheField = [hole, fieldCharacter, fieldCharacter]

        for i in range(0, height):
            field.append([])

        for i in range(0, height):
            for j in range(0, width):
                randomElementOfTheField = elementsOfTheField[randint(0, 2)]

                field[i].append(randomElementOfTheField)

        field[0][0] = pathCharacter

        verticalHatPlace = randint(0, height - 1)
        horizontalHatPlace = randint(0, width - 1)

        while (verticalHatPlace == 0 or horizontalHatPlace == 0):
            verticalHatPlace = randint(0, height - 1)
            horizontalHatPlace = randint(0, width - 1)

        field[verticalHatPlace][horizontalHatPlace] = hat

        return field

    fieldHeightInput = int(input('Entre com a altura do campo: '))
    fieldWidthInput = int(input('Entre com a largura do campo: '))

    while (fieldHeightInput < 3 or fieldWidthInput < 3):
        print('\n A altura e largura devem ser maior que 2!')
        fieldHeightInput = int(input('Entre com a altura do campo: '))
        fieldWidthInput = int(input('Entre com a largura do campo: '))

    generatedField = _generateField(fieldHeightInput, fieldWidthInput)

    def _isOutside(verticalPosition, horizontalPosition):
        maxVerticalPosition = len(generatedField) - 1
        maxHorizontalPosition = len(generatedField[0])

        outsideCondition = verticalPosition > maxVerticalPosition or verticalPosition < 0 or horizontalPosition > maxHorizontalPosition or horizontalPosition < 0

        if (outsideCondition):
            return True

        return False

    def _isHat(playerLocation):
        if (playerLocation == hat):
            return True

        return False

    def _isHole(playerLocation):
        if (playerLocation == hole):
            return True

        return False

    def _gameplay(key):
        if (key.lower() != 'a' and key.lower() != 'w' and key.lower() != 'd' and key.lower() != 's'):
            print('Você deve usar A, W, D ou S para se mover!')

        if (key.lower() == 'a'):
            playerPosition[1] -= 1

        if (key.lower() == 'w'):
            playerPosition[0] -= 1

        if (key.lower() == 'd'):
            playerPosition[1] += 1

        if(key.lower() == 's'):
            playerPosition[0] += 1

        verticalPosition = playerPosition[0]
        horizontalPosition = playerPosition[1]

        if (_isOutside(verticalPosition, horizontalPosition)):
            print('\nVocê foi jubilado!')
            return True
        else:
            isHat = _isHat(
                generatedField[verticalPosition][horizontalPosition])
            isHole = _isHole(
                generatedField[verticalPosition][horizontalPosition])

            if (isHat):
                MAZE_PONTUATION = playerPosition[0] + playerPosition[1]

                session['pontuation'] += MAZE_PONTUATION

                print('Parabéns! Você conseguiu se formar!')
                print('Pontuação final: ', session['pontuation'])
                return True
            elif (isHole):
                print('É, meu caro... A FEI não é fácil!')
                print('Pontuação final: ', session['pontuation'])
                return True
            else:
                generatedField[verticalPosition][horizontalPosition] = pathCharacter

    print('Use A, W, D ou S para se mover!')

    while(not(isFinished)):
        for line in generatedField:
            print(''.join(line))

        playerMovement = input('\nQual direção? \n')

        if (playerMovement == '0'):
            break

        isFinished = _gameplay(playerMovement)

    currentUserSession(session)


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
        session['game'] = 'game2'
        mazeGame(session)
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
