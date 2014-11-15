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
import types
import datetime

"""
MySQL: INTEGER, DATE, DATETIME, VARCHAR(Max: 65535), TEXT (Max: 2^16), MEDIUMTEXT (Max: 2^24), LONGTEXT (Max: 2^32)
PostgreSQL: INTEGER (4 Bytes), BIGINT (8 Bytes), NUMERIC (Before Decimal: 131072, Precision: 16383), DATE, TIMESTAMP, VARCHAR (Max: 1 GB), TEXT (Max: unlimited)
SQLite: INTEGER, NUMERIC, REAL, TEXT
Microsoft SQL Server: INT, NUMERIC, DATE, DATETIME, VARCHAR, TEXT
Oracle: NUMBER (Total: 10^125, Precision: 38), DATE, VARCHAR2 (Max: 4000), CLOB (Max 128 TB)
"""

num_cols = 0
col_names = []
col_max_size = []
col_type = []
create_table_sql = ''

def get_columns_from_header(row, delimiter):
    global col_names, num_cols, col_type, col_max_size

    col_headers = row
    col_names  = col_headers.split(delimiter)
    num_cols = len(col_names)
    for i in range(num_cols):
        col_max_size.append(0)
        col_type.append('TEXT')
    #print col_headers
    #print num_cols

def get_column_sizes(row, delimiter):
    global col_max_size
    row_data = row.split(delimiter)
    for i in range(num_cols):
        if (len(row_data[i]) > col_max_size[i]):
            col_max_size[i] = len(row_data[i])

def get_column_types(row, delimiter):
    global col_type
    row_data = row.split(delimiter)
    for i in range(num_cols):
        if (isinstance(row_data[i], (types.IntType, types.FloatType, types.LongType, types.ComplexType))):
            col_type[i] = 'NUMBER'
        if (isinstance(row_data[i], (types.StringTypes))):
            col_type[i] = 'TEXT'
        if (isinstance(row_data[i], (datetime.datetime))):
            col_type[i] = 'DATETIME'
        if (isinstance(row_data[i], (datetime.date))):
            col_type[i] = 'DATE'

def generate_CREATE_sql():
    sql = 'CREATE TABLE AAA (\n'
    for i in range(num_cols):
        sql = sql + '\t' + col_names[i] + '\t' + col_type[i] + ',\n'
    sql = sql + ')'
    return sql

def analyze_row(row, delimiter):
    global create_table_sql

    get_column_sizes(row, delimiter)
    get_column_types(row, delimiter)

def analyze_file(input_file, output_file, row_delimiter, column_delimiter):
    global col_max_size

    first_line = True
    for line in input_file:
        if (first_line):
            get_columns_from_header(line.rstrip(), column_delimiter)
            first_line = False
        else:
            analyze_row(line.rstrip(), column_delimiter)
    create_table_sql = generate_CREATE_sql()
    print col_names
    print col_max_size
    print col_type
    print create_table_sql

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Analyze data file to determine CREATE SQL for target table.')
    parser.add_argument('-r', '--row_delimiter', default='\\n', help='row delimiter')
    parser.add_argument('-c', '--column_delimiter', default='|', help='column delimiter')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    #print('Rows: %d Columns: %d Column-Size: %d Delimiter %s' % (args.rows, args.columns, args.column_size, args.delimiter))

    analyze_file(args.infile, args.outfile, args.row_delimiter, args.column_delimiter)
