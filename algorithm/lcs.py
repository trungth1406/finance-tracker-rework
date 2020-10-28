def diff_table(first_arr, second_arr, len_x, len_y):
    """Algorithm for creating the longest subsequence table"""
    count_table = [[0 for _ in range(len_y + 1)] for _ in range(len_x + 1)]
    for i in range(len_x + 1):
        for j in range(len_y + 1):
            if i == 0 or j == 0:
                count_table[i][j] = 0
            elif first_arr[i - 1] == second_arr[j - 1]:
                count_table[i][j] = 1 + count_table[i - 1][j - 1]
            else:
                count_table[i][j] = max(count_table[i - 1][j], count_table[i][j - 1])
    return count_table


""" Lesson about default parameters : list [] with name str_builder was initialize with mutable list in python"""


def get_changes_content(count_table, first_str, second_str, len_a, len_b, str_builder):
    if len_a > 0 and len_b > 0 and (first_str[len_a - 1] == second_str[len_b - 1]):
        str_builder.append(f" {first_str[len_a - 1]}")
        get_changes_content(count_table, first_str, second_str, len_a - 1, len_b - 1, str_builder)
    elif len_b > 0 and (len_a == 0 or count_table[len_a - 1][len_b] >= count_table[len_a][len_b - 1]):
        str_builder.append(f" +{second_str[len_b - 1]}")
        get_changes_content(count_table, first_str, second_str, len_a, len_b - 1, str_builder)
    elif len_a > 0 and (len_b == 0 or count_table[len_a - 1][len_b] < count_table[len_a][len_b - 1]):
        str_builder.append(f" -{first_str[len_a - 1]}")
        get_changes_content(count_table, first_str, second_str, len_a - 1, len_b, str_builder)
    return str_builder
