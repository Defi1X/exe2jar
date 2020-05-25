import argparse as ap
import progressbar
import os
import math

parser = ap.ArgumentParser(description='Jar2exe extracter')
parser.add_argument('file', type=str, help='File to process')
args = parser.parse_args()

try:
    inputFile = open(args.file,'rb')
    inputFile.close()
except FileNotFoundError:
    print("No such file!")
    exit()



inputFileLenth = os.stat(args.file).st_size
outputFilename = args.file[0:-4] + '.jar'
outputFile = open(outputFilename, 'wb')

coping = False

fourBytes = []
jarMagicNumbers = [b'\x50', b'\x4b', b'\x03', b'\x04']

print('Starting processing', args.file)

bar = progressbar.ProgressBar().start()

with open(args.file, 'rb') as inputFile:
    byte = inputFile.read(1)
    while byte:
        updateFor = inputFile.tell() // inputFileLenth
        bar.update(updateFor)
        #print('Byte: ', byte)
        if coping == False:
            if len(fourBytes) == 4:
                #print("coping false, buffer full")
                if fourBytes == jarMagicNumbers:
                    #print('YEP THATS FUCKING WHAT WE WANT')
                    coping = True
                    outputFile.write(b'\x50')
                    outputFile.write(b'\x4b')
                    outputFile.write(b'\x03')
                    outputFile.write(b'\x04')
                #print('so, ', fourBytes, ' != ', jarMagicNumbers)
                #print('pop and append new')
                fourBytes.pop(0)
                fourBytes.append(byte)
            else:
                #print('len = ', len(fourBytes),' just adding new')
                fourBytes.append(byte)
        else:
            #print('writing byte to exit file:', byte)
            outputFile.write(byte)
        byte = inputFile.read(1)

bar.finish()
print('Closing files...')

inputFile.close()
outputFile.close()

print('All done!')