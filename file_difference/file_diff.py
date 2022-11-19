"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.
"""
import os

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
        line1 - first single line string
        line2 - second single line string
    Output:
        Returns the index where the first difference between
        line1 and line2 occurs.

        Returns IDENTICAL if the two lines are the same.
    """

    #determine the shortest line length
    len_1 = len(line1)
    len_2 = len(line2)
    min_len = min(len_1, len_2)

    #check pairs of chars in both lines
    #until reaching the end of the shortest line
    for idx in range(min_len):
        if line1[idx] != line2[idx]:
            return idx
  
    #check whether lengths of the lines are different
    #and return the index that is one past the last character 
    #in the shorter line and IDENTICAL otherwise
    if len_1 != len_2:
        return min_len
    
    return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
        line1 - first single line string
        line2 - second single line string
        idx   - index at which to indicate difference
    Output:
        Returns a three line formatted string showing the location
        of the first difference between line1 and line2.

        If either input line contains a newline or carriage return,
        then returns an empty string.

        If idx is not a valid index, then returns an empty string.
    """
    matches = ("\n", "\r")

    #validate the input line strings
    if not any(x in a_string for x in matches for a_string in (line1, line2)):
        #validate the input index
        if 0 <= idx <= len(min(line1, line2)):
            #create a separator line based on the input index
            sep_line = ''
            for _ in range(idx):
                sep_line += '='
            sep_line += '^'
            return '\n'.join((line1, sep_line, line2)) + '\n'

    return ""


def multiline_diff(lines1, lines2):
    """
    Inputs:
        lines1 - list of single line strings
        lines2 - list of single line strings
    Output:
        Returns a tuple containing the line number (starting from 0) and
        the index in that line where the first difference between lines1
        and lines2 occurs.

        Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    #determine the shortest list length
    len_1 = len(lines1)
    len_2 = len(lines2)
    min_len = min(len_1, len_2)

    #check pairs of lines in both lists
    #until reaching the end of the shortest list
    for line_num in range(min_len):
        diff_idx = singleline_diff(lines1[line_num], lines2[line_num])
        if diff_idx != IDENTICAL:
            return line_num, diff_idx 
  
    #check whether lengths of the lines are different
    #and return the index that is one past the last character 
    #in the shorter line and IDENTICAL otherwise
    if len_1 != len_2:
        return min_len, 0
    
    return IDENTICAL, IDENTICAL


def get_file_lines(file_loc):
    """
    Inputs:
        file_loc - location of file to read
    Output:
        Returns a list of lines from the file at (file_loc).  Each
        line will be a single line string with no newline ('\n') or
        return ('\r') characters.

        If the file does not exist or is not readable, then the
        behavior of this function is undefined.
    """
    #open, read the text file and then break it into lines
    with open(file_loc, 'r', encoding='utf-8') as input_file:
        return input_file.read().splitlines()


def file_diff_format(file_loc1, file_loc2):
    """
    Inputs:
        file_loc1 - location of first file
        file_loc2 - location of second file
    Output:
        Returns a four line string showing the location of the first
        difference between the two files named by the inputs.

        If the files are identical, the function instead returns the
        string "The files are identical\n".

        If either file does not exist or is not readable, then the
        behavior of this function is undefined.
    """
    #read and convert each file to a list of lines
    lines_1 = get_file_lines(file_loc1)
    lines_2 = get_file_lines(file_loc2)

    #look for a difference between two lists
    line_num, diff_idx = multiline_diff(lines_1, lines_2)

    #if not identical, print a line number
    #and show a location of the first different char
    if (line_num, diff_idx) != (IDENTICAL, IDENTICAL):
        text = f'Line {line_num}:\n'
        text += singleline_diff_format(lines_1[line_num], lines_2[line_num], diff_idx)
        return text

    return "The files are identical\n"


def test():
    '''
    Running tests for each function
    '''
    print('----------\nTEST START\n----------\n')

    #computing absolute paths to test files
    curr_dir = os.getcwd()
    test_dir = os.path.join(curr_dir, 'file_difference', 'Tests')
    file1_loc = os.path.join(test_dir, 'file1.txt')
    file2_loc = os.path.join(test_dir, 'file2.txt')
    file3_loc = os.path.join(test_dir, 'file3.txt')
    file6_loc = os.path.join(test_dir, 'file6.txt')
    file7_loc = os.path.join(test_dir, 'file7.txt')
    file8_loc = os.path.join(test_dir, 'file8.txt')
    file10_loc = os.path.join(test_dir, 'file10.txt')
    
    #testing (singleline_diff) - PASS
    str_1 = '123456'
    str_2 = '123ab'
    str_3 = '12345678'
    str_4 = ''
    print('(singleline_diff)')
    print(singleline_diff(str_1, str_2)) 
    #expected: 3
    print(singleline_diff(str_1, str_3)) 
    #expected: 6
    print(singleline_diff(str_1, str_4)) 
    #expected: 0
    print(singleline_diff(str_1, str_1)) 
    #expected: -1
    print('-----------------')

    #testing (singleline_diff_format) - PASS
    str_5 = '123\n'
    str_6 = '456'
    str_7 = 'abc\r'
    str_8 = '45ef'
    print('(singleline_diff_format)')
    print(singleline_diff_format(str_5, str_6, 0)) 
    #expected: ""
    print(singleline_diff_format(str_6, str_7, 0)) 
    #expected: ""
    print(singleline_diff_format(str_6, str_8, -1)) 
    #expected: ""
    print(singleline_diff_format(str_6, str_8, 4)) 
    #expected: ""
    print(singleline_diff_format(str_6, str_8, 2)) 
    #extected: "456\n==^\n45ef\n"
    print('------------------------')

    #testing (multiline_diff) - PASS
    list_1 = ['12', '34', '567']
    list_2 = ['12', '35', '6']
    list_3 = ['12', '34', '567', '89']
    print('(multiline_diff)')
    print(multiline_diff(list_1, list_2)) 
    #expected: (1, 1)
    print(multiline_diff(list_1, list_3)) 
    #expected: (3, 0)
    print(multiline_diff(list_1, list_1)) 
    #expected: (-1, -1)
    print('----------------')

    #testing (get_file_lines) - PASS
    print('(get_file_lines)')
    print(get_file_lines(file1_loc)) 
    #expected: ['engineering classes', 'science classes']
    print(get_file_lines(file8_loc)) 
    #expected: ['abc']
    print (get_file_lines(file10_loc)) 
    #expected: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    print('----------------')
    
    #testing (file_diff_format) - PASS
    print('(file_diff_format)')
    print(file_diff_format(file1_loc, file2_loc)) 
    #expected: "Line 1:\nscience classes\n=====^\nscienee classes\n"
    print(file_diff_format(file1_loc, file3_loc)) 
    #expected: "Line 0:\engineering classes\n=====^\nenginneering classes\n"
    print(file_diff_format(file6_loc, file7_loc)) 
    #expected: "The files are identical\n"

    print('----------\nTEST END\n----------\n')


if __name__ == '__main__':
    test()

