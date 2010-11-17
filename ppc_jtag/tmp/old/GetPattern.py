#! /usr/bin/env python

from optparse import OptionParser
import csv, numpy, string
import sys

def ReadInputData(infile, pattern_length):

    # Read data from input file
    try:
        fin = open(infile, "rb")
    except IOError:
        print "Unable to open file:", infile
        sys.exit(1)
        fin.close()
    reader = csv.reader(fin)

    header = reader.next()
    columns = zip(*reader)

    data_dictionary = {}
    for index in range(0,len(columns)):
        data_dictionary[string.upper(header[index])] = columns[index]

    fin.close()

    return data_dictionary


def ProcessData(data_array, pattern_length):
    data_length = len(data_array)
    nr_rows = data_length / pattern_length
    patterns = numpy.array(data_array[:int(nr_rows*pattern_length)]).reshape(nr_rows, pattern_length)

    pattern_dictionary = {}
    for pattern in patterns:
        pattern_key = "".join(pattern)
        if pattern_dictionary.has_key(pattern_key):
            pattern_dictionary[pattern_key] += 1
        else:
            pattern_dictionary[pattern_key] = 1

    return pattern_dictionary



if __name__ == '__main__':

    usage = "%prog [options] <input_file_name>.csv"

    parser = OptionParser(usage=usage, version="%prog 0.1")
    parser.add_option('-l', '--length',
                      dest='pattern_length',
                      default=4,
                      help='Specify length of binary pattern [default=%default]')
    parser.add_option('-c', '--column',
                      dest='pattern_column',
                      default='TMS',
                      help='Column that will be used to construct pattern [default=%default]')
    # Parse options
    (opts, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    # Read in measured data file
    infile = args[0]
    data_dictionary = ReadInputData(infile, opts.pattern_length)

    # extract and process the data according to user input
    print "The following headings are available for selection: ",
    for key in data_dictionary.keys():
        print key +",",
    print
    print "Type <ENTER> to use default", opts.pattern_column
    print "Or type \'q\' to quite\n"
    user_input = raw_input("Please type selected heading: ")
    if len(user_input) > 0:
        opts.pattern_column = user_input
    opts.pattern_column = string.upper(opts.pattern_column)
    print "Processing patterns using column", opts.pattern_column, \
          "\nUsing pattern length", opts.pattern_length

    pattern_dictionary = {}
    if data_dictionary.has_key(opts.pattern_column):
        pattern_dictionary = ProcessData(data_dictionary[opts.pattern_column], int(opts.pattern_length))

    for key in pattern_dictionary.keys():
        print "Pattern", key, "appeard", pattern_dictionary[key], "times"

# fin
