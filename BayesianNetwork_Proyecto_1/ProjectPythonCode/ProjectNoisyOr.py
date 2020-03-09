#!/usr/bin/env python
# coding: utf-8

# # Bayesian Networks

# ### Team 1
# 
# Alfredo Osuna,
# Fabricio Fuentes, 
# Rafael Rojas

# In[1]:


import math 
from pomegranate import *
import json
from copy import copy


# #### Function addNewTable creates all the Conditional Probability Tables of the Bayesian Network

# In[2]:


def addNewTable(node, cond_dis_list):
    
    ##List that contain the distributions and conditionals of the Conditional Probability Table
    conditional_list = []
    distribution_list = []
    
    ##Reads every k in the node
    for k in node.keys():
        
        ##List that contain the probability table of the Conditional Probability Table
        probability_list = []
        complementaryProb_list = []
        
        ##Info has the informations of the name and parents of the state 
        info = k.split("|")
        
        ##Parents has the list of parents of the state 
        parents = info[1].split(",")
        
        ##For every parent of the k it will push it to the probability list
        for i in range(len(parents)):
            probability_list.append(parents[i])
         
        ##Adds parent to probability list
        probability_list.append(info[0])
        
        ##It pushes the numerical value of the probability 
        probability_list.append(node.get(k))
        
        ##Adds that probability to the table
        conditional_list.append(probability_list)
        
        #Adds complementary row to actual probability_list
        complementaryProb_list = copy(probability_list)
        complementaryProb_list[len(complementaryProb_list)-2] = "-" + complementaryProb_list[len(complementaryProb_list)-2]
        complementaryProb_list[len(complementaryProb_list)-1] = 1 - complementaryProb_list[len(complementaryProb_list)-1]
        conditional_list.append(complementaryProb_list)
   
    ##Reads every k in the node
    for k in node.keys():
        
        ##Info has the informations of the name and parents of the state 
        info = k.split("|")
        
        ##Parents has the list of parents of the state 
        parents = info[1].split(",")
        
        ##For every parent of the k it will push it to the distribution list
        for i in range(len(parents)):
            
            ##For every distribution that equals to the parents  will push it to the distribution list
            for d in range(len(cond_dis_list)):
                if parents[i] == cond_dis_list[d][0] or parents[i] == "-"+cond_dis_list[d][0][0]:
                    distribution_list.append(cond_dis_list[d][1])
                    #print("ELEMENT:", cond_dis_list[d][1], "appended!")
                    break 
            
            ##For every distribution that equals to the parents  will push it to the distribution list
        
        break
    
    #print(distribution_list)
    #print(conditional_list)
    
    ##Creates a Conditional Probability Table with the conditional_list and distribution_list generated in the function
    cond = ConditionalProbabilityTable(conditional_list,distribution_list)
    
    ##Returns the Conditional Probability Table cond
    return cond


# #### Function addEdgesOfStates adds all the Edges between states of the Bayesian Network 

# In[3]:


#tuples of length 2 = DISCRETE DISTRIBUTION (NO PARENTS) -> (name, distribution)
#tuples of length 3 = CONDITIONAL PROBABILITY TABLE (WITH PARENTS) -> (name, cond, parents)

def addEdgesOfStates(network, cond_dist_list, state_list):
    cond_dist_list_INDEX = 0;
    for condDist in cond_dist_list:
        #A tuple of length 3 indicates that the distribution consists of a conditional probability table,
        #and thus has a parent which creates an edge with someone else.
        if(len(condDist) == 3):
            #The "son" state will always correspond with the current index of the for loop
            son = state_list[cond_dist_list_INDEX]
            #For each parent found to be associated with X son
            for parentTag in condDist[2]:
                #Searches for STATE associated with parentTag
                for parent in state_list:
                    if(parent.name == parentTag):
                        #Adds edge to the network
                        network.add_edge(parent, son)
        cond_dist_list_INDEX += 1
    
    return network


# #### Function createJsonFile creates a JSON file with the Bayesian Network

# In[4]:


# Receives the baked network 
# Creates and exports a JSON file
def createJsonFile(strToJson):
    print(strToJson)
    with open('BayesExport.json', 'w') as json_file:
        json.dump(strToJson, json_file)


# In[5]:


with open("Noisy_OR.json", "r") as f:
    bayer_data = json.load(f)

##Lists that contain the distributions, conditionals and states of the Bayesian Network
cond_dist_list = []
state_list = []
conditional_list = []
beliefs_list = []
query = None
dic = {}
counter = 0

##Reads every line of the JSON file 
for node in bayer_data:
    
    ##Reads every key value from the node that is reading at the moment
    for k in node.keys():
        
        ##If the k does not have a character "|" it means is a Discrete Distribution
        if k.find("|") == -1:
            name = k[0:len(k):1]
            
            #Looks for BELIEFS and" QUERIES
            if "BELIEF" in k:
                beliefs_list.append((k, node.get(k))) 
            elif "QUERY" in k:
                query = (k, node.get(k))
            
            ##Creates a Discrete Distribution with the k value as the name and the information of the key as the rest and adds it to the dictionary
            else:
                negativeKey = "-" + name + ""
                negativeVal = 1 - node[k]
                distribution = DiscreteDistribution({k : node.get(k), negativeKey: negativeVal})
                tuple_dis =(name, distribution)
                cond_dist_list.append(tuple_dis)
                ##Creates a new state with the distribution and the name k
                state_list.append(State( distribution, name = k))
            
        ##If the k has a "|" it means is a Conditional Probability Table    
        elif k.find("|") == 1: 
            
            info = k.split("|")
            name = info[0]
            parents = info[1].split(",")
            ##Calls the function addNewTable that returns a Conditional Probability Table and adds it to the dictionary
            cond = addNewTable(node, cond_dist_list)
            tuple_cond= (name,cond,parents)
            cond_dist_list.append(tuple_cond)
           
            ##Creates a new state with the conditional and the name k
            state_list.append(State(cond, name = k.split("|")[0]))
            break

#Creates network and adds all States in state_list to it
network = BayesianNetwork("Name of Bayesian Network")
for stateElement in state_list:
    network.add_states(stateElement)

#Adds all edges to the network
network = addEdgesOfStates(network, cond_dist_list, state_list);

#Bakes the network
network.bake()

# Puts the beliefs in a dictionary to sendo to the predict_proba method
#H true, I false, query B
for b in beliefs_list:
    if b[1][0] == '-':
        dic[b[1][1]] = b[1]
    else:
        dic[b[1]] = b[1]
        
beliefs = network.predict_proba(dic)
strToJson = ("n".join( "{}\t{}".format( state.name, str(belief) ) for state, belief in zip( network.states, beliefs )))

#Export Result to JSON File
createJsonFile(strToJson)

