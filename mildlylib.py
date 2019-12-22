import threading

def log(text, logtype):
	string = "[{}/{}]: {}".format(threading.current_thread().name, logtype, text)
	print(string)