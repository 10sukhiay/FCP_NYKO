def Move(position_state):
        movement = np.random.randint(-1, 2, size=(
        pop_size, 2))  # creates a random array of -1 to 1 to add to the current positions
        coords = position_state[:, 0:2] + movement
        coords[coords < 1] = 1  # prevent movement below x and y axis
        coords[coords[:, 0] > (xsize - 2)] = (xsize - 2)  # prevent movement beyond x axis
        coords[coords[:, 1] > (ysize - 2)] = (ysize - 2)  # prevent movement beyond y axis
        position_state[:, 0:2] = coords
        return position_state

def movetype2(position_state):
        movement = np.random.randint(-1, 2, size=(pop_size, 2))  # creates a random array of -1 to 1 to add to the current positions
        coords = position_state[:, 0:2] + movement
        coords[coords < 1] = 1  # prevent movement below x and y axis
        coords[coords[:, 0] > (xsize - 2)] = (xsize - 2)  # prevent movement beyond x axis
        coords[coords[:, 1] > (ysize - 2)] = (ysize - 2)  # prevent movement beyond y axis
        position_state[:, 0:2] = coords
        return position_state