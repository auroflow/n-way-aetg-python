import csv
import argparse
import xlsxwriter

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", default="input.csv", help="path to the CSV source file")
parser.add_argument("-d", "--destination", default='output.xlsx', help="path to destination folder")
parser.add_argument("-n", "--dimension", type=int, default=2, help="dimension of coverage required")
parser.add_argument("-t", "--test", help="validate test cases generated")

args = parser.parse_args()

titles = list()
params = list()

try:
    with open(args.source, "r") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            titles.append(row[0])
            params.append(list(row[1:]))
except FileNotFoundError:
    parser.print_usage()
    quit()

v_count = [len(param) for param in params]
if args.dimension == 2:
    from aetg import AETG
else:
    from aetg_n_way import AETG

aetg = AETG(v_count, dim=args.dimension)
cases = aetg.generate()

with xlsxwriter.Workbook(args.destination) as workbook:
    worksheet = workbook.add_worksheet()
    for i, title in enumerate(titles):
        worksheet.write(0, i, title)
    for i, case in enumerate(cases):
        for j, p in enumerate(case):
            worksheet.write(i + 1, j, params[j][p])
