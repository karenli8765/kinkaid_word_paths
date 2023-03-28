from tkinter import filedialog
from tkinter import Tk
from copy import deepcopy
from typing import TypeVar, List

#TODO: The edges in your graph will represent connections between two words that differ by one letter. You need to
# decide whether you want these edges to be pairs of the words themselves or the indices of them in the list of
# vertices. There is no right or wrong choice here - its up to you. (There is some speed/memory usage) tradeoff.
# Uncomment the version you would prefer:
# Edge_End_Type = TypeVar(int) # defines a new type, Edge_End_Type (which is a fancy name for an int)
Edge_End_Type = TypeVar(str) # defines a new type, Edge_End_Type (which is a fancy name for a string)

Word_Pair = TypeVar(List[Edge_End_Type]) #defining a new type of variable, sort of like a new class, but simpler.

# TODO: Pick one of the following two lines and delete the other one (and this instructions line you are reading, too.)
# This program will use Directed Edges.

class WordPathKeeper:

    def __init__(self):
        self.vertices = []
        self.edges = []

    def load_words(self):
        root = Tk()
        print ("Showing file dialog. Make sure it isn't hiding! \nClick on the small window in the upper left corner of\nthe screen. It may be behind the pycharm window.")
        word_filename = filedialog.askopenfilename(message="Find the list of words.")
        root.update() # allows dialogbox to go away.
        if word_filename == "":
            raise IOError("No file found...")
        self.load_words_from_file(word_filename)

    def load_words_from_file(self,word_filename:str):
        print(f"Loading Vertices from {word_filename}.")
        count = 0
        with open(word_filename, 'r') as ins:
            for line in ins:
                items = line.split("\t")
                if count % 100 == 0: # show progress....
                    print(count)

                count += 1
                self.vertices.append(items[1].split("\n")[0])
        print("Done Loading from file.\n-------------------------------------------")

    def num_mismatched_letters(self, word1: str, word2: str) -> int:
        """
        looks at the two words, character by character and returns the number of
        characters that don't match.
        :param word1: a string
        :param word2: another string, of the same length as word1
        :return: the number of characters that don't match. Two identical strings
        would return 0; "pack" and "pick" would return 1; "mate" and "meta" would return 2.
        """
        assert(len(word1) == len(word2))
        count = 0
        # -----------------------------------------
        # TODO: You need to write this method.
        for i in range(1, len(word1)+1):
            letter_one = word1[i-1: i]
            letter_two = word2[i-1: i]
            if not letter_one == letter_two:
                count = count + 1
        # -----------------------------------------
        return count

    def build_edges(self):
        """
        loops through the list of words in self.vertices. Compares each word to the
        other words on the list. If they differ by exactly one letter, then this method records
        the words to the self.edges data structure.

        Self.edges should be an array of 2-element arrays (which we called Word_Pairs at the top of the file, lines 6-20.)
        - each Word_Pair might take the form of a pair of indices (e.g., [8252, 8253]) or a pair of strings (e.g.,
        ["zooks", "zooms"]). You should have made a choice up there!

        You may also desire to make these unidirectional or
        bidirectional (undirected) edges - for example the connection might be saved
        as [8252, 8253], which would imply a connection in both directions or as
        [8252, 8253] AND [8253, 8252], which would represent two connections from the
        first value to the second. (Obviously, you could use strings, too.)
        The difference is that the former method requires searching the first value
        of the array when looking for a match as well as the second value, but it takes
        half the memory as the latter method.

        Of the four options (id# vs. string) x (unidirectional vs. bidirectional),
        none is "right" or "wrong" here. You can choose the version you wish. Just
        be consistent with the rest of your program, including the choices you made on lines 6-20.
        :return: None
        """
        print("Constructing Edges.")
        # -----------------------------------------
        # TODO: You should write this method!
        n = len(self.vertices)
        for i in range (0, n):
            for k in range (0, n):
                if k == i:
                    continue
                word1 = self.vertices[i]
                word2 = self.vertices[k]
                if self.num_mismatched_letters(word1, word2) == 1:
                    new_edge: Word_Pair = [word1, word2]
                    self.edges.append(new_edge)



        # Note: this method may take some time to run - it is likely to be O(N^2), and some lists have N = 10,000 words or more.
        #  (I've had students decide that their program was "broken" and quit it before this process finished... every time,
        #  not realizing that the program was working hard behind the scenes.)
        #  I recommend that you keep track of the number of edges you have added, and if it is a multiple of 1000, print
        #  something so that you know your program is making progress.


        
        # -----------------------------------------
        print("Done Constructing Edges.\n------------------------------------")

    def get_neighbors(self, node: Edge_End_Type)-> List[Edge_End_Type]:
        """
        returns a list of nodes that are directly connected to the node.
        (Nodes can be either strings or id numbers - programmer's choice.)
        If there are no neighbors, return an empty array.
        :param node:
        :return: an array of nodes
        """
        neighbors = []
        # -----------------------------------------
        # TODO: You should write this method!
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append(edge)

        return neighbors
        # -----------------------------------------

    def find_path(self, word1: str, word2: str) -> List[str]:
        """
        Uses Breadth-First-Search to find a path of words from word1 to word2,
        where each word in the path varies from the previous word by exactly
        one letter. For instance, if word1 is "bike" and word2 is "mods", we might
        get a path = ["bike", "bite", "mite", "mote", "mode", "mods"] (Note: I did
        this manually, so the computer might come up with something else.)

        If no path exists from word1 to word2, return None.
        :param word1:
        :param word2:
        :return: an array of strings, or None.
        """
        path = []
        # -----------------------------------------
        # TODO: you should write this method
        this_word = word1
        frontier: List = [[this_word, path]]
        visited: List[str] = [word1]

        while len(frontier) > 0:
            this_node = frontier.pop(0)
            this_word: str = this_node[0]
            neighbors_list = self.get_neighbors(this_word)
            for edge in neighbors_list:
                temp_path = deepcopy(this_node[1])
                neighbor: str = edge[1]
                if neighbor in visited:
                    continue
                else:
                    visited.append(neighbor)
                if neighbor == word2:
                    temp_path.append(this_word)
                    temp_path.append(word2)
                    path = temp_path
                    break
                temp_path.append(this_word)
                frontier.append([neighbor, temp_path])

        # Note: again, you'll want to make sure that you let your user know that you are making progress,
        #   ...but don't overwhelm them. (Printing is slow, too.) I chose to let the user know whenever the
        #   path length increased, but you can do whatever you like.

        # Note#2: if you just append a word to the end of a list, you've changed that (original) list, and if another
        #   option on your frontier was storing that list, it changed for that one, too. You will probably want to
        #   make use of "deepcopy" to make an independent copy of the path before you start adding information to it.
        #   see https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/ for info on deepcopy.

        if word2 in path:
            return path
        # -----------------------------------------
        return None