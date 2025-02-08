#!/usr/bin/python
# create MEM_CTRL TB directory structure
# MEM_CTRL -> design, verif, MemoryModels -> 
# design -> rtl -> verilog
# verif -> top, axi, memory, checker, coverage, sim
import os
import sys
print ("Creating project directory structure:\n")
print("Enter Project Name:")
#proj = sys.stdin
proj = input()
#proj.rstrip()
#mkdir used to create direcotry in Unix => same can be run perl using system("mkdir MEM_CTRL")
os.system("mkdir %s"%proj)
os.chdir("%s"%proj) # or die "Unable to change to dir $proj$!\n"
cur_dir = os.getcwd()
os.system("mkdir design")
os.chdir("design")
if not os.path.exists("rtl"):
  os.mkdir("rtl")
os.chdir("rtl")
if not os.path.exists("verilog"):
  os.mkdir("verilog")

#come back to place where we started
os.chdir(cur_dir)
cur_dir = os.getcwd()
#verilog will be create inside design 
os.mkdir("verif")
os.chdir("verif")
os.mkdir("sim")
os.mkdir("top")
os.mkdir("axi")
os.mkdir("memory")
os.mkdir("checker")
os.mkdir("coverage")
os.chdir("$cur_dir")
cur_dir = os.getcwd()
if (proj == 'MEM_CTRL') :
	os.mkdir("MemoryModels")
	os.chdir("$cur_dir")
	os.chdir("MemoryModels")
	os.mkdir("sdram")
	os.mkdir("sram")
	os.mkdir("flash")
	os.mkdir("SyncCs")
	os.chdir("sdram")
	FILE_WR = open("sdram.v", "w+")
	FILE_WR.write("module sdram()\n")
	FILE_WR.write("endmodule")
	FILE_WR.close()
