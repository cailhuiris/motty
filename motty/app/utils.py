def remove_last_slash(txt):
    return txt[0:len(txt)-1] if txt[len(txt)-1] == '/' else txt