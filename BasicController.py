'''
Basic controller for the algorithm visualizer.

This is the starting point for the Visualizer. It will start up the view and model, and control running the program.

ToDo:
- Experiment with the algorithms to make them as efficient as possible
- Write in execution timer to GUI
- Save walls on reset, have extra button to reset walls.

Created on February 7th, 2023
@author: Samuel Dahlberg
'''

from BasicModel import Model
from BasicView import View


class Controller:

    def __init__(self):
        # Initializing all changeable variables
        self.numRows = 50
        self.start = 0
        self.end = 2499
        self.tick = 1

        # Initializing the model and view. Also grabbing the list of available search algorithms from model
        self.model = Model(self.numRows)
        self.algoList = self.model.getAlgos()
        self.view = View(self, self.algoList, self.start, self.end, self.numRows)

    # Main method for class, when program is ready to be started, call this
    def main(self):
        self.view.main()

    # Called from View. This method indicates that all set-up the user is doing is complete, and they want to
    # run a search algorithm
    def onRun(self, grid, algoValue, start, end):

        # Start and end can be changed from view, so we will update them in the controller
        self.start = start
        self.end = end

        # Setting up the model's search algorithm
        self.model.setSearch(grid, algoValue, self.start, self.end)
        # While loop to call the search algorithm step at a time, and correspondingly update the view on the steps
        done = False
        while not done:
            newChanges, done = self.model.runSearch(grid, algoValue, self.start, self.end)
            self.view.updateGrid(newChanges, done)





if __name__ == '__main__':
    controller = Controller()
    controller.main()
