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
import time
from scipy import *
from pylab import *
from random import *
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

#Class definition
#1. Animal Class: contains the common features of deer and wolf
class animal:
    #initialization of animal with input parameters:
    #                   x_index, y_index, starvage age, procreation age
    def __init__(self,  i, j, starve_age,  reproduction_age):
        self.old_position = (i, j)      # initialize the old position with i and j
        self.present_position = (i, j)  # initialize the present positon with i and j
        self.age_rep = randint(0,reproduction_age)  # setting procreation age
        self.age_starve = randint(0,starve_age)    # setting starve age
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
    def __init__(self, deer_rep_age, wolf_starve_age, wolf_rep_age, init_number_of_deer, init_number_of_wolf, grid_size):
        self.t = 0
        self.N = grid_size
        self.n_deer = init_number_of_deer
        self.n_wolf = init_number_of_wolf
        self.occupation_matrix = zeros((self.N, self.N))
        
        #lists of deer and wolf
        self.deer_list = []
        self.wolf_list = []
        
        self.deer_starve = 1e10
        self.deer_rep = deer_rep_age 	# 5
        self.wolf_starve = wolf_starve_age
        self.wolf_rep = wolf_rep_age 	#60
        
        #initialize the deer list
        for i in range(self.n_deer):
            #pick up a random position and check whether it is occupied.
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            #if occupied, pick up another position until one free location if found
            while self.occupation_matrix[(x,y)] != 0:
                x = randint(0, self.N-1)   # for randint, randint(0,4) choose 0,1,2,3,4
                y = randint(0, self.N-1)
            #immediately update the occupation matrix
            self.occupation_matrix[(x,y)] = 1
            #create a deer at that position and add it to the list
            deer_instance = deer(x, y, self.deer_starve, self.deer_rep)
            self.deer_list.append(deer_instance)
        
        #initialize the wolf list, same thing done as for deer
        for i in range(self.n_wolf):
            x = randint(0, self.N-1)
            y = randint(0, self.N-1)
            while self.occupation_matrix[(x,y)] != 0:
                x = randint(0, self.N-1)
                y = randint(0, self.N-1)
            self.occupation_matrix[(x,y)] = 2
            wolf_instance = wolf(x, y, self.wolf_starve, self.wolf_rep)
            self.wolf_list.append(wolf_instance)

    
    def eco_evolution(self,total_time_steps,deer_count,wolf_count,time_count,method):
      while self.t <=total_time_steps:
	self.totaltimesteps = 1
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
        for t in range(1):
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
                    self.occupation_matrix[thiswolf.present_position] = 0
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
                    self.occupation_matrix[thisdeer.present_position] = 0
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
                    if self.occupation_matrix[neighbor[k]] == 1: deernb.append(neighbor[k])
                    if self.occupation_matrix[neighbor[k]] == 2: wolfnb.append(neighbor[k])

                #__Two situation of wolf move___
                thiswolf.old_position = thiswolf.present_position
                if len(deernb) == 0:
                    if (len(wolfnb) < 4):
                        thiswolf.present_position = choice([n for n in neighbor if n not in wolfnb])
                else:
                    deerpos = choice(deernb)
                    thiswolf.age_starve = 0   # after eating, reset its age_starve
                    thiswolf.present_position = deerpos
                self.occupation_matrix[thiswolf.old_position] = 0
                self.occupation_matrix[thiswolf.present_position] = 2

                #if it deposite a new one behind (only when the wolf have some where to move)
                if thiswolf.check_breed() == "mature" and thiswolf.old_position != thiswolf.present_position:
                    newpos = thiswolf.old_position
                    x = newpos[0]
                    y = newpos[1]
                    newwolf = wolf(x, y, self.wolf_starve, self.wolf_rep)
                    new_born_wolf_list.append(newwolf)
                    self.occupation_matrix[thiswolf.old_position] = 2
                    thiswolf.age_rep = 0
            #merge newborn wolf list with the original wolf list
            self.wolf_list = self.wolf_list + new_born_wolf_list
            
            #___DEER_eaten_clear_loop
            temp_deer_list = []
            for thisdeer in self.deer_list:
                if self.occupation_matrix[thisdeer.present_position] == 1: #If it is not captured by a wolf
                    temp_deer_list.append(thisdeer)
            self.deer_list = temp_deer_list

            new_born_deer_list = [] #new born deer list buffer
            #___LIVING_DEER_LOOP_____
            for thisdeer in self.deer_list:
                i, j = thisdeer.present_position
                neighbor = [((i-1)%self.N,j), ((i+1)%self.N,j), (i,(j+1)%self.N), (i,(j-1)%self.N)]
                availablenb = [n for n in neighbor if self.occupation_matrix[(n[0], n[1])] == 0]
                # check whether there are available positions for deer to move
                thisdeer.old_position = thisdeer.present_position
                if len(availablenb) > 0:
                    thisdeer.present_position = choice(availablenb)
                self.occupation_matrix[thisdeer.old_position] = 0
                self.occupation_matrix[thisdeer.present_position] = 1
                
                if thisdeer.check_breed() == "mature" and thisdeer.old_position != thisdeer.present_position:
                    newpos = thisdeer.old_position
                    x = newpos[0]
                    y = newpos[1]
                    newdeer = deer(x, y, self.deer_starve, self.deer_rep)
                    new_born_deer_list.append(newdeer)
                    self.occupation_matrix[thisdeer.old_position] = 1
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
	    
	    # Show 2D animation/figure
	    if method == "1":
            	fig.clf()											# Clear the previous figure (makes faster)
	    	plt.title("Predator-Prey Ecosystem: Live Feed \nRed: Predator ; Blue: Prey")		# Figure Title
	    	image=imshow(self.occupation_matrix,interpolation="nearest",cmap=cmap,norm=norm)		# Display 2D grid/environment
	    if (self.t == 1) or (self.t % 50)==0:							# If the first iteration or every 50, save
		plt.savefig("pics/ecosystem_snapshot_%i.png" %(self.t)) 				# Save in pics/ directory
	    deer_count.append(deer_num)									# Append deer count for iteration (used for population plot)
	    wolf_count.append(wolf_num)									# Append deer count for iteration (used for population plot)
	    time_count.append(self.t)									# Append deer count for iteration (used for population plot)
	    # FOR ANIMATION 
	    if method == "1":
		return anim

