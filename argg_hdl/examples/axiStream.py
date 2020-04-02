import argparse
import os,sys,inspect
import copy

from argg_hdl.argg_hdl_base import *
from argg_hdl.argg_hdl_v_Package import *
from argg_hdl.argg_hdl_v_class import *


class axisStream_converter(v_class_converter):
    def __init__(self):
        super().__init__()


    def includes(self,obj, name,parent):
        ret =""
        typeName = obj.data.hdl_conversion__.get_type_simple(obj.data)
        
        ret += "use work.axisStream_"+str(typeName)+".all;\n"
        members = obj.getMember() 
        for x in members:
            ret += x["symbol"].hdl_conversion__.includes(x["symbol"],name,parent)

        return ret
    
    def get_packet_file_name(self, obj):
        typeName = obj.data.hdl_conversion__.get_type_simple(obj.data)
        return "axisStream_"+str(typeName)+".vhd"

    def get_packet_file_content(self, obj):
        typeName = obj.data.hdl_conversion__.get_type_simple(obj.data)
        pack =  "axisStream_"+str(typeName)

        fileContent = make_package(pack,  obj.data)
        return fileContent

class axisStream(v_class):
    def __init__(self,Axitype):
        super().__init__("axiStream_"+Axitype.hdl_conversion__.get_type_simple(Axitype))
        self.hdl_conversion__ =axisStream_converter()
        AddDataType( v_copy( Axitype ) )
        self.valid  = port_out( v_sl() )
        self.last   = port_out( v_sl() )
        self.data   = port_out(  Axitype   )
        self.ready  = port_in( v_sl() )

    def get_master(self):
        return axisStream_master(self)

    def get_slave(self):
        return axisStream_slave(self)

class axisStream_slave_converter(axisStream_converter):
    def __init__(self):
        super().__init__()

    def _vhdl__to_bool(self, obj, astParser):
        hdl = obj.hdl_conversion__._vhdl__call_member_func(obj, "isReceivingData",[obj],astParser)

        if hdl == None:
            astParser.Missing_template=True
            return "-- $$ template missing $$"
        return hdl

    def _vhdl__getValue(self,obj, ReturnToObj=None,astParser=None):

        vhdl_name = str(obj) + "_buff"
        buff =  astParser.try_get_variable(vhdl_name)

        if buff == None:
            buff = v_copy(obj.rx.data)
            buff.vhdl_name = str(obj) + "_buff"
            buff.varSigConst = varSig.variable_t
            astParser.LocalVar.append(buff)


        hdl = obj.hdl_conversion__._vhdl__call_member_func(obj, "read_data",[obj, buff],astParser)
        if hdl == None:
            astParser.AddStatementBefore("-- $$ template missing $$")
            astParser.Missing_template=True
            return buff



        astParser.AddStatementBefore(hdl)
        return buff

    def includes(self,obj, name,parent):
        ret = obj.rx.hdl_conversion__.includes(obj.rx,None,None)
        return ret

    def get_packet_file_name(self, obj):
        ret = obj.rx.hdl_conversion__.get_packet_file_name(obj.rx)
        return ret


    def get_packet_file_content(self, obj):
        ret = obj.rx.hdl_conversion__.get_packet_file_content(obj.rx)
        return ret


