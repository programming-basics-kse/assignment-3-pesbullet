import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-medals", nargs='+')
group.add_argument("-quiet", action="store_true")
parser.add_argument("filename",
                    help="specify file to load data from")

#parser.add_argument("-o", "--output",)
