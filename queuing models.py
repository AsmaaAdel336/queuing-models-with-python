import numpy as np
from scipy.stats import poisson, expon
import math
import statistics


class MM1:
    def __init__(self, arrival_dist, interarrival_time, service_dist, service_time, num_servers, system_capacity, population_size, system_discipline,n):
        self.arrival_dist = arrival_dist
        self.interarrival_time = interarrival_time
        self.service_dist = service_dist
        self.service_time = service_time
        self.num_servers = num_servers
        self.system_capacity = system_capacity
        self.population_size = population_size
        self.system_discipline = system_discipline
        self.n=n

    def calculate(self):
        #calculate arrival rate
        self.arrival_rate = statistics.fmean(self.arrival_dist)

        #calculate departure rate
        self.departure_rate = statistics.fmean(self.service_time)

        #calculate utilization
        self.utilization = self.arrival_rate / self.departure_rate

        #calculate the probability that there are n customers in the system
        self.prob_n_customers = (1-(self.arrival_rate / self.departure_rate))*((self.arrival_rate / self.departure_rate)**self.n)
        
        #calculate the probability of the initial population size (probability that there are no customers in the system)
        self.prob_init_population_size= 1-self.utilization

        #calculate the probability of population size
        self.prob_population_size= (1-self.utilization)*(self.utilization**self.population_size)
        
        #calculate the avarage number of customers in the system
        l= self.arrival_rate / (self.arrival_rate - self.departure_rate)

        #calculate the avarage number of customers in the queue
        lq=  self.arrival_rate**2 / (self.departure_rate * (self.departure_rate - self.arrival_rate))

        #calculate the avarage time a customer spends in the system
        w= 1/(self.departure_rate - self.arrival_rate)

        #calculate the avarage time a customer spends in the queue
        Wq= self.arrival_rate / (self.departure_rate * (self.departure_rate - self.arrival_rate))
        
        #calculate the probability that all servers are busy
        pw=self.arrival_rate / self.departure_rate

        #determine the type of queuing model related to the system
        self.queuing_model_type = 'MM1'

        #print the results
        
        print("\ntype of the queuing model related to the system : ",self.queuing_model_type)
        print("arrival rate : ", self.arrival_rate)
        print("departure rate : ",self.departure_rate)
        print("performance measures: \n1. average service time : ",1/self.departure_rate)
        print("2. probability that there are n customers in the system : ",self.prob_n_customers)
        print("3. avarage number of customers in the system : ",l)
        print("4. avarage number of customers in the queue : ",lq)
        print("5. average time a customer spends in the system : ", w)
        print("6. average time a customer spends in the queue : ",Wq)
        print("7. probability that all servers are busy : ",pw)
        print("8. utilization rate : ",self.utilization)
        print("9. probability of the initial population size : ",self.prob_init_population_size)
        print("10. probability of population size : ",self.prob_population_size)


