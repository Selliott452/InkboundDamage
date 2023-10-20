import threading

from Display import root
from LogParser import parse


def on_closing():
    root.quit()
    root.destroy()


# TODO: update using this algorithm https://pythonassets.com/posts/background-tasks-with-tk-tkinter/
if __name__ == "__main__":
    thread = threading.Thread(target=parse).start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    # TODO after threadifying logparser
    # thread.kill()
    exit()
