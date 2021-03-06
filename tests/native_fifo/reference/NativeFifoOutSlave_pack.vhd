-- XGEN: Autogenerated File

library IEEE;
library UNISIM;
library work;
use IEEE.numeric_std.all;
use IEEE.std_logic_1164.all;
use UNISIM.VComponents.all;
use ieee.std_logic_unsigned.all;
use work.NativeFifoOut_pack.all;
use work.argg_hdl_core.all;
use work.slv32_a_pack.all;
use work.small_buffer_pack.all;


package NativeFifoOutSlave_pack is 

-------------------------------------------------------------------------
------- Start Psuedo Class NativeFifoOutSlave -------------------------

type NativeFifoOutSlave_sig is record 
    rx1 : NativeFifoOut;
    rx2 : NativeFifoOut;
end record;
    
    
  constant NativeFifoOutSlave_sig_null : NativeFifoOutSlave_sig:= (
    rx1 => NativeFifoOut_null,
    rx2 => NativeFifoOut_null
  );


    type NativeFifoOutSlave_sig_a is array (natural range <>) of NativeFifoOutSlave_sig;
        


type NativeFifoOutSlave is record 
    buff : small_buffer;
    empty1 : std_logic;
    enable1 : std_logic;
    rx : NativeFifoOut;
end record;
    
    
  constant NativeFifoOutSlave_null : NativeFifoOutSlave:= (
    buff => small_buffer_null,
    empty1 => '0',
    enable1 => '0',
    rx => NativeFifoOut_null
  );


    type NativeFifoOutSlave_a is array (natural range <>) of NativeFifoOutSlave;
        

  procedure pull (signal self_sig :  in  NativeFifoOutSlave_sig;  self :  inout  NativeFifoOutSlave);
  procedure push (signal self_sig :  in  NativeFifoOutSlave_sig;  self :  inout  NativeFifoOutSlave;  signal self_sig_rx2_s2m : out NativeFifoOut_s2m);
  procedure pull (signal self_sig :  in  NativeFifoOutSlave_sig_a;  self :  inout  NativeFifoOutSlave_a);
  procedure push (signal self_sig :  in  NativeFifoOutSlave_sig_a;  self :  inout  NativeFifoOutSlave_a;  signal self_sig_rx2_s2m : out NativeFifoOut_s2m_a);
  procedure read_data_01 (Signal self_sig :  in  NativeFifoOutSlave_sig; self :  inout  NativeFifoOutSlave; signal data :  out  std_logic_vector(31 downto 0));
  function isReceivingData_0 (Signal self_sig :   NativeFifoOutSlave_sig; self :   NativeFifoOutSlave) return boolean;
------- End Psuedo Class NativeFifoOutSlave -------------------------
-------------------------------------------------------------------------


end NativeFifoOutSlave_pack;


package body NativeFifoOutSlave_pack is

-------------------------------------------------------------------------
------- Start Psuedo Class NativeFifoOutSlave -------------------------
procedure pull (signal self_sig :  in  NativeFifoOutSlave_sig;  self :  inout  NativeFifoOutSlave) is
   
  begin 
 
    
-- Start Connecting
    pull(self.rx1, rx1);
    pull(self.rx, self_sig.rx2_m2s)

-- End Connecting
    
    if (( self.enable1 = '1' and  not  ( self.empty1 = '1' ) ) ) then 
      set_value_00_lshift(self => self.buff, rhs => self.rx.data);
      
    end if;
  self.empty1 := self.rx.empty;
  self.enable1 := self.rx.enable;
  self.rx.enable := '0';
  
             
end procedure;

procedure push (signal self_sig :  in  NativeFifoOutSlave_sig;  self :  inout  NativeFifoOutSlave;  signal self_sig_rx2_s2m : out NativeFifoOut_s2m) is
   
  begin 
 
    
    if ( not  ( isReceivingData_0(self => self.buff) ) ) then 
      self.rx.enable := '1';
      
    end if;
  
-- Start Connecting
    push(self.rx1, rx1);
    push(self.rx, self_sig_rx2_s2m)

-- End Connecting
    
             
end procedure;

procedure pull (signal self_sig :  in  NativeFifoOutSlave_sig_a;  self :  inout  NativeFifoOutSlave_a) is
   
  begin 
 
        for i in 0 to self'length - 1 loop
        pull( self_sig =>  self_sig(i), self =>  self(i), rx1 => rx1(i));
        end loop;
             
end procedure;

procedure push (signal self_sig :  in  NativeFifoOutSlave_sig_a;  self :  inout  NativeFifoOutSlave_a;  signal self_sig_rx2_s2m : out NativeFifoOut_s2m_a) is
   
  begin 
 
        for i in 0 to self'length - 1 loop
        push( self_sig =>  self_sig(i), self =>  self(i), self_sig_rx2_s2m => self_sig_rx2_s2m(i), rx1 => rx1(i));
        end loop;
             
end procedure;

function isReceivingData_0 (Signal self_sig :   NativeFifoOutSlave_sig; self :   NativeFifoOutSlave) return boolean is
   
  begin 
 return isReceivingData_0(self => self.buff);
   
end function;

procedure read_data_01 (Signal self_sig :  in  NativeFifoOutSlave_sig; self :  inout  NativeFifoOutSlave; signal data :  out  std_logic_vector(31 downto 0)) is
   
  begin 
 data <= (others => '0');
  get_value_01_rshift(self => self.buff, rhs => data);
   
end procedure;

------- End Psuedo Class NativeFifoOutSlave -------------------------
  -------------------------------------------------------------------------


end NativeFifoOutSlave_pack;

