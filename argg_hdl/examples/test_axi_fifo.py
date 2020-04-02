

import unittest
import functools
import argparse
import os,sys,inspect
import copy



from argg_hdl.argg_hdl_v_Package import *
from argg_hdl.argg_hdl_v_entity import *
from argg_hdl.examples.rollingCounter import *
from argg_hdl.examples.clk_generator import *
from argg_hdl.examples.axiPrint import *
from argg_hdl.examples.axi_fifo  import *

class test_bench_e123(v_entity):
    def __init__(self):
        super().__init__(__file__)
        self.architecture()

    def architecture(self):
        clkgen = v_create(clk_generator())
        maxCount = v_slv(32,20)
        pipe1 = rollingCounter(clkgen.clk,maxCount) \
            | axiFifo(clkgen.clk)  \
            | axiPrint(clkgen.clk) 
        
        end_architecture()

tb = test_bench_e123()

convert_to_hdl(tb,"test_fifo")

