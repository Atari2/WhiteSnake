    ; get the first free oam index to use, returns y=0 if failed
	LDY #$00
    -
    LDA $0301|!addr,Y
    CMP #$F0
    BEQ +
    INY #4
	CPY #$FC
    BNE -        ;if Y == 0, kill everything
    +
	RTL
