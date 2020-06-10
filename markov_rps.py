from __future__ import division
import random
import itertools


class my_markov():

    def __init__(self, reg=8.0):
        self.reg = reg #in french, decay is like a "décroissance" value
        self.markov_mat = self.matrix_initialization() #if it is the first mouv, we just call my_markov class and logically, the init function run : so we need to initialize a basic markov matrix
    @staticmethod
    def matrix_initialization():
        keys = ['RR', 'RP', 'RS', 'PR', 'PP', 'PS', 'SR', 'SP', 'SS'] #we are going to define all possible keys
        markov_mat = {}
        for key in keys: #for each key
            markov_mat[key] = {'R': {'prob' : 1 / 3,  #we are define the probability of the next action : if the key is RR, the prob to go to P is 0.3333
                                 'occ' : 0 #with n_obs, we can learn  the number of past occurence in the learning process
                                },
                               'P': {'prob' : 1 / 3,
                                 'occ' : 0
                                },
                               'S': {'prob' : 1 / 3,
                                 'occ' : 0
                                }
                          }

        return markov_mat

    def update_matrix(self, pair, inp): 
    	"""not the most fun part, here, we are just going to update the matrix
    	if for example we predict a rock, we also add one to occurence
    	we are also modified the probability of each key (i don t know if it is
    	the best word to define the operation (two last line of function))"""
        
        for i in self.markov_mat[pair]:
            self.markov_mat[pair][i]['occ'] = self.reg * self.markov_mat[pair][i]['occ']

        self.markov_mat[pair][inp]['occ'] = self.markov_mat[pair][inp]['occ'] + 1
        
        n_total = 0
        for i in self.markov_mat[pair]:
            n_total += self.markov_mat[pair][i]['occ']
            
        for i in self.markov_mat[pair]:
            self.markov_mat[pair][i]['prob'] = self.markov_mat[pair][i]['occ'] / n_total            

    def predict(self, pair):

        probs = self.markov_mat[pair]

        if max(probs.values(), key = lambda x: x["prob"])["prob"] == min(probs.values(), key = lambda x:x["prob"])["prob"]: #comaprate the max prob and the min prob.
            return random.choice(['R', 'P', 'S'])#if max = min, we can generate randomly a number because we don't have an evident choice.
        else:
            sortedprobs = sorted(probs.items(), key=lambda x: x[1]['prob'])
            return sortedprobs[-1][0] #this will give you the max letter
            sortedprobs[0][0] #this will give you the min letter


def predict_on_random():
    return random.choice(['R','P','S']) #not predictions : just random for the first choice
    

first = True #if it is the first move, we need to initialize markov and the random
for i in range(10): #we play a game with X rounds : X = 10
	inp = input("You mouv : ") # ask the mouv of the player : we are not predict with this input, just update the matrix of the markov protocol
	if first==True:
		random_predictor = predict_on_random() #define random
		proc_markov = my_markov() #define markov
		prev = '' #define previous (prediction)
		now = '' #define now (prediction)
		first=False
	else: #else, we update the predictions
		prev = now
		now = output + inp

	if prev != '': #if it is not the first mouv, we are predict using markov an output
		proc_markov.update_matrix(prev, inp)
		output = proc_markov.predict(now) #we choose the mouv to do

	else:
		output = predict_on_random() #if it is the first mouv, we predict on a random list of R (Rock), P (Paper), S (Scissors)

	print("AI move : ",output)

#Well, sometimes, the markov processus loose games, because it is a simple implementation of the chain. For exemple, I can add Embedding, or other things.
