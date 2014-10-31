import string
import random
import argparse


MAX_COL_SIZE=65535

col_data = ''

def gen_column_data(col_size):
    if col_size > MAX_COL_SIZE:
        col_size = MAX_COL_SIZE
    return string.zfill('0', col_size)

def gen_line(num_cols, col_size, delimiter):
    global col_data
    if len(col_data) == 0: #Avoid calling gen_column_data more than once
        col_data =  gen_column_data(col_size)
    row_column = []

    for i in range(num_cols):
        col_data_len = random.randint(0, col_size)
        row_column.append(col_data[:col_data_len])

    row_data = delimiter.join(row_column)
    return row_data
    

def gen_test_data(num_rows, num_cols, col_size, delimiter):
    for i in range(num_rows):
        row_data =  gen_line(num_cols, col_size, delimiter)
        print 'Line %s %s' % (i, row_data)

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Generate test data for analyze_this.')
    parser.add_argument('-r', '--rows', default=1000000, type=int, help='number of rows')
    parser.add_argument('-c', '--columns', default=100, type=int, help='number of columns')
    parser.add_argument('-s', '--column_size', default=255, type=int, help='max column size')
    parser.add_argument('-d', '--delimiter', default='|', help='column delimiter',
            choices=['|', ','])
    args = parser.parse_args()

    print('Rows: %d Columns: %d Column-Size: %d Delimiter %s' % (args.rows, args.columns, args.column_size, args.delimiter))

    gen_test_data(args.rows, args.columns, args.column_size, args.delimiter)
