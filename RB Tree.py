# Algorithms HW 4
# Rachael Judy
# Group: Peter Duttweiler
# 9/18/2020
"""
Modifiable Test Functions at Bottom
Table of Contents: Line Number
Node class: line 30 - defines nodes in tree, includes boolean isBlack for color
Tree class: line 40 - defines Tree with NIL nodes for each tree and root, NIL had to be reassigned for NIL's parents
Minimum: line 54 - Minimum finds lowest value from that node by tracing left
Maximum: line 61 - Maximum finds highest tracing right
Successor: line 69 - pass in tree and node to find successor to key of node passed
Predecessor: line 83 - find predecessor of node passed in
Search: line 96 - looks for matching node to key of node passed in
Transplant: 108 - replaces Node with Node v in tree, does not handle v's children
Insert: 123 - put node in BST
Delete: 148 - remove node from BST - contains some unnecessary BST code for the RB BST delete
RB_Delete: 185 - remove node from RB BST, checks if node with requested key exists
RB_Insert: 178 - insert in RB BST
RB_Insert_Fixup: 197 - fix errors caused by insertion
RB_Delete_Fixup: 241 - fix errors caused by deletion in color
Right_Rotate: 311 - rotates tree from x clockwise
Left_Rotate: 298 - rotates tree cc
Print_In_Order: 332 - displays the key values from minimum to max by recursively calling left
Array_Print: 340 - displays the array created for the tree to see positions, can modified to see null nodes
Fill_Tree_Array: 348 - fills the tree array by line - doesn't include NILs for spacing - use with print in order to verify
"""

# Node class used to represent the nodes of the tree
class Node:
    def __init__(self, data=None, black=True):
        self.key = data
        self.parent = None
        self.left = None
        self.right = None
        self.isBlack = black  # black default


# tree class has root and Nil node
class Tree:
    def __init__(self):
        # for RB implementation
        self.NIL = Node()
        self.root = self.NIL

        self.NIL.left = self.root
        self.NIL.right = self.root
        self.root.parent = self.NIL

        self.arrayForm = [[]]  # for the array print version


# finds minimum relative to node passed in, assuming actually in tree
def Minimum(T, node):
    while node.left is not T.NIL:
        node = node.left
    return node


# finds maximum relative to node passed in
def Maximum(T, node):
    while node.right is not T.NIL:
        node = node.right
    return node


# finds successor (next highest value) relative to node key
def Successor(T, node):
    node = Search(T, T.root, node.key)  # find the node referenced if not given present node in tree (for use outside function)
    if node.right is not T.NIL:  # if larger child, trace to minimum
        return Minimum(T, node.right)

    # trace up the tree until no longer right child
    p_node = node.parent
    while p_node is not T.NIL and node == p_node.right:
        node = p_node
        p_node = p_node.parent
    return p_node


# finds predecessor of node
def Predecessor(T, node):
    node = Search(T, T.root, node.key)
    if node.left is not T.NIL:
        return Maximum(T, node.left)

    p_node = node.parent
    while p_node is not T.NIL and node == p_node.left:
        node = p_node
        p_node = p_node.parent
    return p_node


# searches for requested key k from node down in tree
def Search(T, node, k):
    if node is T.NIL or k == node.key:
        return node

    # search down tree
    if k < node.key:
        return Search(T, node.left, k)
    else:
        return Search(T, node.right, k)


# replaces the subtree at u with the subtree at v, leaves u in the cold
def Transplant(T, u, v):
    if u.parent is T.NIL:  # if one node's parent does not exist, set root
        T.root = v
        T.NIL.right = T.root  # must reassign to point NIL at new root
        T.NIL.left = T.root
    elif u == u.parent.left:  # if u is left child, replace subtree
        u.parent.left = v
    else:
        u.parent.right = v

    # can assign regardless because of NIL node use
    #    if v is not T.NIL:  # if v is not a Nil node, give it u's parent
    v.parent = u.parent


