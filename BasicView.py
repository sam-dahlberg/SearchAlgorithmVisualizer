'''
Basic controller for the algorithm visualizer.

This view will give a GUI output using tkinter.

Created on February 7th, 2023
@author: Samuel Dahlberg
'''

import tkinter as tk
from tkinter import ttk
import array as arr


class View(tk.Tk):
    # Size of the grid canvas
    h = 750
    w = 750

    array = arr.array("i")
    running = False

    def __init__(self, controller, algoList, start, end, numRows):
        super().__init__()
        self.title('Algorithm Visualizer')

        self.algoList = algoList
        self.Start = start
        self.End = end
        self.numRow = numRows
        self.controller = controller

        # Creating a 1d array to hold a 2d array of items
        # Get row by dividing by numRow, and flooring
        # Get column by modulo-ing by numRow
        for i in range(self.numRow):
            for i in range(self.numRow):
                self.array.append(0)

        # Array distinguishes tiles by the following:
        # 0: open tile  1: wall  2: start  3: end
        self.array[start] = 2
        self.array[end] = 3

        # Root is the main frame of the tkinter output
        root = tk.Frame(self)
        self.root = root
        root.pack()

        # ButtonFrame is the top row of buttons above the grid
        self.buttonFrame = tk.Frame(root)
        self.buttonFrame.pack(side='top')
        # Run button to start the algorithm / Reset button when algorithm is running
        self.text = 'Run'
        self.btn = ttk.Button(self.buttonFrame, text=self.text, command=self._run)
        self.btn.pack(side='left')
        # Dropdown menu for algorithm chooser
        self.algoValue = tk.StringVar(self.buttonFrame)
        self.algoValue.set(algoList[0])
        self.algoDropdown = tk.OptionMenu(self.buttonFrame, self.algoValue, *algoList)
        self.algoDropdown.pack(side='right')

        # Canvas that represents the grid of tiles
        canvas = tk.Canvas(root, height=self.h + 1, width=self.w + 1, bd=0, bg='black')
        self.canvas = canvas
        self._drawBoard(canvas)
        canvas.pack(side='bottom')

    # Draws a cleared board of open tiles, row/width of numRows, and size of h/w
    def _drawBoard(self, canvas):
        numRow = self.numRow
        h = self.h
        w = self.w

        # draw checkerboard
        for r in range(numRow):
            for c in range(numRow):
                fill = 'white'
                coords = ((c * (w / numRow)) + 2, (r * (h / numRow)) + 2, (c * (w / numRow) + (w / numRow)) + 2,
                          (r * (h / numRow) + (h / numRow)) + 2)
                canvas.create_rectangle(coords, fill=fill, tags='tile')
        canvas.itemconfig(self.Start + 1, fill='blue')
        canvas.itemconfig(self.End + 1, fill='red')
        canvas.itemconfig(self.Start + 1, tags='start')
        canvas.itemconfig(self.End + 1, tags='end')

        # Binding tags for the start and end. Unfortunately needs to be separated (for now) because you cannot
        # pass in the tag, so you cannot tell which tile is moving
        # Additionally, the move and change had to separated (for now) because when moving, you cannot officially move
        # the end/start point until you know you won't move it more
        canvas.tag_bind("start", "<B1-Motion>", self._moveStart)
        canvas.tag_bind("end", "<B1-Motion>", self._moveEnd)
        canvas.tag_bind("end", "<ButtonRelease-1>", self._changeEnd)
        canvas.tag_bind("start", "<ButtonRelease-1>", self._changeStart)
        self.tempEnd = self.End
        self.tempStart = self.Start

        # Binding tags for the tiles
        canvas.tag_bind("tile", "<B1-Motion>", self._onLeftClick)
        canvas.tag_bind("tile", "<Button-1>", self._onLeftClick)
        canvas.tag_bind("tile", "<B3-Motion>", self._onRightClick)
        canvas.tag_bind("tile", "<Button-3>", self._onRightClick)

    # moves the end point
    def _moveEnd(self, event):
        if self.running:
            return

        tmp = self.canvas.find_closest(event.x, event.y)
        end = self.canvas.coords(self.End + 1)

        if ((end[0] <= event.x <= end[2]) & (end[1] <= event.y <= end[3])) | (self.canvas.gettags(tmp[0])[0] == 'start'):
            return
        else:
            self.canvas.itemconfig(tmp[0], fill='red')
            temp = self.End + 1
            self.array[self.End] = 0
            self.End = tmp[0] - 1
            self.array[self.End] = 3
            self.canvas.itemconfig(temp, fill='white')

    # changes the end point to the new mouse location
    def _changeEnd(self, event):
        if self.running:
            return

        tmp = self.canvas.find_closest(event.x, event.y)

        self.canvas.itemconfig(tmp[0], tags='end')
        self.canvas.itemconfig(tmp[0], fill='red')
        self.canvas.itemconfig(self.tempEnd + 1, tags='tile')
        self.tempEnd = tmp[0] - 1

    # moves the start point
    def _moveStart(self, event):
        if self.running:
            return

        tmp = self.canvas.find_closest(event.x, event.y)
        start = self.canvas.coords(self.Start + 1)

        if ((start[0] <= event.x <= start[2]) & (start[1] <= event.y <= start[3])) | (self.canvas.gettags(tmp[0])[0] == 'end'):
            return
        else:
            self.canvas.itemconfig(tmp[0], fill='blue')
            temp = self.Start + 1
            self.array[self.Start] = 0
            self.Start = tmp[0] - 1
            self.array[self.Start] = 2
            self.canvas.itemconfig(temp, fill='white')

    # changes the start point to the new mouse location
    def _changeStart(self, event):
        if self.running:
            return
        tmp = self.canvas.find_closest(event.x, event.y)

        self.canvas.itemconfig(tmp[0], tags='start')
        self.canvas.itemconfig(tmp[0], fill='blue')
        self.canvas.itemconfig(self.tempStart + 1, tags='tile')
        self.tempStart = tmp[0] - 1

    # When left mouse is clicked, try to change to wall
    def _onLeftClick(self, event):
        if self.running:
            return

        tmp = self.canvas.find_closest(event.x, event.y)

        if (self.array[tmp[0] - 1] != 2) & (self.array[tmp[0] - 1] != 3):
            self.canvas.itemconfig(tmp[0], fill='black')
            self.array[tmp[0] - 1] = 1

    # When left mouse is clicked, try to change to white space
    def _onRightClick(self, event):
        # Should be in a try case
        if self.running:
            return

        tmp = self.canvas.find_closest(event.x, event.y)

        if (self.array[tmp[0] - 1] != 2) & (self.array[tmp[0] - 1] != 3):
            self.canvas.itemconfig(tmp[0], fill='white')
            self.array[tmp[0] - 1] = 0

    # Tell the controller to start the algorithm search
    def _run(self):
        if self.running:
            return

        self.btn['text'] = 'Restart'
        self.btn['command'] = self._restart
        self.controller.onRun(self.array, self.algoValue.get(), self.Start, self.End)

    # restarts the grid, clearing it all and setting it up to be run again
    def _restart(self):
        if self.running:
            return

        self.array = arr.array("i")
        for i in range(self.numRow):
            for i in range(self.numRow):
                self.array.append(0)

        self.array[self.Start] = 2
        self.array[self.End] = 3

        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, height=self.h + 1, width=self.w + 1, bd=0, bg='black')

        self._drawBoard(self.canvas)
        self.btn['text'] = 'Play'
        self.btn['command'] = self._run
        self.canvas.pack(side='bottom')

    # Public method, updates the grid canvas with new changes to the tiles
    def updateGrid(self, newChanges, finished):
        self.running = not finished

        if self.running:
            self.algoDropdown.config(state='disabled')
        else:
            self.algoDropdown.config(state='active')

        # 1: visited  2: queued  3: final path
        for n in newChanges:
            if newChanges[n] == 1:
                self.canvas.itemconfig(n + 1, fill='grey90')
            if newChanges[n] == 2:
                self.canvas.itemconfig(n + 1, fill='grey75')
            if newChanges[n] == 3:
                self.canvas.itemconfig(n + 1, fill='green')

        self.canvas.update()

    def main(self):
        self.mainloop()
