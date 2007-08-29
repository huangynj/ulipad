#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2005 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   Meteor is free software; you can redistribute it and/or modify
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


import re
import sets
import types
import os
import os.path
import sys

class TemplateException(Exception): pass
class ObjectType(TemplateException): pass        
class NoPreprocessor(TemplateException): pass
    
class T:
    """Template element class
    """
    def __init__(self, string):
        self.text = string
        
    def getText(self):
        """get template element's text
        """
        return self.text
    
class Preprocessor:
    """pre-processor base class
    
    Using it to analyse a given template file into template elements and relation nodes set.
    Default pre-processor is python template.
    """

    def __init__(self, ptype='python', beginchars='<#', endchars='#>'):
        """ptype is processor name
        beginchars defines template var's left delimeter chars
        endchars defines template var's right delimeter chars
        """
        self.ptype = ptype
        self.beginchars = beginchars
        self.endchars = endchars

        self.vars = {}
        self.nodes = {}
        
    def setBeginChars(self, chars):
        self.beginchars = chars
        
    def setEndChars(self, chars):
        self.endchars = chars
        
    def process(self, modulename):
        """process a template object and return template elements and relation nodes set"""
        dirname = os.path.dirname(os.path.abspath(modulename))
        filename, ext = os.path.splitext(os.path.basename(modulename))
        if ext.lower() not in ('.py', '.pyc', '.pyo'):
            return {}, {}
        if sys.modules.has_key(filename):
            del sys.modules[filename]
        if dirname:
            sys.path.insert(0, dirname)
        mod = __import__(filename)
        if dirname:
            del sys.path[0]

        vars = {}
        nodes = {}
        for vn in dir(mod):
            v = getattr(mod, vn)
            if isinstance(v, T): #hasattr(v, '__class__') and v.__class__.__name__ == 'T':
                vars[vn] = v
                nodes[vn] = self.get_rely_on_node(v.getText())
           
        self.vars = vars
        self.nodes = nodes
        return vars, nodes
    
    def getPattern(self):
        """get template variable pattern"""
        return r'%s(\w+)%s' % (self.beginchars, self.endchars)

    def get_rely_on_node(self, s):
        """get relation nodes set"""
        re_node = re.compile(self.getPattern())
        
        return list(sets.Set(re_node.findall(s)))

    def get_default_target(self):
        keys = self.vars.keys()
        for i in keys:
            for j in keys:
                if i != j:
                    if i in self.nodes[j]:
                        break
            else:
                return i
        return ''

class SimpleTextPreprocessor(Preprocessor):
    """Simple text pre-processor"""
    
    def __init__(self, ptype='text', beginchars='<#', endchars='#>'):
        """ptype is processor name
        beginchars defines template var's left delimeter chars
        endchars defines template var's right delimeter chars
        """
        Preprocessor.__init__(self, ptype, beginchars, endchars)
        
    def process(self, content):
        """content can be a file object or text"""
        if isinstance(content, types.FileType):
            text = content.read()
        else:
            text = file(content).read()
            
        t= T(text)
        vars = {'text':t}
        nodes = {'text':self.get_rely_on_node(t.getText())}
        return vars, nodes
        
    def get_default_target(self):
        return 'text'

class Template:
    """Template controller class"""
    
    preprocess ={}
    
    def __init__(self):
        self.vars = {}
        self.nodes = {}
    
    def load(self, tplfile, tpltype=None, beginchars=None, endchars=None):
        """load template with specified type"""
        if not tpltype:
            filename, ext = os.path.splitext(os.path.basename(tplfile))
            if ext.lower() in ('.py', '.pyc', '.pyo'):
                tpltype = 'python'
            else:
                tpltype = 'text'
        self.pre = self.preprocess.get(tpltype, None)
        if not self.pre:
            raise NoPreprocessor, 'No proper preprocessor'
        if beginchars:
            self.pre.setBeginChars(beginchars)
        if endchars:
            self.pre.setEndChars(endchars)
 
        vars, nodes = self.pre.process(tplfile)
        self.vars.update(vars)
        self.nodes.update(nodes)
                
    def value(self, target=None, values={}):
        """get a template variable 's value"""
        if not target:
            target = self.pre.get_default_target()
        self.values_stack = [values]
        self.target = target
        if isinstance(values, types.DictType):
            return self._value(target, values.get(target, values))
        else:
            return self._value(target, values)
    
    def _value(self, target, values):
        self.values_stack.append(values)

        text = self.fReplace(target, values)
        if text is not None:
            return text
        
        nodes = self.nodes[target]
        
        if not isinstance(values, types.ListType):
            values = [values]
            
        s = []
        for v in values:
            vals = {}
            for node in nodes:
                if not v.has_key(node):
                    if node in self.vars.keys():
                        vals[node] = self._value(node, self._search_value(node))
                    else:
                        ret = self._search_value(node)
                        if ret:
                            vals[node] = ret
                else:
                    if node in self.vars.keys():
                        vals[node] = self._value(node, v[node])
                    else:
                        vals[node] = v[node]
            s.append(self._replace(target, self.vars[target].getText(), vals))
            
        del self.values_stack[-1]

        return ''.join(s)
    
    def _search_value(self, name):
        for i in range(len(self.values_stack) -1, -1, -1):
            values = self.values_stack[i]
            if isinstance(values, types.DictType) and values.has_key(name):
                return values[name]
            
        return {}
    
    def fReplace(self, name, values):
        if hasattr(self, 'OnReplace'):
            return self.OnReplace(self, var)
        else:
            return None
    
    def _replace(self, name, text, values):
        def dosup(matchobj, name=name, text=text, values=values):
            if values:
                result = values.get(matchobj.groups()[0], matchobj.group())
            else:
                result = matchobj.group()
            return result
        
        if not text:
            return text
        return re.sub(self.pre.getPattern(), dosup, text)
    
    def writeDot(self, f=None):
        s = []
        for key, values in self.nodes.items():
            for v in values:
                s.append('%s -> %s;\n' % (key, v))
                if not v in self.vars:  #extern template variable, the shape will be box
                    s.append("%s [shape=box];\n" % v)
        text = 'digraph G{\n' + ''.join(s) + '}\n'
        if isinstance(f, types.FileType):
            f.write(text)
            
        return text
        

def register(preprocess):
    Template.preprocess[preprocess.ptype] = preprocess
    
register(Preprocessor('python'))
register(SimpleTextPreprocessor('text'))