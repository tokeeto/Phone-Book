import mysql.connector
from dotenv import load_dotenv
import os
from time import sleep

class Phonebook:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute("CREATE TABLE Phonebook (Name VARCHAR(30) NOT NULL, Telephone VARCHAR(25) PRIMARY KEY, City VARCHAR(20))")
        except:
            pass

    def mainMenu(self):
        while True:
            opt = input("\n1. ADD CONTACT\t\t4. SEARCH SPECIFIC CONTACT\n2. MODIFY CONTACT\t5. EXIT\n3. DELETE CONTACT\n\nSelect: ")

            if opt == "1":
                self.addContact()
                break
            elif opt == "2":
                self.modifyContact()
                break
            elif opt == "3":
                self.deleteContact()
                break
            elif opt == "4":
                self.searchContact()
                break
            elif opt == "5":
                break
            else:
                print("\nINVALID INPUT!!")

    def addContact(self):
        print("\n\n\t\tADD CONTACT")

        contact_name = input("\n\nEnter the name of contact: ").strip().title()
        if contact_name == "":
            contact_name = None

        tel_num = input("Enter the telephone number: ").strip()
        if tel_num == "":
            tel_num = None

        city = input("Enter the city(Optional): ").strip()
        if city == "":
            city = 'None'

        try:
            self.cursor.execute(f"INSERT INTO Phonebook VALUES('{contact_name}', '{tel_num}', '{city}')")

        except mysql.connector.errors.IntegrityError:
            print("\nErrors occurred! The 'Name' OR 'Telephone number' cannot be empty AND the 'Telephone number' must be unique!")
            self.addContact()

        else:
            print("\nAdding the contact...")
            sleep(2)

            self.db.commit()
            print("\nThe contact number has successfully been added!")

            opt = input("\nEnter '1' to Add another contact, and enter 'any key' to go to main menu: ").strip()
            if opt == "1":
                self.addContact()
            else:
                self.mainMenu()

    def modifyContact(self):
        self.cursor.execute("SELECT Name FROM Phonebook")
        name_list = self.cursor.fetchall()

        contact_name = input("\nEnter the name of contact you want to modify: ").strip().title()
        copy_name = contact_name,    # convert the string into tuple

        print("\nSearching...")
        sleep(2)

        if copy_name in name_list:
            new_num = input("Enter the new telephone number: ").strip()

            self.cursor.execute(f"UPDATE Phonebook SET Telephone = '{new_num}' WHERE Name = '{contact_name}'")
            self.db.commit()

            print("\nModifying...")
            sleep(2)
            print("\nSuccessfully modified!")
        else:
            print(f"\n{contact_name} does not exist within the Phonebook. Please refer to 'ADD CONTACT'!")
        
        opt = input("\nEnter '1' to Modify another contact, and enter 'any key' to go to main menu: ").strip()
        if opt == "1":
            self.modifyContact()
        else:
            self.mainMenu()
    
    def deleteContact(self):
        contact_name = input("\nEnter the contact name: ").strip()

        self.cursor.execute(f"DELETE FROM Phonebook WHERE Name = '{contact_name}'")
        db.commit()

        print("\nDeleting...")
        sleep(2)
        print("\nDeletion of contact is successful!")

        opt = input("\nEnter '1' to Delete another contact, and enter 'any key' to go to main menu: ").strip()
        if opt == "1":
            self.deleteContact()
        else:
            self.mainMenu()
    
    def searchContact(self):
        contact_name = input("\nEnter the contact name to search: ").strip()

        print("\nSearching...")
        sleep(2)

        self.cursor.execute(f"SELECT * FROM Phonebook WHERE Name LIKE '%{contact_name}%'")
        contact_list = self.cursor.fetchall()

        if len(contact_list) == 0:
            print("\nThe searched contact is not found!")
        else:
            for i in range(len(contact_list)):
                print(f"\nContact Name:\t\t{contact_list[i][0]}\nTelephone Number:\t{contact_list[i][1]}\nCity:\t\t\t{contact_list[i][2]}")

        opt = input("\nEnter '1' to Search another contact, and enter 'any key' to go to main menu: ").strip()
        if opt == "1":
            self.searchContact()
        else:
            self.mainMenu()

if __name__ == "__main__":
    load_dotenv()

    db = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        database = os.getenv("DB_NAME")
    )

    my_phonebook = Phonebook(db)
    my_phonebook.mainMenu()
