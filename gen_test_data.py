# The MIT License (MIT)
# 
# Copyright (c) 2014 George Koodarappally
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import string
import random
import argparse
import sys


MAX_COL_SIZE=65535

col_data = ''

def gen_column_data(col_size):
    if col_size > MAX_COL_SIZE:
        col_size = MAX_COL_SIZE
    return string.zfill('0', col_size)

def gen_col_header(num_cols, delimiter):
    column_header = []
    for i in range(num_cols):
        col_name = 'FIELD_NAME_'+str(i)
        column_header.append(col_name)
    col_header = delimiter.join(column_header)
    return col_header

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

def gen_test_data(output_file, num_rows, num_cols, col_size, delimiter):
    col_header =  gen_col_header(num_cols, delimiter)
    output_file.write(col_header+'\n')
    for i in range(num_rows):
        row_data =  gen_line(num_cols, col_size, delimiter)
        output_file.write(row_data+'\n')

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Generate test data for analyze_this.')
    parser.add_argument('-r', '--rows', default=1000, type=int, help='number of rows')
    parser.add_argument('-c', '--columns', default=10, type=int, help='number of columns')
    parser.add_argument('-s', '--column_size', default=255, type=int, help='max column size')
    parser.add_argument('-d', '--delimiter', default='|', help='column delimiter',
            choices=['|', ','])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    #print('Rows: %d Columns: %d Column-Size: %d Delimiter %s' % (args.rows, args.columns, args.column_size, args.delimiter))

    gen_test_data(args.outfile, args.rows, args.columns, args.column_size, args.delimiter)
