import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc

import datetime
import os
from libs import csv
from libs import encrypt
import getpass
import config
import random

#############################################################################
#DATE/LOCATION
def GetDatePrefix():
    year = int(datetime.datetime.today().strftime('%Y'))-2000
    md = datetime.datetime.today().strftime('%m%d')
    return str(year) + str(md)

def GetNetworkLocation():
    NYPath = r'X:'
    NHPath = r'H:'
    
    
    if os.path.isdir(NYPath):
        location = "New York"
        return 0
    elif os.path.isdir(NHPath):
        location = "New Haven"
        return 1
    else:
        print "Could not find NY or NH network"
        return 
    return "You are connected to the {} network.".format(location)

#############################################################################
#ANALYTICS
def SaveToAnalytics(funcName):
    try:
        fileLocations = config.GetDict()
        filepath = fileLocations['Analytics']
        
        
        #filepath = 'data\Analytics.csv'
        
        with open(filepath, 'rb') as File:
            reader = csv.reader(File)
            data = list(reader)
        
        #Update date
        data[0][1] = 'Last Updated: ' + GetDatePrefix()
        
        #Username
        userName = encrypt.encrypt(getpass.getuser())
        
        #Update Column
        colPos = None
        for i,item in enumerate(data[1]):
            if item == funcName:
                colPos = i
        if colPos is None:
            colPos = len(data[1])
            data[1].append(funcName)
        
        rowPos = None
        for i,item in enumerate(data):
            if item[0] == userName: 
                rowPos = i
        if rowPos is None:
            rowPos = len(data)
            data.append([userName])
        
        newCells = (colPos+1) - len(data[rowPos])
        for i in range(newCells):
            data[rowPos].append('')
        
        try:
            data[rowPos][colPos] = int(data[rowPos][colPos]) + 1
        except:
            data[rowPos][colPos] = 1
        
        myFile = open(filepath, 'wb')
        with myFile:
            csvwriter = csv.writer(myFile)
            csvwriter.writerows(data)
    except:
        print "Analytics failed"

def SaveFunctionData(funcName, funcData):
    """
    SaveFunctionData(funcName, funcData)
    funcName = name of function(str)
    funcData = data to save [list]
    """
    try:
        now=datetime.datetime.now()
        monthString=('%02d%02d'%(now.year, now.month))[2:]
        
        fileLocations = config.GetDict()
        filepath = fileLocations['Data Folder']
        
        fileName = monthString + '_' + funcName + '.csv'
        
        fullName = os.path.join(filepath, fileName)
        
        userName = encrypt.encrypt(getpass.getuser())
        now=datetime.datetime.now()
        timeString=('%02d-%02d-%02d_%02d:%02d:%02d.%d'%(now.year, now.month, now.day, now.hour, now.minute,now.second,now.microsecond))[:-4]
        
        if not os.path.isfile(fullName):
            data = [[funcName],['Date', 'User']]
            myFile = open(fullName, 'wb')
            with myFile:
                csvwriter = csv.writer(myFile)
                csvwriter.writerows(data)    
        
        with open(fullName, 'rb') as File:
            reader = csv.reader(File)
            data = list(reader)
        row = [timeString] + [userName]  + funcData
        data.append(row)
        
        myFile = open(fullName, 'wb')
        with myFile:
            csvwriter = csv.writer(myFile)
            csvwriter.writerows(data)
    except:
        print "SaveFunctionData failed"

#############################################################################
#NUMBERS
def RoundNumber(number, decPlaces):
    """Rounds numbers and adds ',' thousand seperator. Returns string. -1 rounds to 10, 0 leaves no decimals, 1 has one decimal place"""
    if decPlaces < 0:
        result = int(round(number, decPlaces))
        result = "{:,}".format(result)
    else:
        result = format(float(number), ',.'+str(decPlaces)+'f')
    return result

def RemapList(values, newMin, newMax):
    origMin = min(values)
    origMax = max(values)
    OldRange = (origMax - origMin)  
    NewRange = (newMax - newMin)
    newValues = []
    for value in values:
        newValues.append((((value - origMin  ) * NewRange) / OldRange) + newMin)
    return newValues

