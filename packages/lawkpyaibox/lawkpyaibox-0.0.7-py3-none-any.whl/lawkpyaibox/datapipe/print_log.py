def print_exception_error(error):
    file = error.__traceback__.tb_frame.f_globals["__file__"]
    rownum = error.__traceback__.tb_lineno
    errorline = "{}#L{}".format(file, rownum)
    print("error exception:{}".format(error))
    print("error line:{}#L{}".format(file, rownum))
    return errorline


def printlog(message, logfile=None):
    print(message)
    try:
        print(message, file=logfile)
    except Exception as e:
        print_exception_error(e)
