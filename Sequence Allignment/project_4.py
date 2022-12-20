

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    entries = alphabet.copy()
    entries.add("-")
    scoring_matrix = {char_1 : {char_2 : 0} for char_1 in entries for char_2 in entries}
    for matrix_row in entries:
        for matrix_col in entries:
            if matrix_row == "-" or matrix_col == "-":
                score = dash_score
            elif matrix_row == matrix_col:
                score = diag_score
            else:
                score = off_diag_score

            scoring_matrix[matrix_row][matrix_col] = score

    return scoring_matrix