class MMC:
    def __init__(self, arrival_dist, interarrival_time, service_dist, service_time, num_servers, system_capacity, population_size, system_discipline,n):
        self.arrival_dist = arrival_dist
        self.interarrival_time = interarrival_time
        self.service_dist = service_dist
        self.service_time = service_time
        self.num_servers = num_servers
        self.system_capacity = system_capacity
        self.population_size = population_size
        self.system_discipline = system_discipline
        self.n=n
    def calculate(self):
        #calculate arrival rate
        self.arrival_rate = statistics.fmean(self.arrival_dist)

        #calculate departure rate
        if 1 <= self.n < self.system_capacity: 
          self.departure_rate = statistics.fmean(self.service_time) * self.n
        elif self.n >= self.system_capacity:
          self.departure_rate = statistics.fmean(self.service_time) * self.system_capacity

        #calculate utilization
        self.utilization = self.arrival_rate / (self.departure_rate * self.system_capacity)

        #calculate the probability of the initial population size (probability that there are no customers in the system)
        self.prob_init_population_size= 0
        for i in range(self.system_capacity-1):
         self.prob_init_population_size += (1/math.factorial(i)) * ((self.arrival_rate / self.departure_rate)**self.n)
        self.prob_init_population_size= 1 / (self.prob_init_population_size +  ((1/math.factorial(self.system_capacity)*((self.arrival_rate/self.departure_rate)**self.system_capacity)*((self.system_capacity*self.departure_rate)/(self.system_capacity*self.departure_rate - self.arrival_rate)) )))

        #calculate the probability that there are n customers in the system
        if self.n <= self.system_capacity:
           self.prob_n_customers =( (( self.arrival_rate/self.departure_rate)**self.n)/(math.factorial(self.n)) ) * self.prob_init_population_size
        elif self.n > self.system_capacity:
           self.prob_n_customers =( (( self.arrival_rate/self.departure_rate)**self.n)/(math.factorial(self.system_capacity) * (self.system_capacity)**(self.n-self.system_capacity)) ) * self.prob_init_population_size
        
        #calculate the probability of population size
        self.prob_population_size= ( (( self.arrival_rate/self.departure_rate)**self.system_capacity)/(math.factorial(self.system_capacity)) ) * self.prob_init_population_size
        
        #calculate the avarage number of customers in the system
        l= ((( self.arrival_rate/self.departure_rate)**self.system_capacity) * self.arrival_rate * self.departure_rate *self.prob_init_population_size) / (math.factorial(self.system_capacity-1)*(self.system_capacity*self.departure_rate-self.arrival_rate)**2) + (self.arrival_rate/self.departure_rate)

        #calculate the avarage number of customers in the queue
        lq=  ((( self.arrival_rate/self.departure_rate)**self.system_capacity) * self.arrival_rate * self.departure_rate *self.prob_init_population_size) / (math.factorial(self.system_capacity-1)*(self.system_capacity*self.departure_rate-self.arrival_rate)**2)

        #calculate the avarage time a customer spends in the system
        w= ((( self.arrival_rate/self.departure_rate)**self.system_capacity) * self.departure_rate *self.prob_init_population_size) / (math.factorial(self.system_capacity-1)*(self.system_capacity*self.departure_rate-self.arrival_rate)**2) + (1/self.departure_rate)
        #calculate the avarage time a customer spends in the queue
        Wq= ((( self.arrival_rate/self.departure_rate)**self.system_capacity) * self.departure_rate *self.prob_init_population_size) / (math.factorial(self.system_capacity-1)*(self.system_capacity*self.departure_rate-self.arrival_rate)**2)
        
        #calculate the probability that all servers are busy
        pw= (1/math.factorial(self.system_capacity))*((self.arrival_rate/self.departure_rate)**self.system_capacity)*((self.departure_rate*self.system_capacity)/(self.departure_rate*self.system_capacity-self.arrival_rate))*self.prob_init_population_size
        
        #determine the type of queuing model related to the system
        self.queuing_model_type = 'MMC'

        #print the results
        
        print("\ntype of the queuing model related to the system : ",self.queuing_model_type)
        print("arrival rate : ", self.arrival_rate)
        print("departure rate : ",self.departure_rate)
        print("performance measures: \n1. average service time : ",1/self.departure_rate)
        print("2. probability that there are n customers in the system : ",self.prob_n_customers)
        print("3. avarage number of customers in the system : ",l)
        print("4. avarage number of customers in the queue : ",lq)
        print("5. avarage time a customer spends in the system : ", w)
        print("6. avarage time a customer spends in the queue : ",Wq)
        print("7. probability that all servers are busy : ",pw)
        print("8. utilization rate : ",self.utilization)
        print("9. probability of the initial population size : ",self.prob_init_population_size)
        print("10. probability of population size : ",self.prob_population_size)
      