######## Function Needed for Animation #######
def init():
        plt.title("Predator-Prey Ecosystem: Live Feed")

#__________Main_function_________

# Input parameter section
print "Predator-Prey Ecosystem: \n1)Show Animation (Single parameter) \n2)Full Parameter Search (No animation) "
print "3)Restricted Parameter Search (Inital wolf/deer populations fixed)"
method=raw_input()

# If using animation, input user defined parameters
if method == "1":
	print "Enter parameters:"
	print "Initial number of deer: "
	init_deer=int(raw_input())
	print "Deer - Reproduction Age: "
	deer_rep=int(raw_input())
	print "Initial number of wolves: "
	init_wolf=int(raw_input())
	print "Wolf - Reproduction Age: "
	wolf_rep=int(raw_input())
	print "Wolf - Starvation Rate: "
	wolf_st=int(raw_input())
	iterations=1

# If NOT using animation, scan through parameters randomly, specify the number of trials
if method == "2":
	print "Number of iterations to perform:"
	iterations=int(raw_input())
	print "For",iterations,"iterations."

if method == "3":
        print "Number of iterations to perform:"
        iterations=int(raw_input())
	print "Initial number of deer: "
	init_deer=int(raw_input())
	print "Initial number of wolves: "
	init_wolf=int(raw_input())
print "Performing using method",method,"..."


#Defining matrices for parameters:
# Reproduction and starving ages
deer_rep_age=[]
wolf_starve=[]
wolf_rep_age=[]

# Storing parameters which result in unstable system (one or both species die out)
red_deer_rep_age=[]
red_wolf_starve=[]
red_wolf_rep_age=[]

# Storing parameters which result in stable system (no species dying out)
blue_deer_rep_age=[]
blue_wolf_starve=[]
blue_wolf_rep_age=[]

# Storing initial value of deer and wolves 
init_w=[]
init_d=[]

# Storing inital value of deer and wolves which result in a species dying out
red_wolf=[]
red_deer=[]

# Storing initial value of deer and wolves which do not result in a species dying out
blue_wolf=[]
blue_deer=[]

# Storing ratio of initial number of deer to wolves
diff_dw=[]
ratio_dw=[]

# Storing ratio of initial number of deer to wolves which result in a species dying out
red_diff_dw=[]
red_ratio_dw=[]

# Storing ratio of initial number of deer to wolves which do not result in a species dying out
blue_diff_dw=[]
blue_ratio_dw=[]

