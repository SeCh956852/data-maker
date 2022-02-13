from doctest import master
import tkinter as Tk
import tkinter.ttk as Ttk
import pandas as pd
import configparser as Confp
import random
from os import listdir
from turtle import width
from typing import Dict


class Configuration:
    """
    Handles configurations
    """
    def __init__(self):
        """
        Set expected configuration file path
        Set default configuration
        """
        self.ConfigParser = Confp.ConfigParser()
        self.ConfigParser.optionxform = str #Config parser preserver uppercase
        self.ConfigPath = r"./config.cfg" #Configuration file path
        self.Layout = {
            "BackgroundColor" : "#ffffff",
            "FontSize" : 14,
        }

    def CreateConfigFile(self):
        """
        Creates a configuration file and setting all values to default
        """

        ConfigParser = self.ConfigParser

        ConfigParser["Layout"] = self.Layout

        with open(self.ConfigPath, "w") as ConfigFile:
            ConfigParser.write(ConfigFile)


    def GetConfig(self):
        """
        Attempts to read configuration path and update 
        If configuration file does not exist, create a new file
        """ 
        try:
            ConfigParser = self.ConfigParser
            
            ConfigParser.read(self.ConfigPath)

            Sections = ConfigParser.sections()

            #if config file does not exist, create a new config file
            if len(Sections) == 0:
                self.CreateConfigFile()
                return

            #if config file exists, iterate and get configurations
            for Section in ConfigParser.sections():
                ConfigSection = getattr(self, Section)
                for Key in ConfigParser[Section]:
                    ConfigSection[Key] = ConfigParser[Section][Key]

        except KeyError:
            pass

        except AttributeError:
            pass

class CustomTtkStyle(Ttk.Style):
    def __init__(self):
        super().__init__(master)

    def SetStyle():
        pass

class TkWindow(Tk.Tk):
    """
    Handles the graphical user interface
    """
    def __init__(self, ObjDataMaker):
        #Initialize attributes
        super().__init__()
        self.Title = "Data Maker"
        self.FieldSection = []
        self.ObjDataMaker = ObjDataMaker

        #Initialize Style
        self.Style = CustomTtkStyle()
        
        #Generate UI
        self.GenerateTitle()
        self.GenerateTopbar()
        self.GenerateBody()
        self.GenerateBottomBar()
        self.GenerateFieldSection()

        #Window Layout
        self.UpdateGeometry()
        self.SetResizeable(False)

        #Activate main event loop
        self.mainloop()
        
    def SetStyle(self):
        Style = self.Style
        #Style.configure("TEntry", )

    def SetResizeable(self, option):
        self.resizable(option, option)

    def UpdateGeometry(self):
        self.update_idletasks() 
        self.Width = self.winfo_width()
        self.Height = self.winfo_height()
        self.CenterApp(self.Width, self.Height)

    def CenterApp(self, WindowWidth, WindowHeight):
        ScreenWidth = self.winfo_screenwidth()
        ScreenHeight = self.winfo_screenheight()

        Left = int((ScreenWidth - WindowWidth)/2)
        Top = int((ScreenHeight - WindowHeight)/2)

        self.geometry(f"{WindowWidth}x{WindowHeight}+{Left}+{Top}")
        self.ResetGeometry()

    def ResetGeometry(self):
        self.geometry("")

    def AddToFieldsList(self, ObjField):
        self.FieldSection.append(ObjField)
        return self.FieldSection
    
    def HandleNewFileButton(self, event):
        self.GenerateFieldSection()

    def HandleDeleteFieldButton(self, event, ObjField, FrameFieldSection):
        FrameFieldSection.destroy()
        #Remove reference to field object
        self.FieldSection.remove(ObjField)
        del ObjField

    def HandleGenerateButton(self, event, FieldSection):
        #Validate Inputs
        try:
            RecordNo = int(self.RecordNo.get())
            FileName = self.FileName.get()
        except (TypeError, ValueError):
            print("Number of Records must be an integer")

        if len(self.FieldSection) != 0 and RecordNo > 0:
            self.ObjDataMaker.MainCreateData(FieldSection, RecordNo, FileName)

    def GenerateTopbar(self):
        self.FrameTopbar = Ttk.Frame(
            master = self
        )
        self.FrameTopbar["padding"] = (0, 15, 0, 0)
        self.ButtonNewFile = Ttk.Button(
            master = self.FrameTopbar, 
            text = "New Field"
        )
        self.LabelNumberOfRecords = Ttk.Label(
            master = self.FrameTopbar,
            text = "Number of Records: "
        )
        self.RecordNo = Tk.StringVar()
        self.EntryNumberOfRecords = Ttk.Entry(
            master = self.FrameTopbar,
            width = 20,
            textvariable = self.RecordNo
        )
        self.LabelFileName = Ttk.Label(
            master = self.FrameTopbar,
            text = "Result File Name: "
        )
        self.FileName = Tk.StringVar()
        self.EntryFileName = Ttk.Entry(
            master = self.FrameTopbar,
            width = 30,
            textvariable = self.FileName
        )

        self.FrameTopbar.pack(
            fill = Tk.X,
        )
        self.ButtonNewFile.grid(
            column = 0,
            row = 0,
            padx = (20, 50),
            pady = 10,
            ipadx = 10,
            ipady = 5
        )
        self.LabelNumberOfRecords.grid(
            column = 1,
            row = 0,
            padx = (50, 0),
        )
        self.EntryNumberOfRecords.grid(
            column = 2,
            row = 0,
            padx = (10, 50),
            ipady = 3,
        )
        self.LabelFileName.grid(
            column = 3,
            row = 0,
            padx = (50, 0),
        )
        self.EntryFileName.grid(
            column = 4,
            row = 0,
            padx = (10, 50),
            ipady = 3,
        )

        self.ButtonNewFile.bind("<Button-1>", self.HandleNewFileButton)
        

    def GenerateBody(self):
        self.FrameBody = Ttk.Frame(
            master = self,
        )
        self.FrameBody["padding"] = (0, 15, 0, 15)

        self.FrameBody.pack(
            fill = Tk.X
        )

    def GenerateFieldSection(self):
        #Create widgets
        FrameFieldSection = Ttk.Frame(
            master = self.FrameBody
        )
        ButtonDeleteField = Ttk.Button(
            master = FrameFieldSection,
            text = "Delete"
        )
        LabelFieldName = Ttk.Label(
            master = FrameFieldSection,
            text = "Field Name: "
        )

        VarFieldName = Tk.StringVar()
        EntryFieldName = Ttk.Entry(
            master = FrameFieldSection,
            width = 20,
            textvariable = VarFieldName
        )

        LabelDataList = Ttk.Label(
            master = FrameFieldSection,
            text = "Type of Data to Generate: "
        )
        
        Options = self.ObjDataMaker.GetAvailableDataList()
        VarDataList = Tk.StringVar()
        VarDataList.set(Options[0])
        OptionMenuDataList = Ttk.OptionMenu(
            FrameFieldSection,
            VarDataList,
            Options[0],
            *Options
        )

        #Create field object
        ObjField = Field(
            VarFieldName,
            VarDataList
        )
        self.AddToFieldsList(ObjField)
        ButtonDeleteField.bind("<Button-1>", lambda event: self.HandleDeleteFieldButton(event, ObjField, FrameFieldSection))

        #Show everything in UI
        FrameFieldSection.pack(
            fill = Tk.X
        )
        ButtonDeleteField.pack(
            side = Tk.LEFT,
            padx = 20,
            pady = 10,
            ipadx = 10,
            ipady = 5
        )
        LabelFieldName.pack(
            side = Tk.LEFT,
            padx = (20, 10)
        )
        EntryFieldName.pack(
            side = Tk.LEFT,
            ipady = 3,
        )
        LabelDataList.pack(
            side = Tk.LEFT,
            padx = (40, 0)
        )
        OptionMenuDataList.pack(
            side = Tk.LEFT,
            padx = (0, 20)
        )


    def GenerateBottomBar(self):
        self.FrameBottomBar = Ttk.Frame(
            master = self
        )
        self.FrameBottomBar["padding"] = (0, 0, 0, 15)
        self.ButtonSubmit = Ttk.Button(
            master = self.FrameBottomBar,
            text = "Generate"
        )
        self.ButtonSubmit.bind("<Button-1>", lambda event: self.HandleGenerateButton(event, self.FieldSection))

        self.FrameBottomBar.pack(
            fill = Tk.X
        )
        self.ButtonSubmit.pack(
            side = Tk.RIGHT,
            ipadx = 10,
            ipady = 5,
            padx = 20,
            pady = 10
        )
    
    def GenerateTitle(self, *args):
        #If supplied a title via argument then use it else use default title in __init__
        if len(args) == 0:
            Title = self.Title
        else:
            Title = args[0]

        self.title(Title)

