import copy
import numpy as np

BOARD_SIZE = 35
MAX_TEMPERATURE = 50


class Board:
    '''
        The board contains 4 layers of ice,  2 in the north and 2 in south
        in the middle there is a lot of sea and some part is forest, land and city
        the city produces air pollution that warms the environment and spreads through the wind
    '''
    def __init__(self):
        self.ground = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE))
        self.temperature = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE))
        self.pollution = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE))
        self.is_cloudy = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE))
        self.ground_dictionary = {'sea': 0, 'ice': 1, 'forest':  2, 'city': 3, 'land': 4}

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i <= 1 or i >= BOARD_SIZE - 2:
                    self.init_cell(i, j, 1, -20, 1, 0) # means ice
                elif 10 <= i <= 20 and 10 <= j <= 20:
                    self.init_cell(i, j, 2, 25, 0, 0)  # means forest
                elif 10 <= i <= 20 and 21 <= j <= 30:
                    self.init_cell(i, j, 3, 25, 0, 3)  # means city
                elif 21 <= i <= 30 and 10 <= j <= 30:
                    self.init_cell(i, j, 4, 25, 0, 0)  # means land
                else:
                    self.init_cell(i, j, 0, 15, 1, 0)  # means sea

    def init_cell(self, x_index, y_index, ground, temperature, is_cloudy, pollution):
        self.ground[x_index][y_index] = ground
        self.temperature[x_index][y_index] = temperature
        self.is_cloudy[x_index][y_index] = is_cloudy
        self.pollution[x_index][y_index] = pollution

    def get_cell(self, x_index, y_index):
        arr = np.zeros(shape=4)
        arr[0] = self.ground[x_index][y_index]
        arr[1] = self.temperature[x_index][y_index]
        arr[2] = self.is_cloudy[x_index][y_index]
        arr[3] = self.pollution[x_index][y_index]
        return arr

    @staticmethod
    def get_neighborhood(x_index, y_index):
        # gets cell by it's indexes and returns an array of tuples of indexes of it's neighbors
        arr = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x_index + i < BOARD_SIZE:
                    if 0 <= y_index + j < BOARD_SIZE:
                        arr.append((x_index+i, y_index+j))
        arr.remove((x_index, y_index))
        return arr

    def get_next_cell(self, x_index, y_index):
        cell = self.get_cell(x_index, y_index)

        # here we declare that the wind is moving from the neighbor with highest temp to the cell
        hottest_temp = -50
        hottest_x_index, hottest_y_index = -1, -1
        for x, y in self.get_neighborhood(x_index, y_index):
            if self.temperature[x][y] > hottest_temp:
                hottest_temp = self.temperature[x][y]
                hottest_x_index, hottest_y_index = x,y
        if self.pollution[hottest_x_index][hottest_y_index] > 0:
            cell[3] = self.pollution[hottest_x_index][hottest_y_index]

        # defining cloud movement with the wind
        if self.is_cloudy[hottest_x_index][hottest_y_index] == 1 and cell[2] == 0:
            self.is_cloudy[hottest_x_index][hottest_y_index] = 0
            cell[2] = 1

        # first we handle pollution that increases the temperature
        if cell[3] == 0:
            for x, y in self.get_neighborhood(x_index, y_index):
                if self.pollution[x][y] == 3:
                    cell[3] = 1
                    break
        if cell[3] > 0:
            cell[1] += cell[3]

        # Lastly we update ice that was melt to become sea
        if cell[0] == 1 and cell[1] >= 0:
            cell[0] = 0  # converts to sea
        if cell[1] > MAX_TEMPERATURE:
            cell[1] = MAX_TEMPERATURE

        return cell

