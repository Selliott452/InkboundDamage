from threading import Thread

from Display import root
from LogParser import parse

if __name__ == '__main__':
    thread = Thread(target=parse).start()
    root.mainloop()
