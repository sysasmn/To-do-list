from os.path import isfile

""" 

To do list should look like this:
Do thing
do next thing
go place

seperated by newlines, and a character limit per line
should there be a "mark as done function? no"

"""
ITEM_LIMIT = 15

def number_item(item, n):
    return (str(n)+". "+item)

def iswhitechar(c):
    if c == ' ' or c == '\t' or c == '\n':
        return True
    return False

def iswhitespace(s):
    for i in s:
        if not iswhitechar(i):
            return False
    return True

def stripnewline(s): #strips string of newlines
    r = ""
    for i in s:
        if i == '\n':
            continue
        r+= i
    return r

def list_to_file(seq, directory):
    #I need to make sure this creates list if the path isn't there
    try:
        f = open(directory, "w+")
    except IOError:
        #print(directory, " : path does not exist.")
        return -1

    for i in seq:
        f.write(stripnewline(i)+'\n')
    #print(f.read())
    f.close()
    return 1

def file_to_list(directory):
    #this of course needs to have an item limit
    #and character limit for each line
    
    #check file exists and create if not
    if not isfile(directory):
        try:
            f = open(directory,"x")
            f.close()
            return []
        except IOError:
            #print(directory, " path does not exist")
            return -1
    try: 
        f = open(directory, "r+")
    except IOError:
        #print(directory, " path does not exist.")
        return -1
    
    l = []
    count = 0
    for i in f.readlines():
        if iswhitespace(i):
            continue

        if count == ITEM_LIMIT:         #too many items
            break       
        k = stripnewline(i)
        if len(k) > 90:
            l.append(k[0:90])
            count += 1
            continue
        l.append(k)
        count += 1

    f.close()
    return(l)

def display_todo_list(l):
    j = 1
    if not l:
        print("To do list is empty.")
    for i in l:
        print(str(j)+". "+i)
        j+=1

def remove_item(l, n):
    #n starts from 1, not zero
    #del l[n-1] - del bad according to stackexchange
    #so instead I'm going to use slicing
    #type of input (as in make sure its an int) should be checked at input
    
    length = len(l)
    
    if length == 0:
        print("List empty.\n")
        return l

    #invalid n
    if n>length or n<=0:
        print(n,": Invalid index.\n")
        return(l)

    if n == 1:
        return l[1:]
    
    if n == length:
        return l[0:n-1] 
    
    return l[0:n-1] + l[n:length]

def add_item(l, item, n):
    #I don't like that list.insert() changes the list. 
    length = len(l)


    if n>length+1 or n<=0:
        print(n, ": Invalid number.\n")
        return(l)

    if length == 0:
        return [item]
    
    if n==length+1:
        return(l+[item])

    if n==1:
        return([item]+l)

    #l.insert(n-1, item)
    return(l[0:n-1]+[item]+l[n-1:])

def swap_items(l, i, j):
    #swaps items with index i and j
    n = length(l)-1
    if i < 0 or i > n-1:
        return -1

    if j < 0 or j > n-1:
        return -1

    temp = l[i]
    l[i] = l[j]
    l[j] = temp
    
    return l

def move_here(l, from_ind, to_ind):
    #pushes everything right
    #finish you later!
    
    n = len(l)-1
    
    if from_ind < 0 or from_ind > n:
        return -1

    if to_ind < 0 or to_ind > n:
        return -1
    
    if from_ind == to_ind:
        return l

    item = l[from_ind]
    
    l.pop(from_ind)
    l.insert(to_ind, item)
    return(l)


def barrier():
    print("==========================")

testlist = ["Do this thing", "go to place", "pay bill"]

#display_todo_list(testlist)


def print_list_instructions(l):
    barrier()
    display_todo_list(l)
    barrier()
    print("enter h for help.")

def print_help():
    print("To do list program. Up to 15 items allowed.")
    print("a \t add item")
    print("d \t delete item")
    print("c \t clear list")
    print("w \t write changes")
    print("p \t print list")
    print("q \t quit")

#print(stripnewline("\n \n testing."))
