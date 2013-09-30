# Alexander Simes, simes.alex@gmail.com
#
# Usage:
# 	Input is expected to describe a boundary / polygon (List of Vector2)
#		Example: [Vector2(x1, y1), Vector2(x2, y2), etc...]
# 	Output is a surface made of triangles (List of List of Vector2)
# 		Example: [[Vector2(a1x, a1y), Vector2(b1x, b1y), Vector2(c1x, c1y)], etc...]
#
# Tips:
#	If nothing appears your surface normal may be pointing the wrong way
# 	If possible, use clockwise boundaries / polygons to avoid reversing the List
#	If you are certain your boundaries / polygons are clockwise the the first two sections can skipped
#
# Warning:
# 	If your boundary / polygon self intersects the while loop will never terminate

from euclid import *
from math import *

TWOPI = math.pi*2.0

def polyTri(inBoundary):
	copyBoundary = inBoundary[:] # Don't modify inBoundary
	outSurface = []
	
	# Determine if the boundary is clockwise or counterclockwise
	circularDirection = 0.0
	cbLen = len(copyBoundary)-1
	for i in range(cbLen):
		bi = copyBoundary[i]
		bn = copyBoundary[i+1]
		circularDirection += (bn.x-bi.x)*(bn.y+bi.y)
	circularDirection += (copyBoundary[0].x-copyBoundary[cbLen].x)*(copyBoundary[0].y+copyBoundary[cbLen].y)
	
	# Reverse the direction if the boundary is counterclockwise
	if circularDirection < 0.0: copyBoundary.reverse()
	
	index = 0
	while len(copyBoundary) > 2:
		cbLen = len(copyBoundary)
		pIndex = (index+cbLen-1)%cbLen
		nIndex = (index+1)%cbLen
		
		bp = copyBoundary[pIndex]
		bi = copyBoundary[index]
		bn = copyBoundary[nIndex]
		
		# Calculate the interior angle described by bp, bi, and bn
		theta = math.atan2(bi.y-bn.y, bi.x-bn.x)-math.atan2(bi.y-bp.y, bi.x-bp.x)
		if theta < 0.0: theta += TWOPI
		
		# If bp, bi, and bn describe an "ear" of the polygon
		if theta < math.pi:
			inside = False
			
			# Make sure other vertices are not inside the "ear"
			for i in range(cbLen):
				if i == pIndex or i == index or i == nIndex: continue
				
				# Black magic point in triangle expressions
				# http://answers.yahoo.com/question/index?qid=20111103091813AA1jksL
				pi = copyBoundary[i]
				ep = (bi.x-bp.x)*(pi.y-bp.y)-(bi.y-bp.y)*(pi.x-bp.x)
				ei = (bn.x-bi.x)*(pi.y-bi.y)-(bn.y-bi.y)*(pi.x-bi.x)
				en = (bp.x-bn.x)*(pi.y-bn.y)-(bp.y-bn.y)*(pi.x-bn.x)
				
				# This only tests if the point is inside the triangle (no edge / vertex test)
				if (ep < 0 and ei < 0 and en < 0) or (ep > 0 and ei > 0 and en > 0):
					inside = True
					break
			
			# No vertices in the "ear", add a triangle and remove bi
			if not inside:
				outSurface.append([bp, bi, bn])
				copyBoundary.pop(index)
		index = (index+1)%len(copyBoundary)
	return outSurface