class Field:
    def __init__(self, VarFieldName, VarDataList):
        self.VarFieldName = VarFieldName
        self.VarDataList = VarDataList


class DataMaker:
    """
    Handles the creation of data
    """
    def __init__(self):
        pass

    def GetAvailableDataList(self):
        Path = "./Datalist"
        ListDataList = [f.replace(".txt", "") for f in listdir(Path) if f.endswith(".txt")]
        return ListDataList

    #Create CSV file from data
    def CreateCSVFile(self, DF, filename):
        DF.to_csv(f"./Result/{filename}.csv", index = False)

    #Read data from text file
    def ReadDataListFile(self, DataListName):
        with open(f"./Datalist/{DataListName}.txt","r") as DataListFile:
            DataListStr = DataListFile.read()
            DataListStr.replace("\n", "")
        
        return DataListStr

    def TrimData(self):
        pass

    def GetData(self, DataListName):
        DataListStr = self.ReadDataListFile(DataListName)
        DataList = DataListStr.split(",")
        return DataList

    def SelectRandomData(self, DataList, RecordNo):
        for i in range(RecordNo):
            RandIndex = random.randrange(0, len(DataList))
            yield DataList[RandIndex]

    #Create data 
    def MainCreateData(self, FieldSection, RecordNo, FileName):
        DataDict = {}
        for Field in FieldSection:
            DataList = self.GetData(Field.VarDataList.get())
            DataDict[Field.VarFieldName.get()] = [i for i in self.SelectRandomData(DataList, RecordNo)]

        DF = pd.DataFrame(DataDict)
        self.CreateCSVFile(DF, FileName)


def Main():
    #Initialize configuration
    ObjConfiguration = Configuration()
    ObjConfiguration.GetConfig()

    #Create data maker object
    ObjDataMaker = DataMaker()

    #Create graphical user interface
    ObjTkWindow = TkWindow(ObjDataMaker)


if __name__ == "__main__":
    Main()




