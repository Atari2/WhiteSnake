if read1($00FFD5) == $23		; check if the rom is sa-1
	sa1rom
	!sa1 = 1
	!SA1 = 1
	!SA_1 = 1
	!dp = $3000
	!addr = $6000
	
	!BankA = $400000
	!BankB = $000000
	!bank = $000000
	
	!Bank8 = $00
	!bank8 = $00
	
	!SprSize = $16
else
	lorom
	!sa1 = 0
	!SA1 = 0
	!SA_1 = 0
	!dp = $0000
	!addr = $0000

	!BankA = $7E0000
	!BankB = $800000
	!bank = $800000
	
	!Bank8 = $80
	!bank8 = $80
	
	!SprSize = $0C
endif

macro define_spr_ow_table(name, addr, addr_sa1)
	if !SA1 == 0
		!<name> = <addr>
	else
		!<name> = <addr_sa1>
	endif
endmacro

macro define_base2_address(name, addr)
	if !SA1 == 0
		!<name> = <addr>
	else
		!<name> = <addr>|!addr
	endif
endmacro

macro define_base2_address_name(name, addr, long_name)
    if !SA1 == 0
        !<name> = <addr>
    else
        !<name> = <addr>|!addr
    endif
    !<long_name> = !<name>
endmacro


; ow sprite tables
%define_base2_address_name("0DDE", $0DDE, "sprite_index")
%define_base2_address_name("0DDF", $0DDF, "starting_oam_index")
%define_base2_address_name("0DE5", $0DE5, "sprite_number")
%define_base2_address_name("0DF5", $0DF5, "misc_table_1")
%define_base2_address_name("0E05", $0E05, "misc_table_2")
%define_base2_address_name("0E15", $0E15, "misc_table_3")
%define_base2_address_name("0E25", $0E25, "misc_table_4")
%define_base2_address_name("0E35", $0E35, "sprite_x_pos_lo")
%define_base2_address_name("0E45", $0E45, "sprite_y_pos_lo")
%define_base2_address_name("0E55", $0E55, "sprite_z_pos_lo")
%define_base2_address_name("0E65", $0E65, "sprite_x_pos_hi")
%define_base2_address_name("0E75", $0E75, "sprite_y_pos_hi")
%define_base2_address_name("0E85", $0E85, "sprite_z_pos_hi")
%define_base2_address_name("0E95", $0E95, "sprite_x_speed")
%define_base2_address_name("0EA5", $0EA5, "sprite_y_speed")
%define_base2_address_name("0EB5", $0EB5, "sprite_z_speed")
%define_base2_address_name("0EC5", $0EC5, "fraction_bit_x_speed")
%define_base2_address_name("0ED5", $0ED5, "fraction_bit_y_speed")
%define_base2_address_name("0EF5", $0EE5, "fraction_bit_z_speed")


; normal sprite tables
%define_base2_address("15E9",$15E9)
%define_spr_ow_table("9E", $9E, $3200)
%define_spr_ow_table("AA", $AA, $9E)
%define_spr_ow_table("B6", $B6, $B6)
%define_spr_ow_table("C2", $C2, $D8)
%define_spr_ow_table("D8", $D8, $3216)
%define_spr_ow_table("E4", $E4, $322C)
%define_spr_ow_table("14C8", $14C8, $3242)
%define_spr_ow_table("14D4", $14D4, $3258)
%define_spr_ow_table("14E0", $14E0, $326E)
%define_spr_ow_table("14EC", $14EC, $74C8)
%define_spr_ow_table("14F8", $14F8, $74DE)
%define_spr_ow_table("1504", $1504, $74F4)
%define_spr_ow_table("1510", $1510, $750A)
%define_spr_ow_table("151C", $151C, $3284)
%define_spr_ow_table("1528", $1528, $329A)
%define_spr_ow_table("1534", $1534, $32B0)
%define_spr_ow_table("1540", $1540, $32C6)
%define_spr_ow_table("154C", $154C, $32DC)
%define_spr_ow_table("1558", $1558, $32F2)
%define_spr_ow_table("1564", $1564, $3308)
%define_spr_ow_table("1570", $1570, $331E)
%define_spr_ow_table("157C", $157C, $3334)
%define_spr_ow_table("1588", $1588, $334A)
%define_spr_ow_table("1594", $1594, $3360)
%define_spr_ow_table("15A0", $15A0, $3376)
%define_spr_ow_table("15AC", $15AC, $338C)
%define_spr_ow_table("15B8", $15B8, $7520)
%define_spr_ow_table("15C4", $15C4, $7536)
%define_spr_ow_table("15D0", $15D0, $754C)
%define_spr_ow_table("15DC", $15DC, $7562)
%define_spr_ow_table("15EA", $15EA, $33A2)
%define_spr_ow_table("15F6", $15F6, $33B8)
%define_spr_ow_table("1602", $1602, $33CE)
%define_spr_ow_table("160E", $160E, $33E4)
%define_spr_ow_table("161A", $161A, $7578)
%define_spr_ow_table("1626", $1626, $758E)
%define_spr_ow_table("1632", $1632, $75A4)
%define_spr_ow_table("163E", $163E, $33FA)
%define_spr_ow_table("164A", $164A, $75BA)
%define_spr_ow_table("1656", $1656, $75D0)
%define_spr_ow_table("1662", $1662, $75EA)
%define_spr_ow_table("166E", $166E, $7600)
%define_spr_ow_table("167A", $167A, $7616)
%define_spr_ow_table("1686", $1686, $762C)
%define_spr_ow_table("186C", $186C, $7642)
%define_spr_ow_table("187B", $187B, $3410)
%define_spr_ow_table("190F", $190F, $7658)

%define_spr_ow_table("1938", $7FAF00, $418A00)
%define_spr_ow_table("7FAF00", $7FAF00, $418A00)

%define_spr_ow_table("1FD6", $1FD6, $766E)
%define_spr_ow_table("1FE2", $1FE2, $7FD6)