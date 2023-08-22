# Importing the Typer module
import typer
import os  
from typing import List
import click
from datetime import datetime
from tqdm import tqdm
import json

import requests

# Creating an instance of the Typer class
app = typer.Typer(name="exerc")

def highlight_last_line(text):
    # Split the text into lines
    lines = text.splitlines()
    
    # Highlight the last line with ANSI escape codes (red color)
    if len(lines) > 1:
        lines[-1] = f"\033[91m{lines[-1]}\033[0m"
    
    # Join the lines back to a single string
    return "\n".join(lines)


# Decorator for defining a func command
@app.command()  
def func():
    print("Welcome to our organization")
    
# Decorator for defining another command called hello with string parameter
@app.command()  
def hello(organization: str):
    print(f"Hello {organization}")
    
@app.command()
def area(height: int, base: int):
    A_of_triangle = (height * base)/2
    print("The Area of triangle is:" + str(A_of_triangle))
    
@app.command()
def init(directory: str):  
# , filenames: List[str]
    try:
        os.mkdir(directory)
        typer.echo(f"{directory} created successfully")
    except FileExistsError:
        typer.echo(f"{directory} already exists")
    except Exception as e:
        typer.echo(f'ERROR: {str(e)}')
    
    # else:
    #     for filename in filenames:
    #         full_path = os.path.join(directory, filename)
    #         try:
    #             with open(full_path, 'x') as f:
    #                 code = click.edit(require_save = True)
    #                 if code is not None:
    #                     f.write("# Write your code below.\n# Press Ctrl+D (Unix/Linux) or Ctrl+Z (Windows) followed by Enter to save and exit.\n")
    #                     f.write(f"# Last modified: {datetime.now()}\n\n")
    #                     f.write(code)
    #                     typer.echo("Code saved successfully.")
    #                 else:
    #                      typer.echo("No code provided. File remains empty.")
    #         except FileExistsError:
    #             typer.echo(f"{filename} already exists in {directory}")
    #         except Exception as e:
    #             typer.echo(f'ERROR: {str(e)}')
    
    
    
    
    
def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
    

# Decorator for defining config command
@app.command()
def config(
    code: str = typer.Option(None, "--code", help="Assignment Code"),
    student_id: str = typer.Option(None, "--student_id", help='Student Id'),
    interactive: bool = typer.Option(True, help="Enable interactive mode"),
):
    
    
    """Configure the repo by providing assignment code and student ID"""
    if interactive:
        if code is None:
            code = typer.prompt("Enter assignment code:")
        if student_id is None:
            student_id = typer.prompt("Enter student ID:")

    config_data = {
        "code": code,
        "student_id": student_id
    }

    try:
        # Create a folder if it doesn't exist
        if not os.path.exists(control_folder_name):
            os.mkdir(control_folder_name)
        config_path = os.path.join(control_folder_name, config_file_name)

        # Save the configuration data to a JSON file
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        typer.echo(f"Repo configured successfully. Configuration saved to {config_path}")
    except Exception as e:
        typer.echo(f"An error occurred while configuring the repo: {e}")

if __name__ == '__main__':
    app()



# import typer
# import requests

# app = typer.Typer()

# def get_student_and_assignment(code: str, student_id: str):
#     # make a get request to fetch data from student_details
#     response_student = requests.get("http://127.0.0.1:5000/student_details")
#     student_file = response_student.json()["student_details"]

#     # make a get request to fetch data from assignment_details
#     response_assignment = requests.get("http://127.0.0.1:5000/assignment_details")
#     assignment_file = response_assignment.json()["assignment_details"]

#     # initialize student as empty variable
#     student = None

#     # iterate through student file to find matching student id
#     for stu_details in student_file:
#         if stu_details["student_id"] == student_id:
#             student = stu_details
#             break

#     # initialize assignment as empty variable
#     assignment = None

#     # iterate through student file to find matching assignment code
#     for assign_details in assignment_file:
#         if assign_details["assignment_code"] == code:
#             assignment = assign_details
#             break

#     # Display student id and assignment code if both are found
#     if student is not None and assignment is not None:
#         typer.echo(f"Student_ID: {student['student_id']}\nAssignment Code: {assignment['assignment_code']}")
#     else:
#         typer.echo("Data not found")

# @app.command()
# def config(
#     code: str = typer.Option(None, "--code", "-c", help="Enter the assignment code"),
#     student_id: str = typer.Option(None, "--student_id", "-s", help="Enter your student Id"),
#     interactive: bool = typer.Option(False, "-I", help="Enable interactive mode"),
# ):
#     if interactive:
#         if code is None:
#             code = typer.prompt("Enter the assignment code")
#         if student_id is None:
#             student_id = typer.prompt("Enter your student Id")

#     if code is not None and student_id is not None:
#         get_student_and_assignment(code, student_id)
#     else:
#         typer.echo("Please provide assignment code and student ID.")

# @app.command()
# def hai():
#     pass

# # Run the script
# if __name__ == "__main__":
#     app()
