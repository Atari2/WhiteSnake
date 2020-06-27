PHB : PHK : PLB
LDA !14E0,x 	
XBA
LDA !E4,X			; load 16 bit x-position in A	
REP #$20
SEC : SBC.w $1A
STA $00				; store in $00, $01
CLC : ADC.w #$0040	; add #$0040 (why this value?)
CMP.w #$0180		; cmp to 0180? what is the function of this CMP if there's no branch after it
SEP #$20			
LDA $01				; load low byte of x position (subtracted and + 0040)
BEQ +				
LDA #$01			; if not zero, load #$01 instead to set the h offscreen flag
+
STA !15A0,X
TDC					; no idea what this does
ROL A				; or this
STA !15C4,x			; store this into another weird offscreen flag
BNE invalid

LDA !14D4,X			; what the actual fuck is going on here
XBA
LDA !190F,X			; why 190F
AND #$20
BEQ CheckOnce
CheckTwice:        ; this label appears unused? not sure why it's here
LDA !D8,x			; load low byte of Y pos
REP #$21			; go into 16 bit, but why 21?
ADC.w #$001C		; add something without CLC ?
SEC : SBC.w $1C		; subtract layer 1 Y position
SEP #$20	
LDA !14D4,X			; load high byte again?
XBA 				
BEQ CheckOnce		; something something
LDA #$02			; set the offscreen Y flag		
CheckOnce:
STA !186C,X			; sprite off screen flag
LDA !D8,X
REP #$21			; again #21?
ADC.w #$000C		
SEC : SBC.w $1C		; subtract the layer 1 Y position AGAIN?
SEP #$21
SBC #$0C			
STA $01				; this is all mystery math
XBA
BEQ OnScreenY
INC !186C,X			; 186C again, for some reason
OnScreenY:
PLB
RTL

invalid:        
LDY #$FF        	; i modified this because I don't need to kill any banks or stuff
PLB
RTL