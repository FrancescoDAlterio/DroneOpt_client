

def toKilo(control,value):

    value = str_to_float(value)[1]
    if control[0]=="M":
        value = value * 1000
    if control[0]== "G":
        value = value * 1000000

    return value


def str_to_i(val):

    try:
        val_int=int(val)
    except ValueError:
        return False,0

    return True,val_int

def str_to_float(val):

    try:
        val_float=float(val)
    except ValueError:
        return False,0

    return True,val_float