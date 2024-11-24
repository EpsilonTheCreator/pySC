# pySC opcodes

Binary opcodes:

00000000 ; halt
00000001 ; addnum
00000010 ; subnum
00000011 ; mulnum
00000100 ; divnum
00000101 ; int (interrupts)
00000110 ; set
00000111 ; memload (loads instructions from mem address)
00001000 ; memamount (loads amount of memory in bytes in reg A)
00001001 ; memset (loads hex data into mem address)
00001101 ; lfd (Load from disk)
00001110 ; bootdev (Boots from device)
Every other unused binary opcode ; abtcb (add bytes to compiled binary)

Register opcodes:

A: 00001010
B: 00001011
C: 00001100
CF/CARRY: 11110000

Interrupt codes:
0x01: Shut down
0x06: Set resolution (A x B)
0x07: Print String In reg A

Device opcodes:
0x01 ; Hard disk
0x02 ; CD (can be any size)
0x03 ; Floppy
0x04 ; BIOS


