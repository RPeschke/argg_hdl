-- XGEN: Autogenerated File

library IEEE;
library UNISIM;
library work;
use IEEE.numeric_std.all;
use IEEE.std_logic_1164.all;
use UNISIM.VComponents.all;
use ieee.std_logic_unsigned.all;
use work.argg_hdl_core.all;


package addr_data_pack is 

-------------------------------------------------------------------------
------- Start Psuedo Class addr_data -------------------------

type addr_data is record 
    address : std_logic_vector(31 downto 0);
    data : std_logic_vector(31 downto 0);
end record;
    
    
  constant addr_data_null : addr_data:= (
    address => (others => '0'),
    data => (others => '0')
  );


    type addr_data_a is array (natural range <>) of addr_data;
        

  procedure pull (self : inout addr_data; signal data_IO :  in  addr_data);
  procedure push (self : inout addr_data; signal data_IO :  out  addr_data);
  procedure reset_0 (self :  inout  addr_data);
------- End Psuedo Class addr_data -------------------------
-------------------------------------------------------------------------


end addr_data_pack;


package body addr_data_pack is

-------------------------------------------------------------------------
------- Start Psuedo Class addr_data -------------------------
procedure pull (self : inout addr_data; signal data_IO :  in  addr_data) is
   
  begin 
 self  := data_IO; 
end procedure;

procedure push (self : inout addr_data; signal data_IO :  out  addr_data) is
   
  begin 
 data_IO  <=  self; 
end procedure;

procedure reset_0 (self :  inout  addr_data) is
   
  begin 
 self.address := (others => '0');
  self.data := (others => '0');
   
end procedure;

------- End Psuedo Class addr_data -------------------------
  -------------------------------------------------------------------------


end addr_data_pack;

