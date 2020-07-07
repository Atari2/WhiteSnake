CODE_04FE62:					;| Routine to store relative overworld sprite positions into $00 and $02.
	TXA							;|  Basically GetDrawInfo for overworld sprites.
	CLC							;|
	ADC.b #$10					;|
	TAX							;|
	LDY.b #$02					;|\ Run for Y position.
	JSL CODE_04FE7D				;|/
	LDX.w !0DDE					;|
	LDA $02						;|\ 
	SEC							;||
	SBC.w !0E55,X				;|| Factor in Z position to the relative Y position.
	STA $02						;||
	BCS CODE_04FE7B				;||
	DEC $03						;|/
CODE_04FE7B:					;|
	LDY.b #$00					;| Run for X position.
CODE_04FE7D:					;|
	LDA.w !0E65,X				;|
	XBA							;|
	LDA.w !0E35,X				;|
	REP #$20					;|\ 
	SEC							;|| $00 = X position onscreen
	SBC.w $1A,Y					;|| $02 = Y position onscreen
	STA $00,Y			        ;||
	SEP #$20					;|/
	RTL							;|