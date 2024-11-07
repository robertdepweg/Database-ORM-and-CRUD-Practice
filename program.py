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

            ####################################
            # Query and print out all entries  #
            ####################################

            ui.print("Query and print out all entries")
            # Get the employees from the database
            employees = session.query(Employee).all()

            # Create string for concatenation
            output_string = ""

            # Convert each employee to a string and add it to the outputstring
            for employee in employees:
                # Concatenate to the output_string
                output_string += f"{employee}{os.linesep}"

            # Use the UI class to print out the string
            ui.print_list(output_string)

            #####################################
            # Query single entry by primary key #
            #####################################

            ui.print("Query single entry by primary key")
            employee_by_pk = session.query(Employee).get(1)
            ui.print_entry(employee_by_pk)

            ####################################
            # Query single entry by critera    #
            ####################################

            ui.print("Query single entry by critera")
            single_employee_by_critera = (
                session.query(
                    Employee,
                )
                .filter(Employee.first_name == "Jean-Luc",
                )
                .first()
            )
            ui.print_entry(single_employee_by_critera)

            ####################################
            # Query multiple entry by critera  #
            ####################################

            ui.print("Query multiple entries by critera")
            employee_by_critera = (
                session.query(
                    Employee,
                ).filter(
                    Employee.weekly_salary > 400,
                )
                .all()
            )
            output_string = ""
            for employee in employee_by_critera:
                output_string += f"{employee}{os.linesep}"
            ui.print_list(output_string)

            ####################################
            # Add a new entry to the database  #
            ####################################

            ui.print("Add a new entry to the database")
            new_employee = Employee("David", "Barnes", 999.99)
            session.add(new_employee)
            session.commit()

            employees = session.query(Employee).all()
            output_string = ""
            for employee in employees:
                output_string += f"{employee}{os.linesep}"
            ui.print_list(output_string)

            #############################################
            # Update an existing entry in the database  #
            #############################################
            
            ui.print("Update an existing entry in the database")
            employee_to_update = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David"
                )
                .first()
            )
            ui.print_entry(employee_to_update)

            employee_to_update.last_name = "BBBBBBarnesssssss"
            session.commit()

            ui.print("Re-Query to verify it was actually updated.")
            employee_to_update = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David"
                )
                .first()
            )
            ui.print_entry(employee_to_update)

            ##############################################
            # Delete an existing entry from the database #
            ##############################################

            ui.print("Delete an entry from the database")
            employee_to_delete = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_delete)
            session.delete(employee_to_delete)
            session.commit()

            # Should result in nothing being being returned now that it's deleted.
            ui.print("Delete an entry from the database")
            employee_to_delete = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_delete)
            if employee_to_delete is None:
                ui.print("Record successfully deleted.")

            # Print whole list again to verify the record is gone
            employees = session.query(Employee).all()
            output_string = ""
            for employee in employees:
                output_string += f"{employee}{os.linesep}"
            ui.print_list(output_string)


        # Check for different choice here if there was one to check.

        # Lastly, re-prompt user for input on what to do.
        selection = ui.display_menu_and_get_response()
