# Berserk Bot Tutorial

У lichess.org недавно появился свой python-клиент для Lichess Api. Изучив его, вы можете найти в документации несколько ошибок, а также не найти ни одного полного примера кода такого бота. В этой статье автор попытался исправить эти недостатки и показать процесс создания бота на python.

# Оглавление
### 1.) [Установка Python](#пункт1)
### 2.) [Установка необходимых библиотек](#пункт2)
### 3.) [Создание аккаунта и получение API токена](#пункт3)
### 4.) [Обновление учетной записи до учетной записи BOT](#пункт4)
### 5.) [Класс Game. Принятие вызовов](#пункт5)
### 6.) [Общение в чате и делание ходов](#пункт6)
### 7.) [RandomMover Bot](#пункт7)
### 8.) [Что дальше?](#пункт8)


<a name="пункт1"></a> 
# 1.) Установка Python на ПК.

### Windows:

Переходим на [официальный сайт Python](https://www.python.org/downloads/windows/) и скачиваем любую версию (минимум 3.8)

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/44b16bc4-7e9e-4ff2-9dbe-7d7266cd29a6)

После этого открываем скачанный .exe файл и следуем **инструкциям** по установке.

### Linux:
(Не думаю, что если вы используете линукс, то не знаете, как установить Python :D)

Переходим в консоль и вводим ```$ sudo apt-get install python[version]```, где вместо [version] подставляем любую версию (минимум 3.8).

### MacOS:

Открываем консоль, пишем ```brew install python[version]```, где вместо [version] подставляем любую версию (минимум 3.8).

<a name="пункт2"></a>
# 2.) Установка необходимых библиотек.

В консоли пишем ```pip install berserk``` или ```pip3 install berserk```. После успешной установки делаем то же самое с модулем **chess**: ```pip install chess``` или ```pip3 install chess```. 

Теперь наш ПК готов приступить к работе!

<a name="пункт3"></a>
# 3.) Создание аккаунта и получение API токена.

Заходим на сайт lichess.org и регистрируем **новый** аккаунт (важно, чтобы на этом аккаунте **не было сыграно ни одной игры**). После этого подтверждаем электронную почту.

Затем переходим [по ссылке](https://lichess.org/account/oauth/token) или вручную переходим на **страницу**: Главное Меню -> Настройки -> API access tokens

После этого генерируем новый токен и копируем его себе. **Важно!** Никто не должен видеть этот токен, иначе другие пользователи смогут получить доступ к учетной записи вашего бота:

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/85c02d39-2e2b-429f-ae98-81977dd8764d)

В разрешениях токена выбирайте все, что **может потребоваться** вашему боту в будущем.

<a name="пункт4"></a>
# 4.) Обновление учетной записи до учетной записи "BOT".

Создаем новый файл, например ```upgrade_bot.py``` и вводим туда следующий код:

```
import berserk

session = berserk.TokenSession('ЗДЕСЬ_ВАШ_ТОКЕН')
client = berserk.Client(session=session)

client.account.upgrade_to_bot()
print('Done!')
```

Сохранив изменения, переходим в консоль и запускаем наш код: ```python upgrade_bot.py``` или ```python3 upgrade_bot.py```. В случае успешного выполнения, на lichess рядом с вашим ником должна появиться **надпись "BOT"**, а в консоли выведено "Done!"

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/53cee44c-6d0e-4490-999d-1c705abb7970)


<a name="пункт5"></a>
# 5.) Класс Game. Принятие вызовов.

Создадим новый файл ```bot.py``` и импортируем необходимые библиотеки:

```
import berserk
import threading
```
***
Создадим переменную client:
```
session = berserk.TokenSession('ЗДЕСЬ_ВАШ_ТОКЕН')
client = berserk.Client(session=session)
```
***
Теперь опишем класс, который будет осуществлять проверку изменений состояния игры:
```
class Game(threading.Thread):
    def __init__(self, client, game_id, color, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
	self.color = color
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)
                
    def handle_state_change(self, state):
        pass
    def handle_chat_line(self, line):
        pass
      
```
***
Чтобы бот мог играть партии, ему необходимо принимать вызовы:
<a name="переменная_event"></a>
```
for event in client.bots.stream_incoming_events():
	  if event['type'] == 'challenge':
		    if event['challenge']['variant']['key'] == 'standard':
			      client.bots.accept_challenge(event['challenge']['id'])
```
**Готово!** Наш бот может принимать все вызовы со стандартным вариантом шахмат. 
***
После принятия вызова необходимо начать взаимодействие с созданным классом Game:
```
game = Game(client, event['challenge']['id'], event['challenge']['finalColor'])
game.start()
```
Кстати, даже в таком банальном коде в документации имеется ошибка:

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/00b4de98-9e46-4c75-b78d-39cdc7940adb)