# insert for BST
def Insert(T, node):  # insert node in tree from root
    y = T.NIL
    x = T.root
    while x is not T.NIL:  # go down tree finding the insertion point
        y = x
        if node.key < x.key:  # if the node's key is less than the current subtree's root
            x = x.left
        else:
            x = x.right
    node.parent = y

    if y is T.NIL:  # if parent is not existent, no element in tree
        T.root = node
        T.NIL.left = T.root  # necessary to fix
        T.NIL.right = T.root
    elif node.key < y.key:  # decide which side to put node
        y.left = node
    else:
        y.right = node

    node.left = T.NIL  #since we're using the NIL node, must explicitly assign
    node.right = T.NIL


# removes node from BST
def Delete(T, node):
    node = Search(T, T.root, node.key)  # works if user says Delete(tree, Node(key))
    y = node
    color = y.isBlack
    if node == T.NIL:
        return
    if node.left is T.NIL:  # no left child  # case 1
        x = node.right  # inplace for RB tree usage
        Transplant(T, node, node.right)
    elif node.right is T.NIL:  # case 2
        x = node.left  # inplace for RB tree usage
        Transplant(T, node, node.left)
    else:  # two children
        y = Minimum(T, node.right)  # gets successor
        color = y.isBlack
        x = y.right  # inplace for RB tree usage
        if y.parent == node:
            x.parent = y
        else:  # case 4
            Transplant(T, y, y.right)
            y.right = node.right
            y.right.parent = y
        Transplant(T, node, y) # case 3
        y.left = node.left
        y.left.parent = y
        y.isBlack = node.isBlack  # inplace for RB tree usage

    return color, x

# inserts node into RB tree
def RB_Insert(T, node):
    Insert(T, node)
    node.isBlack = False
    RB_Insert_Fixup(T, node)  # correct properties broken


# delete node from RB tree - note: was fully reimplemented because inefficient to determine the color
def RB_Delete(T, node):
    node = Search(T, T.root, node.key)
    if node == T.NIL:  # if node requested doesn't exist, quit the process
        return

    color, x = Delete(T, node)  # use slightly modified existing BST design

    if color:  # if original color is black
        RB_Delete_Fixup(T, x)


# fix red black tree from insert
def RB_Insert_Fixup(T, node):
    while not node.parent.isBlack:
        if node.parent.parent.left == node.parent:  # if parent is left child
            y = node.parent.parent.right  # the uncle
            # case 1
            if not y.isBlack:  # red uncle
                node.parent.isBlack = True  # make parent black
                y.isBlack = True  # make uncle black
                node.parent.parent.isBlack = False  # make grandparent red
                node = node.parent.parent
            else:  # uncle is black
                # case 2
                if node.parent.right == node:
                    node = node.parent
                    Left_Rotate(T, node)

                # case 3
                # swap colors of z's parent and grandparent
                node.parent.isBlack = True
                node.parent.parent.isBlack = False
                Right_Rotate(T, node.parent.parent)

        else:  # node's parent is a right child
            y = node.parent.parent.left  # the uncle
            # case 1
            if not y.isBlack:  # red uncle
                node.parent.isBlack = True
                y.isBlack = True
                node.parent.parent.isBlack = False
                node = node.parent.parent
            else:  # uncle is black
                if node.parent.left == node:
                    node = node.parent
                    Right_Rotate(T, node)

                # swap colors of z's parent and grandparent
                node.parent.isBlack = True
                node.parent.parent.isBlack = False
                Left_Rotate(T, node.parent.parent)

    T.root.isBlack = True


