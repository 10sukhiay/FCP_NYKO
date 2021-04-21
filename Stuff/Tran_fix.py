def Transmission(position_state, heat):
    for x in range(len(position_state)):
            if heat[position_state[x,0],position_state[x,1]] > 20 and heat[position_state[x,0],position_state[x,1]] > np.random.randint(0,101):
                position_state[x,2] = 2 # stands for infected
    return position_state

