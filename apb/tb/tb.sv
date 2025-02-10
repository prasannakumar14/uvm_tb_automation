`include "pkg.sv"
`include "intf.sv"

module tb();
  bit clk;

  always #5 clk = ~clk;

  intf vif(clk);

  initial begin
    uvm_config_db#(virtual intf)::set(null, "*", "intf", vif);
    run_test(" ");

    #100
    $finish();
  end
endmodule
