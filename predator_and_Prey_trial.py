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
import numpy as np
import matplotlib.animation as animation

#Class definition
#1. Animal Class: contains the common features of deer and wolf
class animal:
    #initialization of animal with input parameters:
    #                   x_index, y_index, starvage age, procreation age
    def __init__(self,  i, j, starve_age,  reproduction_age):
        self.old_position = (i, j)      # initialize the old position with i and j
        self.present_position = (i, j)  # initialize the present positon with i and j
        self.age_rep = 0  # setting procreation age
        self.age_starve = 0    # setting starve age
        self.breedage = reproduction_age
        self.starveage = starve_age
        self.living_status = "live"     # setting live status of the animal "live"/"dead", each time when we loop over
                                        #the list of animals we will delete the object with status "dead"
        self.breed_status = "immature"  # setting the breed statys of the animal "mature"/"immature", each time when we loop over
                                        #the list of animals we will call the bread function if there is enough space to bread
        self.marked = False
    
    
    #updating the bread stauts
    def check_breed(self):
        if self.age_rep >= self.breedage:
            return "mature"
        else:
            return "immature"
    
    #When calling the bread function, the age and bread status is reset, and the present location of the animal is returned for initialization of the bady animal
    def breed(self):
        self.age = 0
        self.breed_status = "immature"
        return self.old_position

    #starve function will determine the life status according to the age compared to the starving age
    def starve(self):
        if self.age_starve > self.starveage:
            return "dead"
        else:
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
    def __init__(self, init_number_of_deer, init_number_of_wolf, grid_size):
        self.t = 0
        self.N = grid_size
        self.n_deer = init_number_of_deer
        self.n_wolf = init_number_of_wolf
        self.occupication_matrix = zeros((self.N, self.N))
        
        #lists of deer and wolf
        self.deer_list = []
        self.wolf_list = []
        
        self.deer_starve = 1e10
        self.deer_rep = 5
        self.wolf_starve = 20
        self.wolf_rep = 60
        
        #initialize the deer list
        for i in range(self.n_deer):
            #pick up a random position and check whether it is occupied.
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            #if occupied, pick up another position until one free location if found
            while self.occupication_matrix[(x,y)] != 0:
                x = randint(0, self.N-1)   # for randint, randint(0,4) choose 0,1,2,3,4
                y = randint(0, self.N-1)
            #immediately update the occupication matrix
            self.occupication_matrix[(x,y)] = 1
            #create a deer at that position and add it to the list
            deer_instance = deer(x, y, self.deer_starve, self.deer_rep)
            self.deer_list.append(deer_instance)
        
        #initialize the wolf list, same thing done as for deer
        for i in range(self.n_wolf):
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            while self.occupication_matrix[(x,y)] != 0:
                x = randint(0, self.N-1)
                y = randint(0, self.N-1)
            self.occupication_matrix[(x,y)] = 2
            wolf_instance = wolf(x, y, self.wolf_starve, self.wolf_rep)
            self.wolf_list.append(wolf_instance)

    
    #time evolution function (Need lots of work from Fan!!! We can help as well)
    def eco_evolution(self, total_time_steps):
        self.totaltimesteps=1
	#self.totaltimesteps = total_time_steps
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
       
	cmap=matplotlib.colors.ListedColormap(['white','blue','red'])
        bounds=[-.5,.5,1.5,2.5]
        norm= matplotlib.colors.BoundaryNorm(bounds,cmap.N) 
	for t in range(self.totaltimesteps):
            self.t += 1 # after each evolution, time ++
            # first, check the status of wolves
            # wolf and deer aging and dying loop/ these are done first as they change the number and indexing of the list which may caused sutble bugs...

            wolf_temp_list = []
            for thiswolf in self.wolf_list:
                thiswolf.marked = True
                thiswolf.age_starve += 1
                thiswolf.age_rep += 1
                if thiswolf.starve() == "live":
                    wolf_temp_list.append(thiswolf)
                else:
                    print "killed"
                    self.occupication_matrix[thiswolf.present_position] = 0
            self.wolf_list = wolf_temp_list
            
            #aging and clear wolf list complished!
            deer_temp_list = []
            for thisdeer in self.deer_list:
                thisdeer.marked = True
                thisdeer.age_starve += 1
                thisdeer.age_rep += 1
                if thisdeer.starve() == "live":
                    deer_temp_list.append(thisdeer)
                else:
                    self.occupication_matrix[thisdeer.present_position] = 0
            self.deer_list = deer_temp_list
            #aging and clear deer list complished!
            
            
            #From below we ONLY work on the wolf/deer list after killing dead ones!

            new_born_wolf_list = [] #new born wolf list buffer
            #__LIVING_WOLF_LOOP
            for thiswolf in self.wolf_list:

                i,j = thiswolf.present_position
                neighbor = [((i-1)%self.N,j), ((i+1)%self.N,j), (i,(j+1)%self.N), (i,(j-1)%self.N)]

                deernb = []  #deer neighbors of this wolf
                wolfnb = []  #wolf neighbors of this deer
                for k in range(4): # check whether there are deer/wolf neighbors around the wolf, add their positions to the deer/wolf neighbor list
                    if self.occupication_matrix[neighbor[k]] == 1: deernb.append(neighbor[k])
                    if self.occupication_matrix[neighbor[k]] == 2: wolfnb.append(neighbor[k])

                #__Two situation of wolf move___
                thiswolf.old_position = thiswolf.present_position
                if len(deernb) == 0:
                    if (len(wolfnb) < 4):
                        thiswolf.present_position = choice([n for n in neighbor if n not in wolfnb])
                else:
                    deerpos = choice(deernb)
                    thiswolf.age_starve = 0   # after eating, reset its age_starve
                    thiswolf.present_position = deerpos
                self.occupication_matrix[thiswolf.old_position] = 0
                self.occupication_matrix[thiswolf.present_position] = 2

                #if it deposite a new one behind (only when the wolf have some where to move)
                if thiswolf.check_breed() == "mature" and thiswolf.old_position != thiswolf.present_position:
                    newpos = thiswolf.old_position
                    x = newpos[0]
                    y = newpos[1]
                    newwolf = wolf(x, y, self.wolf_starve, self.wolf_rep)
                    new_born_wolf_list.append(newwolf)
                    self.occupication_matrix[thiswolf.old_position] = 2
                    thiswolf.age_rep = 0
            #merge newborn wolf list with the original wolf list
            self.wolf_list = self.wolf_list + new_born_wolf_list
            
            #___DEER_eaten_clear_loop
            temp_deer_list = []
            for thisdeer in self.deer_list:
                if self.occupication_matrix[thisdeer.present_position] == 1: #If it is not captured by a wolf
                    temp_deer_list.append(thisdeer)
            self.deer_list = temp_deer_list

            new_born_deer_list = [] #new born deer list buffer
            #___LIVING_DEER_LOOP_____
            for thisdeer in self.deer_list:
                i, j = thisdeer.present_position
                neighbor = [((i-1)%self.N,j), ((i+1)%self.N,j), (i,(j+1)%self.N), (i,(j-1)%self.N)]
                availablenb = [n for n in neighbor if self.occupication_matrix[(n[0], n[1])] == 0]
                # check whether there are available positions for deer to move
                thisdeer.old_position = thisdeer.present_position
                if len(availablenb) > 0:
                    thisdeer.present_position = choice(availablenb)
                self.occupication_matrix[thisdeer.old_position] = 0
                self.occupication_matrix[thisdeer.present_position] = 1
                
                if thisdeer.check_breed() == "mature" and thisdeer.old_position != thisdeer.present_position:
                    newpos = thisdeer.old_position
                    x = newpos[0]
                    y = newpos[1]
                    newdeer = deer(x, y, self.deer_starve, self.deer_rep)
                    new_born_deer_list.append(newdeer)
                    self.occupication_matrix[thisdeer.old_position] = 1
                    thisdeer.age_rep = 0
            self.deer_list = self.deer_list + new_born_deer_list
                

            deer_num = len(self.deer_list)
            wolf_num = len(self.wolf_list)
            deernum.append(deer_num)
            wolfnum.append(wolf_num)
            timenum.append(self.t)
            print "current deer number, wolf number, time number = " + str(deer_num) + " , " + str(wolf_num) + " , " + str(self.t)
            for wf in self.wolf_list:
                wf.marked = False
            for dr in self.deer_list:
                dr.marked = False
            # still in the evolution loop

            image=plt.imshow(our_eco_system.occupication_matrix,interpolation="none",cmap=cmap,norm=norm)
	    

	return deernum, wolfnum, timenum


#__________Main_function_________
#testing

def init():
	plt.title("Predator-Prey Ecosystem: Live Feed")
	
fig=plt.figure()
our_eco_system=eco_system(1200, 900, 100)
anim = animation.FuncAnimation(fig, our_eco_system.eco_evolution, init_func=init, blit =False)
plt.show()
#our_eco_system = eco_system(100, 20, 100)

#deernum, wolfnum, timenum = our_eco_system.eco_evolution(1000)

plot(timenum, wolfnum, "r", linewidth = 3, label = "wolf population")
plot(timenum, deernum, "b", linewidth = 3, label = "deer population")
legend(loc = "upper right", fontsize = 20)

show()

