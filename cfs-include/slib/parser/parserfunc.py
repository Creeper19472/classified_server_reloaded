# -*- coding: utf-8 -*-

class ParserFunctions():
    def version(vertext):
        keyword_list = vertext.split(' ')
        number_list = keyword_list[0].split('.')
        if len(keyword_list) <= 1:
            return {"number": number_list}
        else:
            return {"number": number_list, "word": keyword_list[1:]}
