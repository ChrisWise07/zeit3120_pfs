#include <stdio.h>
#include <string.h>
int main(int argc, char **argv)
{
    // Make a buffer
    char buffer[500];
    // copy cmdline input into the buffer.
    strcpy(buffer, argv[1]);
    // return 0 because that is what we do if stuff exits normally.
    return 0;
}
