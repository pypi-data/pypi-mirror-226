#include <stdio.h>
#include <unistd.h>
int main() {
   // printf() displays the string inside quotation
   printf("Hello, World!, sleeping...\n");
   int i;
   for(i=0;i<15;i++){
     sleep(1);
     printf("i:%d\n", i);
   }

   printf("\nExecuted successfully\n");
   return 0;
}
