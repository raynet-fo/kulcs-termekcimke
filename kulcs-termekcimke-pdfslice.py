import sys
import os
import csv
from pathlib import Path

# https://stackoverflow.com/questions/490195/split-a-multi-page-pdf-file-into-multiple-pdf-files-with-python
from PyPDF2 import PdfFileWriter, PdfFileReader

import argparse

# parameters
NEV = 0
TERMEKKOD = 1
CIKKSZAM = 2

CSV_DELIMITER = ';'
CSV_INPUT = "input.csv"
PDF_INPUT = "input.pdf"
PDF_DIRECTORY="pages"

parser = argparse.ArgumentParser()
parser.add_argument('-t', action='store_true', default=False, dest='isTest', help='Run in test mode')
results = parser.parse_args()
IS_TEST = results.isTest

with open( PDF_INPUT, "rb" ) as pdf_file:
  pdf_input = PdfFileReader( pdf_file )
  numPages = range( pdf_input.numPages )
  print(f'Number of pages: \t{numPages}' )
  if IS_TEST:
    print(f'RUNNIN IN TEST MODE' )

  if not os.path.exists(PDF_DIRECTORY):
    os.makedirs(PDF_DIRECTORY)

  with open( CSV_INPUT ) as csv_file:
    csv_reader = csv.reader( csv_file, delimiter = CSV_DELIMITER )
    line_count = 0
    for row in csv_reader:
      if IS_TEST and line_count > 5:
        sys.exit(1)
      if line_count == 0:
        print (f'Column names are {", ".join(row)}' )
        line_count += 1
      else:
        print( f'\t{line_count}\t{row[CIKKSZAM]}\t{row[TERMEKKOD]}' )
        pdf_output = PdfFileWriter()
        pdf_output.addPage( pdf_input.getPage( line_count - 1 ) )
        with open( Path(PDF_DIRECTORY ) / ( "%s.pdf" % row[CIKKSZAM] ), "wb" ) as outputStream:
          pdf_output.write( outputStream )
        line_count += 1
    print( f'Processed {line_count} lines.' )
