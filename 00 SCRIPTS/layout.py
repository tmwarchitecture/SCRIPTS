import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import os.path
import layers
import config
import utils

__author__ = 'Tim Williams'
__version__ = "2.2.0"

def AddTitleBlock(size):
    filelocations = config.GetDict()
    rs.EnableRedraw(False)
    if size == 11:
        offset = .354
        row1 = offset
        row2 = row1*2
        row3 = row1*3
        row4 = row1*4
        leftEdge = offset
        middle = 17/2
        rightEdge = 17-offset

        pt1 = [leftEdge, row4]
        pt2 = [rightEdge, 11-row1]
        txtBase1 = [middle,row2]
        txtBase2 = [leftEdge,row2]
        txtBase3 = [rightEdge,row2]
        txtBase4 = [leftEdge,row1]
        txtBase5 = [rightEdge,row1]

        lineSt = [leftEdge, row3]
        lineEnd = [rightEdge, row3]

        txtSizeL = .125
        txtSizeM = .094

        logoPlane = [13.834,.247,0]
        logoWidth = 2.823
        logoHeight = .116

    elif size == 8:
        offset = .229
        row1 = offset
        row2 = row1*2
        row3 = row1*3
        row4 = row1*4
        leftEdge = offset
        middle = 11/2
        rightEdge = 11-offset

        pt1 = [leftEdge, row4]
        pt2 = [rightEdge, 8.5-row1]
        txtBase1 = [middle,row2]
        txtBase2 = [leftEdge,row2]
        txtBase3 = [rightEdge,row2]
        txtBase4 = [leftEdge,row1]
        txtBase5 = [rightEdge,row1]

        lineSt = [leftEdge, row3]
        lineEnd = [rightEdge, row3]

        txtSizeL = .125
        txtSizeM = .063

        logoPlane = [8.347,.157,0]
        logoWidth = 2.434
        logoHeight = .100

    elif size == 18:
        offset = .5
        row1 = offset
        row2 = row1*2
        row3 = row1*3
        row4 = row1*4
        leftEdge = offset
        middle = 24/2
        rightEdge = 24-offset

        pt1 = [leftEdge, row4]
        pt2 = [rightEdge, 18-row1]
        txtBase1 = [middle,row2]
        txtBase2 = [leftEdge,row2]
        txtBase3 = [rightEdge,row2]
        txtBase4 = [leftEdge,row1]
        txtBase5 = [rightEdge,row1]

        lineSt = [leftEdge, row3]
        lineEnd = [rightEdge, row3]

        txtSizeL = .250
        txtSizeM = .125

        logoPlane = [19.627,.367,0]
        logoWidth = 3.885
        logoHeight = .160



    layout = sc.doc.Views.GetPageViews()[-1]
    if layout is None:  return

    sc.doc.Views.ActiveView = layout

    if rs.GetDocumentData(section = "PCPA", entry = "Project_Name") is None:
        rs.SetDocumentData(section = "PCPA", entry = "Project_Name", value = "PROJECT TITLE")
    projectTitle = '%<DocumentText("PCPA\Project_Name")>%'

    if rs.GetDocumentData(section = "PCPA", entry = "Client_Name") is None:
        rs.SetDocumentData(section = "PCPA", entry = "Client_Name", value = "Client Name")
    clientName = '%<DocumentText("PCPA\Client_Name")>%'

    #Add text
    textList = []
    textList.append(rs.AddText("Title", txtBase1, txtSizeL, justification = 2))
    textList.append(rs.AddText(projectTitle, txtBase2, txtSizeL, justification = 1))
    textList.append(rs.AddText('%<Date("MMMM d, yyyy")>%', txtBase3, txtSizeM, justification = 4))

    textList.append(rs.AddText(clientName, txtBase4, txtSizeM, justification = 1))


    #ADD Copyright
    copyright = 'COPYRIGHT ' + u"\u00a9" + ' %<Date("yyyy")>%'
    copyrightText = rs.AddText(copyright, txtBase5, txtSizeM, justification = 4)

    #ADD Pelli Clarke Pelli
    pcp = 'Pelli Clarke Pelli'
    pcpText = rs.AddText(pcp, txtBase5, txtSizeM, justification = 4)
    if rs.IsDimStyle('PCPA_10'):
        dimstyleID = sc.doc.DimStyles.FindName('PCPA_14')

    ##############
    #Just trying to change the dim style here
    #pcpRhobj = rs.coercerhinoobject(pcpText)
    #test = pcpRhobj.Attributes
    #pcpRhobj.CommitChanges()
    ##############

    #ADD Architects
    architects = 'Architects'
    architectsText = rs.AddText(architects, txtBase5, txtSizeM, justification = 4)

    #Horizontal line
    line = rs.AddLine(lineSt, lineEnd)

    #Add detail
    detail = rs.AddDetail(layout.ActiveViewportID, pt1, pt2, "PCPA " + str(layout.PageName), 7)

    #Change layers AddLayerByNumber
    try:
        rs.ObjectLayer(line, layers.GetLayerNameByNumber(8204))
    except:
        pass
    try:
        rs.ObjectLayer(detail, layers.GetLayerNameByNumber(8106))
    except:
        pass
    try:
        for eachText in textList:
            rs.ObjectLayer(eachText, layers.GetLayerNameByNumber(8105))
    except:
        pass
    try:
        rs.ObjectLayer(copyrightText, layers.GetLayerNameByNumber(8211))
    except:
        pass
    try:
        rs.ObjectLayer(pcpText, layers.GetLayerNameByNumber(8210))
    except:
        pass
    try:
        rs.ObjectLayer(architectsText, layers.GetLayerNameByNumber(8211))
    except:
        pass
    rs.EnableRedraw(True)

