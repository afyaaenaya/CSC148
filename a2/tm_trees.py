"""
Assignment 2: Trees for Treemap

=== CSC148 Summer 2023 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith, Andrea Mitchell,
                   Bahar Aameri

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


def get_colour() -> Tuple[int, int, int]:
    """This function picks a random colour selectively such that it is not on
    the grey scale. The colour is close to the grey scale if the r g b values
    have a small variance. This function checks if all the numbers are close to
    the mean, if so, it shifts the last digit by 150.

    This way you can't confuse the leaf rectangles with folder rectangles,
    because the leaves will always be a colour, never close to black / white.
    """
    rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
    avg = sum(rgb) // 3
    count = 0
    for item in rgb:
        if abs(item - avg) < 20:
            count += 1
    if count == 3:
        rgb[2] = (rgb[2] + 150) % 255
    return tuple(rgb)


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect: The pygame rectangle representing this node in the visualization.
    data_size: The size of the data represented by this tree.

    === Private Attributes ===
    _colour: The RGB colour value of the root of this tree.
    _name: The root value of this tree, or None if this tree is empty.
    _subtrees: The subtrees of this tree.
    _parent_tree: The parent tree of this tree; i.e., the tree that contains
    this tree as a subtree, or None if this tree is not part of a larger tree.
    _expanded: Whether this tree is considered expanded for visualization.
    _depth: The depth of this tree node in relation to the root.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - _colour's elements are each in the range 0-255.
    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - if _parent_tree is not None, then self is in _parent_tree._subtrees
    - if _expanded is True, then _parent_tree._expanded is True
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool
    _depth: int

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initializes a new TMTree with a random colour, the provided name
        and sets the subtrees to the list of provided subtrees. Sets this tree
        as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._parent_tree = None
        self._depth = 0
        self._name = name
        self._colour = get_colour()
        self._subtrees = subtrees
        self._expanded = False

        for subtree in subtrees:
            subtree._parent_tree = self

        if not self._subtrees:
            self.data_size = data_size
        else:
            self.data_size = 0
            for subtree in subtrees:
                self.data_size += subtree.data_size

    def is_empty(self) -> bool:
        """Returns True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    # **************************************************************************
    # ************* TASK 2: UPDATE AND GET RECTANGLES **************************
    # **************************************************************************

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Updates the rectangles in this tree and its descendants using the
        treemap algorithm to fill the area defined by the <rect> parameter.
        """
        x, y, width, height = rect

        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif width > height:
            self.rect = rect
            curr_width = x
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_width = math.floor(percent * width)
                else:
                    new_width = width + x - curr_width
                self._subtrees[i].update_rectangles((
                    curr_width, y, new_width, height))
                curr_width += new_width
        else:
            self.rect = rect
            curr_height = y
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_height = math.floor(percent * height)
                else:
                    new_height = height + y - curr_height
                self._subtrees[i].update_rectangles((
                    x, curr_height, width, new_height))
                curr_height += new_height

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Returns a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """

        if self.data_size == 0 or self.is_empty():
            return []
        elif self._expanded is False:
            return [(self.rect, self._colour)]
        else:
            rects_list = []
            for subtree in self._subtrees:
                rects_list.extend(subtree.get_rectangles())
            return rects_list

    # **************************************************************************
    # **************** TASK 3: GET_TREE_AT_POSITION ****************************
    # **************************************************************************

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Returns the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        x, y = pos

        left = self.rect[0]
        right = left + self.rect[2]
        top = self.rect[1]
        bottom = top + self.rect[3]

        if not (left < x <= right and top < y <= bottom):
            return None
        elif self._expanded is False or not self._subtrees:
            return self
        elif self._subtrees:
            for subtree in self._subtrees:
                if subtree.get_tree_at_position(pos) is not None:
                    return subtree.get_tree_at_position(pos)

    # **************************************************************************
    # ********* TASK 4: MOVE, CHANGE SIZE, DELETE, UPDATE SIZES ****************
    # **************************************************************************

    def update_data_sizes(self) -> int:
        """Updates the data_size attribute for this tree and all its subtrees,
        based on the size of their leaves, and return the new size of the given
        tree node after updating.

        If this tree is a leaf, return its size unchanged.
        """
        if self._subtrees:
            data_size = 0
            for subtree in self._subtrees:
                data_size += subtree.update_data_sizes()
            self.data_size = data_size
        if self.data_size < 0:
            self.data_size = 0

        return self.data_size

    def change_size(self, factor: float) -> None:
        """Changes the value of this tree's data_size attribute by <factor>.
        Always rounds up the amount to change, so that it's an int, and
        some change is made. If the tree is not a leaf, this method does
        nothing.
        """
        if not self._subtrees:
            data_size = self.data_size
            change = 0

            if factor > 0:
                change = math.ceil(data_size * factor)
            elif factor < 0:
                change = math.floor(data_size * factor)

            if self.data_size + change < 1:
                self.data_size = 1
            else:
                self.data_size = data_size + change

        if self.get_parent():
            self._parent_tree.update_data_sizes()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful. Only do this if this node
        has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualizer to go back to the parent folder.
        """
        if self.get_parent():
            self._parent_tree._subtrees.remove(self)
            if not self._parent_tree._subtrees:
                self._parent_tree.delete_self()
            return True
        return False

    # **************************************************************************
    # ************* TASK 5: UPDATE_COLOURS_AND_DEPTHS **************************
    # **************************************************************************

    def update_depths(self, depth: int = 0) -> None:
        """Updates the depths of the nodes, starting with a depth of 0 at this
        tree node.
        """
        self._depth = depth
        if self._subtrees:
            for subtree in self._subtrees:
                subtree.update_depths(depth + 1)

    def max_depth(self, max_depth: int = 0) -> int:
        """Returns the maximum depth of the tree, which is the maximum length
        between a leaf node and the root node.
        """
        if self._subtrees:
            for subtree in self._subtrees:
                max_depth += 1
                subtree.max_depth()
        return max_depth

    def update_colours(self, step_size: int) -> None:
        """Updates the colours so that the internal tree nodes are
        shades of grey depending on their depth. The root node will be black
        (0, 0, 0) and all internal nodes will be shades of grey depending on
        their depth, where the step size determines the shade of grey.
        Leaf nodes should not be updated.
        """
        if self._subtrees:
            colour = self._depth * step_size
            self._colour = (colour, colour, colour)
            for subtree in self._subtrees:
                subtree.update_colours(step_size)

    def update_colours_and_depths(self) -> None:
        """This method is called any time the tree is manipulated or right after
        instantiation. Updates the _depth and _colour attributes throughout
        the tree.
        """
        self.update_depths()
        self.max_depth()

        step = 0
        colour = 0
        while colour < 200:
            step += 1
            colour = step * (self.max_depth() - 1)

        if colour > 200:
            self.update_colours(step - 1)
        else:
            self.update_colours(step)

    # **************************************************************************
    # ********* TASK 6: EXPAND, COLLAPSE, EXPAND ALL, COLLAPSE ALL *************
    # **************************************************************************

    def expand(self) -> None:
        """Sets this tree to be expanded. But not if it is a leaf.
        """
        if self._subtrees:
            self._expanded = True
            tree = self
            while tree:
                tree._expanded = True
                tree = tree._parent_tree
        else:
            self._expanded = False

    def expand_all(self) -> None:
        """Sets this tree and all its descendants to be expanded, apart from the
        leaf nodes.
        """
        self.expand()
        for subtree in self._subtrees:
            subtree.expand_all()

    def _collapse_helper(self) -> None:
        """Collapses the parent tree of the given tree node and also collapse
        all of its descendants.
        """
        self._expanded = False
        for subtree in self._subtrees:
            subtree._collapse_helper()

    def collapse(self) -> None:
        """Collapses the parent tree of the given tree node and also collapse
        all of its descendants.
        """
        if self.get_parent():
            self._parent_tree._collapse_helper()

    def collapse_all(self) -> None:
        """ Collapses ALL nodes in the tree.
        """
        tree = self
        while tree.get_parent():
            tree = tree._parent_tree
        tree._collapse_helper()

    # **************************************************************************
    # ************* TASK 7 : DUPLICATE MOVE COPY_PASTE *************************
    # **************************************************************************

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, moves this
        tree to be the last subtree of <destination>. Otherwise, does nothing.
        """
        if not self._subtrees and destination._subtrees:
            if self.get_parent():
                orig_parent = self._parent_tree
                orig_parent._subtrees.remove(self)
                orig_parent.update_data_sizes()
            self._parent_tree = destination
            destination._subtrees.append(self)
            destination.update_data_sizes()

    def duplicate(self) -> Optional[TMTree]:
        """Duplicates the given tree, if it is a leaf node. It stores
        the new tree with the same parent as the given leaf. Returns the
        new node. If the given tree is not a leaf, does nothing.
        """
        twin = None
        if not self._subtrees:
            twin = FileSystemTree(self.get_full_path())
            twin._parent_tree = self._parent_tree
            self._parent_tree._subtrees.append(twin)
        return twin

    def copy_paste(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, this method
        copies the given, and moves the copy to the last subtree of
        <destination>. Otherwise, does nothing.
        """
        if not self._subtrees and destination._subtrees:
            twin = FileSystemTree(self.get_full_path())
            twin._parent_tree = destination
            destination._subtrees.append(twin)
        destination.update_data_sizes()

    # **************************************************************************
    # ************* HELPER FUNCTION FOR TESTING PURPOSES  **********************
    # **************************************************************************
    def tree_traversal(self) -> List[Tuple[str, int, Tuple[int, int, int]]]:
        """For testing purposes to see the depth and colour attributes for each
        internal node in the tree. Used for passing test case 5.
        """

        if len(self._subtrees) > 0:
            output_list = [(self._name, self._depth, self._colour)]
            for tree in self._subtrees:
                output_list += tree.tree_traversal()
            return output_list
        else:
            return []

    # **************************************************************************
    # *********** METHODS DEFINED FOR STRING REPRESENTATION  *******************
    # **************************************************************************
    def get_path_string(self) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Returns the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Returns the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError

    # **************************************************************************
    # **************** HELPER FUNCTION FOR TASK 7  *****************************
    # **************************************************************************
    def get_full_path(self) -> str:
        """Returns the path attribute for this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.

    === Private Attributes ===
    _path: the path that was used to instantiate this tree.
    """
    _path: str

    def __init__(self, my_path: str) -> None:
        """Stores the directory given by <my_path> into a tree data structure
        using the TMTree class.

        Precondition: <my_path> is a valid path for this computer.
        """
        self._path = my_path

        if os.path.isdir(my_path):
            subtrees_lst = []
            paths = []
            for file in os.listdir(my_path):
                paths.append(os.path.join(my_path, file))
            for path in paths:
                subtrees_lst.append(FileSystemTree(path))

            TMTree.__init__(self, os.path.basename(my_path), subtrees_lst, 0)
        else:
            TMTree.__init__(self, os.path.basename(my_path), [],
                            os.path.getsize(my_path))

    def get_full_path(self) -> str:
        """Returns the file path for the tree object.
        """
        return self._path

    def get_separator(self) -> str:
        """Returns the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Returns the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
