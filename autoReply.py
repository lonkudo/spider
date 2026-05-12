from pywinauto import Application, timings
from pywinauto.keyboard import send_keys
from sound import pop_hint

import time

class AutoReply:
    app = None
    win = None
    def __init__(self):
        Application(backend="uia").start(r"C:\Users\ASUS\AppData\Roaming\Telegram Desktop\Telegram.exe")
        self.app = Application(backend="uia").connect(path="Telegram.exe")

        self.win = self.app.top_window()
        self.win.wait("visible", timeout=10)

    def focus(self):
        try:
            self.win.restore()
        except:
            pass
        self.win.set_focus()


    def chatInput(self,messages):
        # Find all Edit controls (Telegram usually has only 1)
        edits = self.win.descendants(control_type="Edit")

        if not edits:
            raise Exception("No Edit control found. Search box not available.")

        search_box = edits[0]

        search_box.click_input()

        # Clear old text
        send_keys("^a{BACKSPACE}")

        # Type chat name
        send_keys(messages)

        # Press Enter to open chat
        send_keys("{ENTER}")

    def chatPaste(self):
        # Find all Edit controls (Telegram usually has only 1)
        # paste messages
        send_keys("^v")
        send_keys("{ENTER}")

    def searchChat(self,chat_name):
        # Focus the search bar using Ctrl+K

        send_keys("{ESC}{ESC}")  # blur chat
        send_keys("^f")  # when chat is blurred , ctrl+f focuses chat search
        time.sleep(0.2)

        # Type the chat name
        send_keys("^a{BACKSPACE}")  # clear previous text
        send_keys(chat_name, with_spaces=True)
        time.sleep(0.4)

        # Open the chat
        send_keys("{ENTER}")
        time.sleep(0.4)

    def pasteToChat(self,chatname):
        self.giveHint()
        self.focus()
        # self.searchChat(chatname)
        self.chatPaste()

    def giveHint(self):
        pop_hint()



if __name__ == "__main__":
    auto = AutoReply()
    tree = auto.win.dump_tree()
    print(tree)


