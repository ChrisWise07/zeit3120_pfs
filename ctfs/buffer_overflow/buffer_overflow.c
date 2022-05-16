#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void winner()
{
    printf("flow changed\n");
}
int main(int argc, char **argv)
{
    char buffer[50];
    strcpy(buffer, argv[1]);
    printf("exit\n");
}