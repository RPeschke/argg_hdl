-- XGEN: Autogenerated File

library IEEE;
library UNISIM;
library work;
use IEEE.numeric_std.all;
use IEEE.std_logic_1164.all;
use UNISIM.VComponents.all;
use ieee.std_logic_unsigned.all;
use work.NativeFifoOutSlave_pack.all;
use work.NativeFifoOut_pack.all;
use work.argg_hdl_core.all;
use work.slv32_a_pack.all;
use work.small_buffer_pack.all;


entity readout_native_fifo is 
  port(
    Data_in_s2m :  out  NativeFifoOut_s2m := NativeFifoOut_s2m_null;
    Data_in_m2s :  in  NativeFifoOut_m2s := NativeFifoOut_m2s_null;
    clk :  in  std_logic := '0'
  );
end entity;



architecture rtl of readout_native_fifo is

--------------------------readout_native_fifo-----------------
  signal counter : std_logic_vector(31 downto 0) := (others => '0'); 
  signal data : std_logic_vector(31 downto 0) := (others => '0'); 
  signal fifo_s_sig : NativeFifoOutSlave_sig := NativeFifoOutSlave_sig_null;
  -------------------------- end readout_native_fifo-----------------

begin
  -- begin architecture
  
-----------------------------------
proc : process(clk) is
  variable fifo_s : NativeFifoOutSlave := NativeFifoOutSlave_null;
  begin
    if rising_edge(clk) then 
      pull( self_sig  =>  fifo_s_sig, self  =>  fifo_s);
  counter <= counter + 1;
    
      if (isReceivingData_0(self_sig => fifo_s_sig, self => fifo_s)) then 
        read_data_01(self_sig => fifo_s_sig, self => fifo_s, data => data);
        
      end if;
        push( self_sig  =>  fifo_s_sig, self  =>  fifo_s, fifo_s_sig_rx2_s2m => fifo_s_sig.rx2_s2m);
  end if;
  
  end process;
  -- end architecture

      -- begin architecture
    -- begin p2
  fifo_s_sig.rx1_s2m.enable <= '
    fifo_s_sig.rx2_s2m.enable when fifo_s_sig.rx1_m2s.empty = '0' else
    0';
  fifo_s_sig.rx2_m2s.empty <= fifo_s_sig.rx1_m2s.empty;
  fifo_s_sig.rx2_m2s.data <= fifo_s_sig.rx1_m2s.data;
  -- end p2;
  -- end architecture
;
  ---------------------------------------------------------------------
--  fifo_s_sig.rx1 << Data_in
fifo_s_sig.rx1_m2s <= Data_in_m2s;
Data_in_s2m <= fifo_s_sig.rx1_s2m;
  
end architecture;