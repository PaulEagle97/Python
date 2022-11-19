"""
Week 4 practice project template for Python Data Representation
Update syntax for print in CodeSkulptor Docs
from "print ..." syntax in Python 2 to "print(...)" syntax for Python 3
"""


def update_line(line):
    """
    Takes a string line representing a single line of code
    and returns a string with 'print' updated
    """
    POSTFIX = "</pre>"

    #find the index of 'print' occurrence
    print_idx = line.find('print')

    if print_idx != -1:
        #calculate the starting index of an expression, 
        #assuming that there is always one whitespace between
        #the 'print' and the expression
        expr_start = print_idx + 5
        #create a tuple of the form ('print', ' ', 'the expression')    
        old_print = line[expr_start-5: ].partition(' ')
        #create a new print statement with '()' around the expression
        new_print = f'{old_print[0]}({old_print[2]})'
        #create a new line by joining 3 parts: string slice from beginning until 'print' 
        #and the updated print statement
        new_line = ''.join([line[:expr_start-5], new_print])

        return new_line
    
    return line


def update_pre_block(pre_block):
    """
    Take a string that correspond to a <pre> block in html and parses it into lines.  
    Returns string corresponding to updated <pre> block with each line
    updated via process_line()
    """
    updated_block = ''
    #create a list of lines
    line_lst = pre_block.split('\n')
    #for each line, update it, add '\n' if not the last line,
    #and add it to the updated block
    for idx, line in enumerate(line_lst):
        updated_line = update_line(line)
        if idx < len(line_lst) - 1:
            updated_line += '\n'
        updated_block += updated_line

    return updated_block


def update_file(input_file_name, output_file_name):
    """
    Open and read the file specified by the string input_file_name
    Proccess the <pre> blocks in the loaded text to update print syntax
    Write the update text to the file specified by the string output_file_name
    """
    import re

    # HTML tags that bound example code
    PREFIX = "<pre class='cm'>"
    POSTFIX = "</pre>"

    # open and read the original html file
    with open(input_file_name, 'r') as input_file:
        old_data = input_file.read()
        new_data = ''
        # a generator of start indexes of each block that needs to be updated
        block_start_idxs = (m.start() + len(PREFIX) for m in re.finditer(PREFIX, old_data))
        end_idx = 0

        # looping over each block index and saving the updated data to (new_data)
        for start_idx in block_start_idxs:
            # adding all the unsaved data before the block
            new_data += old_data[end_idx: start_idx]
            # calculating the end index of the block
            end_idx = start_idx + old_data[start_idx:].find(POSTFIX)
            # computing and adding the updated block string
            new_block = update_pre_block(old_data[start_idx : end_idx])
            new_data += new_block

        # adding all the unsaved data after the last block instance
        new_data += old_data[end_idx: ]

    # writing the updated data to the output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(new_data)


def test():
    '''
    Running tests for each function
    '''
    print('----------\nTEST START\n----------\n')

    # defining inputs and expected outputs for the functions
    inputs = {update_line: ("", "foobar()", "print 1 + 1", "    print 2, 3, 4"),\
              update_pre_block: ("", "foobar()", "if foo():\n    bar()", "print\nprint 1+1\nprint 2, 3, 4",\
                                 "    print a + b\n    print 23 * 34\n        print 1234")}
    exp_outputs = {update_line: ("", "foobar()", "print(1 + 1)", "    print(2, 3, 4)"),\
                   update_pre_block: ("", "foobar()", "if foo():\n    bar()", "print()\nprint(1+1)\nprint(2, 3, 4)",\
                                      "    print(a + b)\n    print(23 * 34)\n        print(1234)")}
    
    # testing the functions
    for func in inputs:
        if func_test(func, inputs[func], exp_outputs[func]) == False:
            return

    # names of the provided test files
    FILENAME_1 = "table.html"
    FILENAME_2 = "docs.html"
    # generating names for updated files
    FILENAME_1_UPD = FILENAME_1[:-5] + '_updated.html'
    FILENAME_2_UPD = FILENAME_2[:-5] + '_updated.html'
    # generating names for solution files
    FILENAME_1_SOL = FILENAME_1[:-5] + '_updated_solution.html'
    FILENAME_2_SOL = FILENAME_2[:-5] + '_updated_solution.html'    

    # running the main function
    update_file(FILENAME_1, FILENAME_1_UPD)
    update_file(FILENAME_2, FILENAME_2_UPD)
    
    # comparing the resulting files with the solution
    files_are_equal(FILENAME_1_UPD, FILENAME_1_SOL)
    files_are_equal(FILENAME_2_UPD, FILENAME_2_SOL)

    print('----------\nTEST END\n----------\n')

    
def func_test(func, inputs, exp_outputs):
    '''
    Runs (func) and compares its actual outputs with the expected ones
    '''    
    fail = False
    for idx, input in enumerate(inputs):
        if func(input) != exp_outputs[idx]:
            print(f'{func.__name__} has failed the test: {input}.\nExpected: {exp_outputs[idx]}\nReturned: {func(input)}\n')
            fail = True
    if not fail:
        print(f'({func.__name__}) has passed all tests\n')
        return True
    else:
        return False  


def files_are_equal(file1_name, file2_name):
    """
    Given two files (whose paths are specified as strings),
    find the first location in the files that differ and
    print a small portion of both files around this location
    """
    print(f"<<< Comparing {file1_name} and {file2_name} >>>")

    WINDOW_SIZE = 10
    
    # open and read both files
    with open(file1_name, 'r') as input_file:
        file1_text = input_file.read()
    with open(file2_name, 'r') as input_file:
        file2_text = input_file.read()

    # calculate the shortest file length
    smaller_length = min(len(file1_text), len(file2_text))

    # iterate through the (smaller_length) number of chars
    # in both files and compare values
    for idx in range(smaller_length):
        if file1_text[idx] != file2_text[idx]:
            start_window = max(0, idx - WINDOW_SIZE)
            end_window = min(smaller_length, idx + WINDOW_SIZE)
            print("Found difference at position:", idx)
            print(file1_name, "has the characters:", file1_text[start_window : end_window])
            print(file2_name, "has the characters:", file2_text[start_window : end_window], '\n')
            return False

    #check whether one file is a prefix of another    
    if len(file1_text) < len(file2_text):
        print(file1_name, "is a prefix of", file2_name)
        return False
    elif len(file2_text) < len(file1_text):
        print(file2_name, "is a prefix of", file1_name)
        return False
    else:
        print(file1_name, "and", file2_name, "are the same\n")
        return True

if __name__ == '__main__':
    test()

