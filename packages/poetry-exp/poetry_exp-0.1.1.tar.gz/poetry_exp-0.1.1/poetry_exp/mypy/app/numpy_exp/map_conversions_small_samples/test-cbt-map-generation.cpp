    #include <stdlib.h>
    #include <errno.h>
    #include <stdio.h>
    #include <inttypes.h>
    #include <string.h>
    #include <stdarg.h>
    #include <fcntl.h>
    #include <unistd.h>
    #include <iostream>
    #include <bits/stdc++.h>
    using namespace std;
    #include <fstream>

    #define VVMAP_BITS_PER_BYTE 8
    #define OFFSET_IN_BYTES(offset)    ((offset) / VVMAP_BITS_PER_BYTE)
    #define FIRST_BYTE_MASK(start) (((uint8_t)(~0U)) << ((start) & (VVMAP_BITS_PER_BYTE - 1)))
    #define LAST_BYTE_MASK(size) (((uint8_t)(~0U)) >> (-(size) & (VVMAP_BITS_PER_BYTE - 1)))


    void setBitMapBuffer(uint8_t *map, unsigned int start, int len)
    {
        uint8_t *p = map + OFFSET_IN_BYTES(start);
        const unsigned int size = start + len;
        std::cout << "size: "<< size <<"\n";

        int total_bits = VVMAP_BITS_PER_BYTE - (start % VVMAP_BITS_PER_BYTE);
        std::cout << "total_bits: "<< total_bits <<"\n";

        uint8_t byte_mask = FIRST_BYTE_MASK(start);
        //std::cout << "byte_mask: "<< byte_mask <<"\n";

        while (len - total_bits >= 0) {
          *p |= byte_mask;
          len -= total_bits;
          total_bits = VVMAP_BITS_PER_BYTE;
          byte_mask = ~0;
          p++;
        }
       //std::cout << "len: "<< len <<"\n";
        if (len) {
          byte_mask &= LAST_BYTE_MASK(size);
          //std::cout << "Insidelen,  byte_mask: "<< byte_mask <<"\n";
          *p |= byte_mask;
        }
    }

   int main () {
       char *buffer = (char*)malloc(255);
       char *token;
       FILE *fp = NULL;
       uint64_t volumeLength = 24; // 42949672960 bytes  vmdk disk size
       uint64_t volumeBlockSize = 2;   // 65536 bytes
       uint64_t blockSize  = volumeBlockSize;
       uint64_t map_length = (volumeLength/blockSize)/VVMAP_BITS_PER_BYTE; // to compress length, otherwise it will be very big
       uint64_t vmware_offset = 0;
       uint64_t vmware_length = 0;
       const char s[2] = ",";
       uint8_t *location = NULL;

       if(location == NULL){
          location = (uint8_t*)malloc(sizeof(uint8_t)*map_length);
          memset(location, 0, map_length);
       }

       fp = fopen("blockinfo", "r");
       if (!fp ) {
          std::cout << "Vmware map file does not exist";
       }

       ofstream outputFile;
       outputFile.open ("bitmap");

       while(fgets(buffer, 255, (FILE*) fp)) {
          token = strtok(buffer, s);
          vmware_offset = (uint64_t)atoll(token);
          token = strtok(NULL, s);
          vmware_length = (uint64_t)atoll(token);
          std::cout << "vmware_offset: "<< vmware_offset << "\tvmware_length: "<< vmware_length<<"\n";
          unsigned int start = vmware_offset/blockSize;
          int length =  vmware_length/blockSize;

          std::cout << "start: "<< start << "\tlength: "<< length<<"\n";
          setBitMapBuffer(location, start, length);
          // start: from where to set
          // length: how many bits to set
          // setBitMapBuffer(location, 0, 9);   1111 1111 1000 0000
       }

       //FILE *fp2 = fopen("bitmap", "w");
       //memcpy(fp2, location, sizeof(uint8_t)*map_length);
       //fclose(fp2);


      int j = 0;
      int k = 0;
      //for(; k<map_length; k++){
      //k = 90615;
      for(; k<map_length; k++){
        uint8_t char_to_print = location[k];
        for (; j<8; j++){
          //std::cout << "" << (char_to_print &  0X01)<<'\t';
          std::cout << "" << (char_to_print &  0X01)<<'\t';
          outputFile << "" << (char_to_print &  0X01)<<'\t';

          char_to_print = char_to_print >> 1;
        }
        j = 0;
        printf("\n\n");
        outputFile << "\n\n";
      }

   out:
   free(buffer);
   fclose(fp);
   outputFile.close();

   return 0;
}
