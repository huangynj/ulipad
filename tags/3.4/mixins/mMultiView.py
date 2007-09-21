#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id$

import wx
from modules import Mixin
from modules import Globals

def add_editor_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (200, 'IDPM_MULTIVIEWWINDOW', tr('Open Multi View Window'), wx.ITEM_NORMAL, 'OnMultiViewWindow', tr('Opens multi view window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_editor_menu)

def createMultiViewWindow(win, side, document):
    dispname = document.getShortFilename()
    filename = document.filename
    if not win.panel.getPage(dispname):
        if hasattr(win.document, 'GetDocPointer'):
            from mixins import Editor
            
            page = Editor.TextEditor(win.panel.createNotebook(side), None, filename, win.document.documenttype, multiview=True)
            page.SetDocPointer(win.document.GetDocPointer())
            page.document = win.document    #save document object
            win.document.lexer.colourize(page, True)
            win.panel.addPage(side, page, dispname)
            return dispname
    else:
        return dispname
Mixin.setMixin('mainframe', 'createMultiViewWindow', createMultiViewWindow)

def OnMultiViewWindow(win, event):
    side = win.getSide()
    dispname = win.mainframe.createMultiViewWindow(side, Globals.mainframe.document)
    if dispname:
        win.panel.showPage(dispname)
Mixin.setMixin('notebook', 'OnMultiViewWindow', OnMultiViewWindow)

def closefile(win, document, filename):
    for pname, v in Globals.mainframe.panel.getPages().items():
        page = v[2]
        if hasattr(page, 'multiview') and page.document is document:
            Globals.mainframe.panel.closePage(pname)
Mixin.setPlugin('mainframe', 'closefile', closefile)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_WINDOW',
        [
            (220, 'IDM_WINDOW_MULTIVIEWWINDOW', tr('Open Multi View Window'), wx.ITEM_NORMAL, 'OnWindowMultiView', tr('Opens multi view window.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnWindowMultiView(win, event):
    dispname = win.mainframe.createMultiViewWindow('bottom', Globals.mainframe.document)
    if dispname:
        win.panel.showPage(dispname)
Mixin.setMixin('mainframe', 'OnWindowMultiView', OnWindowMultiView)

def setfilename(document, filename):
    for pname, v in Globals.mainframe.panel.getPages().items():
        page = v[2]
        if hasattr(page, 'multiview') and page.document is document:
            title = document.getShortFilename()
            Globals.mainframe.panel.setName(page, title)
Mixin.setPlugin('editor', 'setfilename', setfilename)
    
def add_editctrl_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (600, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (700, 'IDM_MULTIVIEW_LEFT', tr('Open View in Left Side'), wx.ITEM_NORMAL, 'OnOpenViewLeft', tr('Opens view of current document in left side.')),
            (800, 'IDM_MULTIVIEW_BOTTOM', tr('Open View in Bottom Side'), wx.ITEM_NORMAL, 'OnOpenViewBottom', tr('Opens view of current document in bottom side.')),
        ]),
    ])
Mixin.setPlugin('editctrl', 'add_menu', add_editctrl_menu)

def OnOpenViewLeft(win, event):
    dispname = win.mainframe.createMultiViewWindow('left', Globals.mainframe.document)
    if dispname:
        win.mainframe.panel.showPage(dispname)
Mixin.setMixin('editctrl', 'OnOpenViewLeft', OnOpenViewLeft)

def OnOpenViewBottom(win, event):
    dispname = win.mainframe.createMultiViewWindow('bottom', Globals.mainframe.document)
    if dispname:
        win.mainframe.panel.showPage(dispname)
Mixin.setMixin('editctrl', 'OnOpenViewBottom', OnOpenViewBottom)