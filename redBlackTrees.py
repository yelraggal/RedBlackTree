import sys
from tkinter import *


# Construct new node with its properties
class Node:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1.Red, 0.Black


class RedBlackTree:
    # Construct empty red black tree where it contains only NIL value at first
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.color = 0
        self.root = self.NIL
        self.count = 0  # To count the number of elements

    def size(self):
        return self.count

    def height(self, node):  # returns the longest path in the tree
        if node is self.NIL:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1

    def search(self, node, key):  # search until find the value or NIL
        if key == node.val:
            return True
        elif node == self.NIL:
            return False
        if key < node.val:
            return self.search(node.left, key)
        return self.search(node.right, key)

    # inserts new nodes
    def insert(self, key):
        flag = False

        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL

        temp_parent = None
        temp_node = self.root

        while temp_node is not self.NIL:
            temp_parent = temp_node  # variable to save the value of the node's parent
            if node.val < temp_node.val:
                temp_node = temp_node.left
            elif node.val > temp_node.val:
                temp_node = temp_node.right
            else:  # break the loop and make the flag true to return
                flag = True
                break

        if flag is True:
            return

        # since we didn't return, the value is new so insert the value and increment the size
        self.count += 1
        node.parent = temp_parent  # make the node's parent the last node before breaking the loop

        if temp_parent is None:  # checks if this is the first element to insert
            node.color = 0
            self.root = node
            return
        elif node.val < temp_parent.val:
            temp_parent.left = node
        else:
            temp_parent.right = node

        if node.parent.parent is None:  # return if this is a second height node since we don't need fixing
            return

        self.fix(node)

    # maintains the red black tree properties
    def fix(self, node):
        while node.parent.color == 1:  # loops until there are no 2 consecutive red nodes
            if node.parent is node.parent.parent.right:  # right-right or right-left
                uncle = node.parent.parent.left
                if uncle.color == 1:  # change colors of parent, uncle, and grandparent
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node is node.parent.left:  # right-left
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0  # right-right
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
            else:  # left-left or left-right
                uncle = node.parent.parent.right
                if uncle.color == 1:  # change colors of parent, uncle, and grandparent
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # left-right
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0  # left-left
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            if node is self.root:  # breaks if the current node is the root
                break
        self.root.color = 0

    def left_rotate(self, node):
        temp = node.right
        node.right = temp.left
        if temp.left is not self.NIL:
            temp.left.parent = node

        temp.parent = node.parent
        if node.parent is None:
            self.root = temp
        elif node is node.parent.left:
            node.parent.left = temp
        else:
            node.parent.right = temp

        temp.left = node
        node.parent = temp

    def right_rotate(self, node):
        temp = node.left
        node.left = temp.right
        if temp.right is not self.NIL:
            temp.right.parent = node

        temp.parent = node.parent
        if node.parent is None:
            self.root = temp
        elif node is node.parent.right:
            node.parent.right = temp
        else:
            node.parent.left = temp

        temp.right = node
        node.parent = temp

    def print_tree_r(self, node, indent, last):
        if node is not self.NIL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.val) + "(" + s_color + ")")
            self.print_tree_r(node.left, indent, False)
            self.print_tree_r(node.right, indent, True)
            ################# End of R-B Trees ######################


# initiate a red black tree
rbt = RedBlackTree()


def load_dictionary():  # open file and load the words
    f = open("EN-US-Dictionary.txt", "r")
    for x in f:
        x = x.strip('\n')   # strips \n from the string
        rbt.insert(x)
    f.close()
    rbt.print_tree_r(rbt.root, "", True)
    print(rbt.size())
    print(rbt.height(rbt.root))


def b_insert():     # inserts a specific word entered by the user
    temp = rbt.size()
    rbt.insert(insertVal.get())
    print(rbt.size())
    print(rbt.height(rbt.root))
    if temp == rbt.size():      # prints error message if the word already exists
        root = Tk()
        root.minsize(100, 100)
        root.title("ERROR")
        val = "ERROR: word already in the dictionary!"
        L = Label(root, text=val)
        L.place(relx=0.5, rely=0.5, anchor=CENTER)
        root.mainloop()


def b_print():      # print size of the tree
    root = Tk()
    root.minsize(100, 100)
    root.title("size")
    size = rbt.size()
    L = Label(root, text=size)
    L.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


def b_search():     # search the tree for specific word entered by the user
    root = Tk()
    root.minsize(100, 100)
    root.title("Search")
    found = rbt.search(rbt.root, searchVal.get())
    L = Label(root, text=str(found))
    L.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


def b_height():     # prints the height of the tree
    root = Tk()
    root.minsize(100, 100)
    root.title("Height")
    val = rbt.height(rbt.root)
    L = Label(root, text=val)
    L.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()

################ START OF GUI #################


top = Tk()
top.minsize(100, 200)
top.title("Red Black Trees")

# First line og GUI
L1 = Label(top, text="Enter Word")
L1.grid(row=0, column=0)
insertVal = StringVar()
E1 = Entry(top, bd=5, textvariable=insertVal)
E1.grid(row=0, column=1)
B_insert = Button(top, text="Insert Word", command=b_insert)
B_insert.grid(row=0, column=2)

# Second line of GUI
L2 = Label(top, text="Enter Word")
L2.grid(row=1, column=0)
searchVal = StringVar()
E2 = Entry(top, bd=5, textvariable=searchVal)
E2.grid(row=1, column=1)
B_search = Button(top, text="Search Word", command=b_search)
B_search.grid(row=1, column=2)

# Buttons for Load, print size, print height
B_load = Button(top, text="Load Dictionary", command=load_dictionary)
B_load.place(relx=0.5, rely=0.5, anchor=CENTER)

B_print = Button(top, text="Print Size", command=b_print)
B_print.place(relx=0.5, rely=0.7, anchor=CENTER)

B_height = Button(top, text="Print Height", command=b_height)
B_height.place(relx=0.5, rely=0.9, anchor=CENTER)
top.mainloop()
############# END OF GUI ##############
