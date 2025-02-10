interface intf(input bit clk);
  logic clk;
  logic rst;

  clocking drv_cb @(posedge clk);
    //write input output signals
  endclocking


  clocking mon_cb @(posedge clk);
    //write input output signals
  endclocking

  modport drv_mp(clocking drv_cb);
  modport mon_mp(clocking mon_cb);

endinterface
