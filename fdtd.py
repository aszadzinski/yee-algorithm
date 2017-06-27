import matplotlib.pyplot as plt
import numpy as nu
import math
import time as tt

class Simulation():
	
	def __init__(self):#def. stalych etc
		
		self.e = 8.8541878176203892*10**(-12)#Electrical permeability in vacuum
		self.u = 1.2566370614359171*10**(-6) #Magnetic permeability in vacuum
		self.c = (1/(self.e*self.u))**(0.5)#speed of light
		self.ds = 0.001#len gain
		self.dt = (0.5*self.ds)/self.c #time gain
		self.sizex = 400#yee net resolution x
		self.sizey = 350#yee net resolution		                      	
		self.n = 1600#duration			
		self.f = 0.03#frequency of light source
		self.six = int(self.sizex/2)#source position x
		self.siy = int(self.sizey/2)# -=- y              
		self.t_w = 200#emission time

		#creating 3D arrays to E and H field components
		self.E, self.H = [], []
		self.ee, self.hh = [], []
		for i in range(2):
			self.E.append(nu.zeros((self.sizex,self.sizey)))
			self.H.append(nu.zeros((self.sizex,self.sizey)))
			self.ee.append(nu.zeros((self.sizex,self.sizey)))
			self.hh.append(nu.zeros((self.sizex,self.sizey)))
			
		for i in range(self.sizex):
			for j in range(self.sizey):
				if i>self.sizex/2:
					self.ee[0][i,j]=1
					self.hh[0][i,j]=1
				else:
					self.ee[0][i,j]=1.
					self.hh[0][i,j]=1.		
		#creating net
		self.xe, self.xh = [], []		            
		
		#other coefficients
		self.ceh=self.dt/(self.ds*self.e)
		self.che=self.dt/(self.ds*self.u)
		self.st=0
		
	def start(self):
		#self.metric()
		e, h = 1., 1.
		for t in range(0,self.n,1):
			start = tt.time()
			if t<self.t_w:
				self.H[0][60,self.siy] = 10e3*math.sin(2*self.f*math.pi*t)
			else:
				self.E[0][5,self.siy]  = 0	
					
			plt.close()
						
			for i in range(0,self.sizex):
				for j in range(1,self.sizey):
						#e = (1-(self.dt*2e-2)/(self.e *2*80))/(1+(self.dt*2e-2)/(self.e *2*80))		
					self.E[0][i,j] = self.ee[0][i,j]*self.E[0][i,j] + self.ceh*(self.H[0][i,j] - self.H[0][i,j-1]) 
					if (i>self.sizex/2 and i<2+self.sizex/2 and (j>150 and j<140)):
						self.E[0][i,j] =0
			for i in range(1,self.sizex):
				for j in range(0,self.sizey):
					self.E[1][i,j] = self.ee[0][i,j]*self.E[1][i,j] + self.ceh*(self.H[0][i-1,j] - self.H[0][i,j])
					if (i>self.sizex/2 and i<2+self.sizex/2 and (j>150 and j<140)):
						self.E[1][i,j] =0
			for i in range(0,self.sizex-1):
				for j in range(0,self.sizey-1): 
						#h = (1-(self.dt*1.3e2)/(self.u *2*0.98))/(1+(self.dt*1.3e2)/(self.u *2*0.98))
					self.H[0][i,j] = self.hh[0][i,j]*self.H[0][i,j] + self.che*(self.E[0][i,j+1] - self.E[0][i,j] + self.E[1][i,j] - self.E[1][i+1,j])
					if (i>self.sizex/2 and i<2+self.sizex/2 and (j>150 and j<140)):
						self.H[0][i,j] =0		
			#print(self.E[0])

			#X = self.xe
			#Y = self.xe
			#X, Y = nu.meshgrid(X, Y)
			Z=self.H[0]
			plt.imshow(Z,interpolation="lanczos",cmap="gray")
			plt.savefig('wyk%r.png' %str(t))
			#plt.show()
			stop = tt.time()
			sumt = (self.n-t+1)*(stop-start)/60
			self.st += (stop-start)/60
			print('[{}/{}] frames, {} minutes left'.format(t+1,self.n,round(sumt,2)))
		print('Done in {} minutes'.format(self.st))
		
if __name__ == '__main__':
	yee = Simulation()
	yee.start()
