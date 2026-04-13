# AiFSC
AI machine for troubleshooting full-flight simulators.
Created by Andrew Marshall, Elyse Grein, and Paige Parson.
Created on April 12, 2026. 

Environment Used:
This application is designed to run on a Windows 10/11 machine using Python 3.10.x (required for Owlready2 compatibility) and Windows Command Prompt (cmd.exe). The program loads and reasons over an OWL ontology using Owlready2 and a bundled Java runtime from the user's local Protege installation.

To run:

Required Tools and Installation Steps:
1. Install Python 3.10 or 3.11 (Owlready2 does not support Python 3.12+)
   1.1 Go to: https://www.python.org/downloads/release/python-31011/
   1.2 Run the installer and check the "Add Python 3.10 to PATH" box
   1.3 Complete the installation
2. Install required Python Packages
   2.1 Install Owlready2 by typing "pip install owlready2" in Command Prompt
   2.2 If pip is not recognized..."python -m pip install owlready2"
3. Project Setup Instructions
   3.1 Simply download all files into one folder (including the .py and .owl files)
   3.2 Verify Java path in the script
     3.2.1 The script contains "owlready2.JAVA_EXE = r"C:\Users\paige\CS 455\Protege-5.6.7-win\Protege-5.6.7\jre\bin\java.exe"...update this path to where your java.exe inside your Protege is installed (---path---\Protege---\jre\bin\java.exe)

How to Run the Program (Command Prompt)
4. Open Command Prompt
5. Navigate to the Project Folder (cd C:\Folder)
6. Run the Application with the command "python techToolsApplication.py"

Program Usage Instructions:
Follow the Main Menus and answer the questions.
The application will come up with a solution or display components!
