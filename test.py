import os

def create_project_directory(project_name):
    # Create the project directory
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

def create_design_directory():
    # Create the design directory and navigate to it
    os.makedirs("design", exist_ok=True)
    os.chdir("design")

def create_rtl_directory():
    # Create the rtl directory and navigate to it
    os.makedirs("rtl", exist_ok=True)
    os.chdir("rtl")

def create_verilog_directory():
    # Create the verilog directory
    os.makedirs("verilog", exist_ok=True)

def create_verification_directory():
    # Create the verification directory and navigate to it
    os.makedirs("verif", exist_ok=True)
    os.chdir("verif")

def create_subdirectories():
    # Create subdirectories in 'verif'
    for subdir in ["sim", "top", "axi", "memory", "checker", "coverage"]:
        os.makedirs(subdir, exist_ok=True)

def create_memory_models_directory(project_name):
    # Check if the project name is 'MEM_CTRL'
    if project_name == 'MEM_CTRL':
        # Create MemoryModels directory
        os.makedirs("MemoryModels", exist_ok=True)
        os.chdir("MemoryModels")
        
        # Create memory model directories
        for model in ["sdram", "sram", "flash", "SyncCs"]:
            os.makedirs(model, exist_ok=True)
        
        # Change to the sdram directory and create the sdram.v file
        os.chdir("sdram")
        with open("sdram.v", "w+") as file:
            file.write("module sdram()\n")
            file.write("endmodule\n")

def main():
    # Prompt for project name
    project_name = input("Enter Project Name: ")

    # Create the project directory
    create_project_directory(project_name)

    # Create the design directory and navigate to it
    create_design_directory()

    # Create the rtl directory and navigate to it
    create_rtl_directory()

    # Create the verilog directory
    create_verilog_directory()

    # Go back to the project directory
    os.chdir("..")

    # Create the verification directory and navigate to it
    create_verification_directory()

    # Create subdirectories in 'verif'
    create_subdirectories()

    # Go back to the project directory
    os.chdir("..")

    # Create MemoryModels directory
    create_memory_models_directory(project_name)

if __name__ == "__main__":
    main()