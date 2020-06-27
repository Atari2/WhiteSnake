; Turning code stolen from Blind Devil's Rounding Boo
; GetDrawInfo stolen from pixi
!MaxXSpd = $06
!TimeToTurn = $40
!StartingY = $40
!StartingX = $58
init:
LDA #!StartingX
STA !E4,x
LDA #!StartingY
STA !D8,x
STZ !14D4,x
STZ !14E0,X
LDA #!TimeToTurn
STA !1540,x
STZ !157C,x
STZ !B6,x
RTL

main:
LDA !C2,x           ; set Y speed for wobbly effect
AND.b #$01
TAY
LDA !AA,X
CLC : ADC.w SpeedTable,Y
STA !AA,x
CMP.w SpeedY,Y
BNE +
INC !C2,x
+

JSR SetAnimationFrame   ; calculate correct animation frame

LDA !1540,x             ; if counter and speed are 0, time to turn
ORA !B6,x
BNE .noswap

LDA #!TimeToTurn        ; turn speed and direction
STA !1540,x

LDA !157C,x
EOR #$01
STA !157C,x

.noswap
LDA $14
AND #$03
BNE .updatepos

LDY !157C,x
LDA !1540,x
BNE .domax

CPY #$00
BEQ .decrright
BRA .decrleft

.domax
LDA !157C,x
LSR : LDA #!MaxXSpd
BCS .goingleft

CMP !B6,x
BEQ .updatepos

.decrleft
INC !B6,x
BRA .updatepos

.goingleft
EOR #$FF : INC
CMP !B6,x
BEQ .updatepos

.decrright
DEC !B6,x

.updatepos 
%savex($01801A)   
%savex($018022)

%getdrawinfo() 
LDY !1602,x
LDA Tiles,y
STA $02
LDY !157C,x
LDA Props,y
STA $03
%getoamindex()
%SetOAMProp($00, $01, $02, $03, #$00)     
RTL

Props:
    db $73, $03
Tiles:
    db $B0, $B1
SpeedY:
    db $18, $E8
SpeedTable:
    db $01,$FF
; 0000 -> 1A -> custom tailored for YI
; C000 -> 1C -> custom tailored for YI

SetAnimationFrame:				
	INC.w !1570,X				
	LDA.w !1570,X				
    LSR #3
	AND.b #$01					
	STA.w !1602,X				
	RTS							