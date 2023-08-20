from pyfiglet import Figlet


def signature(title):
    f = Figlet(font="fender")
    print(f.renderText(title))
    print("*-------------------Author---------------------*")
    print("Ishfaq Ahmed, https://github.com/IshfaqAhmedProg")
