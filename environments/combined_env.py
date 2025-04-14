import gym
from gym import spaces

from environments.machine_env import MachineEnv
from environments.user_env import UserEnv

class CombinedEnv(gym.Env):
    def __init__(self):
        super(CombinedEnv, self).__init__()
        
        available_coffee = [
            "Espresso",
            "Americano",
            "Latte",
            "Cappuccino"
        ]
        
        available_strenght = [10, 16]
        available_temperature = [12, 18]
        available_quantity = [6, 10]
        
        # Initialize the user and machine environments
        self.user_env = UserEnv()
        self.machine_env = MachineEnv(available_coffee, available_strenght, available_temperature, available_quantity)

        # Define state space
        self.observation_space = spaces.MultiDiscrete([3, 3, 3, 3])  
        # [type, strength, temperature, quantity] -> 0: notSimilar, 1: knownSimilar, 2: definedSimilar

        # Define action space
        # inform_type 0 / request_type 4
        # inform_strength 1 / request_strength 5
        # inform_temp 2 / request_temp 6
        # inform_quantity 3 / request_quantity 7
        # set_type 8 / set_strength 9 / set_temp 10 / set_quantity 11 -> for coffee_env
        self.action_space = spaces.Discrete(12)

        # Initial state
        self.state = [0, 0, 0, 0]  # Idle, No user input, Full water, Full beans, Has milk

    def step(self, action):
        reward = 0
        done_amount = 0
        done = False
        
        # type_status, strength_status, temp_status, quant_status = self.state

        # Define how the environment responds to actions
        if action == 0:
            # inform_type
            self.user_env.avail_receive_inform('types', self.machine_env.avail_inform('types'))
        elif action == 1:
            # inform_strength
            self.user_env.avail_receive_inform('strength', self.machine_env.avail_inform('strength'))
        elif action == 2:
            # inform_temp
            self.user_env.avail_receive_inform('temp', self.machine_env.avail_inform('temp'))
        elif action == 3:
            # inform_quantity
            self.user_env.avail_receive_inform('quantity', self.machine_env.avail_inform('quantity'))
        elif action == 4:
            # request_type
            self.user_env.request_state('types')
        elif action == 5:
            # request_strength
            self.user_env.request_state('strength')
        elif action == 6:
            # request_temp
            self.user_env.request_state('temp')
        elif action == 7:
            # request_quantity
            self.user_env.request_state('quantity')
        elif action == 8:
            # set_type
            user_state = self.user_env.state_types
            if user_state is not None:
                self.machine_env.set_state('types', user_state)
        elif action == 9:
            # set_strength
            user_state = self.user_env.state_strength
            if user_state is not None:
                self.machine_env.set_state('strength', user_state)
        elif action == 10:
            # set_temp
            user_state = self.user_env.state_temp
            if user_state is not None:
                self.machine_env.set_state('temp', user_state)
        elif action == 11:
            # set_quantity
            user_state = self.user_env.state_quantity
            if user_state is not None:
                self.machine_env.set_state('quantity', user_state)

        # Update the state
        machine_state = self.machine_env.get_states()
        user_state = self.user_env.get_states()
        
        #print("Machine State: ", machine_state)
        #print("User State: ", user_state)
        
        # Iterating over the machine and user states to calculate the reward
        for (m_key, m_value), (u_key, u_value) in zip(machine_state.items(), user_state.items()):
            if m_value == u_value == "known":
                reward += 1
                if m_key == "types":
                    self.state[0] = 1
                    reward += 99
                elif m_key == "strength":
                    self.state[1] = 1
                elif m_key == "temp":
                    self.state[2] = 1
                elif m_key == "quantity":
                    self.state[3] = 1
            elif m_value == u_value == "defined":
                if m_key == "types" and self.machine_env.state_types == self.user_env.state_types:
                    self.state[0] = 2
                    done_amount += 1
                    reward += 200
                elif m_key == "strength" and self.machine_env.state_strength == self.user_env.state_strength:
                    self.state[1] = 2
                    done_amount += 1
                    reward += 2
                elif m_key == "temp" and self.machine_env.state_temp == self.user_env.state_temp:
                    self.state[2] = 2
                    done_amount += 1
                    reward += 2
                elif m_key == "quantity" and self.machine_env.state_quantity == self.user_env.state_quantity:
                    self.state[3] = 2
                    done_amount += 1
                    reward += 2
                else:
                    reward -= 2
            else:
                if m_key == "types":
                    self.state[0] = 0
                elif m_key == "strength":
                    self.state[1] = 0
                elif m_key == "temp":
                    self.state[2] = 0
                elif m_key == "quantity":
                    self.state[3] = 0
              
        reward = reward / 206 # was 8
                    
        if done_amount == 4:
            done = True
            
        return self.state, reward, done, {}

    def reset(self):
        self.state = [0, 0, 0, 0] # Reset the machine to initial state
        self.user_env.reset()
        self.machine_env.reset()
        return self.state