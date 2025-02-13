import os
import re

def create_project_directory(project_name):
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

def create_design_directory():
    os.makedirs("design", exist_ok=True)
    os.chdir("design")

def create_rtl_fiie(project_name):
    with open(f"{project_name}.v", "w") as f:
      f.write(f"module {project_name}();\nendmodule\n")

def create_verification_directory():
    os.makedirs("tb", exist_ok=True)
    os.chdir("tb")


def create_transaction_file(project_name):
    num_vars = get_number_of_variables()

    variables = []
    for i in range(num_vars):
        while True:
            var_name = input(f"Enter variable {i+1} name (EX: bit clk/bit[31:0] addr/int addr/byte ready): ").strip()
            if re.match(r"(bit|byte|int|logic)(\[\d+:\d+\])? [a-zA-Z_]+", var_name) and not re.search(r"[;@%:,$]", var_name.split()[1]):
                variables.append(var_name)
                break
            else:
                print("Invalid input! Please enter a valid variable name (e.g., 'bit clk' or 'bit[31:0] addr' or 'int addr' or 'logic[31:0] addr' or 'byte ready').")

    with open("xtn.sv", "w") as f:
        f.write(f"class {project_name}_xtn extends uvm_sequence_item;\n"
                f"\n")
        
        for var_name in variables:
            f.write(f"  rand {var_name};\n")

        f.write(f"\n"
                f"  `uvm_object_utils_begin({project_name}_xtn)\n")

        for var_name in variables:
            f.write(f"   `uvm_field_int({var_name.split(" ")[1]}, UVM_ALL_ON)\n")
        
        f.write(f"  `uvm_object_utils_end\n"
                f"{calling_object_function_new(project_name,'xtn')}")
  
        f.write(f"\n"
                f"endclass")
    return variables


def create_agent_file(project_name,agent_type):
    with open("agent.sv", "w") as f:
        f.write(f"class {project_name}_agent extends uvm_agent;\n"
                f"  `uvm_component_utils({project_name}_agent)\n")
        if agent_type == "active":
                f.write(f"\n"
                        f"  {project_name}_driver drvh;\n"
                        f"  {project_name}_monitor monh;\n"
                        f"  {project_name}_sequencer seqrh;\n"
                        f"  {project_name}_coverage covh;\n")
        elif agent_type == "passive":
                f.write(f"\n"
                        f"  {project_name}_monitor monh;\n"
                        f"  {project_name}_coverage covh;\n")

        f.write(f"\n"
                f"{calling_component_function_new(project_name,'agent')}"
                f"{calling_component_build_phase('agent',project_name,agent_type)}")
        f.write(f"{calling_component_connect_phase("driver", agent_type)}")

        f.write(f"\nendclass")


def create_driver_file(project_name):
    with open("driver.sv", "w") as f:
        f.write(f"class {project_name}_driver extends uvm_driver #({project_name}_xtn);\n"
                f"  `uvm_component_utils({project_name}_driver)\n"
                f"\n"
                f"  virtual intf.drv_mp vif;\n"
                f"\n"
                f"{calling_component_function_new(project_name,'driver')}"
                f"{calling_component_build_phase('driver',project_name)}"
                f"{calling_component_run_phase(project_name,'driver')}"
                f"\nendclass")
        
def create_monitor_file(project_name):
    with open("monitor.sv", "w") as f:
        f.write(f"class {project_name}_monitor extends uvm_monitor;\n"
                f"  `uvm_component_utils({project_name}_monitor)\n"
                f"\n"
                f"  virtual intf.mon_mp vif;\n"
                f"\n"
                f"  uvm_analysis_port #({project_name}_xtn) monitor_port;"
                f"\n"
                f"{calling_component_function_new(project_name,'monitor')}"
                f"{calling_component_build_phase('monitor',project_name)}"
                f"{calling_component_run_phase("",'monitor')}"
                f"\nendclass")
        
def create_sequencer_file(project_name):
    with open("sequencer.sv", "w") as f:
        f.write(f"class {project_name}_sequencer extends uvm_sequencer #({project_name}_xtn);\n"
                f"  `uvm_component_utils({project_name}_sequencer)\n"
                f"{calling_component_function_new(project_name,'sequencer')}"
                f"\nendclass")

def create_env_file(project_name):  
    with open("env.sv", "w") as f:
        f.write(f"class {project_name}_env extends uvm_env;\n"
                f"  `uvm_component_utils({project_name}_env)\n"
                f"\n"
                f"  {project_name}_agent agnth;\n"
                f"  {project_name}_scoreboard sb;\n"
                f"{calling_component_function_new(project_name,'env')}"
                f"{calling_component_build_phase('env',project_name)}"
                f"{calling_component_connect_phase("env")}"
                f"\nendclass")
    
