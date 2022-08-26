# Muffin
A custom LSB steganography method

## How does it work
This method essentially functions the same as a conventional LSB method, except for 2 key differences:

- The first few pixels in the image is a header, which contains data of where the bits are hidden, such as the length of the message and the length of the header
- The header also stores information about the step, or the interval of pixels containing the message bits

## How does the key work
The key is just 3 numbers in the range of 1 to 255. The positions of the header is as follows:

`(message_length, step, header_length)`

The key is simply added to these values (e.g. The message length is 100 bits and the first number in the key is `15`, then the value is 100 + 15 = 115)

If the key exceeds 255, the value is determined as follows:
- Get the quotient and remainder of value / key
- Remainder is stored in the first pixel, quotient is stored in the next one
- If remainder is more than 255, then divide it by the key and continue

As such, the header can span across more than 1 pixel.

## Disclaimer
This is still rather insecure and I don't recommend using it as an actual encryption method, it's just cool.

## Vulnerabilities
- The length of the header can be easily deduced since it most likely will look different from the surrounding pixels
- If the original image is found, the step and message length also can be found and the key would be easily broken

## Limitations
- Only supports images with 3 channels i.e. RGB
- Current implementation is not optimised, especially the encoder

## To-Do
- Improve current implementation
- Implement running as a command