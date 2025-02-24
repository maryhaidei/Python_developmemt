import argparse

parser = argparse.ArgumentParser(description = "parse second cow")
parser.add_argument(
    "-E",
    type=str,
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
    "-N", action="store_false",
    help="If given, text in the speech bubble will not be wrapped"
)