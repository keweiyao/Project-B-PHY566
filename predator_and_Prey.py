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
from pylab import *
from random import *

#Class definition
#1. Animal Class: contains the common features of deer and wolf
class animal:
    #initialization of animal with input parameters:
    #                   x_index, y_index, starvage age, procreation age
    def __init__(self,  i, j, starve_age,  reproduction_age):
        self.old_position = [i, j]      # initialize the old position with i and j
        self.present_position = [i, j]  # initialize the present positon with i and j
        self.age = 0                    # initial age is set to zero
        self.age_rep = 0  # setting procreation age
        self.age_starve = 0    # setting starve age
        self.breedage = reproduction_age
        self.starveage = starve_age
        self.living_status = "live"     # setting live status of the animal "live"/"dead", each time when we loop over
                                        #the list of animals we will delete the object with status "dead"
        self.breed_status = "immature"  # setting the breed statys of the animal "mature"/"immature", each time when we loop over
                                        #the list of animals we will call the bread function if there is enough space to bread
        self.marked = False
    
    #aging function, increase age by one
    '''
    def aging(self):
        self.age = self.age + 1
    '''
    #updating the bread stauts
    def check_breed(self):
        if self.age_rep > self.breedage:
            return "mature"
        else:
            return "immature"
    '''
    #When calling the bread function, the age and bread status is reset, and the present location of the animal is returned for initialization of the bady animal
    def breed(self):
        self.age = 0
        self.breed_status = "immature"
        return self.old_position

    #move function of the animal, with changes in x and y direction as input parameters, updates the old and present location
    def move(self, di, dj):
        self.old_position = self.present_position
        self.present_position = [self.old_position[0] + di, self.old_position[1] + dj]
    '''
    #starve function will determine the life status according to the age compared to the starving age
    def starve(self):
        if self.age_starve > self.starveage:
            return "dead"
        if self.age_starve <= self.starveage:
            return "live"
    
#Inherit (from animal) class: deer
class deer(animal):
    #update function
    def update(self):
        #add something here ...
        return