# fix red black tree properties ruined from deletion
def RB_Delete_Fixup(T, x):
    while x is not T.root and x.isBlack:  # while node isn't the root and is black
        if x == x.parent.left:  # if x is left child
            w = x.parent.right  # sibling
            if not w.isBlack:  # switch the sibling's color - case 1, rotate red into x's side
                w.isBlack = True
                x.parent.isBlack = False
                Left_Rotate(T, x.parent)
                w = x.parent.right
            if w.left.isBlack and w.right.isBlack:  # if sibling's children are black - case 2
                w.isBlack = False                   # push blackness into parent and loop will end if it is red
                x = x.parent
            else:
                if w.right.isBlack:  # only right child is black - case 3
                    w.left.isBlack = True   # rotate the tree to make the siblings right child red and top black
                    w.isBlack = False
                    Right_Rotate(T, w)
                    w = x.parent.right
                w.isBlack = x.parent.isBlack  # case 4 - fallen into by case 3, push blackness into x's branch and color the right child
                x.parent.isBlack = True
                w.right.isBlack = True
                Left_Rotate(T, x.parent)
                x = T.root
        else:  # mirror image
            w = x.parent.left  # sibling
            if not w.isBlack:  # switch the sibling's color - case 1, rotate red into x's side
                w.isBlack = True
                x.parent.isBlack = False
                Right_Rotate(T, x.parent)
                w = x.parent.left
            if w.right.isBlack and w.left.isBlack:  # if sibling's children are black - case 2
                w.isBlack = False  # push blackness into parent and loop will end if it is red
                x = x.parent
            else:
                if w.left.isBlack:  # only left child is black - case 3
                    w.right.isBlack = True  # rotate the tree to make the siblings right child red and top black
                    w.isBlack = False
                    Left_Rotate(T, w)
                    w = x.parent.left
                w.isBlack = x.parent.isBlack  # case 4 - fallen into by case 3, push blackness into x's branch and color the right child
                x.parent.isBlack = True
                w.left.isBlack = True
                Right_Rotate(T, x.parent)
                x = T.root

    x.isBlack = True


# move x from top counterclockwise
def Left_Rotate(T, x):
    y = x.right  # y is x's right subtree
    x.right = y.left  # set y's left subtree to be x's right
    if y.left != T.NIL:  # if y had a left subtree, assign the subtree a new parent
        y.left.parent = x
    y.parent = x.parent  # set y's parent to be x's prior

    if x.parent == T.NIL:  # if x didn't have a parent, new root
        T.root = y
        T.NIL.right = T.root
        T.NIL.left = T.root
    elif x == x.parent.left:  # if x was left child, y is now left child
        x.parent.left = y
    else:
        x.parent.right = y

    y.left = x  # make x y's left child
    x.parent = y  # make x's parent y


# move x from top clockwise
def Right_Rotate(T, x):
    y = x.left  # y is x's left subtree
    x.left = y.right
    if y.right != T.NIL:
        y.right.parent = x
    y.parent = x.parent

    if x.parent is T.NIL:
        T.root = y
        T.NIL.right = T.root
        T.NIL.left = T.root
    elif x == x.parent.right:  # if x was right child, so is y now
        x.parent.right = y
    else:
        x.parent.left = y

    y.right = x
    x.parent = y


# prints out the tree in order - need to modify for tree style
def Print_In_Order(T, node):  # node should initially be root
    if node is not T.NIL:
        Print_In_Order(T, node.left)
        print(node.key, node.isBlack)
        Print_In_Order(T, node.right)


# prints out an array form of the tree, including Null nodes to fill gaps
def Array_Print(T):
    Fill_Tree_Array(T, T.root, 0)
    for line in T.arrayForm:
        print(line)
    T.arrayForm = [[]]


# fill the tree array with its values and the NIL nodes for conceptual visualization
def Fill_Tree_Array(T, node, height):
    # use this section instead of the identical section in node if you want to see the NULL's in place without children
    # if height >= len(T.arrayForm):
    #     T.arrayForm.append([])
    if node is not T.NIL:
        if height >= len(T.arrayForm):
            T.arrayForm.append([])
        if node.isBlack:
            color = "B"
        else:
            color = "R"
        T.arrayForm[height].append([node.key, color])
        Fill_Tree_Array(T, node.left, height + 1)
        Fill_Tree_Array(T, node.right, height + 1)

    # use this section to include the NULLs
    # else:
    #     T.arrayForm[height].append(['N' "B"])


