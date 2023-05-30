# Berserk Bot Tutorial

У LiChess недавно появился свой python-клиент для Lichess Api. Изучив его, вы можете найти в документации несколько ошибок, а также не найти ни одного полного примера кода такого бота. В этой статье автор попытался исправить эти недостатки и показать процесс создания бота на python.

## 1.) Установка Python на ПК.

### Windows:

Переходим на [официальный сайт Python](https://www.python.org/downloads/windows/) и скачиваем любую версию (минимум 3.8)

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/44b16bc4-7e9e-4ff2-9dbe-7d7266cd29a6)

После этого открываем скачанный .exe файл и следуем инструкциям по установке.

### Linux:
(Не думаю, что если вы используете линукс, то не знаете, как установить Python :D)

Переходим консоль и вводим ```$ sudo apt-get install python[version]```, где вместо [version] подставляем любую версию (минимум 3.8).

### MacOS:

Открываем консоль, пишем ```brew install python[version]```, где вместо [version] подставляем любую версию (минимум 3.8).

## 2.) Установка необходимых библиотек

Открываем консоль, пишем ```pip install berserk``` или ```pip3 install berserk```. После успешной установки делаем то же самое с модулем **chess**: ```pip install chess``` или ```pip3 install chess```. 

Теперь наш ПК готов приступить к работе!

## 3.) Создание аккаунта LiChess для бота

Заходим на сайт lichess.org и регистрируем новый аккаунт (важно, чтобы на этом аккаунте не было сыграно ни одной игры). После этого подтверждаем электронную почту.

## 4.) Получение API токена Lichess

Переходим [по ссылке](https://lichess.org/account/oauth/token) или вручную переходим на страницу: Главное Меню -> Настройки -> API access tokens

После этого генерируем новый токен и копируем его себе. Важно! Никто не должен видеть этот токен, иначе другие пользователи смогут получить доступ к учетной записи вашего бота:

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/85c02d39-2e2b-429f-ae98-81977dd8764d)

В разрешениях токена выбирайте все, что может потребоваться вашему боту в будущем.

## 5.) Обновление учетной записи до учетной записи "BOT".

Создаем новый файл, например ```upgrade_bot.py``` и вводим туда следующий код:

```
import berserk

session = berserk.TokenSession('ЗДЕСЬ_ВАШ_ТОКЕН')
client = berserk.Client(session=session)

client.account.upgrade_to_bot()
print('Done!')
```

Сохранив изменения, переходим в консоль и запускаем наш код: ```python upgrade_bot.py``` или ```python3 upgrade_bot.py```. В случае успешного выполнения, на lichess рядом с вашим ником должна появиться надпись "BOT", а в консоли выведено "Done!"

![image](https://github.com/theslothbear/berserk-tutorial/assets/128232763/3466dd08-d3d3-454a-b5a1-c738ca11a376)

## 6.) Общение в чате и делание ходов.

Создадим новый файл ```bot.py``` и импортируем необходимые библиотеки:

```
import berserk
import threading
```
Создадим переменную client:
```
session = berserk.TokenSession('ЗДЕСЬ_ВАШ_ТОКЕН')
client = berserk.Client(session=session)
```
Теперь опишем класс, который будет осуществлять проверку изменений состояния игры:
```
class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
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
Нам необходимо каким-либо образом взаимодействовать с созданным классом. Для этого ниже пишем следующий код:
```
for event in client.bots.stream_incoming_events():
	  if event['type'] == 'challenge':
		    if event['challenge']['variant']['key'] == 'standard':
			      client.bots.accept_challenge(event['challenge']['id'])
```
Теперь бот может принимать все вызовы со стандартным вариантом шахмат. 




