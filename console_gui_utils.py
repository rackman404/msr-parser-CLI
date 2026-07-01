# Utility Methods and classes
class bcolors: #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def console_header(header_msg: str):
    '''
    for use in denoting a new major process currently running
    '''
    print(bcolors.HEADER + "###############################################################" + bcolors.ENDC)
    print(bcolors.HEADER + header_msg + bcolors.ENDC)
    print(bcolors.HEADER + "###############################################################" + bcolors.ENDC)

def console_sub_header(header_msg: str):
    '''
    for use in denoting a new minor process currently running
    '''
    print(bcolors.OKGREEN + "----------------------" + header_msg + "----------------------"  + bcolors.ENDC)


def console_help_screen():
    '''
    to be displayed if user inputs -help as a program argument
    '''

def console_print_err(msg: str):
    print(bcolors.FAIL + msg + bcolors.ENDC)

def console_print_success(msg: str):
    print(bcolors.OKGREEN + msg + bcolors.ENDC)