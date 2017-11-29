
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
char* img_file;
struct ext2_super_block superblock;
struct ext2_group_desc group_desc;

int main(int argc, char* argv[]) {
	img_file = NULL; 
	if(argc != 2) {
		fprintf(stderr, "Correct usage: ./lab3a [filename]\n");
		exit(1);
	}
	
	img_file = (char*)malloc(strlen(argv[1]) + 1);
	img_file = argv[1];

	ifd = open(img_file, O_RDONLY);
	int errRead = errno;

	if(ifd < 0) {
		fprintf(stderr, "ERROR opening image file. Failed to open %s\n", img_file);
		fprintf(stderr, "%s\n", strerror(errRead));
		exit(1);
	}
	exit(0);
}
	
