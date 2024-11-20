import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-medals", nargs='+',
                   help="list medals")
group.add_argument("-total", help="total result in year", type=int)
group.add_argument("-overall", help="overall info", nargs='+')
group.add_argument("-interactive",
                   help="enter interactive mode", action="store_true")

group.add_argument("-champions", nargs="+",
                   help="specify gender (M or F) and age group (for ex 18 35)")

parser.add_argument("filename",
                    help="specify file to load data from")

parser.add_argument("-output", "-o",
                    help="specify output file", type=str)
