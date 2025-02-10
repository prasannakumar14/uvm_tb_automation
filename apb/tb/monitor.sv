class apb_monitor extends uvm_monitor;
  `uvm_component_utils(apb_monitor)

  virtual intf.mon_mp vif;


  function new(string name = "apb_monitor", uvm_component parent);
     super.new(name,parent);
  endfunction

  function void build_phase(uvm_phase phase);
     super.build_phase(phase);

     if (!uvm_config_db#(virtual intf)::get(this, "", "intf", vif))
        `uvm_fatal(get_type_name(), "Virtual interface not set!")
  endfunction

  task run_phase(uvm_phase phase);
     forever()
       collect_data();  //Create your collect_data function
  endtask

endclass