def AddLayout(size):
    if size == 11:
        name = '11x17 '
        width = '17 '
        height = '11 '
    elif size == 8:
        name = '8.5x11 '
        width = '11 '
        height = '8.5 '
    elif size == 18:
        name = '18x24 '
        width = '24 '
        height = '18 '
    result = rs.Command('-_Layout ' + name + width + height + '0 ', False)

    if result:
        layers.AddLayerByNumber(8000)
        AddTitleBlock(size)

def AddLayoutButton():
    layouts = ['8.5x11 Landscape', '11x17 Landscape', '18x24 Landscape']
    result = rs.ListBox(layouts, "Select layout to add", "Add Layout", "11x17 Landscape")
    if result is None: return
    if result == "11x17 Landscape":
        func = 11
    elif result == "8.5x11 Landscape":
        func = 8
    elif result == "18x24 Landscape":
        func = 18
    AddLayout(func)

def BatchPrintLayouts():
    print "BatchPrintLayout is WIP. Use with caution."
    try:
        pages = sc.doc.Views.GetPageViews()
        if pages is None or len(pages) < 1:
            print "No layouts in file"
            return

        defaultPath = rs.DocumentPath()

        defaultName = utils.GetDatePrefix() + "_Rhino"

        filename = rs.SaveFileName("Save", "PDF (*.pdf)|*.pdf||", folder = defaultPath, filename = defaultName)
        if filename is None: return

        names = []
        for page in pages:
            names.append([page.PageName, False])
        selectedLayouts = rs.CheckListBox(names, "Select Layouts to print", "Batch Print")
        if selectedLayouts is None: return

        stop = False
        for layout in selectedLayouts:
            if layout[1]==True:
                stop = True
                break
        if stop == False:
            print "No layouts selected"
            return
        try:
            pdf = Rhino.FileIO.FilePdf.Create()
        except:
            print "Failed to load Rhino.FileIO.FilePdf.Create()"
            return
        dpi = 300
        for i, page in enumerate(pages):
                if selectedLayouts[i][1]:
                    capture = Rhino.Display.ViewCaptureSettings(page, dpi)
                    pdf.AddPage(capture)
        pdf.Write(filename)
        print "PDF saved to {}".format(filename)
    except IOError, e:
        print str(e)
        return

def main():
    func = rs.GetInteger()
    if func is None: return

    if func == 0:
        AddLayoutButton()
    elif func > 0:
        AddLayout(func)

    #elif func == 90:
    #    BatchPrintLayouts()

if __name__ == "__main__" and utils.IsAuthorized():
    main()
