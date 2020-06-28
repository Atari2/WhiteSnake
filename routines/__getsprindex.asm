    ; gets the first sprite index to use, returns FF when failed
	LDX #!SprSize
    -
    LDA !14C8,X
    BEQ +
    DEX
    BPL -
    LDX #$FF    ;if not found, set to FF
    +
	TXA
	STA !15E9  
	RTL
