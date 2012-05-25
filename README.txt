      ___           ___           ___           ___                   
     /  /\         /  /\         /  /\         /  /\          __      
    /  /::|       /  /::\       /  /::\       /  /::\        |  |\    
   /  /:|:|      /  /:/\:\     /  /:/\:\     /  /:/\:\       |  |:|   
  /  /:/|:|__   /  /::\ \:\   /  /:/  \:\   /  /:/  \:\      |  |:|   
 /__/:/ |:| /\ /__/:/\:\_\:| /__/:/ \__\:\ /__/:/ \__\:|     |__|:|__ 
 \__\/  |:|/:/ \  \:\ \:\/:/ \  \:\ /  /:/ \  \:\ /  /:/     /  /::::\
     |  |:/:/   \  \:\_\::/   \  \:\  /:/   \  \:\  /:/     /  /:/~~~~
     |__|::/     \  \:\/:/     \  \:\/:/     \  \:\/:/     /__/:/     
     /__/:/       \__\::/       \  \::/       \__\::/      \__\/      
     \__\/            ~~         \__\/            ~~                  
	 
	 
Nick Walker
Current Version: 1.3

This script simulates the interaction of celestial objects in an n-body system.
	
Requirements:
	VPython visual library
		Download at: http://vpython.org/
		
Working Components:
	Gravitation between multiple objects
	Collisions
	Rotation
	Trail mapping
	Color changing
	Trajectory reversal
	Pause/Play functionality
	Material switching
	Mass manipulation of star
	Add/Subtract celestial bodies
	Add/Subtract massive meteors
	Drag and Drop celestial objects
	Camera centers on star
	
Execution:
	Run the script and use the commands detailed in the console window
	
Controls:
	a: add planet
	s: remove the last added object, does not remove star
	k: add meteor, incredibly massive, can knock star out of place
	u: increase mass of star
	d: decrease mass of star
	r: reverse the orbits of the planets, essentially, everything rrelated to motion is negated
	t: toggle whether trails are shown or not
	p: pause/play the simulation
	m: toggle whether or not objects use textures
	c: enable or change solid color appearance of objects
	b: enable binary star system
	v: change viewpoint between first object and center of mass
	You can also click on objects to reposition them, click again to release
	The object retains its velocity