def c_types():
    return [
        ('char', '%c'),
        ('double/float', '%f'),
        ('int', '%d'),
        ('long', '%l'),
        ('long double', '%lF'),
        ('string/char *', '%s'),
        ('short', '%hi'),
        ('unsigned short', '%hi'),
        ('void *', '%p'),
    ]