class apb_test extends uvm_test;
  `uvm_component_utils(apb_test)

  apb_env envh;

  function new(string name = "apb_test", uvm_component parent);
     super.new(name,parent);
  endfunction

  function void build_phase(uvm_phase phase);
     super.build_phase(phase);

     envh=apb_env::type_id::create("envh",this);
  endfunction

endclass