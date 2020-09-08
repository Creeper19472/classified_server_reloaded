# -*- coding:utf-8 -*-

import re

class Blocked:
    def ReplaceBlock(text, level):
        blockends = 0
        while True:
            matchObj = re.search( r'<blocked [0-9]>', text, re.M|re.I)
            if matchObj == None:
                break
            blockstarts = matchObj.span()[0]
            taglevelpos = blockstarts + 9
            taglevel = int(text[taglevelpos])
            blockends = text.find('</blocked>', blockstarts)
            if blockends == -1:
                raise SyntaxError('Missing \'</blocked>\'')
            else:
                blockends = blockends + 10
            if level >= taglevel:
                text = text.replace(text[blockstarts:blockends], text[blockstarts+11:blockends-10])
            else:
                text = text.replace(text[blockstarts:blockends], '[数据删除]')
        return text

if __name__ == '__main__':
    print(Blocked.ReplaceBlock('<blocked 3>This is a test</blocked><blocked 2>64-7-1502</blocked>', 2))