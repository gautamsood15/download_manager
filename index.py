from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
import os.path
from PyQt5.uic import loadUiType


ui = loadUiType('main.ui')

class MainApp(QMainWindow , ui):
    def __init__(self, parent=None):
        