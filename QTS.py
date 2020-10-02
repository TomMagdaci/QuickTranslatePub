from interface import implements, Interface
import time
import keyboard
import webbrowser
import win32clipboard
import win32api
from selenium import webdriver
import time

############################################

class Animation(Interface):

    def doOneFrame(self):
        pass

    def shouldStop(self) -> bool:
        pass

############################################

class AnimationRunner(object):
    def __init__(self):
        self._pauseTime = 0.05
        return

    def run(self, ani: Animation):
        while not ani.shouldStop():
            ani.doOneFrame()
            time.sleep(self._pauseTime)

    def buildAnimationRunner(cls):
        return AnimationRunner()

############################################

class Holding(implements(Animation)):
    def __init__(self):
        self._stop = False
        self._ani = AnimationRunner()
        self._isAlreadyPressed = True
        self._browser = webdriver.Edge()
        self._browser.get("https://translate.google.com/?um=1&ie=UTF-8&hl=iw&client=tw-ob#view=home&op=translate&sl=en&tl=iw&text=")
        time.sleep(3)
        self._browser.minimize_window()

    def shouldStop(self):
        return self._stop

    def doOneFrame(self):
        # is pressed == the last button that was pressed.
        if keyboard.is_pressed('alt'):
            self._stop = True
            self._browser.quit()
        keyboard.wait('esc')
        time.sleep(0.2)
        keyboard.press('ctrl')
        keyboard.press('c')
        time.sleep(0.2)
        keyboard.release('c')
        keyboard.release('ctrl')
        self.translateClipboardSentence()
        return

    def translateClipboardSentence(self):
        senToTran = self.getSenFromClip()
        senConcatenated = self.createConcatenatedSen(senToTran)
        url = "https://translate.google.com/?um=1&ie=UTF-8&hl=iw&client=tw-ob#view=home&op=translate&sl=en&tl=iw&text=" \
              + senConcatenated
        self._browser.get(url)
        self._browser.set_window_size(1400,900)
        state_left = win32api.GetKeyState(0x01)
        time.sleep(1.5)
        a = win32api.GetKeyState(0x01) #get the mouse key state after 1.5 seconds
        if a != state_left:  # Button state changed
            time.sleep(4)
        self._browser.minimize_window()
        return

    def getSenFromClip(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        res = data.split()
        return res

    def createConcatenatedSen(self, sen):
        senConcatenated = ""
        for i in sen:
            senConcatenated += i
            if i == sen[-1]:
                break
            senConcatenated += '+'
        return senConcatenated

############################################
############################################

def main():
    ani = AnimationRunner()
    ani.run(Holding())

main()

