OUTPUT_ARCH(arm)

SECTIONS {
	

	
	.text : {
	
		
		FILL (0x1234)
		
		__text_start = . ;
		*(.init)
		*(.text)
		*(.ctors)
		*(.dtors)
		*(.rodata)
		*(.fini)
		*(COMMON)
		*(.data)
		__text_end  = . ;
		. = ALIGN(4);
		__ovpt_start = .;
		*(.ovpt) /* overlay patches table */
		__ovpt_end = .;
		__bss_start__ = . ;
		*(.bss)
		__bss_end__ = . ;
	_end = __bss_end__ ;
	__end__ = __bss_end__ ;
	}
}
