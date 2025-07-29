import pyqtgraph as pg
# from pyqtgraph import console
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit
# import time

print("finished importing")

# take in serial input; serial input displays pressure and temperature over time, it takes an input, sends an input, yay
# start with that pressure and temp over time; 
# thrust (use estimation); two pressures; 1 temperature
# left side: 4 graphs; right side: command sent (top), command recieved (bottom)
# thrust (top left), temperature (top right), pressure tank (bottom left), pressure combustion chamber (bottom right)
# graph side: takes in input 

#layout 1 (1 row, 2 columns); l1[0][0] has another layout widget that is a 2 x 2

# global status
status = "unarmed"
# three states exist: unarmed, armed, firing

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        bigBoi =  pg.LayoutWidget()

        print(status)

        #creating the halves
        graphWidgies = pg.LayoutWidget()
        interfaceWidgies = pg.LayoutWidget()

        #creating graphs
        self.thrustGraph = pg.PlotWidget()
        self.tempGraph = pg.PlotWidget()
        self.pressure_tank_Graph = pg.PlotWidget()
        self.pressure_combustionChamber_Graph = pg.PlotWidget()

        #adding graphs
        graphWidgies.addWidget(self.thrustGraph, row=0, col=0)
        graphWidgies.addWidget(self.tempGraph, row=0, col=1)
        graphWidgies.addWidget(self.pressure_tank_Graph, row=1, col=0)
        graphWidgies.addWidget(self.pressure_combustionChamber_Graph, row=1, col=1)

        #creating the interface quarters
        actionButtons = pg.LayoutWidget()
        valveButtons = pg.LayoutWidget()
        piOutput = pg.LayoutWidget()
        misc = pg.LayoutWidget()

        #creating buttons for ActionButtons
        self.firingButton = QtWidgets.QPushButton('FIRE')
        self.abortButton= QtWidgets.QPushButton('ABORT')

        self.purgeOpenButton = QtWidgets.QPushButton('Purge Open')
        self.purgeCloseButton = QtWidgets.QPushButton('Purge Close')

        self.valveOpenButton = QtWidgets.QPushButton('Valve Open')
        self.valveCloseButton = QtWidgets.QPushButton('Valve Close')

        # TODO: Make the buttons dinosaur-shaped

        # piOutput section
        # consoleLogger = pg.console.ConsoleWidget()
        self.password = QLineEdit("Password")
        # self.password.setEchoMode(QLineEdit.Password)
        self.password.textChanged.connect(self.passCheck)

        # misc
        self.plottingStartButton = QtWidgets.QPushButton("Enable Plotting")
        self.quitButton = QtWidgets.QPushButton("UNARM")
        self.armButton = QtWidgets.QPushButton("ARM")


        #linking buttons
        self.firingButton.clicked.connect(self.fire)
        self.abortButton.clicked.connect(self.abort)

        self.purgeOpenButton.clicked.connect(self.purgeO)
        self.purgeCloseButton.clicked.connect(self.purgeC)

        self.valveOpenButton.clicked.connect(self.valveO)
        self.valveCloseButton.clicked.connect(self.valveC)

        self.plottingStartButton.clicked.connect(self.plot_data)
        self.quitButton.clicked.connect(self.unarm)
        self.armButton.clicked.connect(self.arm)

        # TODO: sticky fingers option


        #adding the buttons to the layouts
        actionButtons.addWidget(self.firingButton, row=0, col=0)
        actionButtons.addWidget(self.abortButton, row=1, col=0)

        valveButtons.addWidget(self.purgeOpenButton, row=0, col=0)
        valveButtons.addWidget(self.purgeCloseButton, row=1, col=0)

        valveButtons.addWidget(self.valveOpenButton, row=0, col=1)
        valveButtons.addWidget(self.valveCloseButton, row=1, col=1)

        # adding the piOutput stuff
        # piOutput.addWidget(consoleLogger, row=0, col=0)


        # adding misc
        misc.addWidget(self.quitButton, row=0, col=0)
        misc.addWidget(self.armButton, row=0, col=1)
        misc.addWidget(self.plottingStartButton, row=1, col=0)
        misc.addWidget(self.password, row=1, col=1)

        #adding the interface widgies
        interfaceWidgies.addWidget(actionButtons, row=0, col=0)
        interfaceWidgies.addWidget(valveButtons, row=0, col=1)
        interfaceWidgies.addWidget(piOutput, row=1, col=0)
        interfaceWidgies.addWidget(misc, row=1, col=1)


        #finally adding it all to bigBoi
        bigBoi.addWidget(graphWidgies, row=0, col=0)
        bigBoi.addWidget(interfaceWidgies, row=0, col=1)


        self.central = bigBoi

        self.setWindowTitle("DinoSore")
        self.setCentralWidget(self.central)

    def fire(self):
        global status
        if status=="armed":
            print("FIRING")
            status = "firing"
        else:
            print("You can not fire!")
    def abort(self):
        print("ABORTING FETUSES")
    #     ONLY SEND COMMAND, NOTHING ELSE
    def valveO(self):
        if status=="unarmed":
            print("valve open")
        else:
            print("cannot access button!")
    def valveC(self):
        if status == "unarmed":
            print("valve closed")
        else:
            print("cannot access button!")
    def purgeO(self):
        if status == "unarmed":
            print("purge open")
        else:
            print("cannot access button!")
    def purgeC(self):
        if status == "unarmed":
            print("purge closed")
        else:
            print("cannot access button!")

    def plot_thrust(self, xData):
        print("thrust data")
        self.thrustGraph.setTitle("Thrust")
    def plot_temp(self, xData):
        print("temp data")
        self.tempGraph.setTitle("Temp")
    def plot_p_tank(self, xData):
        print("tank data")
        self.pressure_tank_Graph.setTitle("p_Tank")
    def plot_p_combustion_chamber(self, xData):
        print("combustion data")
        self.pressure_combustionChamber_Graph.setTitle("p_Combustion Chamber")

    def unarm(self):
        print("Unarming!")
        global status
        if status == "firing":
            print("buttons are now allowed!")
        status = "unarmed"
        print(status)
    #     Set background to normal
    def arm(self):
        print("arming!")
        global status
        if status != "armed":
            print("buttons are not longer allowed!")
        status = "armed"
        print(status)

    def passCheck(self, text):
        global status
        if text == "92130" and status == "armed":
            print("You are clear to fire!")
        else:
            print("You may not fire!")

    def plot_data(self):
        print("plotting")
        # figure out the whole time stuff
        xData = []

        self.plot_thrust(xData)
        self.plot_temp(xData)
        self.plot_p_tank(xData)
        self.plot_p_combustion_chamber(xData)


app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()