for i in range(0,iterations):
	#Initialize storage of ecosystem population information
        deer_count=[]
        wolf_count=[]
        time_count=[]
	# If animation method: Show animation and plot sinusoidal curve
        if method == "1":
		our_eco_system=eco_system(deer_rep, wolf_st, wolf_rep, init_deer, init_wolf, 100)
                fig = plt.figure()
                animation.FuncAnimation.frames=0
                anim= animation.FuncAnimation(fig,our_eco_system.eco_evolution,1000,fargs=(deer_count,wolf_count,time_count,method),init_func=init,interval=1,blit=
False,repeat=False)
                plt.show()
        	
		# Sinusoidal curve generation
		fig2 = plt.figure()
        	plot(time_count, wolf_count, "r", linewidth = 3, label = "Wolf population")
        	plot(time_count, deer_count, "b", linewidth = 3, label = "Deer population")
        	legend(loc = "upper right", fontsize = 20)
        	title("Ecosystem Population Evolution Through Time")
        	xlabel("Evolution of Time")
        	ylabel("Population (# of Animals)")
        	savefig("pics/Stable_time_evo.png")
		show()

	# If Parameter searches ...
	if method == "2" or method == "3":	
		# Randomly generate sets of deer and wolf age/starvation parameters
		deer_rep_age.append(randint(5,15))
        	wolf_starve.append(randint(5,15))
        	wolf_rep_age.append(randint(5,15))
		
		# Restriction on wolf reproduction age/starvation
    		while wolf_rep_age[i]<=wolf_starve[i]:
			if wolf_starve[i] == 15: # i.e the max possible value
				del wolf_starve[-1]
				wolf_starve.append(randint(5,15))
			del wolf_rep_age[-1]
			wolf_rep_age.append(randint(5,15))
        
		# If full parameter search, randomly generate starting populations
		if method == "2":
        		init_d.append(randint(500,2500))
        		init_w.append(randint(500,2500))
        	
		# If restricted parameter search, use user defined starting populations
		if method == "3":
                        init_d.append(init_deer)
                        init_w.append(init_wolf)
		# Determine difference and ratio between poupluations
		diff_dw.append(init_d[i]-init_w[i])
        	ratio_dw.append(float(init_d[i])/init_w[i])

		print deer_rep_age[i], wolf_starve[i], wolf_rep_age[i], init_d[i], init_w[i]
		print diff_dw[i],ratio_dw[i]

		#Initialize ecosystem (# of deer, # of wolves, grid size)	
        	our_eco_system=eco_system(deer_rep_age[i], wolf_starve[i], wolf_rep_age[i], init_d[i], init_w[i], 100)	
		our_eco_system.eco_evolution(300,deer_count,wolf_count,time_count,method)
		if wolf_count[300] == 0 or deer_count[300] == 0:
        		red_deer_rep_age.append(deer_rep_age[i])
                	red_wolf_starve.append(wolf_starve[i])
                	red_wolf_rep_age.append(wolf_rep_age[i])
        		red_diff_dw.append(diff_dw[i])
        		red_ratio_dw.append(ratio_dw[i])
        	else:
        		blue_deer_rep_age.append(deer_rep_age[i])
                	blue_wolf_starve.append(wolf_starve[i])
                	blue_wolf_rep_age.append(wolf_rep_age[i])
        		blue_diff_dw.append(diff_dw[i])
        		blue_ratio_dw.append(ratio_dw[i])
      
#### Plotting of parameter space:
if method == "2" or method == "3":
	fig = plt.figure(figsize=(15,15))
	ax = fig.add_subplot(111, projection='3d')

	if method == "2":
		ax.scatter(red_deer_rep_age, red_wolf_starve, red_wolf_rep_age, marker='o', color='red', s=red_ratio_dw*600, label='extinction or unstable')
		ax.scatter(blue_deer_rep_age, blue_wolf_starve, blue_wolf_rep_age, marker='o', color='blue', s=blue_ratio_dw*600, label='stable')
		legend()
	if method == "3":
                ax.scatter(red_deer_rep_age, red_wolf_starve, red_wolf_rep_age, marker='o', color='red', s=400, label='extinction or unstable')
                ax.scatter(blue_deer_rep_age, blue_wolf_starve, blue_wolf_rep_age, marker='o', color='blue', s=400, label='stable')
		legend()
	ax.set_xlabel('Deer reproduction age')
	ax.set_ylabel('Wolf starvation age')
	ax.set_zlabel('Wolf redproduction age')

	plt.title('Parameter space')
	if method == "2":
		plt.savefig("All_Parameter_space_3D.png")
	if method == "3":
		plt.savefig("Restricted_Parameter_space_d%i_w%i.png" %(init_deer,init_wolf))
     
	plt.show()

	print "Wolf initial: ", init_w
	print "Deer initial: ", init_d

	print "Red- Deer rep age:", red_deer_rep_age
	print "Red- Wolf Starve:", red_wolf_starve
	print "Red- Wolf rep age:", red_wolf_rep_age
	print "Red diff_dw:", red_diff_dw
	print "Red ratio_dw:", red_ratio_dw
        
	print "Blue- Deer rep age:", blue_deer_rep_age
	print "Blue- Wolf Starve:", blue_wolf_starve
	print "Blue- Wolf rep age:", blue_wolf_rep_age
	print "Blue diff_dw:", blue_diff_dw
	print "Blue ratio_dw:", blue_ratio_dw


