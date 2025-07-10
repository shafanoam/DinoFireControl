import pyqtgraph as pg
from PyQt5 import QtWidgets

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
        graphWidgies = bigBoi.addLayout(row=0, col=0)
        interfaceWidgies = bigBoi.addLayout(row=0, col=1)
        thrustGraph = graphWidgies.addWidget(pg.PlotWidget(background="black"), row=0, col=0)
        tempGraph = graphWidgies.addWidget(pg.PlotWidget(), row=0, col=1)
        pressure_tank_Graph = graphWidgies.addWidget(pg.PlotWidget(), row=1, col=0)
        pressure_combustionChamber_Graph = graphWidgies.addWidget(pg.PlotWidget(), row=1, col=1)
        self.central = bigBoi

        self.setWindowTitle("DinoSore")

        interfaceWidgies.addWidget(pg.GraphicsLayoutWidget(), row=0, col=0)
        # adding buttons and stuff ig
        
        # start the plotting stuff here ig


app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()