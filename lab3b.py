#! /usr/bin/python

#Arti Patankar, Jun Kai Ong
#604594513, 604606304
#artipatankar@ucla.edu, junkai@g.ucla.edu

import sys

def block_audit(lines):
    inode_size
    block_size
    n_blocks
    free_blocks = []
	for line in lines:
	line = line.split(',')
	if(line[0]=='SUPERBLOCK'):
            inode_size = int(line[4])
        if(line[0]=='BFREE'):
	    free_blocks.append(int(line[1])
	if(line[0]=="INODE"):
	    inode_num = int(lines[1])
	    link_count = int(lines[6])
	#process direct blocks
	    for i in range(12, 24):
		block = int(line[i])
	        if(block==0 && block in free_blocks)	
                    print "Error with free block"
                if(block>n_blocks)
		    print "blocks are out of range"
	#process Single indirect block
	        	
        

def main():
    if(len(sys.argv)!=2):
       	sys.stderr.write ("Error: Invalid number of arguments")
    filename = sys.argv[1]
    try: 
	fo = open(filename, "r+")
    except IOError as e:
	sys.stderr.write('Error opening file'+filename)
    lines = fo.read().split('\n')
    block_audit(lines)    

if __name__ == "__main__":
    main()

