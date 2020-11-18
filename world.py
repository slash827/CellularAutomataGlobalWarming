from tkinter import *
from game import *
import matplotlib.pyplot as plt

game = Game()
root = Tk()

title = Label(root, text="World", background="gray").grid(row=0, column=0)
generation_num = Label(root, text='days: '+str(game.age)).grid(row=0, column=1)

num_to_color = {0: 'sea', 1: 'ice', 2: 'forest', 3: 'city', 4: 'land'}
ground_color = {'sea': 'blue', 'land': 'brown', 'city': 'yellow', 'ice': 'white', 'forest': 'green'}
labels = [[Label(root, text='0', background='white').grid(row=i+1, column=j) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]


def start_game():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            current_cell = game.board.get_cell(i, j)
            temperature = current_cell[1]
            color = ground_color[num_to_color[current_cell[0]]]
            labels[i][j] = Label(root, text=str(int(temperature)), background=color).grid(row=i + 1, column=j)

    root.after(1500, update_all())


def update_all():
    game.next_amount_of_generations(1)
    root.grid_slaves(0)[0].config(text=str(game.age))
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            current_cell = game.board.get_cell(i, j)
            temperature = current_cell[1]
            color = ground_color[num_to_color[current_cell[0]]]
            root.grid_slaves(i+1)[j].config(text=str(int(temperature)), background=color)
    root.after(1500, update_all)


def main():
    start_game()
    root.mainloop()


if __name__ == '__main__':
    main()
