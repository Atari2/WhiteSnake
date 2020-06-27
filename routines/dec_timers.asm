; 1540, 154C, 1558, 1564, 15AC, 163E, 1FE2

LDX #!SprSize-1
loop:
LDA !1540,x
BEQ +
DEC !1540,x
+
LDA !154C,x
BEQ +
DEC !154C,x
+
LDA !1558,x
BEQ +
DEC !1558,x
+
LDA !1564,x
BEQ +
DEC !1564,x
+
LDA !15AC,x
BEQ +
DEC !15AC,x
+
LDA !163E,x
BEQ +
DEC !163E,x
+
LDA !1FE2,x
BEQ +
DEC !1FE2,x
+
DEX
BPL loop
RTL
