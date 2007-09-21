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
#   $Id: mClassBrowser.py 475 2006-01-16 09:50:28Z limodou $

import wx
import os.path
from modules import Mixin
from modules import common
from modules import Globals

def pref_init(pref):
    pref.python_classbrowser_show = False
    pref.python_classbrowser_refresh_as_save = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        ('Python', 100, 'check', 'python_classbrowser_show', tr('Show class browser window as open python source file'), None),
        ('Python', 105, 'check', 'python_classbrowser_refresh_as_save', tr('Refresh class browser window as saved python source file'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_PYTHON', #parent menu id
            [
                (100, 'IDM_PYTHON_CLASSBROWSER', tr('Class Browser'), wx.ITEM_CHECK, 'OnPythonClassBrowser', tr('Show python class browser window')),
                (110, 'IDM_PYTHON_CLASSBROWSER_REFRESH', tr('Class Browser Refresh'), wx.ITEM_NORMAL, 'OnPythonClassBrowserRefresh', tr('Refresh python class browser window')),
            ]),
    ])
Mixin.setPlugin('pythonfiletype', 'add_menu', add_mainframe_menu)

def editor_init(win):
    win.class_browser = False
    win.init_class_browser = False #if the class view has shown
Mixin.setPlugin('editor', 'init', editor_init)

def OnPythonClassBrowser(win, event):
    win.document.class_browser = not win.document.class_browser
    win.document.panel.showWindow('LEFT', win.document.class_browser)
    if win.document.panel.LeftIsVisible:
        if win.document.init_class_browser == False:
            win.document.init_class_browser = True
            win.document.outlookbrowser.show()
Mixin.setMixin('mainframe', 'OnPythonClassBrowser', OnPythonClassBrowser)

def aftersavefile(win, filename):
    if (win.documenttype == 'edit' 
        and win.languagename == 'python'
        and win.pref.python_classbrowser_refresh_as_save 
        and win.init_class_browser):
        win.outlookbrowser.show()
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)
        
def OnPythonClassBrowserRefresh(win, event):
    win.document.outlookbrowser.show()
Mixin.setMixin('mainframe', 'OnPythonClassBrowserRefresh', OnPythonClassBrowserRefresh)

def OnPythonUpdateUI(win, event):
    eid = event.GetId()
    if eid == win.IDM_PYTHON_CLASSBROWSER:
        event.Check(win.document.panel.LeftIsVisible and getattr(win.document, 'init_class_browser', False))
Mixin.setMixin('mainframe', 'OnPythonUpdateUI', OnPythonUpdateUI)

def on_enter(mainframe, document):
    wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_CLASSBROWSER, mainframe.OnPythonUpdateUI)
    if mainframe.pref.python_classbrowser_show and document.init_class_browser == False:
        document.class_browser = not document.class_browser
        document.panel.showWindow('LEFT', document.class_browser)
        if document.panel.LeftIsVisible:
            if document.init_class_browser == False:
                document.init_class_browser = True
                document.outlookbrowser.show()
Mixin.setPlugin('pythonfiletype', 'on_enter', on_enter)

def on_leave(mainframe, filename, languagename):
    mainframe.Disconnect(mainframe.IDM_PYTHON_CLASSBROWSER, -1, wx.wxEVT_UPDATE_UI)
Mixin.setPlugin('pythonfiletype', 'on_leave', on_leave)

def add_images(images):
    s = [
        ('CLASS_OPEN', 'minus.gif'),
        ('CLASS_CLOSE', 'plus.gif'),
        ('METHOD', 'method.gif'),
        ('MODULE', 'module.gif'),
        ]
    for name, f in s:
        images[name] = os.path.join(Globals.workpath, 'images/%s' % f)
Mixin.setPlugin('outlookbrowser', 'add_images', add_images)

def parsetext(win, editor):
    if editor.documenttype == 'edit' and editor.languagename == 'python':
        from modules import PyParse
        nodes = PyParse.parseString(editor.GetText())

        imports = nodes['import']
        for info, lineno in imports:
            win.addnode(None, info, win.get_image_id('MODULE'), None, lineno)
        functions = nodes['function'].values()
        functions.sort()
        for info, lineno in functions:
            win.addnode(None, info, win.get_image_id('METHOD'), None,  lineno)
        classes = nodes['class'].values()
        classes.sort()
        for c in classes:
            _id, node = win.addnode(None, c.info, win.get_image_id('CLASS_CLOSE'), win.get_image_id('CLASS_OPEN'), c.lineno)
            functions = c.methods.values()
            functions.sort()
            for info, lineno in functions:
                win.addnode(node, info, win.get_image_id('METHOD'), None,  lineno)
            win.tree.Expand(node)
Mixin.setPlugin('outlookbrowser', 'parsetext', parsetext)

def new_window(win, document, panel):
    from OutlookBrowser import OutlookBrowser
    document.outlookbrowser = OutlookBrowser(panel.left, document)
Mixin.setPlugin('textpanel', 'new_window', new_window)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (2000, 'classbrowser'),
        (2010, 'classbrowserrefresh'),
        (2050, '|'),
    ])
    
    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'classbrowser':(wx.ITEM_CHECK, 'IDM_PYTHON_CLASSBROWSER', common.unicode_abspath('images/classbrowser.gif'), tr('class browser'), tr('Class browser'), 'OnPythonClassBrowser'),
        'classbrowserrefresh':(wx.ITEM_NORMAL, 'IDM_PYTHON_CLASSBROWSER_REFRESH', common.unicode_abspath('images/classbrowserrefresh.gif'), tr('class browser refresh'), tr('Class browser refresh'), 'OnPythonClassBrowserRefresh'),
    })
Mixin.setPlugin('pythonfiletype', 'add_tool_list', add_tool_list)