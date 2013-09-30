from math import *
from euclid import *
from random import *
from omega import *
from cyclops import *
from polyTri import *

# Make an arbitrary boundary / polygon (not self intersecting)
boundary = []
theta = 0
for i in range(50):
	randRadius = random()+1.0
	boundary.append(Vector2(math.cos(theta)*randRadius, math.sin(theta)*randRadius))
	theta += (math.pi*2.0)/50

# Create a surface using the boundary
surface = polyTri(boundary)

# Create a model using the surface
mg = ModelGeometry.create("Surface")
for i in range(len(surface)):
	mg.addVertex(Vector3(surface[i][0].x, surface[i][0].y, 0.0))
	mg.addVertex(Vector3(surface[i][2].x, surface[i][2].y, 0.0)) # Order reversed for normals
	mg.addVertex(Vector3(surface[i][1].x, surface[i][1].y, 0.0)) # Order reversed for normals
mg.addPrimitive(PrimitiveType.Triangles, 0, len(surface)*3)
getSceneManager().addModel(mg)

# Create a surface object
so = StaticObject.create("Surface")
so.setPosition(Vector3(0.0, 2.0, -10.0))
so.setEffect("colored -e #ff0000")
#so.setEffect("colored -e #ff0000 -w") # Use this to see what is going on
