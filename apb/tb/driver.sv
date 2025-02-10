class apb_driver extends uvm_driver #(apb_xtn);
  `uvm_component_utils(apb_driver)

  virtual intf.drv_mp vif;


  function new(string name = "apb_driver", uvm_component parent);
     super.new(name,parent);
  endfunction

  function void build_phase(uvm_phase phase);
     super.build_phase(phase);

     if (!uvm_config_db#(virtual intf)::get(this, "", "intf", vif))
        `uvm_fatal(get_type_name(), "Virtual interface not set!")
  endfunction

  task run_phase(uvm_phase phase);
     req=apb_xtn::type_id::create("req");

     forever begin
        seq_item_port.get_next_item(req);
        send_to_dut(req);  //Create your send_to_dut function
        seq_item_port.item_done();
     end
  endtask

endclass