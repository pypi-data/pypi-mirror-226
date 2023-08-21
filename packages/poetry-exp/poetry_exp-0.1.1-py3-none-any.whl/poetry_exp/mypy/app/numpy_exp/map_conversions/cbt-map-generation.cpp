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

    #define VVMAP_BITS_PER_BYTE 8

    #define OFFSET_IN_BYTES(offset)    ((offset) / VVMAP_BITS_PER_BYTE)
    #define FIRST_BYTE_MASK(start) (((uint8_t)(~0U)) << ((start) & (VVMAP_BITS_PER_BYTE - 1)))
    #define LAST_BYTE_MASK(size) (((uint8_t)(~0U)) >> (-(size) & (VVMAP_BITS_PER_BYTE - 1)))

    //uint8_t *catalystbuffer = (uint8_t *)malloc(2);

    uint8_t catalystbuffer[32];
    void setBitMapBuffer(uint8_t *map, unsigned int start, int len)
    {
        uint8_t *p = map + OFFSET_IN_BYTES(start);
        const unsigned int size = start + len;
        int total_bits = VVMAP_BITS_PER_BYTE - (start % VVMAP_BITS_PER_BYTE);
        uint8_t byte_mask = FIRST_BYTE_MASK(start);

        while (len - total_bits >= 0) {
          *p |= byte_mask;
          len -= total_bits;
          total_bits = VVMAP_BITS_PER_BYTE;
          byte_mask = ~0;
          p++;
        }
        if (len) {
          byte_mask &= LAST_BYTE_MASK(size);
          *p |= byte_mask;
        }
    }

   int main () {
	  // Set first 2 bytes to zero
      catalystbuffer[0] = 0;
      catalystbuffer[1] = 0;
	  // Set the 1st byte and 1st bit of the next byte
      setBitMapBuffer(catalystbuffer, 0, 9);
      //For Printing the array
      int j = 0;
      int k = 0;
      for(; k<2; k++){
        uint8_t char_to_print = catalystbuffer[k];
        for (; j<8; j++){
          std::cout << "" << (char_to_print &  0X01)<<'\t';
           // printf("\n");
          // printf("%i\n", test & 0X01);
          char_to_print = char_to_print >> 1;
        }
        j = 0;
        printf("\n\n");
      }
      return 0;
    }
