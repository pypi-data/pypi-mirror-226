class NodeLinkedList:
    """
    Class responsible for creating the linked list node.

    This class will be used to store the data inside the node that will be chained in the list.
    
    Methods
    -------
    show_datas_linked_list()
        Method responsible for displaying node data.

    """
    def __init__(self, id: int, **kwargs):
        """
        Parameters
        ----------
        id : int
            This parameter is intended to identify each node in the linked list.
        **kwargs : 
            This parameter is responsible for saving the node data.
        """
        self.id = id
        self.kwargs = kwargs
        self.next = None

    def show_datas_linked_list(self):
        """
        Method responsible for displaying node data.

        ...

        """
        print(f"ID: {self.id:}\nDatas:{self.kwargs:}")
        print("-=" * 20)


class LinkedList:
    """
    Class responsible for starting the head of the linked list.

    This class will be responsible for keeping the head of the list.
    
    Methods
    -------
    add_node()
        Method responsible for displaying node data.
    remove_node()
        Method responsible for removing a node from the linked list.
    search_node()
        Method responsible for looking for a node in the list.
    show_linkedlist()
        Method responsible for displaying the data of each node in the list.

    """
    def __init__(self) -> None:
        self.head = None

    def add_node(self, node: NodeLinkedList):
        """
        This method adds the new node to the list.

        This method adds every new node to the end of the list. Loops through the entire list to the end and inserts.

        Parameters
        ----------
        node : NodeLinkedList
            This parameter is responsible for making a copy of the node that will be inserted in the linked list.
        """
        if self.head:
            pointer = self.head
            while pointer.next:
                pointer = pointer.next
            pointer.next = node
        else:
            self.head = node

    def remove_node(self, id: int):
        """
        This method removes the node by the provided key.

        This method looks for the informed key in the whole list, if it finds the node it is removed, whether its position at the beginning, at the end or in the middle of the list.

        Parameters
        ----------
        id: int
            This parameter is responsible for passing the key of the node that will be removed.

        Returns
        -------
        True : bool
            Returns when the node was successfully removed.
        False : bool
            Returns when the informed key of the node does not exist in the list.
        """
        find = self.search_node(id)
        if find[0] != None:
            if find[1] == None:
                self.head = self.head.next
            elif find[0].next == None:
                find[1].next = None
            elif find[1] != None:
                find[1].next = find[0].next
            return True
        else:
            return False

    def search_node(self, id: int):
        """
        This method removes the node by the provided key.

        This method looks for the informed key in the whole list, if it finds the node it is removed, whether its position at the beginning, at the end or in the middle of the list.

        Parameters
        ----------
        id: int
            This parameter is responsible for passing the key of the node that will be removed.
        
        Returns
        -------
        aux, previous : NodeLinkedList, NodeLinkedList or NoneType
            Returns when the given key was found.
        None, previous : NonteType, NoneType
            Returns when the function looks for the key in the list, reaches the end and does not find it.
        """
        aux = self.head
        previous = None
        while aux:
            if aux.id == id:
                return aux, previous
            previous = aux
            aux = aux.next
        return None, previous

    def show_linkedlist(self):
        """
        Method responsible for displaying the data of each node in the list.

        ...

        """
        aux = self.head
        print("-=" * 20)
        while aux:
            aux.show_datas_linked_list()
            aux = aux.next

class NodeBinaryTree:
    """
    Class responsible for representing the node in the binary search tree.

    This class has the purpose of presenting the node in the binary search tree.
    
    Methods
    -------
    _show_data_node_binary_tree()
        Displays node data.

    """
    def __init__(self, id: int, **kwargs) -> None:
        """
        This method creates the node.

        ...

        Parameters
        ----------
        id : int
            Parameter that identifies each node in the tree.
        **kwargs :
            Parameter responsible for storing node data.
        """
        self.id = id
        self.kwargs = kwargs
        self.left = None
        self.right = None

    def _show_data_node_binary_tree(self):
        """
        Displays node data.

        ...

        """
        print(f"ID: {self.id:}\nDatas: {self.kwargs:}")


