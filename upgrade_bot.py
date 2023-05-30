import berserk

session = berserk.TokenSession('ЗДЕСЬ_ВАШ_ТОКЕН')
client = berserk.Client(session=session)

client.account.upgrade_to_bot()
print('Done!')
