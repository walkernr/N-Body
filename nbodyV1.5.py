from visual import *																																						#the necessary packages
from random import *
import py_compile
#fix trails for stars

class Celestial(sphere):																																					#the object used for celestial objects

	def __init__(self,mass=1e5, density=1,position=vector(0.,0.,0.),velocity=vector(0.,0.,0.),acceleration=vector(0.,0.,0.),rotangle=pi/7500,rotaxis=(0,1,0),star=False):
		"""takes mass, density, position vector, velocity vector, acceleration vector, rotation angle, rotation axis arguments
		creates a celestial object"""																																		
		self.m=mass																																							#physical characteristics
		self.d=density
		self.v=velocity
		self.a=acceleration
		self.ra=rotangle
		self.rax=rotaxis
		self.st=star
		sphere.__init__(self,radius=sqrt((self.m*3/4/self.d/pi)),pos=position,make_trail=True,interval=10)																	#child of the sphere class
		
	def resetRadius(self):
		"""takes no arguments
		resets the radius of an object"""
		self.radius=sqrt((self.m*3/4/self.d/pi))
		
	def centripetalVelocity(self,objects,star=False,factor=0.):																												#calculate the centripetal velocity of the object relative to a target object
		"""takes target object as an argument
		returns the calculated centripetal velocity of the object about the center of mass of the system"""
		G=6.67e-11
		m=starMass(objects)																																					#.125,.192,.240,.276,.309,.327
		if self.st:
			m=m*(.1636*log(factor)+.0124)
		c=starCenterOfMass(objects)
		v=sqrt(G*m/mag(self.pos-c))																																			#formula for the magnitude of the velocity
		uv=norm(self.pos-c)																																					#normalized vector between the two objects
		d=rotate(uv,angle=pi/2,axis=(0,1,0))																																#vector rotated pi/2 about the y axis to become a tangential vector
		return v*d
		
def remove(objects,object):																																					#function for popping a celestial object out of the list of objects
	"""takes a list of objects, an object, and the timestep of the animation
	removes the specified object from the system"""
	object.trail_object.visible=False																																		#trail made invisible
	object.visible=False																																					#object made invisible
	if objects.count(object)>0:
		objects.remove(object)
	del object																																								#object deleted
	
def collision(objects,object1,object2):																																		#function for handling the inelastic collision of celestial objects
	"""takes the list of objects, the first object, the second object, and the timestep
	determines if there is a collision between to objects and determines the results through inelastic collision"""
	collision=False																																							#by default, it is assumed there is no collision
	if mag(object1.pos-object2.pos)<object1.radius+object2.radius:																											#if the two objects intersect, there is a collision
		collision=True
	if collision==True:
		if object1.m>=object2.m and not object2.st:																																			#if the first object is larger in mass than the second object, it survives the collision															
			object1.v=(object1.m*object1.v+object2.m*object2.v)/(object1.m+object2.m)																						#calculates the new velocity of the object according to conservation of momentum
			object1.d=(object1.d*object1.m+object2.d*object2.m)/(object1.m+object2.m)																						#calculates new density
			object1.m=object1.m+object2.m																																	#sums the masses as the new mass of the object
			object1.resetRadius()																																			#determines the new radius of the object
			remove(objects,object2)																																			#removes the smaller object
		elif object1.m>=object2.m and object2.st:																																			#if the first object is larger in mass than the second object, it survives the collision															
			object2.v=(object1.m*object1.v+object2.m*object2.v)/(object1.m+object2.m)																						#calculates the new velocity of the object according to conservation of momentum
			object2.d=(object1.d*object1.m+object2.d*object2.m)/(object1.m+object2.m)																						#calculates new density
			object2.m=object1.m+object2.m																																	#sums the masses as the new mass of the object
			object2.resetRadius()																																			#determines the new radius of the object
			remove(objects,object1)																																			#removes the smaller object
	return collision
	
def starMass(objects):
	"""takes the list of objects and calculates the total mass of the stars"""
	mass=0.
	for object in objects:
		if object.st==True:
			mass+=object.m																																					#sum the masses
	return mass
	
def starCenterOfMass(objects):
	"""takes the list of objects and calculates and returns the center of mass of the system of stars"""
	moments=vector(0.,0.,0.)
	for object in objects:
		if object.st==True:
			moments+=object.m*object.pos																																	#sum the moments
	return moments/starMass(objects)																																		#quotient of the moments and the masses
	
