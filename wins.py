# Helper functions to detect wins
def flip_horizontal(result):
    # Flips results horizontally to keep them in a more readable format
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
        
    # Rotate 90 degrees to get text representation of spin in order
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    horizontal_values_2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            horizontal_values_2[y][x] = horizontal_values[x][y]
    return horizontal_values_2 
    
def longest_seq(hit):
    sub_seq_length, longest_seq = 1, 1
    start, end = 0, 0
    for i in range(len(hit) - 1):
        if hit[i] == hit[i + 1] - 1: # Checks if the symbols are right next to each other.
            sub_seq_length += 1
            if sub_seq_length > longest_seq:
                longest_seq = sub_seq_length
                start = i + 2 - sub_seq_length 
                end = i + 2
        else:
            sub_seq_length = 1 # If not matching are found.
    return hit[start:end]