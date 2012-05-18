#Nick Walker
from visual import *
from random import *
class celestial(sphere):
	def __init__(self,radius=1e5,mass=1e20,density=100,position=vector(0.,0.,0.),velocity=vector(0.,0.,0.),acceleration=vector(0.,0.,0.),rotangle=pi/7500,rotaxis=(0,1,0)):
		self._r=radius
		self._m=mass
		self._d=density
		self._p=position
		self._v=velocity
		self._a=acceleration
		self._ra=rotangle
		self._rax=rotaxis
		sphere.__init__(self,radius=self._r,pos=self._p,make_trail=True,interval=10)
	def getmass(self):
		return self._m
	def setmass(self,mass):
		self._m=mass
	def getdensity(self):
		return self._d
	def setdensity(self,density):
		self._d=density
	def getvelocity(self):
		return self._v
	def setvelocity(self,velocity):
		self._v=velocity
	def getacceleration(self):
		return self._a
	def setacceleration(self,acceleration):
		self._a=acceleration
	def getrotangle(self):
		return self._ra
	def setrotangle(self,angle):
		self._ra=angle
	def getrotaxis(self):
		return self._rax
	def setrotaxis(self,axis):
		self._rax=axis
	def centripetalvelocity(self,target):
		G=6.67e-11
		v=sqrt(G*target.getmass()/mag(self.pos-target.pos))
		uv=norm(self.pos-target.pos)
		d=rotate(uv,angle=pi/2,axis=(0,1,0))
		return v*d
def remove(bodies,body,dt):
	body.trail_object.visible=False
	body.visible=False
	if bodies.count(body)==1:
		bodies.remove(body)
	del body
	dt-=1
	return dt
def collision(bodies,body1,body2,dt):
	collision=False
	if mag(body1.pos-body2.pos)<body1.radius+body2.radius:
		collision=True
	if collision==True:
		if body1.getmass()>=body2.getmass():
			body1.radius=(body1.radius**3+body2.radius**3)**(1./3.)
			body1.setvelocity((body1.getmass()*body1.getvelocity()+body2.getmass()*body2.getvelocity())/(body1.getmass()+body2.getmass()))
			body1.setmass(body1.getmass()+body2.getmass())
			remove(bodies,body2,dt)
		else:
			body2.radius=(body1.radius**3+body2.radius**3)**(1./3.)
			body2.setvelocity((body1.getmass()*body1.getvelocity()+body2.getmass()*body2.getvelocity())/(body1.getmass()+body2.getmass()))
			body2.setmass(body1.getmass()+body2.getmass())
			remove(bodies,body1,dt)
	return collision
def newton(bodies,dt):
	G=6.67e-11
	running=False
	texture=False
	trails=True
	material=[materials.wood,materials.marble,materials.BlueMarble,materials.rough]
	colors=[color.orange,color.blue,color.green,color.magenta,color.red,color.cyan,color.yellow]
	print 't: toggle trails'+'\n'+'p: pause/play'+'\n'+'m: toggle materials'+'\n'+'c: toggle colors'+'\n'+'a: add planet'+'\n'+'s: subtract planet'+'\n'+'r: reverse orbits'+'\n'+'u: increase mass of star'+'\n'+'d: decrease mass of star'
	while True:
		if scene.kb.keys:
			k = scene.kb.getkey()
			if k=='t':
				trails=not trails
				for planet in bodies:
					if trails==False:
						planet.retain=0
					if trails==True:
						planet.retain=1000000
			if k=='p':
				running=not running
			if k=='m':
				if bodies[1].color!=color.white:
					texture=not texture
				for planet in bodies:
					planet.color=color.white
					planet.material=choice(material)
				bodies[0].color=color.yellow
				bodies[0].material=materials.emissive
			if k=='c':
				if bodies[1].color==color.white:
					texture=not texture
				for planet in bodies:
					planet.material=materials.diffuse
					planet.color=choice(colors)
					planet.trail_object.color=planet.color
				bodies[0].material=materials.emissive
				bodies[0].color=color.yellow
			if k=='a':
				x=randint(int(-8*bodies[0].radius),int(8*bodies[0].radius))
				z=randint(int(-8*bodies[0].radius),int(8*bodies[0].radius))
				while x<2*bodies[0].radius and x>-2*bodies[0].radius and z<2*bodies[0].radius and z>-2*bodies[0].radius:
					x=randint(int(-8*bodies[0].radius),int(8*bodies[0].radius))
					z=randint(int(-8*bodies[0].radius),int(8*bodies[0].radius))
				planet=celestial(1,randint(1e5,1e10),100,vector(x,0,z),vector(0,0,0),vector(0,0,0),rotangle=randint(75,125)/100.*pi/7500.,rotaxis=(0,1,0))
				planet.radius=sqrt((planet.getmass()*3/4/planet.getdensity()/pi))
				if texture==False:
					planet.color=choice(colors)
					planet.trail_object.color=planet.color
				if texture==True:
					planet.material=choice(material)
					planet.trail_object.color=choice(colors)
				if trails==False:
					planet.retain=0
				planet.setvelocity(planet.centripetalvelocity(star)*randint(75,125)/100)
				bodies.append(planet)
				dt+=1
			if k=='s':
				if len(bodies)>1:
					dt=remove(bodies,bodies[len(bodies)-1],dt)
			if k=='r':
				for planet in bodies:
					planet.setvelocity(-1*planet.getvelocity())
					planet.setrotangle(-1*planet.getrotangle())
			if k=='u':
				bodies[0].setmass(bodies[0].getmass()+5e14)
			if k=='d':
				bodies[0].setmass(bodies[0].getmass()-5e14)
		if running:
			for target in bodies:
				for object in bodies:
					if target!=object:
						if collision(bodies,target,object,dt)==true:
							dt-=1
						else:
							target.unitvector=norm(object.pos-target.pos)
							target.acceleration=G*object.getmass()/mag2(object.pos-target.pos)
							target.accelerationvector=target.acceleration*target.unitvector
							target.setacceleration(target.getacceleration()+target.accelerationvector)
							target.setvelocity(target.getvelocity()+target.getacceleration())
			for planet in bodies:
				planet.pos+=planet.getvelocity()*dt+.5*planet.getacceleration()*dt**2
				planet.rotate(angle=dt*planet.getrotangle(),axis=planet.getrotaxis())
				planet.setacceleration(vector(0.,0.,0.))
scene = display(title="Solar System",width=600,height=600,range=2e5,forward=(-1,-1,-1),autoscale=false,ambient=0)
star=celestial(1e4,1e15,100)
#star.radius=sqrt((star.getmass()*3/4/star.getdensity()/pi))
star.color=color.yellow
star.material=materials.emissive
#light=local_light(pos=(0,0,0),color=color.yellow)
bodies=[star]
newton(bodies,0)