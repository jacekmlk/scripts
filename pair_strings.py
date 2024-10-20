def levenshtein_distance(word_s: str, word_t: str) -> int:
    """
    Compute number of operations necessary to convert one string to another
    Levenshtein distance promote same lenght strings
    Lower value - closer result
    """
    len_s = range(1, len(word_s) + 1)
    len_t = range(1, len(word_t) + 1)
    
    d = [[0 for col in word_s + "a"] for row in word_t + "a"]

    for i in len_s:
        d[0][i] = i
        
    for j in len_t:
        d[j][0] = j
    
    for j in len_t:
        for i in len_s:
            if word_s[i - 1] == word_t[j - 1]:
                cost = 0
            else:
                cost = 1
                
            d[j][i] = min(d[j][i-1] + 1,        # deletion
                          d[j-1][i] + 1,        # insertion
                          d[j-1][i-1] + cost)   # substitution
            
            if (
                i > 1
                and j > 1
                and word_s[i - 1] == word_t[j - 2]
                and word_s[i - 2] == word_t[j - 1]
            ):

                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)  # transposition
                
    return d[-1][-1]


def jaro_winkler(str1: str, str2: str) -> float:
    """
    Jaro-Winkler distance is a string metric measuring an edit distance between two
    sequences.
    Output value is between 0.0 and 1.0.
    Source: https://github.com/TheAlgorithms/Python/blob/master/strings/jaro_winkler.py
    """

    def get_matched_characters(_str1: str, _str2: str) -> str:
        matched = []
        limit = min(len(_str1), len(_str2)) // 2
        for i, char in enumerate(_str1):
            left = int(max(0, i - limit))
            right = int(min(i + limit + 1, len(_str2)))
            if char in _str2[left:right]:
                matched.append(char)
                _str2 = f"{_str2[0:_str2.index(char)]} {_str2[_str2.index(char) + 1:]}"

        return "".join(matched)

    # matching characters
    matching_1 = get_matched_characters(str1, str2)
    matching_2 = get_matched_characters(str2, str1)
    match_count = len(matching_1)

    # transposition
    transpositions = (
        len([(c1, c2) for c1, c2 in zip(matching_1, matching_2) if c1 != c2]) // 2
    )

    if not match_count:
        jaro = 0.0
    else:
        jaro = (
            1
            / 3
            * (
                match_count / len(str1)
                + match_count / len(str2)
                + (match_count - transpositions) / match_count
            )
        )

    # common prefix up to 4 characters
    prefix_len = 0
    for c1, c2 in zip(str1[:4], str2[:4]):
        if c1 == c2:
            prefix_len += 1
        else:
            break

    return jaro + 0.1 * prefix_len * (1 - jaro)


def pair_strings(list_a: list[str], list_b: list[str]) -> dict:
    """
    Pair strings based on levenshtein distance.

    
    :list_a:    base list of strings
    :list_b:    searched list of strings
    """

    cols = range(len(list_a))
    rows = range(len(list_b))
    
    # Create matrix of lists for l_distance
    strings_matrix = [[0 for col in cols] for row in rows]
    
    print(strings_matrix)
    
    # Compute levenstein distance for each element of matrix
    for j in rows:
        for i in cols:
            strings_matrix[j][i] = jaro_winkler(list_a[i], list_b[j])

    map = {}
    # Pair strings based on levenstein distance
    for i in cols:
        pair_location = (0,i)
        min_pos = strings_matrix[0][i]
        for j in rows:
            if strings_matrix[j][i] > min_pos:
                min_pos = strings_matrix[j][i]
                pair_location = (j,i)
        map[list_a[pair_location[1]]] = list_b[pair_location[0]]
        
    return map

if __name__ == "__main__":
    print(pair_strings(["request_id", "attr"], ["request_Id", "attribute", "void"]))
