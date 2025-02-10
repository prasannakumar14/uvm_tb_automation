import os
import re

def create_project_directory(project_name):
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

def create_design_directory():
    os.makedirs("design", exist_ok=True)
    os.chdir("design")

def create_rtl_fiie():
    with open("rtl.v", "w") as f:
      f.write("module rtl();\nendmodule\n")

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
                f"  `uvm_object_utils({project_name}_xtn)\n"
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
                        f"  {project_name}_sequencer sqrh;\n")
        elif agent_type == "passive":
                f.write(f"\n"
                        f"  {project_name}_monitor monh;\n")

        f.write(f"\n"
                f"{calling_component_function_new(project_name,'agent')}"
                f"{calling_component_build_phase('agent',project_name,agent_type)}")
        if agent_type== "active":
                f.write(f"{calling_component_connect_phase()}")

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
                f"{calling_component_function_new(project_name,'env')}"
                f"{calling_component_build_phase('env',project_name)}"
                f"\nendclass")
    
def create_test_file(project_name):
    with open("test.sv", "w") as f:
        f.write(f"class {project_name}_test extends uvm_test;\n"
                f"  `uvm_component_utils({project_name}_test)\n"
                f"\n"
                f"  {project_name}_env envh;\n"
                f"{calling_component_function_new(project_name,'test')}"
                f"{calling_component_build_phase('test',project_name)}"
                f"\nendclass")
        
def create_sequence_file(project_name): 
    with open("sequence.sv", "w") as f:
        f.write(f"class {project_name}_sequence extends uvm_sequence #({project_name}_xtn);\n"
                f"  `uvm_object_utils({project_name}_sequence)\n"
                f"{calling_object_function_new(project_name,'sequence')}"
                f"\nendclass")


def create_tb_file():
        with open("tb.sv", "w") as f:
            f.write(f"`include \"pkg.sv\"\n"
                    f"`include \"intf.sv\"\n"
                    f"\n"
                    f"module tb();\n"
                    f"  bit clk;\n"
                    f"\n"
                    f"  always #5 clk = ~clk;\n"
                    f"\n"
                    f"  intf vif(clk);\n"
                    f"\n"
                    f"  initial begin\n"
                    f"    uvm_config_db#(virtual intf)::set(null, \"*\", \"intf\", vif);\n"
                    f"    run_test(\" \");\n"
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
                f"    //write input output signals\n"
                f"  endclocking\n"
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

        f.write(f"  `include \"agent.sv\"\n")

        if(agent_type == "active"):
                f.write(f"  `include \"sequence.sv\"\n")

        f.write(f"\n"
                f"  `include \"env.sv\"\n"
                f"  `include \"test.sv\"\n"
                f"endpackage\n")
        

def create_run_file():
    with open("run.do", "w") as f:
        f.write(f" #write your commands here\n")


def calling_component_function_new(project_name,component_name):
    return (f"\n"
            f"  function new(string name = \"{project_name}_{component_name}\", uvm_component parent);\n"
            f"     super.new(name,parent);\n"
            f"  endfunction\n")


def calling_object_function_new(project_name,object_name):
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

    if class_name in ["driver", "monitor", "agent"]:
        build_phase_code += (
            f"\n"
            f"     if (!uvm_config_db#(virtual intf)::get(this, \"\", \"intf\", vif))\n"
            f"        `uvm_fatal(get_type_name(), \"Virtual interface not set!\")\n"
        )

    if class_name in ["agent"]:
        build_phase_code += (
            f"\n"
            f"     monh={project_name}_monitor::type_id::create(\"monh\",this);\n"     
        )

    if agent_type == "active":
        build_phase_code += (
            f"     drvh={project_name}_driver::type_id::create(\"drvh\",this);\n"
            f"     sqrh={project_name}_sequencer::type_id::create(\"sqrh\",this);\n"
        )

    if class_name in ["env"]:
        build_phase_code += (
            f"\n"
            f"     agnth={project_name}_agent::type_id::create(\"agnth\",this);\n"     
        )

    if class_name in ["test"]:
        build_phase_code += (
            f"\n"
            f"     envh={project_name}_env::type_id::create(\"envh\",this);\n"     
        )

    build_phase_code += "  endfunction\n"
    return build_phase_code

 
def calling_component_connect_phase():
    return (f"\n"
            f"  function void connect_phase(uvm_phase phase);\n"
            f"     drvh.seq_item_port.connect(seqrh.seq_item_export);\n"
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
                f"     forever()\n"
                f"       collect_data();  //Create your collect_data function\n"
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

    create_rtl_fiie()

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

    create_tb_file()

    create_interface_file(variables_names, agent_type)

    create_package_file(agent_type)

    create_run_file()

    print()

    print("                          BOOM!               ")

    print()

    print("  UVM TB Built! & live! Now, let's find those sneaky bugs before they find us! ")

    print()

    print("                          BOOM!               ")

    print()

    
if __name__ == "__main__":
    main()