def create_test_file(project_name):
    with open("test.sv", "w") as f:
        f.write(f"class {project_name}_test extends uvm_test;\n"
                f"  `uvm_component_utils({project_name}_test)\n"
                f"\n"
                f"  {project_name}_env envh;\n"
                f"{calling_component_function_new(project_name,'test')}"
                f"{calling_component_build_phase('test',project_name)}"
                f"\nendclass\n")
        
        f.write("\n"
                f"class test1 extends {project_name}_test;\n"
                f"  `uvm_component_utils(test1)\n"
                f"\n"
                f"  seq1 seqh1;\n"
                f"{calling_component_function_new('test1')}"
                f"{calling_component_run_phase("",'test')}"
                f"\nendclass")
        
def create_sequence_file(project_name): 
    with open("sequence.sv", "w") as f:
        f.write(f"class {project_name}_sequence extends uvm_sequence #({project_name}_xtn);\n"
                f"  `uvm_object_utils({project_name}_sequence)\n"
                f"{calling_object_function_new(project_name,'sequence')}"
                f"\nendclass\n")
        
        f.write(f"\n"
                f"class seq1 extends {project_name}_sequence;\n"
                f"  `uvm_object_utils(seq1)\n"
                f"{calling_object_function_new("seq1")}"
                f"\n"
                f"  task body();\n"
                f"    repeat(10) begin\n"
                f"      req = {project_name}_xtn::type_id::create(\"req\");\n"
                f"\n"
                f"      start_item(req);\n"
                f"        req.randomize();\n"
                f"      finish_item(req);\n"
                f"    end\n"
                f"  endtask\n"
                f"\nendclass")
        
def create_scoreboard_file(project_name):
    with open("scoreboard.sv", "w") as f:
        f.write(f"class {project_name}_scoreboard extends uvm_scoreboard;\n"
                f"  `uvm_component_utils({project_name}_scoreboard)\n"
                f"\n"
                f"  uvm_tlm_analysis_fifo #({project_name}_xtn) mon_xtn;\n"
                f"\n"
                f"  {project_name}_xtn mon_data;\n"
                f"\n"
                f"{calling_component_function_new(project_name,'scoreboard')}"
                f"{calling_component_run_phase(project_name,'scoreboard')}"
                f"\nendclass")

def create_covergae_file(project_name):
    with open("coverage.sv", "w") as f:
        f.write(f"class {project_name}_coverage extends uvm_subscriber #({project_name}_xtn);\n"
                f"  `uvm_component_utils({project_name}_coverage)\n"
                f"\n"
                f"  {project_name}_xtn cov_data;\n"
                f"\n"
                f"  covergroup cg;\n"
                F"  endgroup\n"
                f"\n"
                f"  function new(string name = \"{project_name}_coverage\", uvm_component parent);\n"
                f"    super.new(name, parent);\n"
                f"    cg = new();\n"
                f"  endfunction\n"
                f"\n"
                f"  function void write({project_name}_xtn x);\n"
                f"    $cast(cov_data,x);\n"
                f"    cg.sample();\n"
                f"  endfunction\n"
                f"\n"
                f"endclass")
        
def create_tb_file(project_name,variables_name):
        with open("top.sv", "w") as f:
            f.write(f"`include \"pkg.sv\"\n"
                    f"`include \"intf.sv\"\n"
                    f"`include \"../design/{project_name}.v\"\n"
                    f"\n"
                    f"module top();\n"
                    f"  import pkg::*;\n"
                    f"  import uvm_pkg::*;\n"
                    f"\n"
                    f"  bit clk;\n"
                    f"\n"
                    f"  always #5 clk = ~clk;\n"
                    f"\n"
                    f"  intf vif(clk);\n"
                    f"\n")
            f.write(f" {project_name} dut(.clk(clk)")
            for var_name in variables_name:
                f.write(f",.{var_name.split()[1]}(vif.{var_name.split()[1]})")  
            f.write(f");\n"
                    f"\n"
                    f"  initial begin\n"
                    f"    uvm_config_db #(virtual intf)::set(null, \"*\", \"intf\", vif);\n"
                    f"    run_test(\"test1\");\n"
                    f"\n"
                    f"    #100\n"
                    f"    $finish();\n"
                    f"  end\n"          
                    f"endmodule\n")


