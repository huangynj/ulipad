#Change log of UliPad releases

Current lastest version is 3.8.1

# 4.1 Version 2011/11/06 #

It's mainly bug vix version.

  1. Upgrade winpdb version to 1.4.8
  1. Improve Edit->Format->Wrap Text functionality to suit for reStructuredText wrap
  1. Made memo file configurable thanks to Helio Perroni Filho
  1. Add Bash support thanks to Helio Perroni Filho
  1. Add some useful methods to support scripts files. Such as emptytab, newtab, etc. thanks to Helio Perroni Filho
  1. Add Lua support thanks to zhangchunlin
  1. Improve python file detect according to #! /usr/bin/env python thanks to zhangchunlin
  1. Add default color theme support, you can set it in Preference
  1. Add Create Python Package menu in context menu of Directory Browser Window
  1. Improve web2py plugin
  1. Improve regex window, and when you set Unicode flag, it'll automatically convert \uXXXX to unichr
  1. Fix strip tailing spaces bug

# 4.0 Version 2008/04/24 #

  1. Add config menu, and add toggle input assistant menu item
  1. Fix refresh directory bug
  1. Add wrap text feature
  1. Add copy filename to clipboard menu on document area tab context menu
  1. When add path, it'll automatically pop up project setting dialog
  1. Add slice syntax support
  1. Can remember the last new file type
  1. Improve preference dialog input assistant checkbox process.
  1. Add line ending mixture check when saving file feature
  1. Add search text count
  1. Add web2py plugin
  1. Improve ReST document render, and fix the setfocus lost bug when auto modified the html output, thanks a lot to ygao
  1. Add auto detect python interpreter in windows platform
  1. Fix script filename cannot be unicode(chinese) bug
  1. Add icon set theme support.
  1. Change DDE to asyncore and asynchat framework
  1. Add new snippet
  1. add php.acp thanks for 魏振 <etggy@163.com>
  1. Add Canvas Test plugin, you can directly test DC api

# 3.9 Version 2007/12/12 #

  1. Fix webopen twice open bug

# 3.8.1 Version 2007/12/12 #

It's a bug fix version:

  1. Remove profile invoke(big mistake)
  1. Fix svn plugin checkout bug

# 3.8 Version 2007/12/06 #

New Features and Changes:

  1. Add mako template syntax highlight support
  1. Add new option in preference, `[Python]`->`Automatically save modified file when running python program`, if it's checked, it'll automatically save the modified file.
  1. Add Shift+Delete => Cut, Shift+Insert => Paste
  1. Upgrade winpdb to lastest version
  1. Now you can set pythonpath option in `config.ini/[default]`, and ulipad will insert it into the sys.path. pythonpath can be a string or a string list of directory.
  1. Svn support, you should install pysvn first, and also support proxy.
  1. Change long line indicator default is true.
  1. Add doctest support, you can run the doctest of current document in `UliPad`
  1. Add time stamp info in debug and error file
  1. Replace the shell window popup menu, and add `Copy Without Prompts` and `Paste and Run` menu items. And if the result cann't be convert to unicode, then display the result as repr().
  1. Script Manager can find menu name from the script content, you can define it as a comment line, format is: `#\s*name:(.*)$`
  1. Add `Run in Shell` menu item in Editor context menu
  1. Add script and shell key binding. Change `Shell` to `External Tool`
  1. Change `Find in Files` dialog to panel
  1. Using meide module to create Preference dialog
  1. Add an option to control if show the docstring in class browser window.
  1. Don't create a tmp file again, directly save the file
  1. Improve Find in Files process with thread
  1. Add some config.ini options support in Preference Dialog
  1. Refactor `Find & Replace` with pane, but not dialog
  1. Made `Open Command Here` work in Linux
  1. Add dropfile plugin. thanks Tyberius Prime. Now you can drop files on toolbar, then `UliPad` will open it. Just like drop files on Directory Browser window.
  1. Add new custom lexer class and refactor related lexer process
  1. Upgrade `FlatNotebook.py` to lastest version, thanks to swordsp
  1. Improve default identifiers process, add type judgement
  1. Add pylint plugin

Bug fix:

  1. Fix print bug, add print line number functionality
  1. Fix snippet template indent bug(when using tab mode, the '\t' in template will be replaced with spaces). And you can press Alt+Q to cancel current snippet.
  1. Fix press Ctrl+B jump position is not correct bug.
  1. Fix that when you change the file type, the icon in directory and dynamic menu don't change bug
  1. Fix line number margin width, and find back End-of-line Marker menu
  1. Fix adding empty directory error
  1. Fix open un-exists file will popup two message dialog bug
  1. Fix line end mix checking bug also including twice prompt dialog bug
  1. Fix webbrowser bug. Thanks Tom Eubank
  1. Fix message console postion bug, thanks for swordsp

# 3.7 Version 2007/08/19 #

New Features and Changes:

  1. Add PEP8 sytle checking
  1. Enhance calltip showing
  1. Add a new option in Preference, which is used for when you toggle comment lines(Ctrl+/ or Ctrl+\) if it'll popup a comment dialog. You can find it in Preference->Document->Show comment character dialog when adding comment.
  1. Saving auto todo window status
  1. Changing shortcut of quote dialog from Ctrl+Q to Ctrl+'
  1. Changing the number of recent files to 20
  1. Changing shortcut Ctrl+Alt+L to Alt+Z, Ctrl+Alt+B to Alt+X
  1. Saving the status of Message window word wrap
  1. Saving the snippets window position
  1. The results of find in files can only show the filenames and you can copy them to clipboard
  1. Add Spanish language translation and Traditional Chinese language translation
  1. Using ZestyParser Module to parse the source code syntax
  1. Improving input assistant functionality
  1. Adding config.txt documentation
  1. When saving files, automatically adding accordingly filename suffix
  1. Adding mixin reload mechanism, it will be very useful when developing
  1. Adding folder sort functionality when adding new folder to directory browser window
  1. Adding template in input assistant, and you can press TAB key to jump to the next field. The template just like: ${1:something}.
  1. Adding LUA syntax support
  1. Adding mako(template module) support plugin
  1. Adding batch filenames rename plugin
  1. Enable ftp window be openned left or bottom pane according to the openning position
  1. Adding Alt+R shortcut for open recently files
  1. Merging new 1.20 version winpdb to ulipad


Bug fix:

  1. Fix ctag support bug
  1. Fix default style bug
  1. Fix the wrong cursor jumping after undo operating
  1. Fix xml lexer type bug
  1. Fix copying bug when the text block has no indent
  1. Fix openning multi-view bug from menu items
  1. Fix the input focus losing bug when openning bottom pane or double-click on directory browser entries
  1. Fix user can open multi find dialogs bug
  1. Fix register functionality in windows