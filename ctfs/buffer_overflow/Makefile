all: elf32

target: elf32
elf32: buffer_overflow.c
	gcc -O0 -fno-builtin -fno-stack-protector -m32 -Wall -std=c11 -ggdb -z execstack -o buffer_overflow.out buffer_overflow.c

target: clean
clean: buffer_overflow.out
	rm buffer_overflow.out

