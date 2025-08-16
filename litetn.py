#!/usr/bin/env python
import sys
import argparse
import re

# static funcs used as regex match evaluators
def selectivelowercase(match):
    # cap letters preceded by nothing and followed by either nothing or 's: preserve
    if match.group("lcpfx") == "" and ( match.group("sfx") == "'s" or match.group("sfx") == "" ):
        return match.group(0)
    # anything else containing caps: lowercase
    else:
        return match.group(0).lower()
def tagorbadcharsub(match):
    if match.group("tag") == None or match.group("tag") == "":
        return " "
    else:
        return " " + match.group("tag") + " "

class litetn:
    # settables
    lowercase = False
    zeroify = False
    uncontract = False
    dashedwords = False
    splitpossessives = False
    tagpuncs = False
    itntoks = False
    lang = "en"

    # main func to normalize strings
    def norm(self, str):
        # just ascii apostrophe
        str = re.sub(r"[’‘′´`]","'",str)
        # general lowercasing mode
        if self.lowercase:
            str = str.lower()
        # lowercase capitalized words but not inits, and not possessed inits like FBI's
        str = re.sub(r"(?P<lcpfx>[a-z]*)(?P<caps>[A-Z]+)(?P<sfx>[A-Z'\-]*?[a-z]*[a-zA-Z'\-]*)",selectivelowercase,str)
        # in zeroify mode, convert all digits to zero
        if self.zeroify:
            str = re.sub(r"\d","0",str)
        # tag puncs if requested
        if self.tagpuncs:
            # tag most puncs, but not single period
            str = re.sub(r"(\.{2,}|-{2,}|[,:\/-](?!\d)|[\?\!]+|;)",r" <punc:\1> ",str)
            # period, sentence finally
            str = re.sub(r"\.([\s\"]*)($|<s>)",r" <punc:.>\1\2",str)
            # <s> is redundant after punc tag
            str = re.sub(r"(<punc:\S+)\s*<s>",r"\1",str)
        # dashedwords mode: allow dashed words.  but clean up leading/trailing dashes
        elif self.dashedwords:
            str = re.sub(r"-(\W|$)",r" \1",str)
            str = re.sub(r"(^|\W)-",r"\1 ",str)
            str = re.sub(r"[,\.:\/](?!\d)"," ",str)
        # default punc hanlding: preserve period, comma, colon, dash around words, clobber elsewhere
        else:
            str = re.sub(r"[,\.:\/-](?!\d)"," ",str)
        # apostrophe only inside a word
        str = re.sub(r"(\s|^)'|'(\s|$)"," ",str)
        # allowed chars and tags
        str = re.sub(r"(?P<tag><punc:\S+>|<s>)|(?P<bad>[^a-záéíúóàèäëïöüãõâêîôûçñß\d\$£\%\@\#\&\.,:\/'-])",tagorbadcharsub,str,flags=re.IGNORECASE)
        # okay -> ok
        str = re.sub(r"\bokay\b", "ok", str)
        # chop 's off of words
        if self.splitpossessives:
            str = re.sub(r"'s\b"," 's", str)
        # contraction splitting
        if self.uncontract and re.match(r"^en",self.lang):
            str = re.sub(r"('(?:s|m|d|ll|re|ve)|n't)\b",r" \1",str)
            str = re.sub(r"\bgonna\b","going to",str)
            str = re.sub(r"\bwanna\b","want to",str)
            str = re.sub(r"\bgotta\b","got to",str)
            str = re.sub(r"\by'all\b","you all",str)
            str = re.sub(r"\blemme\b","let me",str)
            str = re.sub(r"\bmor'n\b","more than",str)
            str = re.sub(r"\bgimme\b","give me",str)
            str = re.sub(r"\bwatcha\b","what are you",str)
            str = re.sub(r"\b(can)(not)\b",r"\1 \2",str)
    
        # clean up whitespace and return
        str = re.sub(r"\s{2,}"," ",str)
        str = re.sub(r"^\s+|\s+$","",str)
        return str

# entry point if this lib is called as a standalone script
if __name__ == '__main__':
    argparser = parser = argparse.ArgumentParser(description='litetn')
    argparser.add_argument("-e", "-echo", dest="echo", action="store_true", help="echo input then output")
    argparser.add_argument("-l", "-lc", "-lowercase", dest="lowercase", action="store_true", help="lowercase")
    argparser.add_argument("-z", "-zero", "-zeroify", dest="zeroify", action="store_true", help="replace all digs with zero")
    argparser.add_argument("-tagpuncs", "-tp", dest="tagpuncs", action="store_true", help="tag syntactic punctuation marks")
    argparser.add_argument("-lang", "-loc", "-locale", dest="lang", type=str, default="en", help="some feats lang-specific")
    argparser.add_argument("-uc","-uncontract",dest="uncontract", action="store_true", help="wanna->want to etc")
    argparser.add_argument("-splitpossessives","-sp",dest="splitpossessives",action="store_true",help="joe's->joe 's")
    args = argparser.parse_args()

    # create normalizer, init according to parsed args
    mynorm = litetn()
    mynorm.lowercase = args.lowercase
    mynorm.zeroify = args.zeroify
    mynorm.tagpuncs = args.tagpuncs
    mynorm.uncontract = args.uncontract
    mynorm.splitpossessives = args.splitpossessives
    mynorm.lang = args.lang
    
    # set up input and output
    inh = sys.stdin
    outh = sys.stdout

    # process lines
    for inputline in inh:
        inputline = inputline.rstrip()
        outputline = mynorm.norm(inputline)
        if args.echo:
            outh.write(inputline + "\t")
        outh.write(outputline)
        outh.write("\n")
