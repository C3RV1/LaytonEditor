#---------------------------------------------------------------------------------
.SUFFIXES:
#---------------------------------------------------------------------------------

ifeq ($(strip $(DEVKITARM)),)
$(error "Please set DEVKITARM in your environment. export DEVKITARM=<path to>devkitARM")
endif


#---------------------------------------------------------------------------------
# path to tools
#---------------------------------------------------------------------------------
export PORTLIBS :=  $(DEVKITPRO)/portlibs/arm
export PATH     :=  $(DEVKITARM)/bin:$(PORTLIBS)/bin:$(PATH)
LIBNDS  :=  $(DEVKITPRO)/libnds

#---------------------------------------------------------------------------------
# the prefix on the compiler executables
#---------------------------------------------------------------------------------
PREFIX      :=  arm-none-eabi-

export CC   :=  $(PREFIX)gcc
export CXX  :=  $(PREFIX)g++
export AS   :=  $(PREFIX)as
export AR   :=  $(PREFIX)ar
export OBJCOPY  :=  $(PREFIX)objcopy
export OBJDUMP  :=  $(PREFIX)objdump
export LD   :=  $(PREFIX)ld


#---------------------------------------------------------------------------------
# TARGET is the name of the output
# BUILD is the directory where object files & intermediate files will be placed
# SOURCES is a list of directories containing source code
# INCLUDES is a list of directories containing extra header files
#---------------------------------------------------------------------------------
TARGET      :=  patch
TARGET_DIR	:=	./output
BUILD       :=  build
SOURCES     :=  ./source
INCLUDES    :=  ../include
BOOTSTRAP	:=	bootstrap

PATCHLENGHT :=

#---------------------------------------------------------------------------------
# options for code generation
#---------------------------------------------------------------------------------
ARCH    :=  

CFLAGS  :=  -g -Wall -O2\
        -march=armv5te -mtune=arm946e-s -fomit-frame-pointer\
		-ffast-math \
		$(ARCH)

CFLAGS  +=  $(INCLUDE) -I$(INCLUDES) -DARM9 -nodefaultlibs -I. -fno-builtin -c
CXXFLAGS    := $(CFLAGS) -fno-rtti -fno-exceptions

ASFLAGS :=  -g $(ARCH)
LDFLAGS =   -T $(CURDIR)/../symbols.x -T $(CURDIR)/../linker.x -g $(ARCH) -Map newcode.map
LDFLAGS_PATCH :=
LDFLAGS_STRAP :=

ifdef CODEADDR
  LDFLAGS_PATCH += -Ttext $(CODEADDR)
endif

ifdef STRAPADDR
  LDFLAGS_STRAP += -Ttext $(STRAPADDR)
endif

CODEADDR ?= 0
STRAPADDR ?= 0

#---------------------------------------------------------------------------------
# any extra libraries we wish to link with the project (order is important)
#---------------------------------------------------------------------------------
LIBS    :=  -lnds9 -lc -lgcc
 
 
#---------------------------------------------------------------------------------
# list of directories containing libraries, this must be the top level containing
# include and lib
#---------------------------------------------------------------------------------
LIBDIRS :=  $(LIBNDS)  $(DEVKITARM) $(DEVKITARM)/arm-none-eabi 

#---------------------------------------------------------------------------------
ifneq ($(BUILD),$(notdir $(CURDIR)))
#---------------------------------------------------------------------------------

export OUTPUT   		:=  $(CURDIR)/$(TARGET_DIR)/$(TARGET)
export BOOTSTRAP_OUTPUT :=	$(CURDIR)/$(TARGET_DIR)/$(BOOTSTRAP)
export VPATH    :=  $(foreach dir,$(SOURCES),$(CURDIR)/$(dir))

export DEPSDIR  :=  $(CURDIR)/$(BUILD)

CFILES      :=  $(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.c)))
CPPFILES    :=  $(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.cpp)))
SFILES      :=  $(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.s)))

export OFILES   :=  $(CPPFILES:.cpp=.o) $(CFILES:.c=.o) $(SFILES:.s=.o)
 
export INCLUDE  :=  $(foreach dir,$(INCLUDES),-iquote $(CURDIR)/$(dir)) \
					$(foreach dir,$(LIBDIRS),-I$(dir)/include) \
					-I$(CURDIR)/$(BUILD)
 
export LIBPATHS :=  $(foreach dir,$(LIBDIRS),-L$(dir)/lib) -L$(DEVKITARM)/lib/gcc/arm-none-eabi/10.2.0

 
.PHONY: $(BUILD) clean
  
#---------------------------------------------------------------------------------
$(BUILD):
	@[ -d $@ ] || mkdir -p $@
	@[ -d $(TARGET_DIR) ] || mkdir -p $(TARGET_DIR)
	@make --no-print-directory -C $(BUILD) -f $(CURDIR)/Makefile
 
#---------------------------------------------------------------------------------
clean:
	@echo clean ...
	@rm -fr $(BUILD) $(TARGET).elf $(TARGET).bin $(TARGET).sym $(TARGET_DIR)

#---------------------------------------------------------------------------------
else
#---------------------------------------------------------------------------------
# main targets
#---------------------------------------------------------------------------------
all: $(OUTPUT).bin $(OUTPUT).sym $(BOOTSTRAP_OUTPUT).bin $(BOOTSTRAP_OUTPUT).sym

$(BOOTSTRAP_OUTPUT).elf: $(OUTPUT).bin $(OUTPUT).sym ../bootstrap.c
	$(CC) $(CFLAGS) -DCODEADDR=$(CODEADDR) -DCODELEN=$(shell stat -L -c %s $(OUTPUT).bin) \
		-c ../bootstrap.c -o bootstrap.o $(ERROR_FILTER)
	$(LD) $(LDFLAGS) $(LDFLAGS_STRAP) bootstrap.o -o $@

%.bin : %.elf
	$(OBJCOPY) -O binary $< $@
	@echo built ... $(notdir $@)

%.sym : %.elf
	$(OBJDUMP) -t $< > $@
	@echo written the symbol table ... $(notdir $@)
	
#---------------------------------------------------------------------------------
$(OUTPUT).elf: $(OFILES)
	@echo linking $(notdir $@)
	$(LD)  $(LDFLAGS) $(LDFLAGS_PATCH) $(OFILES) $(LIBPATHS) $(LIBS) -o $@

#---------------------------------------------------------------------------------
%.o: %.cpp
	@echo $(notdir $<)
	$(CXX) -MMD -MP -MF $(DEPSDIR)/$*.d $(CXXFLAGS) -c $< -o $@ $(ERROR_FILTER)
	
#---------------------------------------------------------------------------------
%.o: %.c
	@echo $(notdir $<)
	$(CC) -MMD -MP -MF $(DEPSDIR)/$*.d $(CFLAGS) -c $< -o $@ $(ERROR_FILTER)
	
#---------------------------------------------------------------------------------
%.o: %.s
	@echo $(notdir $<)
	$(CC) -MMD -MP -MF $(DEPSDIR)/$*.d -x assembler-with-cpp $(ASFLAGS) -c $< -o $@ $(ERROR_FILTER)


-include $(DEPSDIR)/*.d

#---------------------------------------------------------------------------------------
endif
#---------------------------------------------------------------------------------------

