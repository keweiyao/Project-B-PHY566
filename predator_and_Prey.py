"""
Describe the dynamics of biological system in which two species in whcih two species interact, predator and prey

Similar system can be found in chemistry, physics, economics and social science as well.

Lotka - Volterra Eqs
Prey:       dx/dt =     a*x     +   (-)b*x*y =  x(a-by)
            rate        growth      loss
Predator:   dy/dt =     d*x*y   +   (-)c*y   = -y(c-dx)
            rate        growth      loss
LV Eqs have periodic solutions with the maxima of the predator population shifited by a phase compared to the prey population
Or a closed loop in the phase space

Population equilibrium:

1. x = 0; y = 0 --> extinction

2. x = gamma/delta; y = alpha/beta --> stable region of the system

Computationally:
1. solve the diffusion Eqs
2. Monte Carlo approach / Simulation
    a stochastic walk on a 2D world with periodic boundary condition (A torus), with dear and wolves scattered on it.
    Both preys and predators are random walk (with exclusion).
    
    Dear at a certain age will split into two dear, and then the age is reset
    
    Wolf: eat dear/random in the first place, then random walk, rest the fullness, if fullness.
    if survive a certain times, the wolve split.
 
    Step1: deer walk and breed with new deer at the old position
    Step2: wolves hunt and breed and move
"""

from scipy import *

#Class definition
#1. Animal Class: contains the common features of deer and wolf
class animal:
    #initialization of animal with input parameters:
    #                   x_index, y_index, starvage age, procreation age
    def __init__(self,  i,       j,       starve_age,   reprouction_age):
        self.old_position = [i, j]      # initialize the old position with i and j
        self.present_position = [i, j]  # initialize the present positon with i and j
        self.age = 0                    # initial age is set to zero
        self.age_rep = reprouction_age  # setting procreation age
        self.age_starve = starve_age    # setting starve age
        self.living_status = "live"     # setting live status of the animal "live"/"dead", each time when we loop over
                                        #the list of animals we will delete the object with status "dead"
        self.breed_status = "immature"  # setting the breed statys of the animal "mature"/"immature", each time when we loop over
                                        #the list of animals we will call the bread function if there is enough space to bread
    
    #aging function, increase age by one
    def aging():
        self.age = self.age + 1
    
    #updating the bread stauts
    def check_breed():
        if self.age > age_rep:
            self.breed_status = "mature"

    #When calling the bread function, the age and bread status is reset, and the present location of the animal is returned for inialization of the bady animal
    def breed():
        self.age = 0
        self.breed_status = "immature"
        return self.old_position

    #move function of the animal, with changes in x and y direction as input parameters, updates the old and present location
    def move(di, dj):
        self.old_position = self.present_position
        self.present_position = [self.old_position[0] + di, self.old_position[1] + dj]

    #starve function will determine the life status according to the age compared to the starving age
    def starve():
        if age > age_starve:
            self.live_status = "dead"
        if age < age_starve:
            self.live_status = "live"

#Inhereit (from animal) class: deer
class deer(animal):
    #update function
    def update():
        #add something here ...
        return

#Inhereit (from animal) class: deer
class wolf(animal):
    #hunt and eat function, which is called when we loop over the wolf list and there is a deer around
    def hunt_and_eat():
        age = 0
        #add something here ...
    #update function
    def update():
        #add something here ...
        return

#________________Eco_system class________________________________
# it contains the lists of animals, a matrix recording the position of the animals (0: nothing, 1: deer, 2: wolf) and all the statistical data such as the number of deer and wolf ...
class eco_system:
    #initialize the ecosystem with initial number of deer/wolf, world size (100*100 for example), initial time (0 for example)
    def __init__(self, init_number_of_deer, init_number_of_wolf, grid_size, init_time):
        self.t = init_time
        self.N = grid_size
        self.n_deer = init_number_of_deer
        self.n_wolf = init_number_of_wolf
        self.occupication_matrix = zeros((self.N, self.N))
        
        #lists of deer and wolf
        self.deer_list = []
        self.wolf_list = []
        
        #initilize the deer list
        for i in range(self.n_deer):
            #pick up a random position and check wheher it is occupied.
            x = random.randint(0, self.N)
            y = random.randint(0, self.N)
            #if occupied, pick up another position until one free location if found
            while self.occupication_matrix[x][y] != 0:
                x = random.randint(0, self.N)
                y = random.randint(0, self.N)
            #immediately update the occupication matrix
            self.occupication_matrix[x][y] = 1
            #creat a deer at that positon and add it to the list
            deer_instance = deer(x, y, 1e10, 5)
            self.deer_list.append(deer_instance)
        
        #initlize the wolf list, same thing done as for deer
        for i in range(self.n_wolf):
            x = random.randint(0, self.N)
            y = random.randint(0, self.N)
            while self.occupication_matrix[x][y] != 0:
                x = random.randint(0, self.N)
                y = random.randint(0, self.N)
            self.occupication_matrix[x][y] = 2
            wolf_instance = wolf(x, y, 100, 10)
            self.wolf_list.append(wolf_instance)
        
        #output the information of deer and wolf just to test
        i = 0
        for item in self.deer_list:
            print "-----deer%d info:"%i
            print item.old_position
            print item.present_position
            print item.age
            print item.age_rep
            print item.age_starve
            i = i + 1

        i = 0
        for item in self.wolf_list:
            print "-----wolf%d info:"%i
            print item.old_position
            print item.present_position
            print item.age
            print item.age_rep
            print item.age_starve
            i = i + 1

    #time evolution function (Need lots of work from Fan!!! We can help as well)
    def eco_evolution():
        #add a lot of things here
        return

#__________Main_function_________
#testing
Our_eco_system = eco_system(25, 14, 100, 0)

#Inplementing, boundary conditions,


#Visuialization


#...













