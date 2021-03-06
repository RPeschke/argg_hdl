from argg_hdl.argg_hdl_base import v_classType_t,varSig,InOut_t,join_str,argg_hdl_base,InoutFlip

import argg_hdl.argg_hdl_v_function as ah_func

def _get_connector(symb):
    if symb._Inout == InOut_t.Master_t:
        n_connector = symb.__receiver__[-1]
    else :
        n_connector = symb.__Driver__

    return n_connector


def InoutFlip_if(Inout,predicate):

    if predicate:
        Inout = InoutFlip(Inout)

    return  Inout

def if_true_get_first(predicate, Option_list):
    if predicate:
        return Option_list[0]
    return  Option_list[1]

def append_hdl_name(name, suffix):
    ret = ""    
    name_sp = str(name).split("(")
    if len(name_sp) == 2:
        ret = name_sp[0]+suffix+"("+ name_sp[1]
    else:
        ret = name_sp[0]+suffix
    
    return ret
    
class vhdl__Pull_Push():
    def __init__(self,obj, inout):
        self.obj = obj
        self.Inout = inout

    def get_selfHandles(self):
        selfHandles = []
        xs = self.obj.__hdl_converter__.extract_conversion_types(self.obj)
        for x in xs:
            arg = "self"+x["suffix"] + "  =>  " +str(self.obj) + x["suffix"]
            selfHandles.append(arg)
        return selfHandles

    def getConnections(self):
        content = []
        for x in self.obj.getMember( self.Inout,varSig.variable_t):
            n_connector = _get_connector( x["symbol"])


            ys =n_connector.__hdl_converter__.extract_conversion_types(
                    n_connector,
                    exclude_class_type= v_classType_t.transition_t,
                    filter_inout=self.Inout
                )
            for y in ys:
                content.append(x["name"]+" => "+y["symbol"].get_vhdl_name())

        return content

    def getConnections_outputs(self):
        content = []
        if not(self.Inout == InOut_t.output_t):
            return content

        members = self.obj.__hdl_converter__.get_internal_connections(self.obj)
        for x in members:
            inout_local =  self.Inout
            if x["type"] == 'sig2var':
                inout_local =  InoutFlip(self.Inout)



            sig = x["source"]["symbol"].__hdl_converter__.extract_conversion_types(
                    x["source"]["symbol"],
                    exclude_class_type= v_classType_t.transition_t,
                    filter_inout=inout_local
                )
            connector = "_"
            content.append(self.obj.__hdl_name__+"_sig" + connector + x["source"]["name"]+ sig[0]["suffix"] +" => " +self.obj.__hdl_name__+"_sig."  + x["source"]["name"]+ sig[0]["suffix"])

        return content


    def __str__(self):
        if self.obj.__v_classType__  == v_classType_t.Record_t:
            return ""
        content = self.get_selfHandles()



        content += self.getConnections()

        content += self.getConnections_outputs()

        pushpull= "push"
        if self.Inout == InOut_t.input_t:
            pushpull = "pull"

        ret=join_str(
            content,
            start="    " + pushpull + "( ",
            end=");\n",
            Delimeter=", "
            )

        if  not self.obj.__hdl_converter__.Has_pushpull_function(self.obj, pushpull):
            return ""
        return ret



class getHeader():
    def __init__(self, obj, name,parent):
        self.obj = obj
        self.name = name
        self.parent = parent


    def header(self):
        ret = "-------------------------------------------------------------------------\n"
        ret += "------- Start Psuedo Class " +self.obj.getName() +" -------------------------\n"
        return ret

    def footer(self):
        ret = "------- End Psuedo Class " +self.obj.getName() +" -------------------------\n"
        ret += "-------------------------------------------------------------------------\n\n\n"
        return ret

    def From_Conversion_types(self):
        ret = ""
        ts = self.obj.__hdl_converter__.extract_conversion_types(self.obj)
        for t in ts:
            ret +=  self.obj.__hdl_converter__.getHeader_make_record(
                t["symbol"],
                self.name,
                self.parent,
                t["symbol"]._Inout ,
                t["symbol"]._varSigConst
            )
            ret += "\n\n"

        return ret

    def From_members(self):
        ret = ""
        for x in self.obj.__dict__.items():
            t = getattr(self.obj, x[0])
            if issubclass(type(t),argg_hdl_base) and not t._issubclass_("v_class"):
                ret += t.__hdl_converter__.getHeader(t,x[0],self.obj)

        return ret

    def From_Functions(self):
        ret = ""
        funlist =[]
        for x in reversed(self.obj.__hdl_converter__.__ast_functions__):
            if "_onpull" in x.name.lower()  or "_onpush" in x.name.lower() :
                continue
            funDeclaration = x.__hdl_converter__.getHeader(x,None,None)
            if funDeclaration in funlist:
                x.isEmpty = True
                continue
            funlist.append(funDeclaration)
            ret +=  funDeclaration

        return ret
    def __str__(self):

        ret =self.header()
        ret += self.From_Conversion_types()

        self.obj.__hdl_converter__.make_connection(self.obj,self.name,self.parent)


        ret += self.From_members()

        ret += self.From_Functions()


        ret +=self.footer()
        return ret


