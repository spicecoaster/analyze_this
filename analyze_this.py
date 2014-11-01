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

num_cols = 0
col_max_size = []

def get_columns_from_header(row, delimiter):
    global num_cols

    col_headers = row
    num_cols = len(col_headers.split(delimiter))
    for i in range(num_cols):
        col_max_size.append(0)
    #print col_headers
    #print num_cols

def get_column_sizes(row, delimiter):
    row_data = row.split(delimiter)
    for i in range(num_cols):
        if (len(row_data[i]) > col_max_size[i]):
            col_max_size[i] = len(row_data[i])
    pass

def generate_CREATE_sql():
    pass

def analyze_row(row, delimiter):
    get_column_sizes(row, delimiter)
    pass

def analyze_file(input_file, output_file, row_delimiter, column_delimiter):
    global col_max_size

    first_line = True
    for line in input_file:
        if (first_line):
            get_columns_from_header(line.rstrip(), column_delimiter)
            first_line = False
        else:
            analyze_row(line.rstrip(), column_delimiter)
    print col_max_size
    generate_CREATE_sql()

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Analyze data file to determine CREATE SQL for target table.')
    parser.add_argument('-r', '--row_delimiter', default='\\n', help='row delimiter')
    parser.add_argument('-c', '--column_delimiter', default='|', help='column delimiter')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    #print('Rows: %d Columns: %d Column-Size: %d Delimiter %s' % (args.rows, args.columns, args.column_size, args.delimiter))

    analyze_file(args.infile, args.outfile, args.row_delimiter, args.column_delimiter)