Если вы попробуете написать так, то программа завершится ошибкой **KeyError: 'id'**

<a name="пункт6"></a>

# 6.) Общение в чате и делание ходов.

Для начала научим нашего бота **говорить**. Для этого изменим функцию handle_chat_line():
```
def handle_chat_line(self, line):
    if line['username'].upper() != 'ИМЯ_ВАШЕГО_БОТА'.upper():
    	client.bots.post_message(self.game_id, 'Привет! Теперь я умею писать в чате:)')
```
Теперь бот будет отвечать на любое текстовое сообщение в чате.

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/25be85f5-acea-4562-b8ae-a1dfd0726258)

Теперь перейдем к деланию ходов. Для этого у нас есть другая функция, handle_state_change(). Точнее говоря, ход вы можете сделать и в любом другом месте используя ``` client.bots.make_move(self.game_id, 'ход') ```.
```
def handle_state_change(self, state):
    if self.color.upper() == 'BLACK':
    	if len(state['moves'].split()) % 2 == 0:
	    client.bots.make_move(self.game_id, 'g2g4')
		
```
Теперь наш бот может делать первый ход **g2-g4** за белых. 

Важно! LiChess передает данные (в нашем случае [переменную event](#переменная_event)) от лица пользователя (не от бота), поэтому в ```self.color``` у нас хранится цвет фигур противника. При сильном желании, это можно изменить, но, честно говоря, автор не видит в этом смысла.

<a name="пункт7"></a>
# 7.) RandomMover Bot

Теперь, используя уже ранее упомянутые функции и ранее установленную **библиотеку chess**, мы легко можем написать бота, который отвечает случайными ходами. Для этого изменим функцию  handle_state_change(): 
```
def handle_state_change(self, state):
    if self.color.upper() == 'BLACK' and len(state['moves'].split()) % 2 == 0:
        board = chess.Board()
        for move in state['moves'].split():
            board.push(chess.Move.from_uci(move))
            sp = []
            for a in board.legal_moves:
        	sp.append(a)
            if sp:
        	try:
        	    client.bots.make_move(self.game_id, random.choice(sp))
        	except Exception as e:
        	    print(e)
```
Давайте разберемся, что здесь происходит.

 ``` if self.color.upper() == 'BLACK' and len(state['moves'].split()) % 2 == 0: ```

Проверяем, если ход белых, то играем ли мы за белых. Действительно, при каждом ходе белых число сделанных ходов должно быть четно.


*** 
``` 
board = chess.Board()
for move in state['moves'].split():
    board.push(chess.Move.from_uci(move)) 
```

Создаём **шахматную доску** с начальной позицией и по очереди делаем на доске ходы, сделанные в партии.


***
``` 
sp = []
for a in board.legal_moves:
    sp.append(a)
```

Создаем пустой список и добавляем **все возможные** ходы на доске

*** 
``` 
if sp:
    try:
    	client.bots.make_move(self.game_id, random.choice(sp))
    except Exception as e:
    	print(e)
```

Если список **не пустой**, делаем ход, случайно выбранный из списка sp с помощью random.choice(). Если список будет пустой, соответственно, на доске нельзя сделать никакой ход, то есть **игра закончена**.

Аналогичный код пишем в случае, если self.color = 'white':
```
elif self.color.upper() == 'WHITE' and len(state['moves'].split()) % 2 == 1:
    board = chess.Board()
    for move in state['moves'].split():
    	board.push(chess.Move.from_uci(move)
	sp = []
	for a in board.legal_moves:
	    sp.append(a)
	    if sp:
	    	try:
		    client.bots.make_move(self.game_id, random.choice(sp))
		except Exception as e:
		    print(e)
```

[Полный код бота](https://github.com/theslothbear/berserk-tutorial/blob/main/random_mover_bot.py)

<a name="пункт8"></a>
# 8.) Что дальше?

Дальше - только ваша фантазия :). 
Вот несколько полезных ссылок, которые помогут вам с дальнейшим изучением:

* [Berserk Github](https://github.com/lichess-org/berserk)
* [Документация Berserk](https://lichess-org.github.io/berserk/)
* [Документация для разработчиков](https://lichess-org.github.io/berserk/api.html)
* [Документация библиотеки chess](https://python-chess.readthedocs.io/en/latest/)
* [Пример создания простого ИИ на js](https://habr.com/ru/companies/skillbox/articles/437524/)