def starCenterOfMassVelocity(objects):
	"""takes the list of objects and returns the velocity of the center of mass of the stars"""
	momentums=vector(0.,0.,0.)
	for object in objects:
		if object.st:
			momentums+=object.m*object.v																																	#sum the momentums
	return momentums/starMass(objects)																																		#quotient of the momentums and masses
	
def gravitate(objects):
	print 't: toggle trails'+'\n'+'p: pause/play'+'\n'+'m: toggle materials'+'\n'+'c: toggle colors'+'\n'+'a: add planet'+'\n'+'s: subtract planet'+'\n'+'r: reverse orbits'+'\n'+'k: meteor strike'+'\n'+'b: add star'+'\n'+'v: change viewpoint'+'\n'+'click on objects to reposition them'
	running=False
	textures=False
	trails=True
	material=[materials.wood,materials.marble,materials.BlueMarble,materials.rough]																							#choice of materials
	colors=[color.orange,color.blue,color.green,color.magenta,color.red,color.cyan,color.yellow]																			#choice of colors
	ct=1.
	dt=1.
	g=6.67e-11
	sm=starMass(objects)
	scm=starCenterOfMass(objects)
	scmv=starCenterOfMassVelocity(objects)
	r=objects[0].radius
	while True:																																								#animation continues forever
		if scene.mouse.events:																																				#if a mouse event occurs
			mouse=scene.mouse.getevent()																																	#capture event
			for object in objects:
				if mouse.drag and mouse.pick==object:																														#if a object is clicked on
					while not scene.mouse.clicked:
						object.pos=scene.mouse.pos																															#moves object to drag location until click
		if scene.kb.keys:																																					#capture keystrokes
			k = scene.kb.getkey()																																			#record keystroke
			if k=='a':																																						#'a' for add object
				x=randint(int(1.75*r),int(5.25*r))																															#generates x coordinate
				pos=vector(x,0.,0.)																																			#constructs position vector out of coordinates
				pos=scm+rotate(pos,angle=randint(0,360)*pi/180.,axis=(0,1,0))																									#rotates position vector about the origin
				object=Celestial(randint(1,1e5),randint(5,15),pos,vector(0,0,0),vector(0,0,0),randint(80,120)/100.*pi/7500.,(0,1,0))										#new celestial object created 
				if textures==False:																																			#if textures are not in use, generate solid color
					object.color=choice(colors)
					object.trail_object.color=object.color
				if textures==True:																																			#if textures are in use, generate texture
					object.material=choice(material)
					object.trail_object.color=choice(colors)
				if trails==False:																																			#if trails are not in use, retain no points
					object.retain=0
				object.v=object.centripetalVelocity(objects)*randint(80,120)/100.+scmv																						#sets the object's velocity as 80-120% of its centripetal velocity
				objects.append(object)																																		#adds the object to the list of celestial objects
			if k=='k':																																						#'k' for i'm running out of letters
				pos=vector(20*r,0.,0.)																																		#construct position vector
				pos=scm+rotate(pos,angle=randint(0,360)*pi/180,axis=(0,1,0))																								#rotate the position about the origin
				apoc=Celestial(randint(40,80)/100.*objects[0].m,randint(80,120)/100.*objects[0].d,pos,vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0))	#create apocalyptic space object
				apoc.resetRadius()																																			#adjust radius for density
				if textures==False:																																			#use solid colors if textures are not in use
					apoc.color=choice(colors)
					apoc.trail_object.color=apoc.color
				if textures==True:																																			#use textures if textures are in use
					apoc.material=choice(material)
					apoc.trail_object.color=choice(colors)
				if trails==False:																																			#retain no point in the trail if trail not in use
					apoc.retain=0
				v=-norm(apoc.pos-scm)																																		#normalize the vector between the object and the star
				v=rotate(v,angle=ct*randint(-5,5)*pi/180,axis=(0,1,0))																										#rotate the vector
				apoc.v=.25*ct*v+scmv																																		#only one tenth the magnitude of the unit vector
				objects.append(apoc)																																		#add the object to the list of objects interacting with each other
			if k=='b':																																						#'b' for add star, used to be binary
				rot=0
				x=ct*randint(int(1.5*objects[0].radius),int(2*objects[0].radius))																							#generates x coordinate
				pos=vector(x,0.,0.)																																			#constructs position vector out of coordinates
				star=Celestial(objects[0].m,objects[0].d,vector(0,0,0),vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0),True)
				star.color=objects[0].color
				star.material=objects[0].material
				star.trail_object.color=objects[0].trail_object.color
				star.retain=objects[0].retain
				objects.insert(0,star)																																		#put the new star at the front of the list
				ct+=1
				a=2*pi/ct
				for object in objects:
					if object.st:
						object.retain=0
						object.pos=scm+rotate(pos,angle=rot,axis=(0,1,0))																									#move the stars	
						object.m=sm/ct
						object.resetRadius()
						rot+=a
				sm=starMass(objects)																																		#recalculate the centroid, mass, and velocity of the system
				scm=starCenterOfMass(objects)
				scmv=starCenterOfMassVelocity(objects)
				for object in objects:
					if object.st==True:
						object.v=scmv+object.centripetalVelocity(objects,True,ct)																							#set the new velocities
						if trails:
							object.retain=1000000
				r=mag(objects[0].pos-scm)+objects[0].radius																													#new radius for spawning purposes
			if k=='s':																																						#'s' for subtract object
				if objects[len(objects)-1].st==False:
					remove(objects,objects[len(objects)-1])
			if k=='r':																																						#'r' for reverse animation
				for object in objects:
					object.v=-object.v
					object.ra=-object.ra
			if k=='p':																																						#'p' for pause/play
				running=not running
			if k=='t':																																						#'t' for trails toggle
				trails=not trails																																			#switches the bool
				for object in objects:																																		#walks through the list of objects
					if trails==False:
						object.retain=0																																		#retain no position indices
					if trails:																																				
						object.retain=1000000																																#retain arbitrarily high amount of data points
			if k=='m':																																						#'m' for render objects with material textures
				if objects[0].material!=materials.emissive:
					textures=true
				for object in objects:
					object.color=color.white
					object.material=choice(material)
					if object.st==True:
						object.material=materials.emissive
						object.color=color.yellow
			if k=='c':																																						#'c' for render objects with solid textures
				if objects[0].material==materials.emissive:
					textures=false
				for object in objects:
					object.material=materials.diffuse
					object.color=choice(colors)
					object.trail_object.color=object.color
					if object.st==True:
						object.color=color.yellow
						object.trail_object.color=object.color
		if running:
			for target in objects:																																			#pick an object to calculate vectors for
				for object in objects:																																		#pick an object to use for the vector calculations
					if target!=object:																																		#check against self-gravity
						if collision(objects,target,object)==False:																											#check for collisions	
							target.unitvector=norm(object.pos-target.pos)																									#determine the unit vector between the two objects
							target.acceleration=g*object.m/mag2(object.pos-target.pos)																						#calculate the accleration from newton's law of gravitation
							target.accelerationvector=target.acceleration*target.unitvector																					#determine the accleration vector from the magnitude and the unit vector
							target.a+=target.accelerationvector																												#sum the accelerations due to gravity from each object
						elif object.st and target.st:
							ct-=1
				target.v+=target.a																																			#sum the velocities due to gravity using instananeous acceleration
			for object in objects:
				object.pos+=object.v*dt+.5*object.a*dt**2																													#move the object according the the calculated velocity and acceleration
				object.rotate(angle=dt*object.ra,axis=object.rax)																											#rotate the object
				object.a=vector(0.,0.,0.)																																	#reset the acceleration to zero to allow for recalculation
				if mag(object.pos-scm)>50*r:																																#removes objects that leave the system
					remove(objects,object)
		scm=starCenterOfMass(objects)
		scmv=starCenterOfMassVelocity(objects)
		r=mag(objects[0].pos-scm)+objects[0].radius
		scene.center=scm
		
scene=display(title="Solar System",width=600,height=600,range=1e3,forward=(-1,-1,-1),autoscale=false,ambient=0)
star=Celestial(1e10,1e5,vector(0,0,0),vector(0,0,0),vector(0,0,0),randint(75,125)/100.*pi/7500.,(0,1,0),True)
star.color=color.yellow
star.trail_object.color=star.color
objects=[star]
py_compile.compile('nbodyV1.5.py')
gravitate(objects)