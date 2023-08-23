import typer
import os
import ctypes
import platform


# creating an instance of Typer class
app = typer.Typer(name='subsys')

# variable initialization
control_folder_name= '.subsys'
config_file_name = 'config.txt'
assignment_file_name = 'assignment_info.txt'
assignment_details = None


# decorator for defining init command
@app.command() 
def init(): 
    
    """ This function initialize a repo as .subsys in a project folder"""
    
    # check if the repo folder exist
    if os.path.exists(control_folder_name):
        typer.echo("Repository is already initialized")
    else:
        try:
            # check the operating system types and make a repo folder
            os.mkdir(control_folder_name)
            if platform.system() == "Windows":
                # set the folder attribute to be hidden on windows
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ret = ctypes.windll.kernel32.SetFileAttributesW(control_folder_name, FILE_ATTRIBUTE_HIDDEN)
                if ret == 0:
                    raise ctypes.WinError()
                typer.echo(f"The {control_folder_name} repo initialized successfully.")
                
            elif platform.system() == "Linux" or platform.system() == "Darwin":
             # Rename the folder with a dot prefix to make it hidden on Linux and macOS
                typer.echo(f"The {control_folder_name} repo initialized successfully.")
                
        except OSError as e:
            typer.echo(f"Failed to initialize the repo: {e}. An error occurred while accessing the OS information:")
        except Exception as e:
            typer.echo(f"An unexpected error occurred: {e}. Please report this issue for assistance")
            

def config_file(config_data):
    
    """ this function configure the repo by saving/writing configuration data on config_file_name """
    
    # path to the configuration file
    config_path = os.path.join(control_folder_name, config_file_name)
    
    try:
        if not os.path.exists(control_folder_name):
            typer.echo("\nSeems your repo is not initialized.")
            typer.echo("Initialize the repo with subsys init command,\nThen proceed with configuration\n")
            
        # Write configuration data to the file
        with open(config_path, 'w') as file:
            file.write(f"Assignment_Code: {config_data['assignment_code']}\n")
            if 'student_id' in config_data:
                file.write(f"Student_ID: {config_data['student_id']}\n")
        typer.echo(f"Repo configured successfully. Configuration saved to {config_path}")
    except Exception as e:
        typer.echo(f"An error occurred while configuring the repo: {e}")
        

def write_on_assignment_file(assignment_name):
    """ This function Write the assignment name to assignment_name_file"""
    assignment_name_path = os.path.join(control_folder_name, assignment_file_name)
    try:
        with open(assignment_name_path, 'w') as file:
            file.write(assignment_name)
    except Exception as e:
        typer.echo(f"An error occurred while writing on assignment file: {e}")

        
# decorator for defining config command 
@app.command()
def config(
    assignment_code: str = typer.Option(None, "--code", help="Assignment Code"),
    student_id: str = typer.Option(None, "--student_id", help='Student Id'),
    interactive: bool = typer.Option(False, '-i', help="Enable interactive mode"),
): 
    
    """This function configures the repo by allowing students to enter student id and assignment code interactively"""
    
    # declare assignment_details globally to be modified inside the function
    global assignment_details
    
    # check if the interactive mode is enable
    if interactive:
        if assignment_code is None:
            assignment_code = typer.prompt("Enter the assignment code")
        if student_id is None:
            student_id = typer.prompt("Enter the student id")
        
        # create a dictionary variable to hold configured data
        config_data = {
            "assignment_code": assignment_code,
            "student_id": student_id
        }
        
        # Check if the file already exists
        config_path = os.path.join(control_folder_name, config_file_name)
        if os.path.exists(config_path):
            typer.echo('Repo is already configured')
            return
        # calling the config function and save data to file
        config_file(config_data)
        
    else:
        # if not interactive provide the users option to config the repo
        if not interactive and assignment_code is None:
            typer.echo("Usage: subsys config [OPTIONS]\n")
            typer.echo("This function configures the repo by allowing students to enter student id\nand assignment code interactively\n")
            typer.echo("Options:\n --code TEXT\t\t Assignment Code\n --student_id TEXT\t Student Id\n -i\t\t\t Enable interactive\n --help \t\t Show this message and exit")
        else:
            config_data = {
                "assignment_code": assignment_code,
            }
            if student_id is not None:
                config_data["student_id"] = student_id
            
            # Check if the file already exists
            config_path = os.path.join(control_folder_name, config_file_name)
            if os.path.exists(config_path):
                typer.echo('Repo is already configured')
                return
            
            # call config_file function
            config_file(config_data)
        
        # Check if the assignment_file_name file exists and read the content
        assignment_name_path = os.path.join(control_folder_name, assignment_file_name)
        if os.path.exists(assignment_name_path):
            try:
                with open(assignment_name_path, 'r') as file:
                    assignment_details = file.read().strip()
            except Exception as e:
                typer.echo(f"An error occurred while reading assignment file info: {e}")

# decorator for defining a command to point to an assignment
@app.command()
def get_assignment_name(
    assignment_name: str = typer.Argument(..., help="Assignment Info")
):
    """This command points the repo to a specific assignment"""
    
    global assignment_details
    assignment_details = assignment_name
    write_on_assignment_file(assignment_name)
    typer.echo(f"Repo points to {assignment_name} assignment only")
    
    
# Run the script 
if __name__ == '__main__':
    app()
