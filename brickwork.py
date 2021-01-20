from collections import deque


class BrickWall:

    def __init__(self, width: str, length: str):
        self.layout_one = []  # Two dimensional array representing layout one
        self.n = int(width)  # An integer variable representing layout's width
        self.m = int(length)  # An integer variable representing layout's length
        self.pattern = ''  # Keeps keep track of what pattern is used to build current block
        self.layout_two = [[] for _ in range(self.n)]  # Two dimensional array representing layout two
        self.available_bricks = deque([brick for brick in range(1, (self.n * self.m // 2) + 1)])  # Creates a list with
        # all available bricks to choose from when building layout two

    def layout_area_validator(self):
        """Validates layout area and returns
        True if less than 100, else returns False"""
        result = False
        if self.n <= 100 and self.m <= 100:
            result = True
        return result

    def layout_one_input_validator(self):
        """Validates input and returns True if entries
        are correct, else returns False"""
        result = False
        rows = 0
        columns = 0
        for i in range(self.n):
            rows += 1
            columns += len(self.layout_one[i])
        if rows == self.n and columns == self.m * self.n:
            result = True
        return result

    def layout_one_builder(self):
        """Builds a two dimensional array representing layout number one / client's input"""

        for _ in range(self.n):
            self.layout_one.append([int(brick) for brick in input().split()])

    def brick_span_validator(self):
        """This method is used to iterate through all bricks quarters
        and will check if any brick number spans over three columns or rows.
        True will be returned if no bigger bricks are found, else it will return False.
        """
        result = True
        bricks_size = {}  # A dictionary where all bricks numbers will be kept as
        for i in range(self.n):  # keys and the number of spanning as values
            for j in range(self.m):  # If three quarters of the same brick are found spanning
                key = self.layout_one[i][j]  # the loop will be stopped and the value returned
                if key not in bricks_size.keys():
                    bricks_size[key] = 1
                elif key in bricks_size.keys():
                    if bricks_size[key] + 1 <= 2:
                        bricks_size[key] += 1
                    elif bricks_size[key] + 1 > 2:
                        result = False
                        break
            if result is False:
                break
        return result

    def layout_pattern_setter(self):
        """"This method sets the pattern used in building
        layout number two by scanning the very first brick in layout number one"""

        if self.layout_one[0][0] == self.layout_one[0][1]:      # In case the very first brick in layout one is put
            self.pattern = 'vertical'                           # horizontally then 'layout' variable will be set to
        elif self.layout_one[0][0] == self.layout_one[1][0]:    # 'vertical' and layout number two will start with
            self.pattern = 'horizontal'                         # a brick put vertically or the opposite

    def layout_two_builder(self):
        """"Builds layout number two"""

        self.layout_pattern_setter()  # Sets pattern variable

        j = 0  # Keeps track of current position while moving along the length of the wall
        # and gets incremented depending on 'pattern' variable

        for i in range(0, self.n, 2):  # for' loop used to move down the width while using
                                        # increments of two to cover a whole block

            while j < self.m:  # 'while' loop used to move down the wall, using step of two so we cover

                if j == self.m - 2 and self.pattern == 'vertical':  # In case the penultimate brick is set to be put
                    self.pattern = 'horizontal'                     # vertically then 'pattern' variable will be changed
                                                                    # to horizontal and two bricks will be put instead

                if self.pattern == 'horizontal':    # Checks pattern so we know how to lay down
                                                    # the new block in layout two and how to increment 'j' variable

                    bricks_to_cover = self.bricks_scanner(i, j)  # Keeps information of which bricks will be covered

                    bricks_to_use = self.bricks_picker(bricks_to_cover)  # Keeps information of which bricks will be used in layout two

                    self.layout_two[i].append(bricks_to_use[0])      # Adds the chosen bricks to layout two
                    self.layout_two[i].append(bricks_to_use[0])
                    self.layout_two[i + 1].append(bricks_to_use[1])
                    self.layout_two[i + 1].append(bricks_to_use[1])

                    self.pattern = 'vertical'  # Pattern will then be changed to 'vertical'
                    j += 2  # and 'j' will be incremented by two

                elif self.pattern == 'vertical':

                    bricks_to_cover = self.bricks_scanner(i, j)  # Adds the chosen brick to layout two
                    brick_to_use = self.bricks_picker(bricks_to_cover)
                    self.layout_two[i].append(brick_to_use)
                    self.layout_two[i + 1].append(brick_to_use)

                    self.pattern = 'horizontal'
                    j += 1
            j = 0  # variable changed back to zero so when 'i' is incremented the new
            # block starts from the beginning of the column

    def bricks_scanner(self, row, col):
        """A method to check which brick/s is/are covered in the current block.
        Returns a tuple representing each half of the covered brick/s."""

        if self.pattern == 'horizontal':
            brick_one = self.layout_one[row][col], self.layout_one[row][col + 1]
            brick_two = self.layout_one[row + 1][col], self.layout_one[row + 1][col + 1]
            return brick_one, brick_two
        elif self.pattern == 'vertical':
            brick_one = self.layout_one[row][col], self.layout_one[row + 1][col]
            return brick_one

    def bricks_picker(self, *args):
        """This method will choose the brick/s to
        be used in building the blocks in layout two"""

        if self.pattern == 'horizontal':  # In this case we know that a block of two by two needs to be covered
            bricks_to_cover_one = args[0][0]  # so we create two variables each representing a brick and then we
            bricks_to_cover_two = args[0][1]  # compare each quarter of the bricks and then choose among the
            # available bricks from initialized variable 'available_bricks'

            brick_one = None  # A variable to store the first chosen brick
            brick_two = None  # A variable to store the second chosen brick

            while True:  # A 'while' loop will be kept running until a suitable brick is chosen

                brick_one = self.available_bricks.popleft()  # chooses the first brick

                if self.m <= 4:  # If the length of the wall is less then four quarters then
                    # only haft of the brick which is about to be covered will be compared to
                    # the chosen brick from the variable 'available_bricks'

                    if brick_one != bricks_to_cover_one[0] or brick_one != bricks_to_cover_one[1]:  # When a suitable
                        break  # brick is found the 'while' loop will be broken
                    else:
                        self.available_bricks.append(brick_one)  # If the chosen brick is no good then it will be
                        brick_one = None  # put back in to the 'available_bricks' variable and brick_one will be set
                        # back to 'None'

                elif brick_one != bricks_to_cover_one[0] and brick_one != bricks_to_cover_one[1]:  # If wall's length
                    break  # is bigger than four then both quarters for each brick will be compared
                else:
                    self.available_bricks.append(brick_one)  # In case of no match the chosen brick will be restored in
                    brick_one = None  # 'available_bricks' variable and 'brick_one' will be set back to 'None'

            while True:  # Same applies for picking brick number two
                brick_two = self.available_bricks.popleft()
                if self.m <= 4:
                    if brick_two != bricks_to_cover_two[0] or brick_two != bricks_to_cover_two[1]:
                        break
                    else:
                        self.available_bricks.append(brick_two)
                        brick_two = None
                elif brick_two != bricks_to_cover_two[0] and brick_two != bricks_to_cover_two[1]:
                    break
                else:
                    self.available_bricks.append(brick_two)
                    brick_two = None

            return brick_one, brick_two

        elif self.pattern == 'vertical':  # In case 'pattern' is set to 'vertical' then only one brick will be chosen
            bricks_to_cover_one = args
            brick_one = None
            while True:
                brick_one = self.available_bricks.popleft()
                if brick_one != bricks_to_cover_one[0][0] and brick_one != bricks_to_cover_one[0][1]:
                    break
                else:
                    self.available_bricks.append(brick_one)
                    brick_one = None
            return brick_one

    def __repr__(self):
        """This method will return a two dimensional list joined by new line which represents
         layout number two"""

        result = [' '.join([str(brick) for brick in row]) for row in self.layout_two]  # List comprehension used to
        return '\n'.join(result)  # convert all integers in to strings and then joined by space in a single list then
        # the result is joined by new line and return.


n, m = input().split()

layout = BrickWall(n, m)
if layout.layout_area_validator():
    layout.layout_one_builder()
    if layout.layout_one_input_validator():
        if layout.brick_span_validator():
            layout.layout_two_builder()
            print(layout)
        else:
            print('-1')
            print('A brick spans over three rows / columns')
    else:
        print('-1')
        print('Invalid rows / columns entries.')
else:
    print('-1')
    print('Area must be less than 100 rows / columns.')