def create_interface_file(variables,agent_type):
    with open("intf.sv", "w") as f:
        f.write(f"interface intf(input bit clk);\n")
                
        for var in variables:
            f.write(f"  logic {var.replace('bit', '').strip()};\n")
        
        if(agent_type == "active"):
            f.write(f"\n"
                f"  clocking drv_cb @(posedge clk);\n"
                f"    //write input output signals\n"
                f"  endclocking\n"
                f"\n")
            
        f.write(f"\n"
                f"  clocking mon_cb @(posedge clk);\n"
                f"    input ")
        for i, var in enumerate(variables):
                if i == len(variables) - 1:
                    f.write(f"{var.split()[1]};\n")
                else:
                    f.write(f"{var.split()[1]}, ")
        f.write(f"  endclocking\n"
                f"\n")
        
        if(agent_type == "active"):
                f.write(f"  modport drv_mp(clocking drv_cb);\n")

        f.write(f"  modport mon_mp(clocking mon_cb);\n"
                f"\n"
                f"endinterface\n")
        
def create_package_file(agent_type):
    with open("pkg.sv", "w") as f:
        f.write(f"package pkg;\n"
                f"  `include \"uvm_macros.svh\"\n"
                f"  import uvm_pkg::*;\n"
                f"\n"
                f"  `include \"xtn.sv\"\n")
        if(agent_type == "active"):
                f.write(f"  `include \"driver.sv\"\n")

        f.write(f"  `include \"monitor.sv\"\n")

        if(agent_type == "active"):
                f.write(f"  `include \"sequencer.sv\"\n")
            
        f.write(f"  `include \"coverage.sv\"\n")

        f.write(f"  `include \"agent.sv\"\n")

        if(agent_type == "active"):
                f.write(f"  `include \"sequence.sv\"\n")

        f.write(f"\n"
                f"  `include \"scoreboard.sv\"\n"
                f"  `include \"env.sv\"\n"
                f"  `include \"test.sv\"\n"
                f"endpackage\n")
        

def create_run_file():
    with open("run.do", "w") as f:
        f.write(f"vlog top.sv \n"
                f"vsim -novopt -suppress 12110 top -assertdebug -coverage\n"
                f"add wave -position insertpoint sim:/top/vif/*\n"
                f"run -all\n")


def calling_component_function_new(project_name,component_name=None):
    if(component_name == None):
        return (f"\n"
                f"  function new(string name = \"{project_name}\", uvm_component parent);\n"
                f"     super.new(name,parent);\n"
                f"  endfunction\n")
    elif(component_name == "scoreboard"):
        return(f"  function new(string name = \"{project_name}_{component_name}\", uvm_component parent);\n"
               f"     super.new(name,parent);\n"
               f"     mon_xtn=new(\"mon_xtn\",this);\n"
               f"  endfunction\n")
    elif(component_name == "monitor"):
        return (f"\n"
                f"  function new(string name = \"{project_name}_{component_name}\", uvm_component parent);\n"
                f"     super.new(name,parent);\n"
                f"     monitor_port=new(\"monitor_port\",this);\n"
                f"  endfunction\n")
    else:
        return (f"\n"
                f"  function new(string name = \"{project_name}_{component_name}\", uvm_component parent);\n"
                f"     super.new(name,parent);\n"
                f"  endfunction\n")


def calling_object_function_new(project_name,object_name=None):
    if(object_name == None):
        return (f"\n"
            f"  function new(string name = \"{project_name}\");\n"
            f"     super.new(name);\n"
            f"  endfunction\n")
    else:
        return (f"\n"
            f"  function new(string name = \"{project_name}_{object_name}\");\n"
            f"     super.new(name);\n"
            f"  endfunction\n")


def calling_component_build_phase(class_name,project_name=None, agent_type=None):
    build_phase_code = (
        f"\n"
        f"  function void build_phase(uvm_phase phase);\n"
        f"     super.build_phase(phase);\n"
    )

    if class_name in ["driver", "monitor"]:
        build_phase_code += (
            f"\n"
            f"     if (!uvm_config_db#(virtual intf)::get(this, \"\", \"intf\", vif))\n"
            f"        `uvm_fatal(get_type_name(), \"Virtual interface not set!\")\n"
        )

    if class_name in ["agent"]:
        build_phase_code += (
            f"\n"
            f"     monh={project_name}_monitor::type_id::create(\"monh\",this);\n"
            f"     covh={project_name}_coverage::type_id::create(\"covh\",this);\n"     
        )

    if agent_type == "active":
        build_phase_code += (
            f"     drvh={project_name}_driver::type_id::create(\"drvh\",this);\n"
            f"     seqrh={project_name}_sequencer::type_id::create(\"seqrh\",this);\n"
        )

    if class_name in ["env"]:
        build_phase_code += (
            f"\n"
            f"     agnth={project_name}_agent::type_id::create(\"agnth\",this);\n"
            f"     sb={project_name}_scoreboard::type_id::create(\"sb\",this);\n"    
        )

    if class_name in ["test"]:
        build_phase_code += (
            f"     envh={project_name}_env::type_id::create(\"envh\",this);\n"     
        )

    build_phase_code += "  endfunction\n"
    return build_phase_code

 
