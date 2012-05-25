#N-Body 
#Nick Walker
#23/5/2012
#Simulates the interactions of celestial bodies in a n-body system with three dimensional vector graphics

from visual import *																																						#the necessary packages
#from sympy import *
from random import *
class Celestial(sphere):																																					#the object used for celestial objects

	def __init__(self,radius=1,mass=1e5,density=1,position=vector(0.,0.,0.),velocity=vector(0.,0.,0.),acceleration=vector(0.,0.,0.),rotangle=pi/7500,rotaxis=(0,1,0),star=False):
		"""takes radius, mass, density, position vector, velocity vector, acceleration vector, rotation angle, rotation axis arguments
		creates a celestial object"""																																		#the celestial class
		self._r=radius																																						#physical values from inputs
		self._m=mass
		self._d=density
		self._p=position
		self._v=velocity
		self._a=acceleration
		self._ra=rotangle
		self._rax=rotaxis
		self._star=star
		sphere.__init__(self,radius=self._r,pos=self._p,make_trail=True,interval=10)																						#child of the sphere class
		
	def getMass(self):																																						#return the mass of the object
		"""takes no arguments
		returns the mass of the object"""
		return self._m
		
	def setMass(self,mass):																																					#set the mass of the object
		"""takes mass argument
		sets the mass of the object"""
		self._m=mass
		
	def getDensity(self):																																					#return the density of the object
		"""takes no arguments
		returns the density of the object"""
		return self._d
		
	def setDensity(self,density):																																			#set the density of the object
		"""takes density argument
		sets the density of the argument"""
		self._d=density
		
	def getVelocity(self):																																					#return the velocity of the object
		"""takes no arguments
		returns the velocity of the object"""
		return self._v
		
	def setVelocity(self,velocity):																																			#set the velocity of the object
		"""takes velocity vector argument
		sets the velocity of the object"""
		self._v=velocity
		
	def getAcceleration(self):																																				#return the acceleration of the object
		"""takes no arguments
		returns the acceleration of the object"""
		return self._a
		
	def setAcceleration(self,acceleration):																																	#set the acceleration of the object
		"""takes acceleration vector as an argument
		sets the acceleration of the object"""
		self._a=acceleration
		
	def getRotAngle(self):																																					#return the rotation angle change of the object
		"""takes no arguments
		returns the rotation angle change of the object"""
		return self._ra
		
	def setRotAngle(self,angle):																																			#set the rotation angle change of the object
		"""takes and angle in radians
		sets the rotation andgle change"""
		self._ra=angle
		
	def getRotAxis(self):																																					#return the roation axis of the object
		"""takes no arguments
		returns the rotation axis of the object"""
		return self._rax
		
	def setRotAxis(self,axis):																																				#set the rotation axis of the object
		"""takes rotation axis vector of the object
		sets the rotation axis of the object"""
		self._rax=axis
	
	def getStar(self):																																						#return whether or no the object is a star
		"""returns bool for whether or no the object is a star"""
		return self._star
		
	def setStar(self,bool):																																					#set the status of the object (star or non-star)
		"""takes a bool value as an argument
		sets the bool value determining whether and object is a star or not"""
		self._star=bool
		
	def centripetalVelocity(self,position,mass):																															#calculate the centripetal velocity of the object relative to a target object
		"""takes target object as an argument
		returns the calculated centripetal velocity of the object about a target object"""
		G=6.67e-11
		v=sqrt(G*mass/mag(self.pos-position))																																#formula for the magnitude of the velocity
		uv=norm(self.pos-position)																																			#normalized vector between the two objects
		d=rotate(uv,angle=pi/2,axis=(0,1,0))																																#vector rotated pi/2 about the y axis to become a tangential vector
		return v*d
		
