import json


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


def main():
    loginMenu = input(
        'Bem-vindo! \n 1 - Login \n 2 - Registrar-se no sistema \n tecla qualquer - Sair\n Digite: ')

    if (loginMenu == '1'):
        user = input('usuário: ')
        password = input('senha: ')

        if (isLoginCorrect(user, password)):
            print('gamesMenu()')
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
