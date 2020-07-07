CODE_04FE90:					;| Routine to update overworld sprite low positions.
	TXA							;|
	CLC							;|
	ADC.b #$20					;|
	TAX							;|
	JSL CODE_04FEAB				;| Run for Z position.
	LDA.w !0E35,X				;|
	BPL CODE_04FEA0				;|
	STZ.w !0E35,X				;|
CODE_04FEA0:					;|
	TXA							;|
	SEC							;|
	SBC.b #$10					;|
	TAX							;|
	JSL CODE_04FEAB				;| Run for Y position.
	LDX.w !0DDE					;| Run for X position.
CODE_04FEAB:					;|
	LDA.w !0E95,X				;|\
	ASL							;||
	ASL							;||
	ASL							;|| Update fraction bits.
	ASL							;||
	CLC							;||
	ADC.w !0EC5,X				;||
	STA.w !0EC5,X				;|/
	LDA.w !0E95,X				;|
	PHP							;|
	LSR							;|
	LSR							;|
	LSR							;|
	LSR							;|
	LDY.b #$00					;|
	PLP							;|
	BPL CODE_04FEC9				;|
	ORA.b #$F0					;|
	DEY							;|
CODE_04FEC9:					;|
	ADC.w !0E35,X				;|\
	STA.w !0E35,X				;||
	TYA							;|| Update sprite position.
	ADC.w !0E65,X				;||
	STA.w !0E65,X				;|/
	RTL							;|