def remove(bodies,body,dt):																																					#function for popping a celestial object out of the list of objects
	"""takes a list of objects, an object, and the timestep of the animation
	removes the specified body from the system and adjusts the list of bodies and the timestep accordingly"""
	body.trail_object.visible=False																																			#trail made invisible
	body.visible=False																																						#object made invisible
	if bodies.count(body)==1:																																				#if the body is an object in the list and has a count of one, it is removed from the list
		bodies.remove(body)
	del body																																								#object deleted
	dt-=1																																									#timestep reduced to compensate for the loss of an object in the system
	return dt
	
def collision(bodies,body1,body2,dt):																																		#function for handling the inelastic collision of celestial objects
	"""takes the list of objects, the first object, the second object, and the timestep
	determines if there is a collision between to objects and determines the results through inelastic collision"""
	collision=False																																							#by default, it is assumed there is no collision
	if mag(body1.pos-body2.pos)<body1.radius+body2.radius:																													#if the two objects intersect, there is a collision
		collision=True
	if collision==True:
		if body1.getMass()>=body2.getMass():																																#if the first object is larger in mass than the second object, it survives the collision															
			body1.setVelocity((body1.getMass()*body1.getVelocity()+body2.getMass()*body2.getVelocity())/(body1.getMass()+body2.getMass()))									#calculates the new velocity of the object according to conservation of momentum
			body1.setDensity(body1.getDensity()*body1.getMass()/(body1.getMass()+body2.getMass())+body2.getDensity()*body2.getMass()/(body1.getMass()+body2.getMass()))		#calculates new density
			body1.setMass(body1.getMass()+body2.getMass())																													#sums the masses as the new mass of the object
			body1.radius=sqrt((body1.getMass()*3/4/body1.getDensity()/pi))																									#determines the new radius of the object
			remove(bodies,body2,dt)																																			#removes the smaller object
		else:																																								#if the second object is larger or equal to the first object in  mass, it survives the collision
			body2.setVelocity((body1.getMass()*body1.getVelocity()+body2.getMass()*body2.getVelocity())/(body1.getMass()+body2.getMass()))									#calculates the new velocity of the object according to conservation of momentum
			body2.setDensity(body1.getDensity()*body1.getMass()/(body1.getMass()+body2.getMass())+body2.getDensity()*body2.getMass()/(body1.getMass()+body2.getMass()))		#calculates new density
			body2.setMass(body1.getMass()+body2.getMass())																													#sums the masses as the new mass of the object
			body2.radius=sqrt((body2.getMass()*3/4/body2.getDensity()/pi))																									#determines the new radius of the object
			remove(bodies,body1,dt)																																			#removes the smaller object
	return collision

def centerOfMass(bodies):																																					#calculate the center of mass of the system
	"""takes the list of objects and calculates and returns the center of mass of the system"""
	moments=vector(0,0,0)
	mass=0.
	for planet in bodies:
		moments+=planet.getMass()*planet.pos																																#sum the moments
		mass+=planet.getMass()																																				#sum the masses
	return moments/mass																																						#quotient of the moments and the masses
	
def totalMass(bodies):																																						#calculate the total mass
	"""takes the list of objects and calculates the total mass of the system"""
	mass=0.
	for planet in bodies:
		mass+=planet.getMass()																																				#sum the masses
	return mass
	
def centerOfMassVelocity(bodies):																																			#calculate the velocity of the center of mass
	momentums=vector(0,0,0)
	mass=0.
	for planet in bodies:
		momentums+=planet.getMass()*planet.getVelocity()																													#sum the momentums
		mass+=planet.getMass()																																				#sum the masses
	return momentums/mass																																					#quotient of the momentums and masses
	
