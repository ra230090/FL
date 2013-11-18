#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
static unsigned long long s_i=0;
#ifdef __cplusplus
        extern "C" void __gcov_flush();
#endif
void my_handler(int signum)
{
    //printf("received signal:%llu\n",s_i);
    __gcov_flush();
}

__attribute__((constructor)) static void _bar()
{
	//printf("bar\n");

	struct sigaction new_action,old_action;
	new_action.sa_handler = my_handler;
	sigemptyset(&new_action.sa_mask);
	new_action.sa_flags = 0;
	sigaction(SIGUSR1,NULL,&old_action);
	if(old_action.sa_handler != SIG_IGN)
		sigaction(SIGUSR1,&new_action,NULL);
}

