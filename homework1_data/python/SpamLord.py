import sys
import os
import re
import pprint

# email patterns
my_e_pat = []
my_e_pat.append('(\w*\.?\w+) ?@ ?(\w*\.?\w+).(edu|EDU)')
my_e_pat.append('(\w+) WHERE (\w+) DOM edu')
my_e_pat.append('(\w+)&#x40;(\w*\.?\w+)\.edu')
my_e_pat.append('(\w*\.?\w+) \(followed by .+@(\w*\.?\w+)\.edu')
my_e_pat.append('(\w\-.*)@(.*).-e-d-u') # e.g.'d-l-w-h-@-s-t-a-n-f-o-r-d-.-e-d-u'
my_e_pat.append('(\w+)@(\w+) dt com')
my_e_pat.append('(\w+)@(\w+ \w+) edu')
my_e_pat.append('(\w+)@(\w*;?\w+);edu')
my_e_pat.append("'(\w+)\.edu','(\w+)'") # e.g."('stanford.edu','jurafsky')"

# phone number patterns
my_p_pat = []
my_p_pat.append('\((\d+)\) ?(\d+)\-(\d+)')
my_p_pat.append(' (\d+)\-(\d+)\-(\d+)')
my_p_pat.append('(\d+)\-(\d+)\-(\d+) ')
my_p_pat.append('(\d+)\-(\d+)\-(\d+)\(') # e.g.'650-725-4802(office)'
my_p_pat.append('\+\d+ (\d+) (\d+) ?\-?(\d+)') # e.g.'+1 650 723 5666'


"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        line = re.sub(' at ', '@', line)
        line = re.sub(' dot ', '.', line)
        for pat in my_e_pat:
            matches = re.findall(pat,line)
            for m in matches:
                if m[0] == 'Server':
                    continue
                if pat == my_e_pat[-1]:
                    email = '%s@%s.edu' % (m[-1], m[-2])
                elif pat == my_e_pat[-2]:
                    address = re.sub(';', '.', m[1])
                    email ='%s@%s.edu' % (m[0], address)
                elif pat == my_e_pat[-3]:
                    address = re.sub(' ', '.', m[1])
                    email ='%s@%s.edu' % (m[0], address)
                elif pat == my_e_pat[-4]:
                    email ='%s@%s.com' % (m[0], m[1])
                elif pat == my_e_pat[-5]:
                    address1 = re.sub('-', '', m[0])
                    address2 = re.sub('-', '', m[1])
                    email = '%s@%s.edu' % (address1, address2)
                else:
                    email ='%s@%s.edu' % (m[0], m[1])
                res.append((name,'e',email))
        
        for pat in my_p_pat:
            matches = re.findall(pat, line)
            for m in matches:
                phone = '%s-%s-%s' % (m[0], m[1], m[2])
                res.append((name,'p',phone))
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        try:
            f = open(path,'r', encoding="utf-8")
            f_guesses = process_file(fname, f)
            f.close()
        except:
            f = open(path,'r', encoding="windows-1252")
            f_guesses = process_file(fname, f)
            f.close()

        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding="utf-8")
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    f_gold.close()
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print ('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
