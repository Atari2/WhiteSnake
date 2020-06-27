macro SetOAMProp(XPos, YPos, Tile, Props, Size)
    LDA <XPos> : STA $0300|!addr,y    ; xpos on screen
    LDA <YPos> : STA $0301|!addr,y    ; ypos on screen
    LDA <Tile> : STA $0302|!addr,y    ; tile
    LDA <Props> : STA $0303|!addr,y   ; yxppccct
    TYA : LSR #$2 : TAY
    LDA <Size> : STA $0460|!addr,y
endmacro

macro savex(label)
    PHX : JSL <label> : PLX
endmacro

macro bankWrapper(label)
	PHB : PHK : PLB : JSR label : PLB
endmacro

macro setDB(label, db)
	PHB
	LDA <db>
	PLA
	PLB 
	JSL label
	PLB
endmacro
	
