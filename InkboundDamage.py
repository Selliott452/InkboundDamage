import threading

from Display import root
from LogParser import LogParserThread, parse


def on_closing():
    root.quit()
    root.destroy()


# TODO: update using this algorithm https://pythonassets.com/posts/background-tasks-with-tk-tkinter/
if __name__ == "__main__":
    thread = LogParserThread()
    thread.start()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    SystemExit()
