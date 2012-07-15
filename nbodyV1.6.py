#Nick Walker	15/7/2012	N-Body

from visual import *
from random import *
import py_compile

py_compile.compile('nbodyV1.6.py')

scene=display(title="Solar System",width=600,height=600,range=1e3,forward=(-1,-1,-1),autoscale=false,ambient=0)
g=6.67e-11
dt=1.
ct=1.
running=False
trails=True
textures=False
material=[materials.wood,materials.marble,materials.BlueMarble,materials.rough]
colors=[color.orange,color.blue,color.green,color.magenta,color.red,color.cyan,color.yellow]

starmass=[float(1e10)]
stardensity=[float(1e5)]
starposition=[vector(0.,0.,0.)]
starmomentum=[vector(0.,0.,0.)]
starrotation=[pi/7500]
starstatus=[True]
objects=[sphere(radius=sqrt(starmass[0]*3/4/stardensity[0]/pi),pos=starposition[0],make_trail=True,interval=10,color=color.yellow)]
objects[0].trail_object.color=color.yellow
r=objects[0].radius
starradius=[objects[0].radius]

mass=array(starmass)
density=array(stardensity)
position=array(starposition)
momentum=array(starmomentum)
rotation=array(starrotation)
status=array(starstatus)
radius=array(starradius)

totalmass=1e10
centerofmass=vector(0.,0.,0.)
centerofmassvelocity=vector(0.,0.,0.)