def newton(bodies,dt):																																						#function for animating an n-body system with newtons's laws of gravitation
	"""takes a list of objects, timestep
	animates an n-body system according to newton's law of gravitation"""
	G=6.67e-11
	running=False																																							#animation starts out paused
	texture=False																																							#animation starts out with solid colors
	trails=True																																								#animation starts out with trails
	material=[materials.wood,materials.marble,materials.BlueMarble,materials.rough]																							#choice of materials
	colors=[color.orange,color.blue,color.green,color.magenta,color.red,color.cyan,color.yellow]																			#choice of colors
	print 't: toggle trails'+'\n'+'p: pause/play'+'\n'+'m: toggle materials'+'\n'+'c: toggle colors'+'\n'+'a: add planet'+'\n'+'s: subtract planet'+'\n'+'r: reverse orbits'+'\n'+'u: increase mass of star'+'\n'+'d: decrease mass of star'+'\n'+'k: meteor strike'+'\n'+'b: binary stars'+'\n'+'v: change viewpoint'+'\n'+'click on objects to reposition them'
	com=centerOfMass(bodies)																																				#initialize center of mass
	tm=totalMass(bodies)																																					#initialize total mass
	binary=False																																							#initialize the indicator for type of system
	view='star'																																								#initialize viewpoint
	r=bodies[0].radius																																						#initialize radius
	while True:																																								#animation continues forever
		if scene.mouse.events:																																				#if a mouse event occurs
			mouse=scene.mouse.getevent()																																	#capture event
			for planet in bodies:
				if mouse.drag and mouse.pick==planet:																														#if a planet is clicked on
					while not scene.mouse.clicked:
						planet.pos=scene.mouse.pos																															#moves planet to drag location until click
		if scene.kb.keys:																																					#capture keystrokes
			k = scene.kb.getkey()																																			#capture keystrokes
			if k=='b' and binary==False:																																	#'b' for binary orbit
				x=randint(int(bodies[0].radius),int(2*bodies[0].radius))																									#generates x coordinate
				y=randint(-int(bodies[0].radius/4),int(bodies[0].radius/4))																									#generates y coordinate
				z=randint(int(bodies[0].radius),int(2*bodies[0].radius))																									#generates z coordinate
				position=vector(x,y,z)																																		#constructs position vector out of coordinates
				star=Celestial(bodies[0].radius,bodies[0].getMass(),bodies[0].getDensity(),vector(0,0,0),vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0),True)
				star.color=bodies[0].color
				star.material=bodies[0].material
				star.trail_object.color=bodies[0].trail_object.color
				star.retain=bodies[0].retain
				bodies.insert(0,star)																																		#put the new star at the front of the list
				bodies[0].retain=0																																			#momentarily turn off trails for relocation
				bodies[1].retain=0
				bodies[0].pos+=position																																		#move the stars	
				bodies[1].pos-=position
				com=centerOfMass(bodies)																																	#recalculate the centroid, mass, and velcoity of the system
				m=totalMass(bodies)
				v=centerOfMassVelocity(bodies)
				bodies[0].setVelocity(centerOfMassVelocity(bodies)+.5*bodies[0].centripetalVelocity(com,tm))																#set the new velocities
				bodies[1].setVelocity(bodies[1].getVelocity()+.5*bodies[1].centripetalVelocity(com,tm))
				binary=True																																					#this is now a binary system
				if view=='star':																																			#the viewpoint is changed
					view=(bodies[1].pos+bodies[0].pos)/2
				if view=='com':
					view=com
				r=(mag(bodies[0].pos-com)+bodies[0].radius)/2																												#new radius for spawning purposes
				if trails==True:																																			#turn the trails back on
					bodies[0].retain=1000000																																
					bodies[1].retain=1000000
			if k=='a':																																						#'a' for add planet
				x=randint(int(1.5*r),int(5*r))																																#generates x coordinate
				y=randint(-int(bodies[0].radius/4),int(bodies[0].radius/4))																									#generates y coordinate
				z=randint(int(1.5*r),int(5*r))																																#generates z coordinate
				position=vector(x,y,z)																																		#constructs position vector out of coordinates
				position=com+rotate(position,angle=randint(0,360)*pi/180,axis=(0,1,0))																						#rotates position vector about the origin
				planet=Celestial(1,randint(1,1e5),randint(5,15),position,vector(0,0,0),vector(0,0,0),randint(80,120)/100.*pi/7500.,(0,1,0))									#new celestial object created
				planet.radius=sqrt((planet.getMass()*3/4/planet.getDensity()/pi))																							#reset radius to match density and mass
				if texture==False:																																			#if textures are not in use, generate solid color
					planet.color=choice(colors)
					planet.trail_object.color=planet.color
				if texture==True:																																			#if textures are in use, generate texture
					planet.material=choice(material)
					planet.trail_object.color=choice(colors)
				if trails==False:																																			#if trails are not in use, retain no points
					planet.retain=0
				planet.setVelocity(planet.centripetalVelocity(com,tm)*randint(80,120)/100.+centerOfMassVelocity(bodies))													#sets the planet's velocity as 75-125% of its centripetal velocity
				bodies.append(planet)																																		#adds the planet to the list of celestial objects
				dt+=1																																						#increments the timestep
			if k=='s':																																						#'s' for subtract planet
				if len(bodies)>2 and binary==True:
					dt=remove(bodies,bodies[len(bodies)-1],dt)
				elif len(bodies)>1 and binary==False:
					dt=remove(bodies,bodies[len(bodies)-1],dt)
			if k=='t':																																						#'t' for trails toggle
				trails=not trails																																			#switches the bool
				for planet in bodies:																																		#walks through the list of objects
					if trails==False:
						planet.retain=0																																		#retain no position indices
					if trails==True:																																				
						planet.retain=1000000																																#retain arbitrarily high amount of data points
			if k=='p':																																						#'p' for pause/play
				running=not running
			if k=='m':																																						#'m' for render planets with material textures
				if bodies[0].material!=materials.emissive:
					texture=true
				for planet in bodies:
					planet.color=color.white
					planet.material=choice(material)
				bodies[0].material=materials.emissive
				bodies[0].color=color.yellow
				if binary==True:
					bodies[1].material=materials.emissive
					bodies[1].color=color.yellow
			if k=='c':																																						#'c' for render planets with solid textures
				if bodies[0].material==materials.emissive:
					texture=false
				for planet in bodies:
					planet.material=materials.diffuse
					planet.color=choice(colors)
					planet.trail_object.color=planet.color
				bodies[0].color=color.yellow
				bodies[0].trail_object.color=bodies[0].color
				if binary==True:
					bodies[1].color=color.yellow
					bodies[1].trail_object.color=bodies[0].color
			if k=='r':																																						#'r' for reverse animation
				for planet in bodies:
					planet.setVelocity(-1*planet.getVelocity())
					planet.setRotAngle(-1*planet.getRotAngle())
			if k=='u':																																						#'u' for increase mass of the star
				bodies[0].setMass(bodies[0].getMass()+1e10)
				bodies[0].radius=sqrt((bodies[0].getMass()*3/4/bodies[0].getDensity()/pi))																					#readjust radius
				if binary==True:
					bodies[1].setMass(bodies[1].getMass()+1e10)
					bodies[1].radius=sqrt((bodies[1].getMass()*3/4/bodies[1].getDensity()/pi))
			if k=='d':																																						#'d' for decrease mass of the star
				if bodies[0].getMass()>1e10:
					bodies[0].setMass(bodies[0].getMass()-1e10)
					bodies[0].radius=sqrt((bodies[0].getMass()*3/4/bodies[0].getDensity()/pi))																				#readjust radius
				if binary==True and bodies[1].getMass()>1e10:
					bodies[1].setMass(bodies[1].getMass()+1e10)
					bodies[1].radius=sqrt((bodies[1].getMass()*3/4/bodies[1].getDensity()/pi))
			if k=='k':																																						#'k' for i'm running out of letters
				x=randint(0,int(12*r))																																		#generate random radius from star
				y=randint(-int(bodies[0].radius/4),int(bodies[0].radius/4))																									#generate random off-plane y coordinate
				z=sqrt((25*r)**2-x**2)																																		#calculate z coordinate needed for standard radius form star
				position=vector(x,y,z)																																		#construct position vector
				position=com+rotate(position,angle=randint(0,360)*pi/180,axis=(0,1,0))																						#rotate the position about the origin
				apocalypse=Celestial(1,randint(1e8,1e9),randint(1e4,1e5),position,vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0))						#create apocalyptic space object
				apocalypse.radius=sqrt((apocalypse.getMass()*3/4/apocalypse.getDensity()/pi))																				#adjust radius for density
				if texture==False:																																			#use solid colors if textures are not in use
					apocalypse.color=choice(colors)
					apocalypse.trail_object.color=apocalypse.color
				if texture==True:																																			#use textures if textures are in use
					apocalypse.material=choice(material)
					apocalypse.trail_object.color=choice(colors)
				if trails==False:																																			#retain no point in the trail if trail not in use
					apocalypse.retain=0
				velocity=-norm(apocalypse.pos-com)																															#normalize the vector between the object and the star
				velocity.x=velocity.x*randint(50,150)/100.																													#introduce some uncertainty
				velocity.y=velocity.y*randint(50,150)/100.
				velocity.z=velocity.z*randint(50,150)/100.
				velocity=rotate(velocity,angle=randint(-15,15)*pi/180,axis=(0,1,0))																							#rotate the vector
				apocalypse.setVelocity(.15*velocity)																														#only one tenth the magnitude of the unit vector
				bodies.append(apocalypse)																																	#add the object to the list of objects interacting with each other
				dt+=1																																						#increment the timestep accordingly
			if k=='v':																																						#'v' for change viewpoint
				if view=='com':																																				#switches between the star and the center of mass
					view='star'
				else:
					view='com'
		if running:
			for target in bodies:																																			#pick an object to calculate vectors for
				for object in bodies:																																		#pick an object to use for the vector calculations
					if target!=object:																																		#check against self-gravity
						if collision(bodies,target,object,dt)==true and target.getStar() and object.getStar():																#check for collisions
							binary=False
							dt-=1																																			#reduce timestep due to collision
						elif collision(bodies,target,object,dt)==true:																										#check for collisions
							dt-=1	
						else:
							target.unitvector=norm(object.pos-target.pos)																									#determine the unit vector between the two objects
							target.acceleration=G*object.getMass()/mag2(object.pos-target.pos)																				#calculate the accleration from newton's law of gravitation
							target.accelerationvector=target.acceleration*target.unitvector																					#determine the accleration vector from the magnitude and the unit vector
							target.setAcceleration(target.getAcceleration()+target.accelerationvector)																		#sum the accelerations due to gravity from each object
							target.setVelocity(target.getVelocity()+target.getAcceleration())																				#sum the velocities due to gravity using instananeous acceleration
						if mag(object.pos-com)>100*bodies[0].radius:																										#removes planets that leave the system
							dt=remove(bodies,object,dt)
			for planet in bodies:
				planet.pos+=planet.getVelocity()*dt+.5*planet.getAcceleration()*dt**2																						#move the planet according the the calculated velocity and acceleration
				planet.rotate(angle=dt*planet.getRotAngle(),axis=planet.getRotAxis())																						#rotate the planet
				planet.setAcceleration(vector(0.,0.,0.))																													#reset the acceleration to zero to allow for recalculation
			com=centerOfMass(bodies)
			tm=totalMass(bodies)
			if view=='com':																																					#centers camera on toggle value
				scene.center=com
			else:
				if binary==True:
					scene.center=(bodies[1].pos+bodies[0].pos)/2
				else:
					scene.center=bodies[0].pos																																			
				
scene = display(title="Solar System",width=600,height=600,range=1e3,forward=(-1,-1,-1),autoscale=false,ambient=0)
#scene.stereo = 'redcyan'																																					#3D
star=Celestial(100,1e10,1e5,vector(0,0,0),vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0),True)
star.radius=sqrt((star.getMass()*3/4/star.getDensity()/pi))
star.color=color.yellow
star.trail_object.color=star.color
bodies=[star]
newton(bodies,1)