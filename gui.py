import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

print("finished importing")

# take in serial input; serial input displays pressure and temperature over time, it takes an input, sends an input, yay
# start with that pressure and temp over time; 
# thrust (use estimation); two pressures; 1 temperature
# left side: 4 graphs; right side: command sent (top), command recieved (bottom)
# thrust (top left), temperature (top right), pressure tank (bottom left), pressure combustion chamber (bottom right)
# graph side: takes in input 

#layout 1 (1 row, 2 columns); l1[0][0] has another layout widget that is a 2 x 2

# there is a timer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        bigBoi =  pg.LayoutWidget()

        #creating the halves
        graphWidgies = pg.LayoutWidget()
        interfaceWidgies = pg.LayoutWidget()

        #creating graphs
        thrustGraph  = pg.PlotWidget(background="black")
        tempGraph = pg.PlotWidget()
        pressure_tank_Graph = pg.PlotWidget()
        pressure_combustionChamber_Graph = pg.PlotWidget()

        #adding graphs
        graphWidgies.addWidget(thrustGraph, row=0, col=0)
        graphWidgies.addWidget(tempGraph, row=0, col=1)
        graphWidgies.addWidget(pressure_tank_Graph, row=1, col=0)
        graphWidgies.addWidget(pressure_combustionChamber_Graph, row=1, col=1)

        #creating the interface quarters
        actionButtons = pg.LayoutWidget()
        valveButtons = pg.LayoutWidget()
        piOutput = pg.GraphicsLayoutWidget()
        misc = pg.GraphicsLayoutWidget()

        #creating buttons for ActionButtons
        self.firingButton = QtWidgets.QPushButton('FIRE')
        self.abortButton= QtWidgets.QPushButton('ABORT')

        self.purgeOpenButton = QtWidgets.QPushButton('Purge Open')
        self.purgeCloseButton = QtWidgets.QPushButton('Purge Close')

        self.valveOpenButton = QtWidgets.QPushButton('Valve Open')
        self.valveCloseButton = QtWidgets.QPushButton('Valve Close')

        # TODO: Make the buttons dinosaur-shaped

        #linking buttons
        self.firingButton.clicked.connect(self.fire)
        self.abortButton.clicked.connect(self.abort)

        self.purgeOpenButton.clicked.connect(self.purgeO)
        self.purgeCloseButton.clicked.connect(self.purgeC)

        self.valveOpenButton.clicked.connect(self.valveO)
        self.valveCloseButton.clicked.connect(self.valveC)

        # sticky fingers option

        #adding the buttons to the layouts
        actionButtons.addWidget(self.firingButton, row=0, col=0)
        actionButtons.addWidget(self.abortButton, row=1, col=0)

        valveButtons.addWidget(self.purgeOpenButton, row=0, col=0)
        valveButtons.addWidget(self.purgeCloseButton, row=1, col=0)

        valveButtons.addWidget(self.valveOpenButton, row=0, col=1)
        valveButtons.addWidget(self.valveCloseButton, row=1, col=1)

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
        print("FIRING")
    def abort(self):
        print("ABORTING FETUSES")
    def valveO(self):
        print("valve open")
    def valveC(self):
        print("valve closed")
    def purgeO(self):
        print("purge open")
    def purgeC(self):
        print("purge closed")

app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()
