# -*- coding:utf-8 -*-

import re


class replacer:
    def replaceTag(tagname, srctext, level, replacetext):
        taglength = len(tagname)
        pos1 = 0
        while True:
            matchObj = re.search(r"<%s [0-9]>" % tagname, srctext, re.M | re.I)
            if matchObj == None:
                result = srctext
                break
            pos1 = matchObj.span()[0]
            levelpos = pos1 + taglength + 2
            taglevel = int(srctext[levelpos])
            pos2 = srctext.find("</%s>" % tagname, pos1)
            if pos2 == -1:
                raise SyntaxError("Missing '</%s>'" % tagname)
            else:
                pos2 = pos2 + taglength + 3
            if level >= taglevel:
                srctext = srctext.replace(
                    srctext[pos1:pos2], srctext[pos1 + taglength + 4 : pos2 - taglength - 3]
                )
            else:
                srctext = srctext.replace(srctext[pos1:pos2], replacetext)
        return result


if __name__ == "__main__":
    print(replacer.replaceTag("blocked","<blocked 3>64-7-1502</blocked>", 2, "Fuck"))
    print(replacer.replaceTag("example1","<example1 5>187277</example1>!aknsinsins<example1 2>xxx</example1>", 3, "..."))
