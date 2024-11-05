"""Program code"""

# System Imports
import os

# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# First-Party imports
from employee import Employee, Base
from user_interface import UserInterface
from utils import CSVProcessor

engine = create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def create_database():
    """Create the database"""
    Base.metadata.create_all(engine)


def populate_database(employees):
    """Populate database from list of employees"""
    for employee in employees:
        session.add(employee)
        session.commit()


def main(*args):
    """Method to run program"""

    employees = []

    # Make a new instance of the UserInterface class
    ui = UserInterface()

    # If we do not have the database, we can create it.
    if not os.path.exists("./db.sqlite3"):
        # Create the database
        create_database()

    # Check to see if there are any records in the DB
    # If not, use CSV to load up Employees. Then put in DB.
    if session.query(Employee).first() is None:

        # Path to CSV file
        path_to_csv_file = "employees.csv"

        # Make new instance of CSVProcessor class
        csv_processor = CSVProcessor()

        # Reading the CSV file could raise exceptions. Be sure to catch them.
        try:
            # Call the import_csv method sending in our path to the csv and the Employee list.
            csv_processor.import_csv(path_to_csv_file, employees)
        except FileNotFoundError:
            ui.print_file_not_found_error()
        except EOFError:
            ui.print_empty_file_error()

        # Populate the database with data from the CSV
        populate_database(employees)

    # Get some input from the user
    selection = ui.display_menu_and_get_response()

    # While the choice they selected is not 2, continue to do work.
    while selection != ui.MAX_MENU_CHOICES:
        # See if the input they sent is equal to 1.
        if selection == 1:
            # Create string for concatenation
            output_string = ""

            # Convert each employee to a string and add it to the outputstring
            for employee in employees:
                # Concatenate to the output_string
                output_string += f"{employee}{os.linesep}"

            # Use the UI class to print out the string
            ui.print_list(output_string)

        # Check for different choice here if there was one to check.

        # Lastly, re-prompt user for input on what to do.
        selection = ui.display_menu_and_get_response()
