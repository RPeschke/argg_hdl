-- XGEN: Autogenerated File

library IEEE;
library UNISIM;
library work;
use IEEE.numeric_std.all;
use IEEE.std_logic_1164.all;
use UNISIM.VComponents.all;
use ieee.std_logic_unsigned.all;
use work.argg_hdl_core.all;
use work.axisStream_slv32.all;
use work.klm_globals_pack.all;
use work.register_t_pack.all;


entity InputDelay_print is 
  port(
    ConfigIn_s2m :  out  axiStream_slv32_s2m := axiStream_slv32_s2m_null;
    ConfigIn_m2s :  in  axiStream_slv32_m2s := axiStream_slv32_m2s_null;
    globals :  in  klm_globals := klm_globals_null
  );
end entity;



architecture rtl of InputDelay_print is

--------------------------InputDelay_print-----------------
  signal counter : integer := 0; 
  signal d : std_logic_vector(31 downto 0) := (others => '0'); 
-------------------------- end InputDelay_print-----------------

begin
  -- begin architecture
  
-----------------------------------
proc : process(globals.clk) is
  variable ax_slave : axiStream_slv32_slave := axiStream_slv32_slave_null;
  variable ax_slave_buff : std_logic_vector(31 downto 0) := (others => '0');
  begin
    if rising_edge(globals.clk) then 
      pull( self  =>  ax_slave, rx => ConfigIn_m2s);
  counter <= counter + 1;
    
      if (isReceivingData_0(self => ax_slave)) then 
        read_data_00(self => ax_slave, dataOut => ax_slave_buff);
        d <= ax_slave_buff;
        
      end if;
    
      if (counter > 15) then 
        counter <=  0;
        
      end if;
        push( self  =>  ax_slave, rx => ConfigIn_s2m);
  end if;
  
  end process;
  -- end architecture
end architecture;