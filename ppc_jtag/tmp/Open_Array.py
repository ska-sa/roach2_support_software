#!/usr/bin/python
import csv
import string
import sys

def open_file_to_array(in_file):
  
  #read data from input file
  try:
    file_in = open(in_file, 'rb')
    #print 'File opened succsesfully'
  except IOError:
    print 'Unable to open file:', in_file
    sys.exit(1)
    file_in.close()
  reader = csv.reader(file_in)

  header = reader.next()
  #print header
  columns = zip(*reader)
  #print columns

  data_dictionary = {}
  for index in range(0, len(columns)):
    data_dictionary[string.upper(header[index])] = columns[index]

  file_in.close()

  #print data_dictionary
  return data_dictionary

  #main
if __name__ == '__main__':
  input_file = 'temp_file.csv'
  data_dictionary = open_file_to_array(input_file)
  
  #endof main
