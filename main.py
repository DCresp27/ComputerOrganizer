import os  # file and directory operations
import shutil  # file moving operations
import threading
from subprocess import call  # open files using QuickLook
import re  # To use Regex
from subprocess import Popen, DEVNULL # So that the code will continue running while quicklook is open we import Popen instead of call

# Expanduser user allows the '~' symbol to be used to mean home directory (just like in cmd line).
# This defines the path to the downloads folder, which is used globally by the script
downloads_folder = os.path.expanduser(
    "~/Downloads")
new_folder_path = os.path.expanduser(
    "~/Desktop/New Folder")  # Path to the new folder is defined. It will be used to create it in the code


def main():
    for file_name in sorted(os.listdir(downloads_folder)):
        # Create the new directory if it doesn't already exist using the path defined above
        os.makedirs(new_folder_path, exist_ok=True)

        if not file_name.startswith('.'):  # This excludes hidden files which contain meta-data or system configs

            file_path_name = os.path.join(downloads_folder, file_name)
            if os.path.isfile(file_path_name):
                print(f"\nProcessing file: {file_name}")
                process_file(file_path_name)
    print("Folder is empty!")




def process_file(file_path):
    choice = get_user_choice()
    if choice == "1":  # Remove File
        os.remove(file_path)
        print("File: ", file_path, "Has been deleted")

    elif choice == "2":
        renameFile(file_path)


    elif choice == "3":  # Open QuickLook to decide what to do
        quicklook(file_path, timeout=10)


    else:
        print("Invalid choice.")
        get_user_choice()


def quicklook(file_path, timeout=10):
    # Start the QuickLook process
    ql = Popen(["qlmanage", "-p", file_path], stdout=DEVNULL, stderr=DEVNULL)  # Popen instead of Call so that the code does not stall when quicklook is open


    print("QuickLook opened.")
    print("What would you like to do now?")


    # Start a timer to kill the QuickLook process after a delay
    timer = threading.Timer(timeout, ql.terminate)
    timer.start()
    process_file(file_path)

def renameFile(file_path):
    extension = os.path.splitext(file_path)[1]  # splitext returns a tuple. The first index is the extension
    new_name = input("Please enter a new name for the file: ")
    new_path = os.path.join(downloads_folder, new_name)
    if validNameChecker(
            new_path):  # Handle the conflict here, such as prompting for a new name or generating a unique name
        try:
            fully_qualified_new_name = new_path + extension  # Adds the file extension to the new name (.txt and such)
            os.rename(file_path, fully_qualified_new_name)
            print(f"File renamed to: {new_name}")
            MoveToNewFolder(new_name, extension, fully_qualified_new_name)

        except OSError as e:  # Normal errors (illegal chars used and duplicate file names are all accounted for manually in the code
            print(f"An unexpected error occurred while renaming the file: {e}")

    else:
        print("It seems like another file with this name exists in this directory.")
        renameFile(file_path)


def MoveToNewFolder(new_name, extension, fully_qualified_new_name):
    new_path_in_new_folder = os.path.join(new_folder_path,
                                          new_name + extension)  # Combines the file path to the new folder, with the name (just the name, not the path) of our newly named file
    shutil.move(fully_qualified_new_name, new_path_in_new_folder)
    print(f"File moved to {new_folder_path}")


def validNameChecker(new_path):
    checkNameForSymbols(new_path)
    if os.path.exists(new_path):
        print("A file with the same name already exists. Please provide a different name.")
        return False
    else:
        return True


def checkNameForSymbols(new_path):
    pattern = r'^[^<>:"/\\|?*\x00-\x1F]*$'  # ^ is negation in regex. So it will match a string that has none of the forbidden chars
    return re.match(pattern, new_path) is not None  # A regex that does not match returns 'None'


def get_user_choice():
    print("Options:")
    print("1. Delete")
    print("2. Rename and move")
    print("3. QuickLook")
    choice = input("Enter your choice (1/2/3): ")
    return choice


if __name__ == "__main__":
    print("Cleaning Downloads folder...\n")
    main()