#############################################################################
#GEOMETRY
def FindMostDistantPointInCurve(obj, resolution = 20):
    """
    Returns the approximately most distant point within a closed curve
    inputs:
        obj (curve): closed planar curves
        resolution (int)[optional]: numbers of sample points in a resolutionXresolution grid
    returns:
        point (point): point furthest from curve
    """
    if rs.IsCurve(obj) == False:
        print "Curves supported only"
        return None
    if rs.IsCurvePlanar(obj) == False:
        print "Curve not planar"
        return None
    if rs.IsCurveClosed(obj) == False:
        print "Curve not closed"
        return None
    
    
    rhobj = rs.coercecurve(obj)
    bbox = rhobj.GetBoundingBox(rs.WorldXYPlane())
    
    minX = bbox.Min[0]
    minY = bbox.Min[1]
    minZ = bbox.Min[2]
    
    maxX = bbox.Max[0]
    maxY = bbox.Max[1]
    maxZ = bbox.Max[2]
    
    xVals = []
    yVals = []
    
    for i in range(resolution):
        xVals.append(i)
        yVals.append(i)
    
    newXvals = RemapList(xVals, minX, maxX)
    newYvals = RemapList(yVals, minY, maxY)
    
    furthestPt = None
    furthestDist = 0
    maxDist = 99999
    for xVal in newXvals:
        for yVal in newYvals:
            newPt = rc.Geometry.Point3d(xVal, yVal, minZ)
            result =  rhobj.Contains(newPt, rs.WorldXYPlane())
            if result == rc.Geometry.PointContainment.Inside:
                param = rhobj.ClosestPoint(newPt, maxDist)
                crvPt = rhobj.PointAt(param[1])
                dist = rs.Distance(crvPt, newPt)
                if dist > furthestDist:
                    furthestPt = newPt
                    furthestDist = dist
    if furthestDist == 0:
        return None
    return furthestPt

def FindMostDistantPointOnSrf(obj, resolution = 20):
    """
    Returns the approximately most distant point within a closed curve
    inputs:
        obj (curve): closed planar curves
        resolution (int)[optional]: numbers of sample points in a resolutionXresolution grid
    returns:
        point (point): point furthest from curve
    """
    #HATCH
    if rs.IsHatch(obj):
        rhobj = rs.coercegeometry(obj)
        boundaryCrvs = []
        crvs = rhobj.Get3dCurves(False)
        for crv in crvs:
            boundaryCrvs.append(crv)
        for crv in rhobj.Get3dCurves(True):
            boundaryCrvs.append(crv)
        obj = sc.doc.Objects.AddBrep(rc.Geometry.Brep.CreatePlanarBreps(boundaryCrvs)[0])
        rhobj = rs.coercesurface(obj)
        brep = rs.coercebrep(obj)
        rs.DeleteObject(obj)
    else:
        rhobj = rs.coercesurface(obj)
        brep = rs.coercebrep(obj)
    edges = brep.Edges
    duplEdgs = [edg.DuplicateCurve() for edg in edges]
    duplEdgs = rc.Geometry.Curve.JoinCurves(duplEdgs)                
    
    uDir = rhobj.Domain(0)
    vDir = rhobj.Domain(1)
    
    uVals = []
    vVals = []
    for i in range(resolution):
        uVals.append(i)
        vVals.append(i)
    
    newUvals = RemapList(uVals, uDir[0], uDir[1])
    newVvals = RemapList(vVals, vDir[0], vDir[1])
    
    furthestPt = None
    furthestDist = 0
    maxDist = 999999
    for uVal in newUvals:
        for vVal in newVvals:
            u = uVal
            v = vVal
            srf_pt = rhobj.PointAt(u,v)
            result = rhobj.IsPointOnFace(u,v) != rc.Geometry.PointFaceRelation.Exterior
            if result:
                thisPtsDistances = []
                for eachEdge in duplEdgs:
                    param = eachEdge.ClosestPoint(srf_pt, maxDist)
                    crvPt = eachEdge.PointAt(param[1])
                    thisPtsDistances.append(rs.Distance(crvPt, srf_pt))
                
                dist = min(thisPtsDistances)
                if dist > furthestDist:
                    furthestPt = srf_pt
                    furthestDist = dist
    if furthestDist == 0:
        return None
    return furthestPt

def FindMostDistantPointRand(obj, resolution = 20):
    """
    Returns the approximately most distant point within a closed curve
    inputs:
        obj (curve): closed planar curves
        resolution (int)[optional]: numbers of sample points in a resolutionXresolution grid
    returns:
        point (point): point furthest from curve
    """
    if rs.IsCurvePlanar(obj) == False:
        print "Curve not planar"
        return None
    if rs.IsCurveClosed(obj) == False:
        print "Curve not closed"
        return None
    
    rhobj = rs.coercecurve(obj)
    bbox = rhobj.GetBoundingBox(rs.WorldXYPlane())
    
    minX = bbox.Min[0]
    minY = bbox.Min[1]
    minZ = bbox.Min[2]
    
    maxX = bbox.Max[0]
    maxY = bbox.Max[1]
    maxZ = bbox.Max[2]
    
    #########################
    xVals = []
    yVals = []
    
    random.seed(1)
    for i in range(resolution):
        xVals.append(random.uniform(0,1))
        yVals.append(random.uniform(0,1))
    
    newXvals = RemapList(xVals, minX, maxX)
    newYvals = RemapList(yVals, minY, maxY)
    
    furthestPt = None
    furthestDist = 0
    maxDist = 99999
    for xVal in newXvals:
        for yVal in newYvals:
            newPt = rc.Geometry.Point3d(xVal, yVal, minZ)
            result =  rhobj.Contains(newPt, rs.WorldXYPlane())
            if result == rc.Geometry.PointContainment.Inside:
                param = rhobj.ClosestPoint(newPt, maxDist)
                crvPt = rhobj.PointAt(param[1])
                dist = rs.Distance(crvPt, newPt)
                if dist > furthestDist:
                    furthestPt = newPt
                    furthestDist = dist
    if furthestDist == 0:
        return None
    return furthestPt

