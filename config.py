fileLocationsHOME = {
'Template File' : r'X:\05_RHINO STANDARDS\PCPA.3dm',
'Template Folder' : r'X:\05_RHINO STANDARDS',
'ACAD Scheme Folder' : r'X:\05_RHINO STANDARDS\01 GENERAL SETTINGS\ACAD_Schemes',
'Display Mode Folder' : r'X:\05_RHINO STANDARDS\02 DISPLAY SETTINGS\2018 Display Modes',
'PCPA GH Components' : r'X:\05_RHINO STANDARDS\04 GRASSHOPPER\03_Install+Plugins\PCPA\V.01.02',
'Analytics' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON\Analytics.csv',
'FunctionCounter.py' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON',
'PCPA_Layers' : r'C:\Users\Tim\Desktop\temp\template\PCPA LAYERS.csv',
'CSV' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON\dependencies\csv.py'
}

fileLocationsPCPNY = {
'Template File' : r'X:\05_RHINO STANDARDS\PCPA.3dm',
'Template Folder' : r'X:\05_RHINO STANDARDS',
'ACAD Scheme Folder' : r'X:\05_RHINO STANDARDS\01 GENERAL SETTINGS\ACAD_Schemes',
'Display Mode Folder' : r'X:\05_RHINO STANDARDS\02 DISPLAY SETTINGS\2018 Display Modes',
'PCPA GH Components' : r'X:\05_RHINO STANDARDS\04 GRASSHOPPER\03_Install+Plugins\PCPA\PCPA_GH_TOOLBAR',
'Analytics' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON\Analytics.csv',
'FunctionCounter.py' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON',
'PCPA_Layers' : r'X:\05_RHINO STANDARDS\01 GENERAL SETTINGS\PCPA LAYERS\PCPA LAYERS.csv',
'CSV' : r'X:\05_RHINO STANDARDS\05 SCRIPTS\PYTHON\dependencies\csv.py'
}

def GetDict():
    return fileLocationsPCPNY 

def GetValue(key):
    return fileLocationsPCPNY [key]