class MM1K:
    def __init__(self, arrival_dist, interarrival_time, service_dist, service_time, num_servers, system_capacity, population_size, system_discipline,n):
        self.arrival_dist = arrival_dist
        self.interarrival_time = interarrival_time
        self.service_dist = service_dist
        self.service_time = service_time
        self.num_servers = num_servers
        self.system_capacity = system_capacity
        self.population_size = population_size
        self.system_discipline = system_discipline
        self.n=n

    def calculate(self):
                                                                       # k=1=one server  ,  f=k=capacity
        #calculate arrival rate
        
        self.arrival_rate = statistics.fmean(self.arrival_dist)
        
        #calculate departure rate
        self.departure_rate = statistics.fmean(self.service_time)

        #calculate the probability of the initial population size (probability that there are no customers in the system)
        sum1,sum2=0,0
        for i in range(1,self.num_servers):
           sum1+=((self.arrival_rate/self.departure_rate)**self.n)*math.factorial(i)
        for j in range(self.num_servers+1 , self.system_capacity):
           sum2+= (self.arrival_rate/(self.departure_rate*self.num_servers))**(j-self.num_servers)
        self.prob_init_population_size= 1/(1+sum1+ (((self.arrival_rate/self.departure_rate)**self.num_servers)/math.factorial(self.num_servers)) + sum2)
        
        #calculate the probability that there are n customers in the system
        if self.n < self.num_servers:
            self.prob_n_customers = ((self.arrival_rate/self.departure_rate)**self.n *self.prob_init_population_size)/(math.factorial(self.n))
        else:
            self.prob_n_customers = ((self.arrival_rate/self.departure_rate)**self.n *self.prob_init_population_size)/(math.factorial(self.num_servers)*(self.num_servers)**(self.n-self.num_servers))

        #calculate the utilization
        self.utilization = 0
        for i in range(0,self.system_capacity-1):
           self.utilization += ((self.arrival_rate/self.departure_rate)**i *self.prob_init_population_size)/(math.factorial(i))
        self.utilization = (self.arrival_rate*self.utilization)/(self.num_servers*self.departure_rate)
        

        #calculate the probability of population size
        self.prob_population_size= (1-self.utilization)*(self.utilization**self.population_size)
        
        #calculate the avarage number of customers in the system
        x= 0
        for i in range(0,self.num_servers):
           x+=((self.arrival_rate/self.departure_rate)**i *self.prob_init_population_size)/(math.factorial(i))
        bracket=(self.arrival_rate/(self.departure_rate*self.num_servers))
        l = ((self.prob_init_population_size*((self.arrival_rate/self.departure_rate)**self.num_servers)*bracket)*(1-bracket**(self.system_capacity-self.num_servers) -(self.system_capacity-self.num_servers)*(bracket**(self.system_capacity-self.num_servers))*(1-bracket)))/(math.factorial(self.num_servers)*(1-bracket)**2) + x*self.n + self.num_servers*(1-x)

        #calculate the avarage number of customers in the queue
        lq=  l- ( x*self.n + self.num_servers*(1-x))
        #calculate the avarage time a customer spends in the system
        w= l/(self.arrival_rate*x)

        #calculate the avarage time a customer spends in the queue
        Wq= lq/(self.arrival_rate*x)

        #calculate the probability that all servers are busy
        pw=1-x

        
        #determine the type of queuing model related to the system
        self.queuing_model_type = 'MM1K'

        #print the results
        
        print("\ntype of the queuing model related to the system : ",self.queuing_model_type)
        print("arrival rate : ", self.arrival_rate)
        print("departure rate : ",self.departure_rate)
        print("performance measures: \n1. average service time : ",1/self.departure_rate)
        print("2. probability that there are n customers in the system : ",self.prob_n_customers)
        print("3. avarage number of customers in the system : ",l)
        print("4. avarage number of customers in the queue : ",lq)
        print("5. average time a customer spends in the system : ", w)
        print("6. average time a customer spends in the queue : ",Wq)
        print("7. probability that all servers are busy : ",pw)
        print("8. utilization rate : ",self.utilization)
        print("9. probability of the initial population size : ",self.prob_init_population_size)
        print("10. probability of population size : ",self.prob_population_size)

