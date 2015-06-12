Screenshot

![http://haokanbu.s3.amazonaws.com/picture/external/e529cf9cb6d54563944c9b125b7b04f1.jpeg](http://haokanbu.s3.amazonaws.com/picture/external/e529cf9cb6d54563944c9b125b7b04f1.jpeg)

You can change the supported language syntax highlight color settings, here is a example for python,, it's black theme.

```
[styleitems]
controlchar = u"fore:#FFFFFF"
p_default = u"fore:#FFFFF"
number = u"fore:#6B238E"
classname = u"bold,fore:#FF0000"
triple = u"fore:#EABF71"
operator = u"fore:#BBBBBB"
defname = u"bold,fore:#4179C5"
stringeol = u"fore:#408080,back:#E0C0E0,eol"
character = u"fore:#E19618"
-selback = u"back:#8080FF"
bracebad = u"bold,fore:#0000FF"
string = u"fore:#E19618"
bracelight = u"bold,fore:#FF0000"
tripledouble = u"fore:#EABF71"
commentline = u"italic,fore:#626262"
commentblock = u"italic,fore:#626262"
-caretback = u"back:#050349"
keyword = u"bold,fore:#6AB825"
default = u"fore:#8000FF,back:#000000,face:Courier New,size:11"
-caretfore = u"fore:#FF0000"
linenumber = u"fore:#000000,back:#AAFFAA,size:10"
identifier = u"fore:#BBBBBB"
```

Create a `stx` folder in `conf` folder if there is not existed. Then create a file `python.stx`, then paste above content to this file. Restarting the UliPad and open a python file, you'll see the result.