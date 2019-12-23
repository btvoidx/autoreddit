import threading

def log(text, logtype):
	string = "[{}/{}]: {}".format(threading.current_thread().name, logtype, text)
	print(string)

class localization:
	new_post = "В группе новая запись."
	now = "Теперь"
	invalid_command = "Такой команды не существует!"

	mailing_notification = "(Изменять настройки рассылки можно по команде !рассылка)"
	mailing_level_current = "Ваши текущие настройки рассылки: "
	mailing_level_howtochange = "Чтобы изменить настройки рассылки, отправьте !рассылка (цифра от 0 до 3, отвечающая за уровень)."
	mailing_level_changed = "Настройки получения рассылки изменены."
	mailing_level_0 = "Вы не получаете рассылку."
	mailing_level_1 = "Вы получаете только эксклюзивные новости."
	mailing_level_2 = "Вы получаете эксклюзивные новости и записи, выложенные администрацией."
	mailing_level_3 = "Вы получаете эксклюзивные новости и все записи."
	mailing_level_invalid = "Уровень рассылки указан не верно. Доступные уровни: "
