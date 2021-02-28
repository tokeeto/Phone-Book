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
        except:  # bad! Always be explicit about which exceptions you can handle. What if you had a ConnectionError exception?
            pass

    def mainMenu(self):
        while True:
            opt = -1
            while opt not in ('1', '2', '3', '4', '5'):
                opt = input("\n1. ADD CONTACT\t\t4. SEARCH SPECIFIC CONTACT\n2. MODIFY CONTACT\t5. EXIT\n3. DELETE CONTACT\n\nSelect: ")
                if opt not in ('1', '2', '3', '4', '5'):
                    print('INVALID INPUT')

            if opt == "1":
                self.addContact()
            if opt == "2":
                self.modifyContact()
            if opt == "3":
                self.deleteContact()
            if opt == "4":
               self.searchContact()
            if opt == "5":
                return
        
    def addContact(self):
        print("\n\n\t\tADD CONTACT")

		print('\n\n')
        contact_name = input("Enter the name of contact: ").strip().title() or None
        tel_num = input("Enter the telephone number: ").strip() or None
        city = input("Enter the city(Optional): ").strip() or None
        
        try:
            self.cursor.execute(f"INSERT INTO Phonebook VALUES('{contact_name}', '{tel_num}', '{city}')")
        except mysql.connector.errors.IntegrityError:
            print("\nErrors occurred! The 'Name' OR 'Telephone number' cannot be empty AND the 'Telephone number' must be unique!")
            self.addContact()
        else:
            print("\nAdding the contact...")
            self.db.commit()
            print("\nThe contact number has successfully been added!")

    def modifyContact(self):
        self.cursor.execute("SELECT Name FROM Phonebook")
        name_list = self.cursor.fetchall()

        contact_name = input("\nEnter the name of contact you want to modify: ").strip().title()
        copy_name = contact_name,    # convert the string into tuple

        print("\nSearching...")

        # bad sql code - names could be identical
        if copy_name in name_list:
            new_num = input("Enter the new telephone number: ").strip()

            self.cursor.execute(f"UPDATE Phonebook SET Telephone = '{new_num}' WHERE Name = '{contact_name}'")
            self.db.commit()
            print("Successfully modified!")
        else:
            print(f"\n{contact_name} does not exist within the Phonebook. Please refer to 'ADD CONTACT'!")
    
    def deleteContact(self):
        contact_name = input("\nEnter the contact name: ").strip()
        self.cursor.execute(f"DELETE FROM Phonebook WHERE Name = '{contact_name}'")
        db.commit()
        print("\nDeletion of contact is successful!")
        
    def searchContact(self):
        contact_name = input("\nEnter the contact name to search: ").strip()
        self.cursor.execute(f"SELECT * FROM Phonebook WHERE Name LIKE '%{contact_name}%'")
        contact_list = self.cursor.fetchall()

        for i in range(len(contact_list)):
            print(f"\nContact Name:\t\t{contact_list[i][0]}\nTelephone Number:\t{contact_list[i][1]}\nCity:\t\t\t{contact_list[i][2]}")
        else:
            print("\nThe searched contact is not found!")

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
        
