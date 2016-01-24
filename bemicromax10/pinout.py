#!/usr/bin/python

import sys

colors = {}
styles = {"base":1}


def usage():
    """
    """
    print """

        Usage:
           ./pinout.py <txtfile>
          
          """
    sys.exit(-1)
#enddef

def printColor(color="pin"):
    print "\definecolor{%s}{RGB}{108,210,118}" % color

#enddef

def printBaseStyles():
    print """
\\tikzset{
        dot/.style={inner sep=0pt,minimum size=10pt,fill=black,circle},
        linel/.style = {rectangle, inner sep=0pt, minimum height=0pt, minimum width=10ex, draw},
        lines/.style = {rectangle, inner sep=0pt, minimum height=0pt, minimum width=2ex, draw},"""
#enddef

def printStyle(style='base'):
    
    print "        %s/.style={rectangle,fill=pin,draw,rounded corners=3,anchor=center,text depth=.0ex}," % style
    
#enedef

def getColorAndClass(item):
    color = None
    style = None
    name = item
    
    if item.find('#') != -1:
        name,color = item.split("#")
        colors[color] = 1
    
    if item.find('!') != -1:
        name,style = item.split("!")
        styles[style] = 1
    else:
        style = 'base'
    #endif
    
    return (name,style,color)
#enddef

def printMatrix(matrix,side='left',name='m1', padding=0 ):
    """
    """
    print "\\matrix(%s) [row sep=0.8ex,column sep=0.5ex] at (0,0) {" % name
    for r in matrix:
        row = ''
        for i in xrange(0,len(r)):
            nm = r[i][0].replace('_','\\_')
            if r[i][2]: 
                row += " \\node [%s, fill=%s] {%s};" % (r[i][1],r[i][2],nm)
            else:
                row += " \\node [%s,] {%s};" % (r[i][1],nm)
            #endif
            if i != len(r) - 1:
                row += "& \\node [lines]{}; &"
            #endif
        #endfor
        # fix lef and right
        if side == 'left':
            row = ' ' + '&'*2*(padding - len(r)) +  row + "& \\node [linel]{}; & \\node [dot] {} ;\\\\"
        else:
            row = " \\node [dot] {} ; & \\node [linel]{}; &" + row + "\\\\"
        #endif
        print row
    #endfor
    print '};'
#enddef


def main ():
    """
    """
    left = []
    right = []
    padding = 1

    if len(sys.argv) != 2:
        usage()
    #endif
   
    

    #open file
    fl = open(sys.argv[1],'rt')

    for ln in fl.xreadlines():
        #separate left and right side
       
        data = ln.split('|')
        
        if len(data) != 2:
            continue
        #endif


        lf,rt = map(str.strip, data)
        
        #parse pins
        if lf != '':
            left.append(map(getColorAndClass,lf.split(' ')))
            pinscnt = len(left[-1])
            if pinscnt > padding:
                padding = pinscnt
            #endif

        #endif
        if rt != '':
            right.append(map(getColorAndClass,rt.split(' ')))
        #endif
 
    #endfor
    
    printColor()
    for color in colors:
        printColor(color)
    #endfor

    printBaseStyles()
    for style in styles:
        printStyle(style)
    #endfor
    print '}'
    
    print

    printMatrix(left,'left',"lm",padding)
    printMatrix(right,'right',"rm",padding)

#enddef



if __name__ == "__main__":
    main()
#endif
