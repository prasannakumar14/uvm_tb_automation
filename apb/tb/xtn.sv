class apb_xtn extends uvm_sequence_item;
  `uvm_object_utils(apb_xtn)

  rand bit clk;
  rand bit rst;

  `uvm_object_utils_begin(apb_xtn)
   `uvm_field_int(clk, UVM_ALL_ON)
   `uvm_field_int(rst, UVM_ALL_ON)
  `uvm_object_utils_end

  function new(string name = "apb_xtn");
     super.new(name);
  endfunction

endclass