""" This is a Module to do Something."""


def PrintIt(STRING):
    """
    This method is to print s text sent by the called.

    Parameters:
    STRING (str): a string to be printed on screen.

    Returns:
    str: a Predefined message stating that STRING was printed Successfully.
    """
    print(STRING)
    return f"The Following Message was Printed Sucessfully: {STRING}"