#Inherit (from animal) class: deer
class wolf(animal):
    #hunt and eat function, which is called when we loop over the wolf list and there is a deer around
    def hunt_and_eat(self):
        age = 0
        #add something here ...
    #update function
    def update(self):
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
        self.totaltimesteps = 100
        
        #lists of deer and wolf
        self.deer_list = []
        self.wolf_list = []
        
        self.deer_starve = 5
        self.deer_rep = 2
        self.wolf_starve = 10
        self.wolf_rep = 6
        
        #initialize the deer list
        for i in range(self.n_deer):
            #pick up a random position and check whether it is occupied.
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            #if occupied, pick up another position until one free location if found
            while self.occupication_matrix[x,y] != 0:
                x = randint(0, self.N-1)   # for randint, randint(0,4) choose 0,1,2,3,4
                y = randint(0, self.N-1)
            #immediately update the occupication matrix
            self.occupication_matrix[x][y] = 1
            #create a deer at that position and add it to the list
            deer_instance = deer(x, y, self.deer_starve, self.deer_rep)
            self.deer_list.append(deer_instance)
        
        #initialize the wolf list, same thing done as for deer
        for i in range(self.n_wolf):
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            while self.occupication_matrix[x][y] != 0:
                x = randint(0, self.N-1)
                y = randint(0, self.N-1)
            self.occupication_matrix[x][y] = 2
            wolf_instance = wolf(x, y, self.wolf_starve, self.wolf_rep)
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
    def eco_evolution(self):
        #add a lot of things here
        '''
        should return three lists: the number of deers at that time, the number of wolves at that time, and time
        deernum[] wolfnum[] timenum[]
        '''
        deer_num = len(self.deer_list)
        wolf_num = len(self.wolf_list)
        deernum = [deer_num]
        wolfnum = [wolf_num]
        timenum = [self.t]
        for t in range(self.totaltimesteps):
            self.t += 1 # after each evolution, time ++
            # first, check the status of wolves
            wolf_delete_number = []
            for thiswolf in self.wolf_list:
                thiswolf.marked = True
                i,j = thiswolf.present_position
                nbb = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)]
                neighbor = []
                for nb in nbb: 
                    if nb[0] >= self.N:
                        nb = (nb[0]-self.N, nb[1])
                    if nb[1] >= self.N:
                        nb = (nb[0], nb[1]-self.N)
                    if nb[0] < 0:
                        nb = (nb[0]+self.N, nb[1])
                    if nb[1] < 0:
                        nb = (nb[0], nb[1]+self.N)
                    neighbor.append(nb)
                    # generate appropriate neighbor positions
                deernb = []  #deer neighbors
                wolfnb = []  #wolf neighbors
                for k in range(4): # check whether there are deer neighbors around the wolf, add their positions to the deer neighbor list
                    if self.occupication_matrix[neighbor[k]] == 1: deernb.append(neighbor[k])
                    if self.occupication_matrix[neighbor[k]] == 2: wolfnb.append(neighbor[k])
                if len(deernb) == 0:
                    '''
                    If there are no deer around the wolf, need to consider:
                    1. if wolf starve to death? if yes, kill; if not, leave
                    2. if wolf reproduce? if yes, put a new wolf at original position, if not, just move
                    let wolf's age + 1 after eating and moving
                    another extreme situation:
                    all wolves around this wolf, then just don't move and don't reproduce
                    '''
                    thiswolf.age_starve += 1
                    thiswolf.age_rep += 1
                    if (len(wolfnb) != 4): 
                        if thiswolf.starve() == "dead":
                            self.occupication_matrix[thiswolf.present_position] = 0
                            self.wolf_list = [w for w in self.wolf_list if w != thiswolf]
                        else:
                            if thiswolf.check_breed() == "mature":
                                newpos = thiswolf.present_position
                                x = newpos[0]
                                y = newpos[1]
                                newwolf = wolf(x, y, 10, 6)
                                newwolf.marked = True;
                                self.wolf_list.append(newwolf)
                                thiswolf.age_rep = 0
                            else: self.occupication_matrix[thiswolf.present_position] = 0
                            thiswolf.old_position = thiswolf.present_position
                            thiswolf.present_position = choice(neighbor)
                            # wolf.aging
                            self.occupication_matrix[thiswolf.present_position] = 2
                            # update wolf position, old position no need to change (occupied by new wolf)
                            # new position need to change to 2
                    else: 
                        thiswolf = thiswolf
                else:
                    '''
                    if there are deers around the wolf, the deers' positions are recorded in deernb[], consider:
                    1. choose a random deer to eat -> reset starve age -> pop that deer out of deerlist, clear correspondent grid point
                    2. if wolf reproduce? if yes, breed; if not, just move
                    '''
                    deerpos = choice(deernb)
                    thiswolf.age_starve = 0   # after eating, reset its age_starve
                    self.deer_list = [d for d in self.deer_list if d.present_position != deerpos]  # pop out eaten deer
                    self.occupication_matrix[deerpos] = 2  # update deer's number to wolf's number
                    if thiswolf.check_breed() == "mature":
                        newpos = thiswolf.present_position
                        x = newpos[0]
                        y = newpos[1]
                        newwolf = wolf(x, y, 10, 6)
                        self.wolf_list.append(newwolf)
                        newwolf.marked = True
                        thiswolf.age_rep = 0
                    else: self.occupication_matrix[thiswolf.present_position] = 0
                    thiswolf.old_position = thiswolf.present_position
                    thiswolf.present_position = deerpos
                    # wolf.aging
            # sort(wolf_delete_number)
            # print len(wolf_delete_number)
            # for i in range(len(wolf_delete_number)):
                # self.wolf_list.pop(wolf_delete_number[-i-1])
            '''
            the method to pop our wolves need to be deleted, otherwise the change of list would be complicated
            '''
            
            for thisdeer in self.deer_list:
                nbb = [(i-1,j), (i+1,j), (i,j+1), (i, j-1)]
                neighbor = []
                for nb in nbb: 
                    if nb[0] >= self.N:
                        nb = (nb[0]-self.N, nb[1])
                    if nb[1] >= self.N:
                        nb = (nb[0], nb[1]-self.N)
                    if nb[0] < 0:
                        nb = (nb[0]+self.N, nb[1])
                    if nb[1] < 0:
                        nb = (nb[0], nb[1]+self.N)
                    neighbor.append(nb)
                    # generate appropriate neighbor positions
                availablenb = [nb for nb in neighbor if self.occupication_matrix[nb] == 0]
                # check whether there are available positions for deer to move
                thisdeer.age_rep += 1
                thisdeer.age_starve += 1
                if len(availablenb) != 0:
                    '''if there are available position for deer to move, need to consider
                    1. if deer reproduce? if yes, produce and move; if no, just move
                    2. aging
                    if no available position, no need to move or produce, just add age_rep
                    '''
                    if thisdeer.check_breed() == "mature":
                        newpos = thisdeer.present_position
                        x = newpos[0]
                        y = newpos[1]
                        newdeer = deer(x, y, 5, 2)
                        self.deer_list.append(newdeer)
                        thisdeer.age_rep = 0
                    else: self.occupication_matrix[thisdeer.present_position] = 0
                    thisdeer.old_position = thisdeer.present_position
                    thisdeer.present_position = choice(availablenb)
                    self.occupication_matrix[thisdeer.present_position] = 1
                    # deer.aging
                else:
                    if thisdeer.starve() == "dead":
                        self.dear_list = [d for d in self.deer_list if d != thisdeer]
                        self.occupication_matrix[thisdeer.present_position] = 0
            deer_num = len(self.deer_list)
            wolf_num = len(self.wolf_list)
            deernum.append(deer_num)
            wolfnum.append(wolf_num)
            timenum.append(self.t)
            print "current deer number, wolf number, time number = " + str(deer_num) + " , " + str(wolf_num) + " , " + str(self.t)
            # still in the evolution loop
        return deernum, wolfnum, timenum


#__________Main_function_________
#testing
our_eco_system = eco_system(80, 20, 10, 0).eco_evolution()
deernum = our_eco_system[0]
wolfnum = our_eco_system[1]
timenum = our_eco_system[2]
plot(timenum,wolfnum, "r")
plot(timenum, deernum, "b")
show()
#Inplementing, boundary conditions,


#Visuialization


#...











