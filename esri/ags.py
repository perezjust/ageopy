import os
import sys
from collections import defaultdict

#local libs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from util import filesys


class GPErrorDict(object):
    
    def __init__(self):
        '''
            Group errors so they can be reported in organized way
            useful when try/excepting through a geoprocessing operation
            against items
        '''
        self.errordict = defaultdict(list)
        

    def add(self, messagelist):
        error = messagelist[0]
        item = messagelist[1]
        self.errordict[error].append(item)


    def write_to_disk(self, outputfolder):
        errorfile = os.path.join(outputfolder, "error_" + filesys.get_nice_date("Alt") + ".txt")
        with open(errorfile, 'w') as outfile:
            for dictitem in self.errordict:
                outfile.write(str(dictitem) + '\n')
                for listitem in self.errordict[dictitem]:
                    outfile.write(str(listitem) + '\n')
                outfile.write('\n')
                outfile.write("+" * 100)
                outfile.write('\n')
        return errorfile

        
