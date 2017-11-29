
/*
Arti Patankar, Jun Kai Ong
604594513, 604606304
artipatankar@ucla.edu, junkai@g.ucla.edu
*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <getopt.h>
#include <time.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include "ext2_fs.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>

#define BLOCKSIZE 1024

int ifd;
char* filename;

int block_consistency_summary(){
	int inode_num;

	int res = scanf("INODE,%d, %[^,], %[^,], %[^,], %d, %f\n",&inode_num, &addr, &city, &state, &zip, &amt);	
	

}




int main(int argc, char* argv[]) {
	filename = NULL; 
	if(argc != 2) {
		fprintf(stderr, "Correct usage: ./lab3b [filename]\n");
		exit(1);
	}
	
	filename = (char*)malloc(strlen(argv[1]) + 1);
	filename = argv[1];

	ifd = open(img_file, O_RDONLY);
	int errRead = errno;

	if(ifd < 0) {
		fprintf(stderr, "ERROR opening image file. Failed to open %s\n", img_file);
		fprintf(stderr, "%s\n", strerror(errRead));
		exit(1);
	}
	exit(0);
	// Block Consistency Audits
		
}
	
