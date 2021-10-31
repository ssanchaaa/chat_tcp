import socket, getpass, sys, colorama, threading, time, datetime

colorama.init()


def log_in():
    passwd = input("Ваш пароль: ")
    sor.send((f'@$^name={alias}@$^pass={passwd}').encode('utf-8'))# Уведомляем сервер о подключении
    sys.stdout.write("\033[H\033[J")
    answr = ""
    t_end = time.time() + 10.0
    answr = sor.recv(1024)
    if answr.decode("utf-8") == "^$@goodLog_in":
        print(f"Добро пожаловать, {alias}")
        return 1
    elif answr.decode("utf-8") == "^$@incPass":
        print(f"Неверный пароль")
        return 0
    elif answr.decode("utf-8") == "^$@incLog":
        print("Нет такого логина")
        return 0
    elif answr.decode("utf-8") == "^$@alredExistLog":  
        print("Кто-то уже зашел в систему с вашего логина")
        return 0
    else:
        print("some error on the server")
        return 0
        
    
def auth():
    pas = input("Придумайте пароль: ")
    sor.send((f'@$^auth={alias}@$^pass={pas}').encode('utf-8'))
    sys.stdout.write("\033[H\033[J")
    
    data = ""
    data = sor.recv(1024)
    
    if data.decode("utf-8") == "^$@goodAuth":
        print(f"Добро пожаловать, {alias}")
        return 1
    elif data.decode("utf-8") == "^$@existsLog":
        print("Пользователь с таким логином уже зарегистрирован")
        return 0
    else:    
        print("some error on the server")
        return 0


def read_sok():
    while 1 :
        data = sor.recv(1024)
        print(data.decode('utf-8'))
        
         
server = 'localhost', 5050  # Данные сервера
sor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sor.bind(('', 0)) # Задаем сокет как клиент
sor.connect(server)
alias = ""

a = 0
while a == 0:
    action = input("1 - войти, 2 - зарегистрироваться: ")
    sys.stdout.write("\033[H\033[J")

    if action == str(1):
        alias = input("Ваш логин: ") # Вводим наш псевдоним
        a = log_in()
        
    elif action == str(2):
        alias = input("Придумайте логин: ") # Вводим наш псевдоним
        a = auth()

    else:
        print("incorrect value")


potok = threading.Thread(target= read_sok)
potok.start()

while 1 :
    msg = input('')
    print("")
    sys.stdout.write("\x1b[2A")
    print(f"{datetime.datetime.now().time()} вы: {msg}")
    sor.send(f'[{alias}]: {msg}'.encode('utf-8'))
    
    
colorama.deinit()    