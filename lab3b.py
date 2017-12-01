#!/usr/bin/python

# Arti Patankar, Jun Kai Ong
# 604594513, 604606304
# artipatankar@ucla.edu, junkai@g.ucla.edu

import sys
def process_block(free_blocks, block, group_num, n_blocks, inode_num, block_level):
	offset = block - group_num * 8192

	# check for invalid blocks
	if (block < 0 or block > n_blocks):
		sys.stdout.write("INVALID " + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
    
	# check for reserved blocks
	if (block <= group_num * 8192 + 218 and block >= group_num * 8192):
		sys.stdout.write("RESERVED " + block_level + " BLOCK " + str(block) + " IN NODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
    
	# check for unreferenced blocks
	if (block == 0 and block not in free_blocks):
		sys.stdout.write("UNREFERENCED " + block_level + " BLOCK " + str(block) + "\n")

def duplicate_block(block, group_num, n_blocks, inode_num, block_level):
	offset = block - group_num * 8192
	sys.stdout.write("DUPLICATE " + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
    
def block_audit(lines):
	#inode_size
	#block_size
	#n_blocks
	#group_num
	free_blocks = []
	allocated_blocks = []

	for line in lines:
        	offset = 0
        	line = line.split(',')
        	if (line[0] == 'SUPERBLOCK'):
            		inode_size = int(line[4])
            		n_blocks = int(line[5])
        	if (line[0] == 'BFREE'):
			free_blocks.append(int(line[1]))
        	if (line[0] == 'GROUP'):
			group_num = int(line[1])
        	if (line[0] == "INODE"):
			inode_num = int(line[1])
            		link_count = int(line[6])
                               
            		# process direct blocks
            		for i in range(12, 27):
                		block = int(line[i])
                		process_block(free_blocks, block, group_num, n_blocks, inode_num, "")
                		if (block not in allocated_blocks):
            	    			allocated_blocks.append(block)
                		else:
                    			duplicate_block(block, group_num, n_blocks, inode_num, "")
            		
			# process single indirect block
            		block = int(line[24])
            		process_block(free_blocks, block, group_num, n_blocks, inode_num, "INDIRECT")
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
            		else:
                		duplicate_block(block, group_num, n_blocks, inode_num, "INDIRECT")
                               
            		# process double indirect block
            		block = int (line[25])
            		process_block(free_blocks, block, group_num, n_blocks, inode_num, "DOUBLE INDIRECT")
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
            		else:
                		duplicate_block(block, group_num, n_blocks, inode_num, "DOUBLE INDIRECT")
                               
            		# process triple indirect block
            		block = int (line[26])
			process_block(free_blocks, block, group_num, n_blocks, inode_num, "TRIPLE INDIRECT")
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
            		else:
                		duplicate_block(block, group_num, n_blocks, inode_num, "TRIPLE INDIRECT")
            
      
def inode_audit(lines):
	#inode_size
	#first_inode
	free_inodes = []
	allocated_inodes = []

	for line in lines:
        	line = line.split(',')
        	if (line[0] == 'SUPERBLOCK'):
            		inode_size = int(line[4])
            		first_inode = int(line[7])
			last_inode = int(line[6])
        	if (line[0] == "IFREE"):
        		free_inodes.append(int(line[1]))	
        	if (line[0] == "INODE"):
            		# check if allocated inode in free inode list
            		inode_num = int(line[1])
            		allocated_inodes.append(inode_num)
			if (inode_num in free_inodes):
            			sys.stdout.write("ALLOCATED INODE " + str(inode_num) + " ON FREELIST" + "\n")
 
	# check if unallocated nodes not in free inode list
	for i in range(first_inode, last_inode):
    		if (i not in allocated_inodes and i not in free_inodes):
        		sys.stdout.write("UNALLOCATED INODE " + str(i) + " NOT ON FREELIST" + "\n")  
                         
def main():
	if (len(sys.argv) != 2):
		sys.stderr.write("Error: Invalid number of arguments" + "\n")
	filename = sys.argv[1]
    	try: 
		fo = open(filename, "r+")
    	except IOError as e:
		sys.stderr.write('Error: cannot open file ' + filename + "\n")
	lines = fo.read().split('\n') # lines of csv file
	block_audit(lines)
	inode_audit(lines)  

if __name__ == "__main__":
    main()