class MMinf:
    def __init__(self, arrival_dist, interarrival_time, service_dist, service_time, num_servers, system_capacity, population_size, system_discipline,n):
        self.arrival_dist = arrival_dist
        self.interarrival_time = interarrival_time
        self.service_dist = service_dist
        self.service_time = service_time
        self.num_servers = num_servers
        self.system_capacity = system_capacity
        self.population_size = population_size
        self.system_discipline = system_discipline
        self.n=n
    
    def calculate(self):
        #calculate arrival rate
        self.arrival_rate = statistics.fmean(self.arrival_dist)

        #calculate departure rate
        self.departure_rate = statistics.fmean(self.service_time) * self.n

        #calculate utilization
        self.utilization = self.arrival_rate / self.departure_rate

        #calculate the probability of the initial population size (probability that there are no customers in the system)
        self.prob_init_population_size= math.exp(-self.utilization)

        #calculate the probability that there are n customers in the system
        self.prob_n_customers = (((self.arrival_rate/self.departure_rate)**self.n)*math.exp(-self.arrival_rate/self.departure_rate))/math.factorial(self.n)

        #calculate the probability of population size
        self.prob_population_size= (((self.arrival_rate/self.departure_rate)**self.population_size)*math.exp(-self.arrival_rate/self.departure_rate))/math.factorial(self.population_size)
        
        #calculate the avarage number of customers in the system
        l= self.arrival_rate / self.departure_rate

        
        #calculate the avarage time a customer spends in the system
        w= 1/self.departure_rate

        
        
        #determine the type of queuing model related to the system
        self.queuing_model_type = 'MM infinity'

        #print the results
        
        print("\ntype of the queuing model related to the system : ",self.queuing_model_type)
        print("arrival rate : ", self.arrival_rate)
        print("departure rate : ",self.departure_rate)
        print("performance measures: \n1. average service time : ",1/self.departure_rate)
        print("2. probability that there are n customers in the system : ",self.prob_n_customers)
        print("3. avarage number of customers in the system : ",l)
        print("4. average time a customer spends in the system : ", w)
        print("5. utilization rate : ",self.utilization)
        print("6. probability of the initial population size : ",self.prob_init_population_size)
        print("7. probability of population size : ",self.prob_population_size)


def Main():
  population_size=int(input("Enter the population size : "))
  arrival_dist=[]
  interarrival_time=[]
  service_dist=[]
  service_time=[]
  for i in range(1, population_size+1):
   arrival_dist.append(float(input("Enter the probability distribution of arrival of customer number {} : ".format(i))))
  for i in range(1, population_size+1):
   interarrival_time.append(float(input("Enter the the Interarrival time for customer number {} : ".format(i))))
  for i in range(1, population_size+1):
   service_dist.append(float(input("Enter the probability distribution of Service time for customer number {} : ".format(i))))
  for i in range(1, population_size+1):
   service_time.append(float(input("Enter the Service time for customer number {} : ".format(i))))
  num_servers=int(input("Enter the number of servers, if it is infinity enter 100 : "))
  system_capacity=int(input("Enter the system capacity, if it is infinity enter 100 : "))
  system_discipline=str(input("Enter the system discipline : "))
  n=int(input("to calculate the probability that there are n customers in the system please enter the value of n : "))

  if ((num_servers==1) and (system_capacity==100)) :
   Model=MM1(arrival_dist,interarrival_time,service_dist,service_time,num_servers,system_capacity,population_size,system_discipline,n)
   print(Model.calculate())
  elif ( 1< num_servers <100 ):
    Model=MMC(arrival_dist,interarrival_time,service_dist,service_time,num_servers,system_capacity,population_size,system_discipline,n)
    print(Model.calculate())
  elif ((num_servers==1) and (system_capacity<100)):
     Model=MM1K(arrival_dist,interarrival_time,service_dist,service_time,num_servers,system_capacity,population_size,system_discipline,n)
     print(Model.calculate())
  elif (num_servers==100):
     Model=MMinf(arrival_dist,interarrival_time,service_dist,service_time,num_servers,system_capacity,population_size,system_discipline,n)
     print(Model.calculate())
   
Main()