while 1:
	if running:
		displacement=position-position[:,newaxis]
		
		for n in range(mass.__len__()):
			displacement[n,n]=1e6
			
		displacementmag=sqrt(sum(square(displacement),-1))
		collision=less_equal(displacementmag,radius+radius[:,newaxis])
		collisionlist=sort(nonzero(collision.flat)[0]).tolist()
		force=g*mass*mass[:,newaxis]*displacement/displacementmag[:,:,newaxis]**3
		
		for n in range(mass.__len__()):
			force[n,n]=0.
		
		momentum+=sum(force,1)*dt
		position+=(momentum/mass)*dt
		
		for n in range(mass.__len__()):
			objects[n].pos=position[n]
			objects[n].rotate(angle=rotation[n],axis=(0,1,0))
			
		totalmass=0.
		for n in range(mass.__len__()):
			if status[n]:
				totalmass+=mass[n]
		
		centerofmass=vector(0.,0.,0.)
		for n in range (mass.__len__()):
			if status[n]:
				centerofmass+=mass[n]*position[n]
		centerofmass=centerofmass/totalmass
			
		centerofmassvelocity=vector(0.,0.,0.)
		for n in range(mass.__len__()):
			if status[n]:
				centerofmassvelocity+=momentum[n]
		centerofmassvelocity=centerofmassvelocity/totalmass
			
		########Modify for deletion rather than hiding########
		for ij in collisionlist:
			i,j=divmod(ij,len(objects))
			if not objects[i].visible: continue
			if not objects[j].visible: continue
			newposition=(position[i]*mass[i,0]+position[j]*mass[j,0])/(mass[i,0]+mass[j,0])
			newmass=mass[i,0]+mass[j,0]
			newdensity=(mass[i,0]*density[i,0]+mass[j,0]*density[j,0])/(mass[i,0]+mass[j,0])
			newmomentum=momentum[i]+momentum[j]
			newradius=sqrt(newmass*3/4/newdensity/pi)
			iset,jset=i,j
			if mass[j]>mass[i]:
				iset,jset=j,i
			objects[iset].radius=newradius
			mass[iset,0]=newmass
			position[iset]=newposition
			momentum[iset]=newmomentum
			radius[iset]=newradius
			objects[jset].trail_object.visible=False
			objects[jset].visible=0
			momentum[jset]=vector(0,0,0)
			mass[jset,0]=1e-30
			position[jset]=rotate((randint(1e25,1e30),0,0),angle=randint(0,360)*pi/180,axis=(0,1,0))
			if status[jset]:
				ct-=1
		
		r=ct**2*objects[0].radius
		scene.center=centerofmass
	
	if scene.mouse.events:
		mouse=scene.mouse.getevent()
		for n in range(len(objects)):
			if mouse.drag and mouse.pick==objects[n]:
				while not scene.mouse.clicked:
					objects[n].pos=scene.mouse.pos
					position[n]=scene.mouse.pos
					
	if scene.kb.keys:
		k = scene.kb.getkey()
		
		if k=='p':
			running=not running
		
		if k=='t':
			trails=not trails
			for object in objects:
				if trails==False:
					object.retain=0
				if trails:																																				
					object.retain=1000000
		
		if k=='m':
			if objects[0].material!=materials.emissive:
				textures=true
			for n in range(len(objects)):
				objects[n].color=color.white
				objects[n].material=choice(material)
				if status[n]:
					objects[n].material=materials.emissive
					objects[n].color=color.yellow
					
		if k=='c':
			if objects[0].material==materials.emissive:
				textures=false
			for n in range(len(objects)):
				objects[n].material=materials.diffuse
				objects[n].color=choice(colors)
				objects[n].trail_object.color=objects[n].color
				if status[n]:
					objects[n].color=color.yellow
					objects[n].trail_object.color=objects[n].color
					
		if k=='r':
			for n in range(momentum.__len__()):
				momentum[n]=-momentum[n]
				
		if k=='s':
			if not status[status.__len__()-1]:
				mass=resize(mass,(len(mass)-1,1))
				density=resize(density,(len(density)-1,1))
				position=resize(position,(len(position)-1,3))
				momentum=resize(momentum,(len(momentum)-1,3))
				status=resize(status,(len(status)-1,1))
				radius=resize(radius,(len(radius)-1,1))
				radius=radius.ravel()
				temp=objects[len(objects)-1]
				temp.trail_object.visible=False
				temp.visible=False
				objects.remove(temp)
				del temp
				dt-=.5
		
		if k=='b':
			mass=resize(mass,(len(mass)+1,1))
			density=resize(density,(len(density)+1,1))
			position=resize(position,(len(position)+1,3))
			momentum=resize(momentum,(len(momentum)+1,3))
			rotation=resize(rotation,(len(rotation)+1,1))
			status=resize(status,(len(status)+1,1))
			radius=resize(radius,(len(radius)+1,1))
			rot=0.
			nposition=vector(ct*randint(int(1.5*r),int(2*r)),0.,0.)
			mass[len(mass)-1]=1e10
			density[len(density)-1]=1e5
			rotation[len(density)-1]=pi/7500
			status[len(status)-1]=True
			objects.append(sphere(radius=objects[0].radius,pos=objects[0].pos,make_trail=True,interval=10,color=objects[0].color))
			objects[len(objects)-1].trail_object.color=objects[len(objects)-1].color
			radius[len(radius)-1]=objects[len(objects)-1].radius
			radius=radius.ravel()
			ct+=1
			a=2*pi/ct
			m=1e10*(.1636*log(ct)+.0124)
			for n in range(len(objects)):
				if status[n]:
					objects[n].retain=0
					mass[n]=1e10/ct
					position[n]=rotate(nposition,angle=rot,axis=(0,1,0))
					velocity=sqrt(g*m/mag(position[n]-centerofmass))*rotate(norm(position[n]-centerofmass),angle=pi/2,axis=(0,1,0))+centerofmassvelocity
					momentum[n]=mass[n]*velocity
					objects[n].radius=sqrt((mass[n]*3/4/density[n]/pi))
					if trails:
						objects[n].retain=1000000
					rot+=a
			dt+=.5
					
		if k=='k':
			mass=resize(mass,(len(mass)+1,1))
			density=resize(density,(len(density)+1,1))
			position=resize(position,(len(position)+1,3))
			momentum=resize(momentum,(len(momentum)+1,3))
			rotation=resize(rotation,(len(rotation)+1,1))
			status=resize(status,(len(status)+1,1))
			radius=resize(radius,(len(radius)+1,1))
			nposition=rotate(vector(20*r,0.,0.),angle=randint(0,360)*pi/180,axis=(0,1,0))+centerofmass
			mass[len(mass)-1]=randint(1e4,1e8)
			density[len(density)-1]=randint(1e3,1e4)
			position[len(position)-1]=nposition
			velocity=randint(80,120)/100.*.25*ct*rotate(-norm(nposition-centerofmass),angle=ct*randint(-5,5)*pi/180,axis=(0,1,0))
			momentum[len(momentum)-1]=mass[len(mass)-1]*velocity
			rotation[len(rotation)-1]=randint(80,120)/100.*pi/7500
			status[len(status)-1]=False
			objects.append(sphere(radius=sqrt((mass[mass.__len__()-1]*3/4/density[density.__len__()-1]/pi)),pos=position[position.__len__()-1],make_trail=True,interval=10))
			radius[len(radius)-1]=objects[len(objects)-1].radius
			radius=radius.ravel()
			if not textures:
				objects[len(objects)-1].color=choice(colors)
				objects[len(objects)-1].trail_object.color=objects[len(objects)-1].color
			if textures:
				objects[len(objects)-1].color=color.white
				objects[len(objects)-1].material=choice(material)
			if not trails:
				objects[len(objects)-1].retain=0
			dt+=.5
		
		if k=='a':
			mass=resize(mass,(len(mass)+1,1))
			density=resize(density,(len(density)+1,1))
			position=resize(position,(len(position)+1,3))
			momentum=resize(momentum,(len(momentum)+1,3))
			rotation=resize(rotation,(len(rotation)+1,1))
			status=resize(status,(len(status)+1,1))
			radius=resize(radius,(len(radius)+1,1))
			x=randint(2*int(r),8*int(r))
			nposition=rotate(vector(x,0.,0.),angle=randint(0,360)*pi/180.,axis=(0,1,0))+centerofmass
			mass[len(mass)-1]=randint(1,1e5)
			density[len(density)-1]=randint(5,15)
			position[len(position)-1]=nposition
			velocity=randint(80,120)/100.*sqrt(g*ct*mass[0]/mag(nposition-centerofmass))*rotate(norm(nposition-centerofmass),angle=pi/2,axis=(0,1,0))+centerofmassvelocity
			momentum[len(momentum)-1]=mass[len(mass)-1]*velocity
			rotation[len(rotation)-1]=randint(80,120)/100.*pi/7500
			status[len(status)-1]=False
			objects.append(sphere(radius=sqrt((mass[mass.__len__()-1]*3/4/density[density.__len__()-1]/pi)),pos=position[position.__len__()-1],make_trail=True,interval=10))
			radius[len(radius)-1]=objects[len(objects)-1].radius
			radius=radius.ravel()
			if not textures:
				objects[len(objects)-1].color=choice(colors)
				objects[len(objects)-1].trail_object.color=objects[len(objects)-1].color
			if textures:
				objects[len(objects)-1].color=color.white
				objects[len(objects)-1].material=choice(material)
			if not trails:
				objects[len(objects)-1].retain=0
			dt+=.5