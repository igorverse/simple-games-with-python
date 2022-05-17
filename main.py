import json
from random import randint
from unicodedata import normalize
from threading import Thread
from tabulate import tabulate


def currentUserSession(session):
    with open('members.json') as members:
        users = json.load(members)

    for user in users:
        if (user['login'] == session['login']):
            user.get(session['game'])['pontuation'] += session['pontuation']

            with open('members.json', 'w') as members:
                json.dump(users, members)

    Thread(target=keepPlaying, args=(session, )).start()


def isLoginCorrect(login, password):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json', encoding='utf-8') as members:
        users = json.load(members)

    isUserFounded = False

    for user in users:
        if (user['login'] == login and user['password'] == password):
            session = {
                'login': user['login'],
                'password': user['password'],
                'game': None,
                'pontuation': 0
            }

            Thread(target=gamesMenu, args=(session, )).start()
            isUserFounded = True

    if (not(isUserFounded)):
        print('\n🤦 Usuário não encontrado!')
        Thread(target=main).start()


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


def keepPlaying(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    print('\nQuer continuar jogando?')
    options = [[1, 'Continuar'], ['Qualquer tecla', 'Encerrar sessão']]
    headers = ['Digite', 'Operação']

    print(tabulate(options, headers, tablefmt="psql"))

    userAnswer = input('Escolha uma opção: ')

    if (userAnswer == '1'):
        Thread(target=gamesMenu, args=(session, )).start()
    else:
        Thread(target=main).start()


def registerUser(newUser, password):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json') as members:
        users = json.load(members)

    users.append({"login": newUser.lower(),
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

    themeTable = [[1, 'Heróis'], [2, 'Vilões'], [
        3, 'Nomes'], [4, 'Animais'], [5, 'Países'], ['Qualquer tecla', 'Encerrar sessão']]
    themeHeaders = ['Digite', 'Tema']

    print('\nJogo da Forca')
    print(tabulate(themeTable, themeHeaders, tablefmt='psql'))

    chooseTheme = input('Escolha uma opção: ')

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
        Thread(target=main).start()

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
            print('\n⚠️ Jogada inválida!\n')
            userGuess = input('Insira APENAS uma letra: ').lower()
            continue

        if (userGuess in guesses):
            print('⚠️ Você já usou esta letra!\n')
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

    print('O jogo acabou! Sua pontuação: ', session['pontuation'])

    Thread(target=currentUserSession, args=(session, )).start()


def mazeGame(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    print('\nLabirinto InFEInal')
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
        print('\n ⚠️ A altura e largura devem ser maior que 2!')
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
            print('\n⚠️ Você deve usar A, W, D ou S para se mover!\n')

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
            print('\nVocê foi jubilado! 🤦')
            return True
        else:
            isHat = _isHat(
                generatedField[verticalPosition][horizontalPosition])
            isHole = _isHole(
                generatedField[verticalPosition][horizontalPosition])

            if (isHat):
                MAZE_PONTUATION = playerPosition[0] + playerPosition[1]

                session['pontuation'] += MAZE_PONTUATION

                print('Parabéns! Você conseguiu se formar! 🎓')
                print('Pontuação final: ', MAZE_PONTUATION)
                return True
            elif (isHole):
                print('É, jovem... A FEI não é fácil! 🤦')
                print('Pontuação final: ', session['pontuation'])
                return True
            else:
                generatedField[verticalPosition][horizontalPosition] = pathCharacter

    print('\nUse A, W, D ou S para se mover!\n')

    while(not(isFinished)):
        for line in generatedField:
            print(''.join(line))

        playerMovement = input('\nQual direção? \n')

        if (playerMovement == '0'):
            break

        isFinished = _gameplay(playerMovement)

    Thread(target=currentUserSession, args=(session, )).start()


def scoreboard(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """
    with open('members.json', encoding='utf-8') as members:
        users = json.load(members)

    scoreTable = []
    scoreHeaders = ["Jogador", "Jogo da Forca",
                    "Labirinto InFEInal", "Pontuação total"]

    for user in users:
        totalScore = user['game1']['pontuation'] + user['game2']['pontuation']
        formattedUser = [user['login'], user['game1']
                         ['pontuation'], user['game2']['pontuation'], totalScore]

        scoreTable.append(formattedUser)

    TOTAL_SCORE_INDEX = 3

    for i in range(0, len(scoreTable)):
        for j in range(0, len(scoreTable) - i - 1):
            if (scoreTable[j][TOTAL_SCORE_INDEX] < scoreTable[j+1][TOTAL_SCORE_INDEX]):
                tmpHolder = scoreTable[j]
                scoreTable[j] = scoreTable[j+1]
                scoreTable[j+1] = tmpHolder

    scoreTable[0][0] = scoreTable[0][0].upper()
    scoreTable[0][0] += ' ᕦ(ò_óˇ)'

    print(tabulate(scoreTable, scoreHeaders, tablefmt="fancy_grid"))

    Thread(target=keepPlaying, args=(session, )).start()


def gamesMenu(session):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """

    gameOptions = [[1, 'Jogo da Forca'], [
        2, 'Labirinto InFEInal'], [3, 'Placar dos Jogos'], ['Qualquer tecla', 'Encerrar sessão']]
    gameOptionsHeaders = ['Digite', 'Operação']

    print('\nHora da diversão (ou não)! 🔥🔥')
    print(tabulate(gameOptions, gameOptionsHeaders, tablefmt='psql'))

    chooseOption = input('Escolha uma opção: ')

    if (chooseOption == '1'):
        HANGMAN_GAME_START_PONTUATION = 6

        session['game'] = 'game1'
        session['pontuation'] = HANGMAN_GAME_START_PONTUATION

        Thread(target=hangmanGame, args=(session, )).start()
    elif (chooseOption == '2'):
        session['game'] = 'game2'

        Thread(target=mazeGame, args=(session, )).start()
    elif (chooseOption == '3'):
        scoreboard(session)
    else:
        Thread(target=main).start()


def main():
    loginOptions = [[1, 'Fazer Login'], [
        2, 'Registrar-se'], ['Qualquer tecla', 'Sair']]
    loginHeaders = ['Digite', 'Operação']

    print('\n🖖  Saudações 🖖')
    print(tabulate(loginOptions, loginHeaders, tablefmt='psql'))

    loginMenu = input('Escolha uma opção: ')

    if (loginMenu == '1'):
        user = input('usuário: ')
        password = input('senha: ')

        Thread(target=isLoginCorrect, args=(user, password, )).start()
    elif (loginMenu == '2'):
        newUser = input('nome de usuário: ')
        password = input('senha: ')

        while (isUserAlreadyRegistered(newUser)):
            print('⚠️ Este nome de usuário já foi registrado. Tente um outro...')
            newUser = input('nome de usuário: ')

        Thread(target=registerUser, args=(newUser, password,)).start()

        print('Seja bem-vindx, %s! 🚀🚀🚀' % (newUser))

        session = {
            'login': newUser,
            'password': password,
            'game': None,
            'pontuation': 0
        }

        gamesMenu(session)
    else:
        print('\n👋 Até a próxima!')


main()
