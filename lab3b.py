#!/usr/bin/python

# Arti Patankar, Jun Kai Ong
# 604594513, 604606304
# artipatankar@ucla.edu, junkai@g.ucla.edu

import sys


duplicate_blocks = []

def process_block(free_blocks, block, group_num, n_blocks, inode_num, block_level, n_inodes, offset, flag = False):
	if (not flag):
		offset = 0
		if (block_level == " INDIRECT"):
			offset += 12
		elif (block_level == " DOUBLE INDIRECT"):
			offset += 12 + 256
		elif (block_level == " TRIPLE INDIRECT"):
			offset += 12 + 256 + 256*256 

	# check for invalid blocks
	if (block < 0 or block > n_blocks):
		sys.stdout.write("INVALID" + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
    
	# check for reserved blocks
	if (block < group_num * 8192 + 4 + n_inodes):
		sys.stdout.write("RESERVED" + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
    
	# check for unreferenced blocks
	if (block == 0 and block not in free_blocks):
		sys.stdout.write("UNREFERENCED" + block_level + " BLOCK " + str(block) + "\n")



def duplicate_block(block, group_num, n_blocks, inode_num, block_level, offset, flag = False):	
	if (not flag):
		offset = 0
		if (block_level == " INDIRECT"):
			offset += 12
		elif (block_level == " DOUBLE INDIRECT"):
			offset += 12 + 256
		elif (block_level == " TRIPLE INDIRECT"):
			offset += 12 + 256 + 256*256 
	
	sys.stdout.write("DUPLICATE" + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
	
	for b in duplicate_blocks:
		if (b[0] == block):
			inode_num = b[1]
			offset = b[3]
			if (b[2] == 1):
				block_level = " INDIRECT"
			elif (b[2] == 2):
				block_level = " DOUBLE INDIRECT"
			elif (b[2] == 3):
				block_level = " TRIPLE INDIRECT"
			else:
				block_level = ""
	offset = 0
	if (block_level == " INDIRECT"):
		offset += 12
	elif (block_level == " DOUBLE INDIRECT"):
		offset += 12 + 256
	elif (block_level == " TRIPLE INDIRECT"):
		offset += 12 + 256 + 256*256 
	sys.stdout.write("DUPLICATE" + block_level + " BLOCK " + str(block) + " IN INODE " + str(inode_num) + " AT OFFSET " + str(offset) + "\n")
	
def block_audit(lines):
	#inode_size
	#block_size
	n_blocks = 0
	n_inodes = 0
	group_num = 0
	free_blocks = []
	allocated_blocks = []
	for line in lines:
        	offset = 0
        	line = line.split(',')
        	if (line[0] == 'SUPERBLOCK'):
            		inode_size = int(line[4])
			block_size = int(line[3])
        	if (line[0] == 'BFREE'):
			free_blocks.append(int(line[1]))
        	if (line[0] == 'GROUP'):
			group_num = int(line[1])
			n_inodes = int (line[3]) 
			n_blocks = int(line[2])
        	if (line[0] == "INODE"):
			inode_num = int(line[1])                       
            		# process direct blocks
            		for i in range(12, 24):
                		block = int(line[i])
				if (block != 0):
                			process_block(free_blocks, block, group_num, n_blocks, inode_num, "", n_inodes * (inode_size / block_size), 0)
                		if (block not in allocated_blocks):
            	    			allocated_blocks.append(block)
					entry = []
					entry.append(block)
					entry.append(inode_num)
					entry.append(i-12)
					entry.append(0)
					duplicate_blocks.append(entry)
                		elif (block != 0):
                    			duplicate_block(block, group_num, n_blocks, inode_num, "", 0)
            		
			# process single indirect block
            		block = int(line[24])
            		if (block != 0):
				process_block(free_blocks, block, group_num, n_blocks, inode_num, " INDIRECT", n_inodes * (inode_size / block_size), 0)
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
				entry = []
				entry.append(block)
				entry.append(inode_num)
				entry.append(1)
				duplicate_blocks.append(entry)
            		elif (block != 0):
                		duplicate_block(block, group_num, n_blocks, inode_num, " INDIRECT", 0)
                               
            		# process double indirect block
            		block = int (line[25])
            		if (block != 0):
				process_block(free_blocks, block, group_num, n_blocks, inode_num, " DOUBLE INDIRECT", n_inodes * (inode_size / block_size), 0)
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
				entry = []
				entry.append(block)
				entry.append(inode_num)
				entry.append(2)
				duplicate_blocks.append(entry)
            		elif (block != 0):
                		duplicate_block(block, group_num, n_blocks, inode_num, " DOUBLE INDIRECT", 0)
                               
            		# process triple indirect block
            		block = int (line[26])
			if (block != 0):
				process_block(free_blocks, block, group_num, n_blocks, inode_num, " TRIPLE INDIRECT", n_inodes * (inode_size / block_size), 0)
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
				entry = []
				entry.append(block)
				entry.append(inode_num)
				entry.append(3)
				duplicate_blocks.append(entry)
            		elif (block != 0):
                		duplicate_block(block, group_num, n_blocks, inode_num, " TRIPLE INDIRECT", 0)
		if (line[0] == "INDIRECT"):
			block = int(line[5])
			level = int(line[2])
			inode_num = int(line[1])
			level_indirection = ""
			offset = int(line[3])
			if (level == 1):
				level_indirection = "INDIRECT"
			elif (level == 2):
				level_indirection = "DOUBLE INDIRECT"
			elif (level == 3):
				level_indirection = "TRIPLE INDIRECT"
			process_block(free_blocks, block, group_num, n_blocks, inode_num, level_indirection, n_inodes * (inode_size / block_size), offset, True)
			
            		if (block not in allocated_blocks):
                		allocated_blocks.append(block)
				entry = []
				entry.append(block)
				entry.append(inode_num)
				entry.append(level)
				duplicate_blocks.append(entry)
            		elif (block != 0):
                		duplicate_block(block, group_num, n_blocks, inode_num, level_indirection, offset, True)

	for block in allocated_blocks:
		if (block in free_blocks):
			sys.stdout.write("ALLOCATED BLOCK " + str(block) + " ON FREELIST" + "\n");	

	for i in range(5 + n_inodes, n_blocks):
		if (i not in allocated_blocks and i not in free_blocks):
			sys.stdout.write("UNREFERENCED BLOCK " + str(i) + '\n')

def inode_audit(lines):
	#inode_size
	first_inode = 0
	last_inode = 0
	free_inodes = []
	allocated_inodes = []

	for line in lines:
        	line = line.split(',')
        	if (line[0] == "SUPERBLOCK"):
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
                        
def dir_audit(lines):
	allocated_inodes = []
	dir_links = []	
	for line in lines:
		line = line.split(',')
		if (line[0] == "SUPERBLOCK"):
			first_inode = int(line[7])
			last_inode = int(line[6])
		if (line[0] == "INODE"):
			allocated_inodes.append(int(line[1]))
		if (line[0] == "DIRENT"):
			dir_links.append(int(line[3]))
	
	for line in lines:
		line = line.split(',')
		if (line[0] == "INODE"):
			inode_num = int(line[1])	
			
			# link consistency
			links = dir_links.count(inode_num)
			link_count = int(line[6]) 
			if (links != link_count):
				sys.stdout.write("INODE " + str(inode_num) + " HAS " + str(links) + " LINKS BUT LINKCOUNT IS " + str(link_count) + "\n")	
		if (line[0] == "DIRENT"):
			parent_num = int(line[1])
                        inode_num = int(line[3])
			name = line[6]
                        if (inode_num not in allocated_inodes):
				# inode allocation if inode_num is valid
				if (inode_num in range(first_inode, last_inode)):
                                	sys.stdout.write("DIRECTORY INODE " + str(parent_num) + " NAME " + line[6] + " UNALLOCATED INODE " + str(inode_num) + "\n")
				# inode validity
				else:
					sys.stdout.write("DIRECTORY INODE " + str(parent_num) + " NAME " + line[6] + " INVALID INODE " + str(inode_num) + "\n")

			if (name == "\'.\'" and parent_num != inode_num):
				sys.stdout.write("DIRECTORY INODE " + str(parent_num) + " NAME " + line[6] + " LINK TO INODE " + str(inode_num) + " SHOULD BE " + str(parent_num) + "\n")

			if (name == "\'..\'"):
				if (parent_num == 2):
					if (inode_num != 2):
						sys.stdout.write("DIRECTORY INODE " + str(parent_num) + " NAME " + name + " LINK TO INODE " + str(inode_num) + " SHOULD BE " + str(parent_num) + "\n")

				elif (parent_num != 2):
					# look for parent directory by traversing the lines to find a directory where the referenced inode (line[3]) is parent_num, then inode_num should be the parent inode (line[1])
					for line in lines:
						line = line.split(',')
						# exclude the "." directory from the search for the parent directory
						if (line[0] == "DIRENT" and line[6] != "\'.\'" and line[3] == str(parent_num) and line[1] != str(inode_num)):
							sys.stdout.write("DIRECTORY INODE " + str(parent_num) + " NAME " + name + " LINK TO INODE " + str(inode_num) + " SHOULD BE " + line[1] + "\n")  
 
def main():
	if (len(sys.argv) != 2):
		sys.stderr.write("Error: Invalid number of arguments" + "\n")
		exit(1)
	filename = sys.argv[1]
    	try: 
		fo = open(filename, "r+")
    	except IOError as e:
		sys.stderr.write('Error: cannot open file ' + filename + "\n")
		exit(1)
	lines = fo.read().split('\n') # lines of csv file
	block_audit(lines)
	inode_audit(lines)  
	dir_audit(lines)
if __name__ == "__main__":
    main()
