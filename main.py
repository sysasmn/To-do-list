import curses
from curses.textpad import Textbox, rectangle 

from todo import *
from os.path import isdir, isfile
from sys import exit

todo_directory = "./" #include final backslash!

if not isdir(todo_directory):
    print("directory: "+todo_directory+"  does not exist. Exiting")
    exit()

todo_name="list.txt"
todo_address = todo_directory+todo_name

bar = "="*90

def main(stdscr, todo_list):
    stdscr.clear()
    curses.curs_set(0)
    
    MIN_Y = 40
    MIN_X = 91

    length = len(todo_list)

    def initialize_windows(y, x):
        list_x = 0
        list_y = 0
        list_l = 90
        list_h = ITEM_LIMIT+4
        
        message_x = 0
        message_y = list_h + list_y + 1
        message_l = 90
        message_h = 2

        other_y = 27
        other_h = 8

        if y < other_y + other_h:
            return -1 

        return [curses.newwin(list_h, list_l, list_y, list_x), 
                curses.newwin(message_h, message_l, message_y, message_x),
                curses.newwin(1,90,26,0),
                curses.newwin(other_h,90,other_y,0)]
    
    y, x = stdscr.getmaxyx()
   
    while y < MIN_Y or x < MIN_X:
        c = stdscr.getch()
        if curses.is_term_resized(y, x):
            y, x = stdscr.getmaxyx()
    try:
        list_win, message_win, entry_win, other_win = initialize_windows(y,x)
    
    except TypeError:
        return 0        #maybe some more feedback
        
    tb = curses.textpad.Textbox(entry_win)
    
    def display_instructions():
        other_win.clear()
        j = 0
        other_win.addstr(j,0, "a \t add item"); j+=1
        other_win.addstr(j,0, "d \t delete item"); j+=1
        other_win.addstr(j,0, "c \t clear list"); j+=1
        other_win.addstr(j,0, "w \t write changes to file"); j+=1
        other_win.addstr(j,0, "m \t move item, pushing others right."); j+=1
        other_win.addstr(j,0, "h \t prints this help."); j+=1
        other_win.addstr(j,0, "q \t quit"); j+=1

        other_win.refresh()
        #stdscr.refresh()

    def message_description():
        message_win.clear()
        message_win.addstr(0,0, "To do list. maximum 15 items, 90 characters each. Press h for help")
        message_win.refresh()
        #stdscr.refresh()

    def message_update(new_message):
        #puts any message to the user in the message window
        message_win.clear()
        message_win.addstr(0,0, new_message)
        message_win.refresh()
        stdscr.refresh()

    def update_list_screen():
        #changes list_win to display the current list in buffer
        list_win.clear()
        j = 0 #y position in the window

        list_win.addstr(j,35, "~~~ To do list ~~~")
        list_win.addstr(j+1,0, bar)
        j+=2

        if not todo_list:
            list_win.addstr(j,0, "List empty.")
            list_win.addstr(j+1, 0, bar)
            j += 2

        else:
            list_index = 1
            for i in todo_list:
                if list_index > 15:
                    break
                list_win.addstr(j,0, number_item(i, list_index))
                j += 1
                list_index += 1
            list_win.addstr(j, 0, bar)
            j+=1

        list_win.refresh()
        #stdscr.refresh()

    #display_instructions()
    #message_description()
    update_list_screen()
    stdscr.refresh()

    y, x = stdscr.getmaxyx()
    
    
    screen_too_small = 0
    message_description()
    update_list_screen()
    stdscr.refresh() 
    changeflag = 0

    def display_message(s):
        message_win.clear()
        message_win.addstr(s)
        message_win.refresh()
    
    while True:
        
        c = stdscr.getch()

        if c == ord('q'):
            if screen_too_small == 1:
                break
            if changeflag == 1:
                message_update("List not saved. Save changes? Enter y to confirm, anything else to deny")
                c = stdscr.getch()
                if c == ord('y'):
                    list_to_file(todo_list, todo_address)
                    message_update("list written to "+ todo_address+" , press any key to quit")
                    c = stdscr.getch()
            break
            
        if curses.is_term_resized(y,x):
            y, x = stdscr.getmaxyx()

            if x < MIN_X or y < MIN_Y:
                screen_too_small = 1

                list_win.clear()
                other_win.clear()
                message_win.clear()
                entry_win.clear()

                stdscr.clear()
                
                try:
                    stdscr.addstr("TERMINAL TOO SMALL")
                except curses.error:
                    pass

                stdscr.refresh()
                curses.resizeterm(y,x)
                continue

            else:
                stdscr.clear()
                curses.resizeterm(y,x)
                screen_too_small = 0
                
                list_win, message_win, entry_win, other_win = initialize_windows(y,x)
    
                tb = curses.textpad.Textbox(entry_win)
    
                stdscr.refresh()
                continue                
        
        if screen_too_small == 1:
            continue

        message_win.clear()
        message_description()
        update_list_screen()
        other_win.refresh()
        entry_win.clear()
        entry_win.refresh()
        stdscr.refresh()

        length = len(todo_list)

        if c == ord('w'): #this somehow
            n = list_to_file(todo_list, todo_address)
             
            if n == -1:
                message_update("Could not write to "+ todo_address+" .")
                continue

            message_update("list written to "+ todo_address+" .")
            message_win.refresh()
            stdscr.refresh()
            changeflag = 0
            
            continue
            
        elif c == ord('c'):
            
            if length == 0:
                message_update("List is empty!!")
                continue

            message_update("Clear list? Press y to confirm, any other key to cancel.")
            c = stdscr.getch()
            if c == ord('y'):
                todo_list = []
                length = 0
            
            changeflag = 1
            continue

        elif c == ord('h'):
            display_instructions()
            message_update("Press any key to continue.")
            other_win.clear()
            stdscr.refresh() 

        elif c == ord('a'):
            
            if length == ITEM_LIMIT:
                message_update("Item limit reached. Press any key to continue.")
                continue

            message_update("Enter new item. Leave blank or whitespace to cancel.") 
            s = tb.edit()
            if not s:
                message_update("Cancelling.")
                entry_win.clear()
                entry_win.refresh()
                continue
            
            todo_list.append(s)
            message_update("Updated.")
            changeflag = 1
            entry_win.clear()
            entry_win.refresh()
            continue

        elif c == ord('d'):
            
            if length == 0:
                message_update("List is empty. Cannot delete item. Press any key to continue.")
                continue
            
            message_update("Enter list item number (1-"+str(length)+") to delete. Enter anything else to cancel.")
            c = tb.edit()
            try:
                n = int(c)
            except ValueError:
                #message_update(str(c))
                message_update("Invalid entry. Cancelling. Press any key to continue.")
                continue

            if n < 1 or n > length:
                message_update("Cancelling. Press any key to continue.")
                continue

            todo_list = remove_item(todo_list, n)
            message_update("Item "+str(n)+" removed. Press any key to continue")
            changeflag = 1
            continue

        elif c == ord('m'):
            message_update("Enter list item (1-"+str(length)+") to be moved. Enter anything else to cancel.")
            c = tb.edit()
            try:
                n = int(c)
            except ValueError:
                message_update("Invalid Entry. Cancelling. Press any key to continue.")
                continue
            if n<1 or n>length:
                message_update("Invalid Entry. Cancelling. Press any key to continue.")
                continue
            
            entry_win.clear()
            entry_win.refresh()
            message_update("Enter list item (1-"+str(length)+") to move it to. Enter any thing else to cancel.")
            c = tb.edit()
            try:
                m = int(c)
            except ValueError:
                message_update("Invalid Entry. Cancelling. Press any key to continue.")
                continue
            
            if m<1 or m>length:
                message_update("Invalid Entry. Cancelling. Press any key to continue.")
                continue

            if n == m:
                message_update("Moved. Press any key to continue.")
                continue
            
            move_here(todo_list, n-1, m-1)
            message_update("Moved. Press any key to continue.")
            changeflag = 1
            continue

        else:
            continue
    
todo_list = file_to_list(todo_address)

if todo_list == -1: #file_to_list could not open or a create a file. There must be a problem with permissions or dir
    print("Cannot open or create a file at "+todo_address+". Check permissions. Exiting")
    exit()

curses.wrapper(main,todo_list) #to make sure terminal works correctly after non-standard exit from program
