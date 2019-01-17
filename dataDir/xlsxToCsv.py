import xlrd
import csv

def csv_from_excel(xlsx_filename):
    wb = xlrd.open_workbook('raw_data/' + xlsx_filename + '.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    csv_file = open('data/' + xlsx_filename + '.csv', 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print('Reading from file %s.xlsx' % args.filename)
    csv_from_excel(args.filename)
