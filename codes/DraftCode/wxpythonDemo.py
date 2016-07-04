
# import wx
#
# # create a new app, don't redirect stdout/stderr to a window
# app = wx.App(False)
#
# # a frame is a top-level window
# frame = wx.Frame(None, wx.ID_ANY, "Hello World")
# # show the frame
# frame.Show(True)
#
# app.MainLoop()

import wx

class MyFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self,
                         parent,
                         title = title,
                         size = (200, 100))

        self.control = wx.TextCtrl(self,
                                   style = wx.TE_MULTILINE)

        self.CreateStatusBar()

        fileMenu = wx.Menu()

        menuFile = fileMenu.Append(wx.ID_ABOUT,
                                   "Open File",
                                   "Open The File")

        menuAbout = fileMenu.Append(wx.ID_ABOUT,
                                    "&About",
                                    "Information about this program")

        menuExit = fileMenu.Append(wx.ID_EXIT,
                                   "&Exit",
                                   "Terminate the program")


        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

    def OnAbout(self, event):

        dlg = wx.MessageDialog(self,
                               "A small text editor",
                               "About Sample Editor",
                               wx.OK)

        dlg.ShowModal()

        dlg.Destroy()

    def OnExit(self, event):

        self.Close(True)

app = wx.App(False)
frame = MyFrame(None, "Sample Editor")
app.MainLoop()


