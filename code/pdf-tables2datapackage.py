import camelot
import os

cwd = os.getcwd()
print(cwd)
os.chdir('../data/raw')

cwd = os.getcwd()
print(cwd)

tables = camelot.read_pdf('MagnardSM.pdf', pages='22,23,24,25',flavor='stream',split_text=True)
print(tables)

tables.export('science.csv', f='csv', compress=False)

data=tables[0].df
print(data)

