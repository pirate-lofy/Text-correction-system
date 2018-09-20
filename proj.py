import re 
from collections import Counter as counter


def get_words(txt):return re.findall(r'\w+',txt.lower()) # make it easier by convert to lower case

txt=open('big.txt').read()
bigList=counter(get_words(txt)) # couner will help in calculating the probalbilty of existence

def prob(word):
    n=sum(bigList.values())
    return bigList[word]/n

def correct(word):
    return max(other_poss(word),key=prob) # maximize based on the probalility of every word

def other_poss(word): # find all existent possible words
    return known([word]) or known(edit1(word)) or known(edit2(word)) or [word]

def known(words): # see if those words are existant in the original dictionary to reduce the number of genrated words
    return set(w for w in words if w in bigList)

def edit1(word): # genrate all candidates that need only one litter to be changed
    letters     = 'abcdefghijklmnopqrstuvwxyz'
    splits      =[(word[:i],word[i:])   for i in range(len(word)+1)]
    swaps       =[l+r[1]+r[0]+r[2:]     for l,r in splits if len(r)>2]
    deletes     =[l+r[1:]               for l,r in splits if len(r)>1]
    replaces    =[l+c+r[1:]             for l,r in splits if len(r)>1 for c in letters]
    inserts     =[l+c+r                 for l,r in splits for c in letters]

    return set(swaps+deletes+replaces+inserts)

def edit2(word):  # genrate all candidates that need two litter to be changed
    return set(s2 for s1 in edit1(word) for s2 in edit1(s1))


# the test phase, can be ignored
def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correct(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in bigList)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, bigList[w], right, bigList[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


def test():
    spelltest(Testset(open('spell-testset1.txt'))) # Development set