def IsRectangle(obj):
    """
    Checks if a curve is a rectangle. Must be closed, planar, 4 line segments, all 90 degrees. Uses UnitAngleTolerance
    inputs:
        obj (curve): curve to evaluate
    returns (list):
        [0] (Boolean): If rectangle
        [1] (String): explaination of why it failed
    """
    explaination = ''
    tol = rs.UnitAngleTolerance()
    rhobj = rs.coercecurve(obj)
    if rs.IsCurveClosed(obj):
        if rs.IsCurvePlanar(obj):
            segments = rhobj.DuplicateSegments()
            if len(segments) == 4:
                for segment in segments:
                    if segment.Degree != 1:
                        explaination = "Not all segments are lines"
                        return [False, explaination]
                for i in range(3):
                    angle = rs.Angle2(segments[i], segments[i+1])
                    dist1 = abs(abs(180 - angle[0])-90)
                    dist2 = abs(abs(180 - angle[1])-90)
                    if dist1 > tol or dist2 > tol:
                        explaination = "Angle not 90"
                        return [False, explaination]
                angle = rs.Angle2(segments[-1], segments[0])
                dist1 = abs(abs(180 - angle[0])-90)
                dist2 = abs(abs(180 - angle[1])-90)
                if dist1 > tol or dist2 > tol:
                    explaination = "Final angle not 90"
                    return [False, explaination]
                explaination = "ITS A RECTANGLE"
                return [True, explaination]
            else:
                explaination = "Curve does not have 4 sides"
                return [False, explaination]
        else:
            explaination = "Curve not planar"
            return [False, explaination]
    else:
        explaination = "Curve not closed"
        return [False, explaination]

def GetUphillVectorFromPlane(obj, u = 0, v = 0):
    """Gets the uphill vector from a surface, with optional u, v
    Parameters:
      surface (surface): surface to test
      u (float)[optional]: u parameter
      v (float)[optional]: v parameter
    Returns:
      vector(guid, ...): identifiers of surfaces created on success
    """
    rhobj = rs.coercesurface(obj)
    frame = rhobj.FrameAt(u,v)[1]
    pt0 = rhobj.PointAt(u,v)
    pt1 = rc.Geometry.Point3d.Add(pt0, rc.Geometry.Vector3d(0,0,10))
    projPoint = frame.ClosestPoint(pt1)
    vec = rs.VectorCreate(projPoint, pt0)
    if rs.VectorLength(vec) < rs.UnitAbsoluteTolerance():
        uphillVec = rc.Geometry.Vector3d(0,0,1)
    else:
        uphillVec = rs.VectorUnitize(vec)
    return uphillVec

#############################################################################
#STRINGS
def StringPlusOne(word):
    """Adds one to the last numbers in a string.
    Parameters:
      word (str): String to process.
    Returns:
      word(str): String thats been iterated
    """
    try:
        suffixNumber = ''
        splitIndex = 0
        for i, l in enumerate(word[::-1]):
            try:
                int(l)
                suffixNumber += l
            except:
                splitIndex = i
                break
        suffixNumber = suffixNumber[::-1]
        if len(suffixNumber) < 1:
            return word
        newNum = int(suffixNumber)+1
        finalNum = (len(suffixNumber)-len(str(newNum)))*'0' + str(newNum)
        return word[:len(word)-splitIndex] + finalNum
    except:
        print "StringPlusOne Error"
        return None

def UpdateString(word):
    try:
        prefix = word[:6]
        int(prefix)
        curDate = GetDatePrefix()
        if prefix == curDate:
            return StringPlusOne(word)
        else:
            return  curDate + word[6:]
    except:
        return StringPlusOne(word)

if __name__ == "__main__":
    obj = rs.GetObject()
    print GetUphillVectorFromPlane(obj)
    pass
