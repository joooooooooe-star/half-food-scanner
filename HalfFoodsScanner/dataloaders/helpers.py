
def error_checker(str_one: str, str_two: str) -> bool:
    
    assert(len(str_one) == len(str_two))
    error_count = 0
    for i, ch in enumerate(str_one):
        if str_two[i] != ch:
            error_count += 1
        if error_count > 2:
            return False
    return True