class axisStream_slave(v_class_slave):
    def __init__(self, Axi_in):
        super().__init__(Axi_in.type+"_slave")
        self.hdl_conversion__ =axisStream_slave_converter()
        
        self.rx =  variable_port_Slave( Axi_in)
        self.rx  << Axi_in
    
        self.data_isvalid            = v_variable( v_sl() )
        self.data_internal2          = v_variable( Axi_in.data )
        self.data_internal_isvalid2  = v_variable( v_sl())
        self.data_internal_was_read2 = v_variable(v_sl())
        self.data_internal_isLast2   = v_variable( v_sl())
        
        
        
    def observe_data(self, dataOut = variable_port_out(dataType())):
        if self.data_internal_isvalid2:
            dataOut << self.data_internal2
    
    
    def read_data(self, dataOut ):
        if self.data_internal_isvalid2:
            dataOut << self.data_internal2
            self.data_internal_was_read2 << 1
    

    def isReceivingData(self):
        return  self.data_internal_isvalid2 == 1


    def IsEndOfStream(self):
        return  self.data_internal_isvalid2 > 0 and  self.data_internal_isLast2 > 0

    def __bool__(self):
        return self.isReceivingData()

    def _onPull(self):
        if self.rx.ready and self.rx.valid:
            self.data_isvalid << 1
        
        self.data_internal_was_read2 << 0
        self.rx.ready << 0      
   
        if self.data_isvalid  and not self.data_internal_isvalid2:
            self.data_internal2 << self.rx.data 
            self.data_internal_isvalid2 << self.data_isvalid
            self.data_internal_isLast2 << self.rx.last
            self.data_isvalid << 0
        
   
      
    def _sim_get_value(self):
        if self.data_internal_isvalid2:
            self.data_internal_was_read2 << 1

        return self.data_internal2._sim_get_value()

    def _onPush(self):
        if self.data_internal_was_read2:
            self.data_internal_isvalid2 << 0

        if not self.data_isvalid and not self.data_internal_isvalid2:
            self.rx.ready << 1
        


class axisStream_master_converter(axisStream_converter):
    def __init__(self):
        super().__init__()

    def _vhdl__to_bool(self, obj, astParser):
        ret =  obj.hdl_conversion__._vhdl__call_member_func(obj, "ready_to_send",[obj],astParser)
        if ret == None:
            astParser.Missing_template=True
            return "$$missing_template$$"
        return ret
    
    def _vhdl__reasign(self,obj, rhs,astParser,context_str=None):
        ret =  obj.hdl_conversion__._vhdl__call_member_func(obj, "send_data",[obj, rhs],astParser)
        if ret == None:
            astParser.Missing_template=True
            return "$$missing_template$$"
        return ret


    
    def includes(self,obj, name,parent):
        ret = obj.tx.hdl_conversion__.includes(obj.tx,None,None)
        return ret

    def get_packet_file_name(self, obj):
        ret = obj.tx.hdl_conversion__.get_packet_file_name(obj.tx)
        return ret

    def get_packet_file_content(self, obj):
        ret = obj.tx.hdl_conversion__.get_packet_file_content(obj.tx)
        return ret

class axisStream_master(v_class_master):
    def __init__(self, Axi_Out):
        super().__init__(Axi_Out.type + "_master")
        self.hdl_conversion__ =axisStream_master_converter()
        self.tx =  variable_port_Master( Axi_Out)
        Axi_Out  << self.tx


   

        
    def send_data(self, dataIn ):
        self.tx.valid   << 1
        self.tx.data    << dataIn    
    
    def ready_to_send(self):
        return not self.tx.valid

    def Send_end_Of_Stream(self, EndOfStream=True):
        if EndOfStream:
            self.tx.last << 1
        else:
            self.tx.last << 0


    def _onPull(self):

        if self.tx.ready: 
            self.tx.valid << 0 
            self.tx.last  << 0  
#            self.tx.data  << 0

    
    def __lshift__(self, rhs):
        self.send_data(value(rhs))

    def __bool__(self):
        
        return self.ready_to_send()





def make_package(PackageName,AxiType):
    s = isConverting2VHDL()
    set_isConverting2VHDL(True)

    ax_t = axisStream(AxiType)
    ax = v_package(PackageName,sourceFile=__file__,
    PackageContent = [
        ax_t,
        axisStream_slave(ax_t),
        axisStream_master(ax_t),
        #axisStream_slave_signal(ax_t)
        #axisStream_master_with_strean_counter(ax_t)
    ]
    
    
    )
    fileContent = ax.to_string()
    set_isConverting2VHDL(s)
    return fileContent


