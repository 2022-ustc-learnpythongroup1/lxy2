import sys

from PyQt5.QtWidgets import QApplication

# from core.daemon import daemonize
from core.pet import DesktopPet
if __name__ == '__main__':
    argv = sys.argv
    if "--daemon" in argv:
        # daemonize()
        pass5
    if "--tray" in argv:
        tray = True
    else:
        tray = False
    app = QApplication(argv)
    pet = DesktopPet(tray=tray)
    pet.show()
    pet.ShowWelcome()
    sys.exit(app.exec())