class BinarySearchTree:
    """
    Class responsible for initializing the root of the tree.

    This class will be responsible for maintaining the first node, which is the root of the entire tree.
    
    Methods
    -------
    call_insert_binary_tree()
        This method has the purpose of invoking the insertion method in the tree.
    _insert_binary_tree()
        This method has the purpose of inserting the node in the tree.
    call_show_binary_tree()
        This method calls the display tree method.
    _show_binary_tree()
        This method displays the entire tree.
    call_remove_node_binary_tree()
        This method has the purpose of calling the tree removal method.
    _remove_node_binary_tree()
        This method is responsible for removing the node from the tree.
    _is_leaf()
        This method checks if the node to be removed is a leaf.
    _one_son()
        This method checks if the node to be removed has only one child.
    _get_help_one_son()
        This method returns the child of the node that has only one child.
    _two_son()
        This method checks if the node to be removed has two children.
    _get_biggest_son_left()
        This method takes the rightmost node when removing a node that has two children.
    _get_node()
        This method just returns the passed node.
    """
    def __init__(self):
        """
        Constructor method that initializes the root of the tree.

        This method has the purpose of starting the root that will be changed.

        """
        self._root = None

    def call_insert_binary_tree(self, key, **kwargs):
        """
        This method invokes the method that inserts the node into the tree.

        This method inserts nodes into a binary search tree where the largest nodes are on the right and the smallest on the left, respecting the maximum number of children, which are two.

        Parameters
        ----------
        key: int
            This parameter is the identifier of each node within the structure.
        **kwargs : dict
            This parameter consists of the data that will be stored in the tree node.
        """
        self._root = self._insert_binary_tree(self._root, key, **kwargs)

    def _insert_binary_tree(self, node, key, **kwargs):
        """
        This method is responsible for inserting the node in the tree.

        This method inserts nodes into a binary search tree where the largest nodes are on the right and the smallest on the left, respecting the maximum number of children, which are two.

        Parameters
        ----------
        node: NodeBinaryTree or NoneType
            This parameter represents the current node of the tree where from them it will be inserted or traversed in the tree.
        key: int
            This parameter is the identifier of each node within the structure.
        **kwargs : dict
            This parameter consists of the data that will be stored in the tree node.
        
        Returns
        -------
        new : NodeBinaryTree
            Returns when the node was successfully inserted.
        node : NonteType or NodeBinaryTree
            It returns when the recursion has reached its limit and returns by chaining the nodes.
        """
        if node is None:
            new = NodeBinaryTree(key, **kwargs)
            return new
        elif key < node.id:
            node.left = self._insert_binary_tree(node.left, key, **kwargs)
        else:
            node.right = self._insert_binary_tree(node.right, key, **kwargs)

        return node
    
    def call_show_binary_tree(self):
        """
        This method is responsible for calling the tree view method.

        ...

        """
        self._show_binary_tree(self._root)

    def _show_binary_tree(self, root):
        """
        This method is responsible for displaying the tree.

        This method displays the current node and traverses to your left returning displaying those on the right.

        Parameters
        ----------
        root: NodeBinaryTree or NoneType
            Parameter that represents the node to be displayed.
        """
        if root is None:
            pass
        else:
            root._show_data_node_binary_tree()
            self._show_binary_tree(root.left)
            self._show_binary_tree(root.right)

    def call_remove_node_binary_tree(self,key : int):
        """
        This method invokes the tree node removal method.

        ...

        Parameters
        ----------
        key: int
            Represents the key of the node that will be removed.
        """
        self._root =  self._remove_node_binary_tree(self._root,key)
    
    def _remove_node_binary_tree(self, node,key: int):
        """
        This method removes the node from the key passed by parameter.

        This method has the purpose of removing the node with the key passed by parameter, where if the node is a leaf it is assigned None, if it has a child this child is assigned to the node and if it has two children the largest child on the left is assigned.

        Parameters
        ----------
        node: NodeBinaryTree or NoneType
            Represents the current node of the tree, which is checked if it has the same key as the parameter's key.
        key: int
            Represents the key of the node you want to remove from the structure.
        
        Returns
        -------
        None : NoneType
            Returns when the current node is None or when the node was found and is a child.
        node : NonteType or NodeLinkedList
            It returns when it has passed all checks and there is no need to change the structure.
        self._get_help_one_son(node) : NodeBinaryTree
            Returns when the node to be removed has only one child and the child is returned to maintain chaining.
        son : NodeBinaryTree
            Returns when the node to be removed has two children and the largest child on the left is assigned to the previous recursion.
        """
        if node is None:
            return None

        if key == node.id:
            if self._is_leaf(node) == 1:
                return None
            elif self._one_son(node) == 1:
                return self._get_help_one_son(node)
            elif self._two_son(node) == 1:
                son = self._get_biggest_son_left(node.left)
                son.left = self._get_node(node.left)
                son.right = self._get_node(node.right)
                return son
        elif key < node.id:
            node.left = self._remove_node_binary_tree(node.left,key)
        else:
            node.right = self._remove_node_binary_tree(node.right, key)

        # return node

    
    def _is_leaf(self, node):
        """
        This method checks if the node is a leaf.

        This method checks whether the node is a leaf by looking at its left and right children if both are None.

        Parameters
        ----------
        node: NodeBinaryTree
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 if the node is not a leaf and 1 if it is a leaf.
        """
        yes = 0

        if node.left is None and node.right is None:
            yes = 1

        return yes
        
    def _one_son(self, node):
        """
        This method checks if the node has only one child.

        This method checks if the node has only one child, checking if left is None and right is None or if left is None and right is None.

        Parameters
        ----------
        node: NodeBinaryTree or NoneType
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 if the node does not have only one child, 1 if it has only one child.
        """
        yes = 0

        if ((node.left is None and not(node.right is None)) or (not(node.left is None) and node.right is None)):
            yes = 1

        return yes
    
    def _get_help_one_son(self, node):
        """
        This method returns the child of the parent node.

        This method returns the child of the parent node being changed in the remove function. The method checks if the left is None, if it is, look to the right.

        Parameters
        ----------
        node: NodeBinaryTree
            Node that will be checked.
        
        Returns
        -------
        son : NodeBinaryTree
            Returns the child of the parent node that was checked.
        """
        son = None

        if node.left is None:
            son = node.right
        if node.right is None:
            son = node.left

        return son
    
    def _two_son(self, node):
        """
        This method checks if the node to be removed has two children.

        This method checks if the passed node is a leaf by checking if the left and right nodes are of type None.

        Parameters
        ----------
        node: NodeBinaryTree or NoneType
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 when the passed node does not have two children, 1 otherwise.
        """
        yes = 0

        if not(node.left is None) and not(node.right is None):
            yes = 1

        return yes
    
    def _get_biggest_son_left(self,node):
        """
        This method aims to find the largest node of the left child of the parent node.

        This method takes the left child and will look for the largest one from there.

        Parameters
        ----------
        node: NodeBinaryTree
            Represents the left child of the node that has two children that will be removed.
        
        Returns
        -------
        biggest : NodeBinaryTree
            Returns the largest child on the right.
        """
        biggest = None

        while node.right is not None:
            save_node = node
            node = node.right

        save_node.right = None
        biggest = node
        
        return biggest
    
    def _get_node(self,node):
        """
        This method is just a helper to return the passed node.

        ...

        Parameters
        ----------
        node: NodeBinaryTree
            Past node that will be returned.
        Returns
        -------
        node : NonteType or NodeBinaryTree
            Returns the node that was passed by parameter.
        """
        return node
    
