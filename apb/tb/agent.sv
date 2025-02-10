class apb_agent extends uvm_agent;
  `uvm_component_utils(apb_agent)

  apb_driver drvh;
  apb_monitor monh;
  apb_sequencer sqrh;


  function new(string name = "apb_agent", uvm_component parent);
     super.new(name,parent);
  endfunction

  function void build_phase(uvm_phase phase);
     super.build_phase(phase);

     if (!uvm_config_db#(virtual intf)::get(this, "", "intf", vif))
        `uvm_fatal(get_type_name(), "Virtual interface not set!")

     monh=apb_monitor::type_id::create("monh",this);
     drvh=apb_driver::type_id::create("drvh",this);
     sqrh=apb_sequencer::type_id::create("sqrh",this);
  endfunction

  function void connect_phase(uvm_phase phase);
     drvh.seq_item_port.connect(seqrh.seq_item_export);
  endfunction

endclass