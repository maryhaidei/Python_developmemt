import argparse
import cowsay
import sys


parser = argparse.ArgumentParser(description = "parse second cow")
parser.add_argument(
    "-E",
    type=str,
    default=None,
    help="An eye string. This is ignored if a preset mode is given",
    dest="eyes",
    default=Option.eyes,
    metavar="eye_string",

)
parser.add_argument(
    "-F", type=str, metavar="cowfile",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)
parser.add_argument(
    "-N", 
    default=True,
    action="store_false",
    help="If given, text in the speech bubble will not be wrapped"
)

def get_max_str(a):
    m=0; k=0
    for b in a: 
        if b=='\n' : m=m if m>=k else k; k=0
        k+=1
    return m
    

cow1=cowsay.cowsay(sys.argv[-2])
cow2=cowsay.cowsay(sys.argv[-1], F, eyes = E, wrap_text=N)
l1=cow1.count('\n')
l2=cow2.count('\n')
if l1==l2: 
    