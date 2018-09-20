from tkinter import *


class App:
    def __init__(self, parent):

        self.maxx = 700  # canvas width, in pixels
        self.maxy = 700  # canvas height, in pixels
        self.cell_size = 10
        self.play = False
        self.end = False
        self.wait_time = 100
        self.parent = parent
        self.frame = Frame(parent)
        self.frame.pack()
        self.top_frame = Frame(self.frame)
        self.top_frame.pack(side=TOP)
        self.canvas = Canvas(self.top_frame, background="gray", width=self.maxx, height=self.maxy)
        self.canvas.pack()
        self.bottom_frame = Frame(self.frame)
        self.bottom_frame.pack(side=BOTTOM)
        self.next_ = Button(self.bottom_frame, text="Next", command=self.next_gen)
        self.next_.pack(side=LEFT)
        self.start_ = Button(self.bottom_frame, text="Start", command=self.start)
        self.start_.pack(side=LEFT)
        self.stop_ = Button(self.bottom_frame, text="Stop", command=self.stop)
        self.stop_.pack(side=LEFT)
        self.slower_ = Button(self.bottom_frame, text="Slower", command=self.slower)
        self.slower_.pack(side=LEFT)
        self.faster_ = Button(self.bottom_frame, text="Faster", command=self.faster)
        self.faster_.pack(side=LEFT)
        self.clear_ = Button(self.bottom_frame, text="Clear", command=self.clear)
        self.clear_.pack(side=LEFT)
        self.quit_ = Button(self.bottom_frame, text="Quit", command=self.quit)
        self.quit_.pack(side=RIGHT)

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        presetmenu = Menu(menu)
        menu.add_cascade(label="Presets", menu=presetmenu)
        presetmenu.add_command(label="Glider", command=self.glider)
        presetmenu.add_command(label="Gosper Glider Gun", command=self.gosper)

        self.boxes = []
        for i in range(self.maxx // self.cell_size):
            self.boxes.append([])
            for j in range(self.maxy // self.cell_size):
                self.boxes[i].append([0, 0])  # [current gen, next gen]

    def glider(self):
        self.play = False
        self.clear()
        self.quick_place(3, 3)
        self.quick_place(4, 4)
        self.quick_place(5, 4)
        self.quick_place(5, 3)
        self.quick_place(5, 2)

    def gosper(self):
        self.play = False
        self.clear()
        self.quick_place(3, 6)
        self.quick_place(4, 6)
        self.quick_place(3, 7)
        self.quick_place(4, 7)
        self.quick_place(11, 7)
        self.quick_place(13, 7)
        self.quick_place(11, 8)
        self.quick_place(13, 6)
        self.quick_place(12, 8)
        self.quick_place(12, 6)
        self.quick_place(25, 5)
        self.quick_place(27, 5)
        self.quick_place(25, 6)
        self.quick_place(27, 4)
        self.quick_place(26, 6)
        self.quick_place(26, 4)
        self.quick_place(19, 8)
        self.quick_place(20, 8)
        self.quick_place(19, 9)
        self.quick_place(19, 10)
        self.quick_place(21, 9)
        self.quick_place(38, 11)
        self.quick_place(39, 11)
        self.quick_place(38, 12)
        self.quick_place(38, 13)
        self.quick_place(40, 12)
        self.quick_place(38, 11)
        self.quick_place(29, 16)
        self.quick_place(28, 16)
        self.quick_place(27, 16)
        self.quick_place(27, 17)
        self.quick_place(28, 18)
        self.quick_place(37, 4)
        self.quick_place(38, 4)
        self.quick_place(37, 5)
        self.quick_place(38, 5)

    def cell_size_floor(self, x):
        while x % self.cell_size != 0:
            x -= 1
        return x

    def next_gen(self):
        self.analyze()
        self.canvas.delete("all")
        self.redraw()
        self.canvas.update()  # Actually refresh the drawing on the canvas.
        self.canvas.after(int(self.wait_time))

    def clear(self):
        self.canvas.delete("all")
        for i in range(self.maxx // self.cell_size):
            for j in range(self.maxy // self.cell_size):
                self.boxes[i][j] = [0, 0]

    def start(self):
        self.play = True

    def stop(self):
        self.play = False

    def faster(self):
        if self.wait_time > 12:
            self.wait_time /= 2

    def slower(self):
        if self.wait_time < 800:
            self.wait_time *= 2

    def quit(self):
        self.end = True
        self.parent.destroy()

    def place(self, event):
        x = self.cell_size_floor(event.x)
        y = self.cell_size_floor(event.y)
        z = self.cell_size
        if self.boxes[x // z][y // z][0] == 0:  # places cell
            self.canvas.create_rectangle(x, y, x + z, y + z, fill='purple', width=0)
            self.boxes[x // z][y // z] = [1, 0]
        else:  # removes cell
            self.canvas.create_rectangle(x, y, x + z, y + z, fill='gray', width=0)
            self.boxes[x // z][y // z] = [0, 0]

    def quick_place(self, x, y):
        z = self.cell_size
        self.boxes[x][y] = [1, 0]
        self.canvas.create_rectangle(x * 10, y * 10, x * 10 + z, y * 10 + z, fill='purple', width=0)

    def neighbors(self, x, y):
        count = 0
        x_end = self.maxx // self.cell_size - 1
        y_end = self.maxy // self.cell_size - 1
        if x != 0 and y != 0 and self.boxes[x - 1][y - 1][0] == 1:
            count += 1
        if x != 0 and self.boxes[x - 1][y + 0][0] == 1:
            count += 1
        if x != 0 and y != y_end and self.boxes[x - 1][y + 1][0] == 1:
            count += 1
        if y != 0 and self.boxes[x + 0][y - 1][0] == 1:
            count += 1
        if y != y_end and self.boxes[x + 0][y + 1][0] == 1:
            count += 1
        if x != x_end and y != 0 and self.boxes[x + 1][y - 1][0] == 1:
            count += 1
        if x != x_end and self.boxes[x + 1][y + 0][0] == 1:
            count += 1
        if x != x_end and y != y_end and self.boxes[x + 1][y + 1][0] == 1:
            count += 1
        return count

    def analyze(self):  # game logic
        for x in range(self.maxx // self.cell_size):
            for y in range(self.maxy // self.cell_size):
                neighbors = self.neighbors(x, y)
                if self.boxes[x][y][0] == 0:  # for dead cells
                    if neighbors == 3:  # checks if cell has 3 live neighbors
                        self.boxes[x][y][1] = 1
                else:  # for live cells
                    if neighbors < 2 or neighbors > 3:  # under/over pop.
                        self.boxes[x][y][1] = 0
                    elif neighbors == 2 or neighbors == 3:  # next gen.
                        self.boxes[x][y][1] = 1

    def redraw(self):  # draws next generation
        z = self.cell_size
        for x in range(self.maxx // self.cell_size):
            for y in range(self.maxy // self.cell_size):
                if self.boxes[x][y][1] == 0:
                    self.boxes[x][y][0] = 0
                else:  # places cell
                    self.boxes[x][y] = [1, 0]
                    self.canvas.create_rectangle(x * z, y * z, x * z + z, y * z + z, fill='purple', width=0)

    def run(self):
        while not self.end:
            self.canvas.bind('<Button-1>', self.place)

            if self.play:
                self.analyze()
                self.canvas.delete("all")
                self.redraw()

            self.canvas.update()  # Actually refresh the drawing on the canvas.
            self.canvas.after(int(self.wait_time))


if __name__ == "__main__":
    root = Tk()
    root.title("Conway's Game of Life")
    app = App(root)
    app.run()
    root.mainloop()
