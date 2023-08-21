
def validate_string(string):
    par_map = {
        "(": ")",
        "[": "]",
        "{": "}"
    }
    open_par = par_map.keys()
    close_par = par_map.values()

    par_close_order = []
    for char in string:
        if char in open_par:
            par_close_order.append(par_map.get(char))
        else:
            exp_par = par_close_order.pop()
            if char != exp_par:
                return False

    return True


if __name__ == '__main__':
    print validate_string('({[()]})') # True
    print validate_string('({[(}]})') # False