class getMemberArgs():
    def __init__(self,obj, InOut_Filter,InOut,suffix="", IncludeSelf =False,PushPull=""):
        self.obj = obj
        self.InOut_Filter = InOut_Filter
        self.InOut = InOut
        self.suffix  = suffix
        self.IncludeSelf = IncludeSelf
        self.PushPull = PushPull

    def get_SelfPush(self):
        members_args = []

        if not self.PushPull == "push":
            return members_args

        varsig = " signal "

        i_members = self.obj.__hdl_converter__.get_internal_connections(self.obj)
        for m in i_members:
            internal_inout_filter = InoutFlip_if(self.InOut_Filter, m["type"] == 'sig2var')


            sig = m["source"]["symbol"].__hdl_converter__.extract_conversion_types(
                m["source"]["symbol"],
                exclude_class_type= v_classType_t.transition_t,
                filter_inout=internal_inout_filter
            )

            members_args.append(
                varsig + "self_sig_" +  m["source"]["name"] + sig[0]["suffix"]  + 
                            " : out "  + 
                sig[0]["symbol"].getType()+self.suffix
            )

        return members_args

    def get_Self(self):
        members_args = []

        if not self.IncludeSelf:
            return members_args

        xs = self.obj.__hdl_converter__.extract_conversion_types(self.obj )
        for x in xs:
            isSignal = x["symbol"]._varSigConst == varSig.signal_t
            varsig = if_true_get_first(isSignal, [" signal ", " "])
            self_InOut = if_true_get_first(isSignal, [" in ", " inout "])

            members_args.append(
                varsig + "self" + x["suffix"]  +
                           " : " +
                self_InOut + " "  + x["symbol"].getType()+self.suffix
            )


        members_args += self.get_SelfPush()


        return members_args

    def __str__(self):
        members_args = self.get_Self()

        members = self.obj.getMember(self.InOut_Filter, VaribleSignalFilter=varSig.variable_t)

        for i in members:
            n_connector = _get_connector(i["symbol"])
            xs = i["symbol"].__hdl_converter__.extract_conversion_types(
                    i["symbol"],
                    exclude_class_type= v_classType_t.transition_t,
                    filter_inout=self.InOut_Filter
                )

            for x in xs:

                varsig = " "
                if n_connector._varSigConst == varSig.signal_t :
                    varsig = " signal "

                members_args.append(varsig + i["name"] + " : " + self.InOut + " "  + x["symbol"].getType()+self.suffix)


        ret=join_str(
            members_args,
            Delimeter="; "
            )
        return ret


class getConnecting_procedure_vector():
    def __init__(self,obj, InOut_Filter,PushPull,procedureName=None):
        super().__init__()
        self.obj = obj
        self.InOut_Filter = InOut_Filter
        self.PushPull = PushPull
        self.procedureName = procedureName

    def get_isempty_From_non_vector_method(self):
        isEmpty = False
        if self.PushPull== "push":
            isEmpty = self.obj.push.isEmpty

        else:
            isEmpty = self.obj.pull.isEmpty
        return isEmpty

    def get_argumentList(self):
        inout = " in "
        if self.PushPull== "push":
            inout = " out "


        argumentList =  self.obj.__hdl_converter__.getMemberArgs(
            self.obj,
            self.InOut_Filter,
            inout,
            suffix="_a",
            IncludeSelf = True,
            PushPull=self.PushPull
        ).strip()

        return argumentList

    def get_self_args(self) :
        content = []

        xs = self.obj.__hdl_converter__.extract_conversion_types(self.obj )
        for x in xs:
            line = "self" + x["suffix"] + " =>  self" + x["suffix"]+"(i)"
            content.append(line)

        return content

    def get_internal_connections(self) :
        content = []
        if not self.PushPull == "push":
            return  content

        members = self.obj.__hdl_converter__.get_internal_connections(self.obj)
        for x in members:
            inout_local = InoutFlip_if(self.InOut_Filter, x["type"] == 'sig2var')

            sig = x["destination"]["symbol"].__hdl_converter__.extract_conversion_types(
                x["destination"]["symbol"],
                exclude_class_type=v_classType_t.transition_t,
                filter_inout=inout_local
            )
            
            content.append(
                self.obj.__hdl_name__ + "_sig_"  + x["source"]["name"] + sig[0]["suffix"] +
                " => " +
                self.obj.__hdl_name__ + "_sig_"  + x["source"]["name"] + sig[0]["suffix"] + "(i)"
            )

        return content

    def get_procedure(self):

        isEmpty = self.get_isempty_From_non_vector_method()

        argumentList = self.get_argumentList()

        content = self.get_self_args()

        content += self.get_internal_connections()

        members = self.obj.getMember(self.InOut_Filter)

        args = join_str(content + [
                str(x["name"]) + " => " + str(x["name"]+"(i)")
                for x in members
            ],
            Delimeter= ", ",
            IgnoreIfEmpty=True
            )


        ret = ah_func.v_procedure(
            name=self.procedureName,
            argumentList=argumentList,
            body='''
        for i in 0 to self'length - 1 loop
        {PushPull}( {args});
        end loop;
            '''.format(
                PushPull=self.PushPull,
                args=args
            ),
            isFreeFunction=True,
            IsEmpty=isEmpty
        )

        return ret

