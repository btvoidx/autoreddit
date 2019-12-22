import threading

def log(text, logtype):
	string = "[{}/{}]: {}".format(threading.current_thread().name, logtype, text)
	print(string)

class localization:
	new_post = "В группе новая запись."
	mailing_notification = "\n\n(Чтобы отписаться от рассылки напишите !отписаться)"