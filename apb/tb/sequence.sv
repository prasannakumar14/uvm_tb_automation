class apb_sequence extends uvm_sequence #(apb_xtn);
  `uvm_object_utils(apb_sequence)

  function new(string name = "apb_sequence");
     super.new(name);
  endfunction

endclass
class seq1 extends apb_sequence);
  `uvm_object_utils(seq1)

  function new(string name = "seq1");
     super.new(name);
  endfunction

  task body();
    repeat(10) begin
      req = apb_xtn::type_id::create("req");
      start_item(req);
        req.randomize();
      finish_item(req);
  endtask

endclass