class NodeAVLTree:
    """
    Class responsible for representing the node in the AVL tree.

    This class has the purpose of presenting the node in the AVL tree.
    
    Methods
    -------
    _show_data_node_avl_tree()
        Displays node data.

    """
    def __init__(self, id: int, **kwargs) -> None:
        """
        This method creates the node.

        ...

        Parameters
        ----------
        id : int
            Parameter that identifies each node in the tree.
        **kwargs :
            Parameter responsible for storing node data.
        """
        self.id = id
        self.kwargs = kwargs
        self.height = -1
        self.left = None
        self.right = None

    def _show_data_node_avl_tree(self):
        """
        Displays node data.

        ...

        """
        print(f"ID: {self.id:}\nDatas: {self.kwargs:}")


class BinaryAVLTree:
    """
    Class responsible for initializing the root of the tree.

    This class will be responsible for maintaining the first node, which is the root of the entire tree.
    
    Methods
    -------
    call_insert_avl_tree()
        This method has the purpose of invoking the insertion method in the tree.
    _insert_avl_tree()
        This method has the purpose of inserting the node in the tree.
    call_show_avl_tree()
        This method calls the display tree method.
    _show_avl_tree()
        This method displays the entire tree.
    call_remove_node_avl_tree()
        This method has the purpose of calling the tree removal method.
    _remove_node_avl_tree()
        This method is responsible for removing the node from the tree.
    _is_leaf()
        This method checks if the node to be removed is a leaf.
    _one_son()
        This method checks if the node to be removed has only one child.
    _get_help_one_son()
        This method returns the child of the node that has only one child.
    _two_son()
        This method checks if the node to be removed has two children.
    _get_biggest_son_left()
        This method takes the rightmost node when removing a node that has two children.
    _get_node()
        This method just returns the passed node.
    """
    def __init__(self):
        """
        Constructor method that initializes the root of the tree.

        This method has the purpose of starting the root that will be changed.

        """
        self._root = None

    def call_insert_avl_tree(self, key, **kwargs):
        """
        This method invokes the method that inserts the node into the tree.

        This method inserts nodes into a binary search tree where the largest nodes are on the right and the smallest on the left, respecting the maximum number of children, which are two.

        Parameters
        ----------
        key: int
            This parameter is the identifier of each node within the structure.
        **kwargs : dict
            This parameter consists of the data that will be stored in the tree node.
        """
        self._root = self._insert_avl_tree(self._root, key, **kwargs)

    def _insert_avl_tree(self, node, key, **kwargs):
        """
        This method is responsible for inserting the node in the tree.

        This method inserts nodes into a binary search tree where the largest nodes are on the right and the smallest on the left, respecting the maximum number of children, which are two.

        Parameters
        ----------
        node: NodeAVLTree or NoneType
            This parameter represents the current node of the tree where from them it will be inserted or traversed in the tree.
        key: int
            This parameter is the identifier of each node within the structure.
        **kwargs : dict
            This parameter consists of the data that will be stored in the tree node.
        
        Returns
        -------
        new : NodeAVLTree
            Returns when the node was successfully inserted.
        node : NonteType or NodeLinkedList
            It returns when the recursion has reached its limit and returns by chaining the nodes.
        """
        if node is None:
            new = NodeAVLTree(key, **kwargs)
            new.height = self._calculate_height(new)
            return new
        elif key < node.id:
            node.left = self._insert_avl_tree(node.left, key, **kwargs)
        else:
            node.right = self._insert_avl_tree(node.right, key, **kwargs)
        fb = self._balancing_factor(node)
        if fb == 2:
            if self._balancing_factor(node.left) < 0:
                node.left = self._left_rotation(node.left)
            node = self._right_rotation(node)
        elif fb == -2:
            if self._balancing_factor(node.right) > 0:
                node.right = self._right_rotation(node.right)
            node = self._left_rotation(node)    
        self._update_height(node)
        return node
    
    def call_show_avl_tree(self):
        """
        This method is responsible for calling the tree view method.

        ...

        """
        self._show_avl_tree(self._root)

    def _show_avl_tree(self, root):
        """
        This method is responsible for displaying the tree.

        This method displays the current node and traverses to your left returning displaying those on the right.

        Parameters
        ----------
        root: NodeAVLTree or NoneType
            Parameter that represents the node to be displayed.
        """
        if root is None:
            pass
        else:
            root._show_data_node_avl_tree()
            self._show_avl_tree(root.left)
            self._show_avl_tree(root.right)

    def call_remove_node_avl_tree(self,key : int):
        """
        This method invokes the tree node removal method.

        ...

        Parameters
        ----------
        key: int
            Represents the key of the node that will be removed.
        """
        self._root =  self._remove_node_avl_tree(self._root,key)
    
    def _remove_node_avl_tree(self, node,key: int):
        """
        This method removes the node from the key passed by parameter.

        This method has the purpose of removing the node with the key passed by parameter, where if the node is a leaf it is assigned None, if it has a child this child is assigned to the node and if it has two children the largest child on the left is assigned.

        Parameters
        ----------
        node: NodeAVLTree or NoneType
            Represents the current node of the tree, which is checked if it has the same key as the parameter's key.
        key: int
            Represents the key of the node you want to remove from the structure.
        
        Returns
        -------
        None : NoneType
            Returns when the current node is None or when the node was found and is a child.
        node : NonteType or NodeAVLTree
            It returns when it has passed all checks and there is no need to change the structure.
        self._get_help_one_son(node) : NodeAVLTree
            Returns when the node to be removed has only one child and the child is returned to maintain chaining.
        son : NodeAVLTree
            Returns when the node to be removed has two children and the largest child on the left is assigned to the previous recursion.
        """
        if node is None:
            return None

        if key == node.id:
            if self._is_leaf(node) == 1:
                return None
            elif self._one_son(node) == 1:
                return self._get_help_one_son(node)
            elif self._two_son(node) == 1:
                son = self._get_biggest_son_left(node.left)
                son.left = self._get_node(node.left)
                son.right = self._get_node(node.right)
                return son
        elif key < node.id:
            node.left = self._remove_node_avl_tree(node.left,key)
        else:
            node.right = self._remove_node_avl_tree(node.right, key)
        if node is not None:
            fb = self._balancing_factor(node)
            if fb == 2:
                if self._balancing_factor(node.left) < 0:
                    node.left = self._left_rotation(node.left)
                node = self._right_rotation(node)
            elif fb == -2:
                if self._balancing_factor(node.right) > 0:
                    node.right = self._right_rotation(node.right)
                node = self._left_rotation(node)
            self._update_height(node)

        return node
    
    def _is_leaf(self, node):
        """
        This method checks if the node is a leaf.

        This method checks whether the node is a leaf by looking at its left and right children if both are None.

        Parameters
        ----------
        node: NodeAVLTree
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 if the node is not a leaf and 1 if it is a leaf.
        """
        yes = 0

        if node.left is None and node.right is None:
            yes = 1

        return yes
        
    def _one_son(self, node):
        """
        This method checks if the node has only one child.

        This method checks if the node has only one child, checking if left is None and right is None or if left is None and right is None.

        Parameters
        ----------
        node: NodeAVLTree or NoneType
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 if the node does not have only one child, 1 if it has only one child.
        """
        yes = 0

        if ((node.left is None and not(node.right is None)) or (not(node.left is None) and node.right is None)):
            yes = 1

        return yes
    
    def _get_help_one_son(self, node):
        """
        This method returns the child of the parent node.

        This method returns the child of the parent node being changed in the remove function. The method checks if the left is None, if it is, look to the right.

        Parameters
        ----------
        node: NodeAVLTree
            Node that will be checked.
        
        Returns
        -------
        son : NodeAVLTree
            Returns the child of the parent node that was checked.
        """
        son = None

        if node.left is None:
            son = node.right
        if node.right is None:
            son = node.left

        return son
    
    def _two_son(self, node):
        """
        This method checks if the node to be removed has two children.

        This method checks if the passed node is a leaf by checking if the left and right nodes are of type None.

        Parameters
        ----------
        node: NodeAVLTree or NoneType
            Node that will be checked.
        
        Returns
        -------
        yes : int
            Returns 0 when the passed node does not have two children, 1 otherwise.
        """
        yes = 0

        if not(node.left is None) and not(node.right is None):
            yes = 1

        return yes
    
    def _get_biggest_son_left(self,node):
        """
        This method aims to find the largest node of the left child of the parent node.

        This method takes the left child and will look for the largest one from there.

        Parameters
        ----------
        node: NodeAVLTree
            Represents the left child of the node that has two children that will be removed.
        
        Returns
        -------
        biggest : NodeAVLTree
            Returns the largest child on the right.
        """
        biggest = None

        while node.right is not None:
            save_node = node
            node = node.right

        save_node.right = None
        biggest = node
        
        return biggest
    
    def _get_node(self,node):
        """
        This method is just a helper to return the passed node.

        ...

        Parameters
        ----------
        node: NodeAVLTree
            Past node that will be returned.
        Returns
        -------
        node : NonteType or NodeAVLTree
            Returns the node that was passed by parameter.
        """
        return node
    
    def _calculate_height(self,node):
        """
        This method aims to calculate the height of the node.

        ...

        Parameters
        ----------
        node: NodeAVLTree
            Node that will have the calculated height.
        Returns
        -------
        h : int
            Returns the height of the node passed by parameter.
        """
        if node is not None:
            he = self._calculate_height(node.left)
            hd = self._calculate_height(node.right)
            if he > hd:
                h = he + 1
            else:
                h = hd + 1
        else:
            h = 0
        return h

    def _balancing_factor(self, node):
        """
        This method aims to calculate the node balancing factor.

        This method checks the balancing factor and through it depending on its result the node will be rotated in some direction.

        Parameters
        ----------
        node: NodeAVLTree
            Node that will have the balancing factor calculated.
        Returns
        -------
        value : int
            Returns the balancing factor.
        """
        return self._calculate_height(node.left) - self._calculate_height(node.right)
    
    def _left_rotation(self,node):
        """
        This method has the purpose of rotating the passed node to the left.

        ...

        Parameters
        ----------
        node: NodeAVLTree
            Node that will be rotated.
        Returns
        -------
        node : NodeAVLTree
            Returns the rotated node.
        """
        q = node.right
        aux = q.left
        q.left = node
        node.right = aux
        node = q
        return node

    def _right_rotation(self,node):
        """
        This method has the purpose of rotating the passed node to the right.

        ...

        Parameters
        ----------
        node: NodeAVLTree
            Node that will be rotated.
        Returns
        -------
        node : NodeAVLTree
            Returns the rotated node.
        """
        q = node.left
        aux = q.right
        q.right = node
        node.left = aux
        node = q
        return node
    
    def _update_height(self,node):
        """
        This method updates the height of the rotated node.

        ...

        Parameters
        ----------
        node: NodeAVLTree
            Node that will have the updated height.
        Returns
        -------
        value : int
            Returns the new height.
        """
        return self._calculate_height(node)