def calling_component_connect_phase(component_name=None,agent_type=None):
    if(component_name == "driver" and agent_type == "active"):
        return (f"\n"
            f"  function void connect_phase(uvm_phase phase);\n"
            f"     drvh.seq_item_port.connect(seqrh.seq_item_export);\n"
            f"     monh.monitor_port.connect(covh.analysis_export);\n"
            f"  endfunction\n")
    elif(component_name == "driver"):
        return (f"\n"
            f"  function void connect_phase(uvm_phase phase);\n"
            f"     monh.monitor_port.connect(covh.analysis_export);\n"
            f"  endfunction\n")
    else:
        return (f"\n"
            f"  function void connect_phase(uvm_phase phase);\n"
            f"     agnth.monh.monitor_port.connect(sb.mon_xtn.analysis_export);\n"
            f"  endfunction\n")


def calling_component_run_phase(project_name=None,component_name=None):
    if(component_name == "driver"):
        return (f"\n"
            f"  task run_phase(uvm_phase phase);\n"
            f"     req={project_name}_xtn::type_id::create(\"req\");\n"
            f"\n"
            f"     forever begin\n"
            f"        seq_item_port.get_next_item(req);\n"
            f"        send_to_dut(req);  //Create your send_to_dut function\n"
            f"        seq_item_port.item_done();\n"
            f"     end\n"
            f"  endtask\n")
    elif (component_name == "monitor"):
        return (f"\n"
                f"  task run_phase(uvm_phase phase);\n"
                f"     forever\n"
                f"       collect_data();  //Create your collect_data function\n"
                f"  endtask\n")
    elif (component_name == "test"):
        return (f"\n"
                f"  task run_phase(uvm_phase phase);\n"
                f"     seqh1=seq1::type_id::create(\"seqh1\");\n"
                f"\n"
                f"     phase.raise_objection(this);\n"
                f"       seqh1.start(envh.agnth.seqrh);\n"
                f"     phase.drop_objection(this);\n"
                f"  endtask\n")
    elif(component_name == "scoreboard"):
        return (f"\n"
                f"  task run_phase(uvm_phase phase);\n"
                f"     forever begin\n"
                f"       mon_xtn.get(mon_data);\n"
                f"     end\n"
                f"  endtask\n")


def get_project_name():
    while True:
        project_name = input("Enter Project Name: ").strip()
    
        if re.match(r"^[a-zA-Z_]+$", project_name):
            return project_name.lower()
        else:
            print("Invalid input! Please enter a valid project name (letters and underscores only).")

def get_number_of_variables():
    while True:
        project_number = input("Enter number_of_variables: ").strip()

        if project_number.isdigit():  
            return int(project_number)  
        else:
            print("Invalid input! Please enter a valid number (digits only).")

def get_agent_type():
    while True:
        agent_type = input("Enter agent type (active/passive): ").strip().lower()
        if agent_type in ["active", "passive"]:
            return agent_type.lower()
        else:
            print("Invalid input! Please enter 'active' or 'passive'.")

def main():
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    UNDERLINE = "\033[4m"
    BOLD = "\033[1m"
    RESET = "\033[0m"  # Reset to default color

    project_name = get_project_name()
    
    create_project_directory(project_name)

    create_design_directory()

    create_rtl_fiie(project_name)

    os.chdir("..")

    create_verification_directory()

    variables_names=create_transaction_file(project_name)

    agent_type = get_agent_type()
  
    create_agent_file(project_name, agent_type)
  
    if(agent_type == "active"):
       create_driver_file(project_name)
    
    create_monitor_file(project_name)

    if(agent_type == "active"):
      create_sequencer_file(project_name)

    create_env_file(project_name)

    create_test_file(project_name)
 
    if(agent_type == "active"):
      create_sequence_file(project_name)

    create_scoreboard_file(project_name)

    create_covergae_file(project_name)

    create_tb_file(project_name,variables_names)

    create_interface_file(variables_names, agent_type)

    create_package_file(agent_type)

    create_run_file()

    print()

    print(f"{RED}{BOLD}                          BOOM!               {RESET}")

    print()

    print(f"{YELLOW}{BOLD}🛠️  UVM TB Built! & live! Now, {MAGENTA}let's find those sneaky bugs before they find us! {RESET}")

    print()

    print(f"{RED}{BOLD}                          BOOM!               {RESET}")

    print()

    
if __name__ == "__main__":
    main()
