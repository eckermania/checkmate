import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from time import strftime


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=100, color1="#EDBB99", color2="#D6EAF8"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="#5D6D7E")
        self.canvas.pack(side="top", fill="both", expand=True)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

def prep_img(img_filepath):
    image = Image.open(img_filepath)
    resized_image = image.resize((50, 50))
    prepped_img = ImageTk.PhotoImage(resized_image)
    return prepped_img

class Player(tk.Frame):
    def __init__(self, parent, rows=1, columns=1, size=300, color1="#EDBB99", color2="#D6EAF8"):
        '''size is the size of a square, in pixels'''

        self.parent = parent
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.time = strftime('%H:%M:%S %p')

        self.canvas_width = columns * size
        self.canvas_height = rows * size

        # Name entry fields
        self.a = Label(parent, text="Player 1 Name")
        self.a1 = Entry(parent)
        self.b = Label(parent, text="Player 2 Name")
        self.b1 = Entry(parent)
        self.a.pack()
        self.a1.pack()
        self.b.pack()
        self.b1.pack()

        self.name_button = Button(parent, text="Submit", command=self.clear_form, fg="black", cursor="arrow")
        self.name_button.pack()

        #Player clock for current turn
        self.clock_label = Label(parent, font=('calibri', 30, 'bold'), background='black', foreground='white')

        # Entry fields for moving a piece
        self.starty_label = Label(parent, text="Current Y coordinate (A - H)")
        self.starty_entry = Entry(parent)
        self.startx_label = Label(parent, text="Current X coordinate (1 - 8)")
        self.startx_entry = Entry(parent)

        self.endy_label = Label(parent, text="Move to Y coordinate (A - H)")
        self.endy_entry = Entry(parent)
        self.endx_label = Label(parent, text="Move to X coordinate (1 - 8)")
        self.endx_entry = Entry(parent)

        self.move_button = Button(parent, text="Submit", fg="black", command=self.move_piece, cursor="arrow")

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=self.canvas_width, height=self.canvas_height, background="#5D6D7E")
        self.canvas.pack(side="bottom", fill="both", expand=True)

    def clear_form(self):
        # self.clock_label.pack_forget()
        self.a.pack_forget()
        self.a1.pack_forget()
        self.b.pack_forget()
        self.b1.pack_forget()
        self.name_button.pack_forget()

        current_time = "Turn start:\n" + self.time
        self.clock_label['text'] = current_time
        self.clock_label.pack(side = LEFT)

        self.starty_label.pack()

        self.starty_entry.pack()
        self.startx_label.pack()

        self.startx_entry.pack()

        self.endy_label.pack()
        self.endy_entry.pack()

        self.endx_label.pack()
        self.endx_entry.pack()

        self.move_button.pack()

    def get_piece_name(self, x, y):

        for piece in board.pieces:
            if board.pieces[piece] == (x, y):
                return piece

    def move_piece(self):
        start_x_coord = self.startx_entry.get()
        start_y_coord = ord(self.starty_entry.get())
        end_x_coord = self.endx_entry.get()
        end_y_coord = ord(self.endy_entry.get())

        cleaned_start_x_coord = int(start_x_coord) - 1
        cleaned_start_y_coord = start_y_coord - 65

        cleaned_end_x_coord = int(end_x_coord) - 1
        cleaned_end_y_coord = end_y_coord - 65

        piece_name = self.get_piece_name(cleaned_start_x_coord, cleaned_start_y_coord)

        board.placepiece(piece_name, cleaned_end_x_coord, cleaned_end_y_coord)

        self.reset_move_form()

    def reset_move_form(self):

        # clear entry fields
        self.startx_entry.delete(0, END)
        self.starty_entry.delete(0, END)
        self.endx_entry.delete(0, END)
        self.endy_entry.delete(0, END)

    # This function is used to
    # display time on the label
    def time(self):
        string = "Turn start:\n" + strftime('%H:%M:%S %p')
        self.clock_label.config(text=string)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Welcome to CheckMate")

    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true")

    player = Player(root)
    player.pack(side="right", fill="both", expand="true")

    # populate board with starting positions and pieces
    white_tower = prep_img('assets/w_tower.png')
    board.addpiece("whitetower1", white_tower, 0, 0)
    board.addpiece("whitetower2", white_tower, 7, 0)

    black_tower = prep_img('assets/b_tower.png')
    board.addpiece("blacktower1", black_tower, 0, 7)
    board.addpiece("blacktower2", black_tower, 7, 7)

    white_knight = prep_img('assets/w_knight.png')
    board.addpiece("whiteknight1", white_knight, 1, 0)
    board.addpiece("whiteknight2", white_knight, 6, 0)

    black_knight = prep_img('assets/b_knight.png')
    board.addpiece("blackknight1", black_knight, 1, 7)
    board.addpiece("blackknight2", black_knight, 6, 7)

    white_bishop = prep_img('assets/w_bishop.png')
    board.addpiece("whitebishop1", white_bishop, 2, 0)
    board.addpiece("whitebishop2", white_bishop, 5, 0)

    black_bishop = prep_img('assets/b_bishop.png')
    board.addpiece("blackbishop1", black_bishop, 2, 7)
    board.addpiece("blackbishop2", black_bishop, 5, 7)

    white_queen = prep_img('assets/w_queen.png')
    board.addpiece("whitequeen", white_queen, 4, 0)

    black_queen = prep_img(('assets/b_queen.png'))
    board.addpiece("blackqueen", black_queen, 4, 7)

    white_king = prep_img('assets/w_king.png')
    board.addpiece("whiteking", white_king, 3, 0)

    black_king = prep_img('assets/b_king.png')
    board.addpiece("blackking", black_king, 3, 7)

    white_pawn = prep_img('assets/w_pawn.png')
    board.addpiece("whitepawn1", white_pawn, 0, 1)
    board.addpiece("whitepawn2", white_pawn, 1, 1)
    board.addpiece("whitepawn3", white_pawn, 2, 1)
    board.addpiece("whitepawn4", white_pawn, 3, 1)
    board.addpiece("whitepawn5", white_pawn, 4, 1)
    board.addpiece("whitepawn6", white_pawn, 5, 1)
    board.addpiece("whitepawn7", white_pawn, 6, 1)
    board.addpiece("whitepawn8", white_pawn, 7, 1)

    black_pawn = prep_img('assets/b_pawn.png')
    board.addpiece("blackpawn1", black_pawn, 0, 6)
    board.addpiece("blackpawn2", black_pawn, 1, 6)
    board.addpiece("blackpawn3", black_pawn, 2, 6)
    board.addpiece("blackpawn4", black_pawn, 3, 6)
    board.addpiece("blackpawn5", black_pawn, 4, 6)
    board.addpiece("blackpawn6", black_pawn, 5, 6)
    board.addpiece("blackpawn7", black_pawn, 6, 6)
    board.addpiece("blackpawn8", black_pawn, 7, 6)


    root.mainloop()

