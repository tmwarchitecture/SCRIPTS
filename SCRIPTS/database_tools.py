#Read from YAML database
import os
from libs import yaml

root = os.path.dirname(os.path.realpath(__file__))
yamlPath = os.path.join(root, "data\Database_Template.yaml")

def GetDatabaseTemplate():
    '''
    Gets the yaml databse template
    Input: None
    Returns: Dictionary of yaml file on success
    '''
    try:
        with open(yamlPath, 'r') as fileDescriptor:
            databaseTemplate = yaml.load(fileDescriptor)
        return databaseTemplate
    except:
        return None

def SaveDatabase(data, databaseFile):
    '''
    Saves data from dictionary to a yaml file
    Input:
        data - dictionary
        databaseFile - path to folder to save file
        versionName - Filename for the yaml file
    Returns: "Done" on Success
    '''
    try:
        stream = file(databaseFile, 'w')
        yaml.safe_dump(data, stream, default_flow_style=False)
        return "DONE"
    except:
        return "ERROR"

def SaveProjectLevelData(data, oldDatabaseFile, newDatabaseFile, bldgNum):
    existingData = GetProjectDatabase(oldDatabaseFile)
    
    for row in data:
        #Name
        existingData['building'][int(bldgNum)]['level'][row[0]]['name'] = row[1]
        #Func
        existingData['building'][int(bldgNum)]['level'][row[0]]['functions'] = row[2]
        #FTF
        existingData['building'][int(bldgNum)]['level'][row[0]]['ftf'] = row[3]
        # Z
        existingData['building'][int(bldgNum)]['level'][row[0]]['z'] = row[4]
    
    SaveDatabase(existingData, newDatabaseFile)
    print "{} saved".format(newDatabaseFile)

def GetProjectDatabase(databaseFile):
    '''
    Gets the yaml project databse
    Input:
        databaseFile - path to the database
        versionName - name for the yaml file (e.g. 180426_Database.yaml)
    Returns: Dictionary of yaml file on success
    '''
    try:
        with open(databaseFile, 'r') as fileDescriptor:
            databaseTemplate = yaml.load(fileDescriptor)
        return databaseTemplate
    except:
        return None

def GetProjectLevelData(databaseFile, bldgNum):
    data = GetProjectDatabase(databaseFile)
    levels = []
    try:
        levelData = data['building'][int(bldgNum)]['level']
    except:
        return None
    
    for key in levelData.keys():
        levels.append([key, levelData[key]['name'], levelData[key]['functions'], levelData[key]['ftf'], levelData[key]['z']])
    return levels

if __name__ == "__main__":
    
    #data = GetDatabaseTemplate()
    #data['project']['name'] = "TEst"
    #path = r'C:\Users\twilliams\Desktop\TEMP\Database'
    #print SaveDatabase(data, path, 'Project_Info.yaml')
    
    path = r'C:\Users\twilliams\Desktop\TEMP\Database'
    GetProjectLevels(path, 'Project_Info.yaml')
    