# BST tree test
def testBST():
    tree = Tree()
    Insert(tree, Node(15.9))
    Insert(tree, Node(9.1))
    Insert(tree, Node(3.6))
    Insert(tree, Node(11.5))
    Insert(tree, Node(17.9))
    Insert(tree, Node(28.6))
    Insert(tree, Node(24.2))
    Insert(tree, Node(1.6))
    Insert(tree, Node(14.3))
    Insert(tree, Node(13.8))
    Insert(tree, Node(12.1))
    Insert(tree, Node(23.4))
    # Delete(tree, Node(17.9))  # test case 1 - no left child
    Insert(tree, Node(18.2))
    Insert(tree, Node(24.5))
    node = Node(11.1) # for deletion of node in tree
    Insert(tree, node)
    Insert(tree, Node(14.7))
    # Delete(tree, Node(18))  # make sure doesn't lose tree with invalid node
    # Delete(tree, Node(18.2))  # test case 1, no children
    # Delete(tree, Node(3.6))  # test case 2
    # Delete(tree, Node(24.2))  # test case 4 - two children, immediate child
    # Delete(tree, node)  # test node deletion
    # Delete(tree, tree.root)  # delete root
    # Delete(tree, Node(11.5))  # test case 3, with other deletes commented out

    Array_Print(tree)
    Print_In_Order(tree, tree.root)



# # RB tree, test all cases
def testRB():
    tree2 = Tree()
    RB_Insert(tree2, Node(7))  # will change the root to top color
    RB_Insert(tree2, Node(23)) # no fixup
    RB_Insert(tree2, Node(2))
    RB_Insert(tree2, Node(45)) # case 1
    RB_Insert(tree2, Node(41)) # case 2 right left -> case 3 right right
    RB_Insert(tree2, Node(9)) # case 3 left left
    RB_Insert(tree2, Node(19)) # case 2 left right
    RB_Insert(tree2, Node(28)) # case 1 -> 2 - > 3
    RB_Insert(tree2, Node(8)) # bottom of data nodes
    RB_Insert(tree2, Node(1))
    RB_Insert(tree2, Node(30))
    # RB_Insert(tree2, Node(12))
    # RB_Insert(tree2, Node(18))
    # RB_Insert(tree2, Node(19)) # test duplicate
    # RB_Insert(tree2, Node(38))
    # RB_Insert(tree2, Node(40))
    # RB_Insert(tree2, Node(51))
    # RB_Insert(tree2, Node(90))
    # RB_Insert(tree2, Node(21))
    # RB_Insert(tree2, Node(45))
    # RB_Insert(tree2, Node(52))
    # RB_Insert(tree2, Node(59))
    # RB_Insert(tree2, Node(87))
    # RB_Insert(tree2, Node(78))
    # RB_Insert(tree2, Node(67))
    # RB_Insert(tree2, Node(54))
    # RB_Insert(tree2, Node(64))
    #
    # # also tested deleting the whole tree node by node
    # # RB_Delete(tree2, Node(23))  # case 1, no delete fixup
    RB_Delete(tree2, Node(9))  # case 2 delete, just switch color delete fixup
    RB_Delete(tree2, Node(19)) # remove root
    RB_Delete(tree2, Node(41)) # case 3, immediate successor, rb delete fixup case 4
    # RB_Delete(tree2, Node(7)) # farther successor, case 2 to 4 fixup
    # RB_Delete(tree2, Node(1))
    # # RB_Delete(tree2, Node(2)) # case 2 to 4 fixup, case 1
    # # RB_Delete(tree2, Node(45)) # fixup with a left sibling, case 1, case 4

    Array_Print(tree2)
    Print_In_Order(tree2, tree2.root)

#print(Predecessor(tree2, Node(19)).key)  # test successor/predecessor

# test trees
print("Hello world: I am a binary tree")
# testBST()
# testRB()
tree2 = Tree()
RB_Insert(tree2, Node(3))  # will change the root to top color
RB_Insert(tree2, Node(6))  # no fixup
RB_Insert(tree2, Node(2))  # will change the root to top color
RB_Insert(tree2, Node(4))  # no fixup
RB_Insert(tree2, Node(1))  # will change the root to top color
RB_Insert(tree2, Node(7))  # no fixup
RB_Insert(tree2, Node(5))  # no fixup
RB_Delete(tree2, Node(7))
Array_Print(tree2)
Print_In_Order(tree2, tree2.root)