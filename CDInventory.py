#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AyersA, 2022-Nov-16, Moved logic from procedural into functions.
#                      Created function to append new CDs into the list.
#                      Created Function to process deletes from the list. 
#                      Added code to write_file function.
#                      Created function to accept user inputs
# AyersA, 2022-Nov-25, Adjusted file operations to use pickle in read/write functions.
#                      Added error handling to handle text inputs for delete operation.
#                      Added error handling to handle text inputs for ID when adding entry.
#                      Added error handling to create a file if isn't found. 
#------------------------------------------#

# -- PACKAGES -- #
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def append_record_to_list(id_num, title, artist):
        """
        Function to append a new record to the table
        
        Converts ID to an int, Appends the ID, Title, and Artist as a dictionary to the lstTbl.
        
        Parameters
        ----------
            id_num (string): id number of the record to be added
            title (string): Title of the album to be added
            artist (string): Artist for the albumb being added
        
        Returns
        -------
            Text Reponse. 
        """
        intID = int(id_num)
        dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
        lstTbl.append(dicRow)
        return 'The CD was added'

    @staticmethod
    def process_deletes(intIDDel):
        """
        Function to process deletes from the table.

        Parameters
        ----------
        id_num : TYPE
            ID number of the item to be deleted.

        Returns
        -------
        Text response. 

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            return 'The CD was removed'
        else:
            return 'Could not find this CD!'

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from a binary file to a list of dictionaries

        Assumes pickled data.  Unpickles and reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Parameters
        ----------
            file_name (string): name of file used to read the data from. Requires data to be saved in binary. 
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns
        -------
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file

        with open(file_name, 'rb') as fileObj:
            data = pickle.load(fileObj)
            for i in data:
                table.append(i)

            
        
    @staticmethod
    def write_file(file_name, table):
        """Function to manage data saving from a list of dictionaries to a file in a binary format.

        Reads the data from a list of dictionaries into a file identified by file_name and saves data as binary.

        Parameters
        ----------
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns
        -------
            Text reponse.
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)
       
        print('Data was saved to file \n')


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Parameters
        ----------
            None.

        Returns
        -------
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Parameters
        ----------
            None.

        Returns
        -------
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Parameters
        ----------
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns
        -------
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')
        
    def get_album_inputs():
        """
        function to get user inputs for album id number, title, and arist.

        Returns
        -------
            Tuple: ID number, title, artist

        """

        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        
        return (strID, strTitle, stArtist)


# 1. When program starts, read in the currently saved Inventory
try:
    FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError:
    # create a blank file if a file is not found
    FileProcessor.write_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        inputs = IO.get_album_inputs()
        try:
            int(inputs[0])
        except ValueError:
            print('\nError: ID must be an integer.')
            print('Entry not saved.\n ')
            continue
        # 3.3.2 Add item to the table
        DataProcessor.append_record_to_list(inputs[0], inputs[1], inputs[2])
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = input('Which ID would you like to delete? ').strip()
        try: 
            toInt = int(intIDDel)
            intIDDel = toInt
        except ValueError:
            print('\nError: ID to delete must be an Integer.\n')
            continue        
        # 3.5.2 search thru table and delete CD
        DataProcessor.process_deletes(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




