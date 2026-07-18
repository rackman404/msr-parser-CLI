import argparse
import utility

#TODO https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module add tests
#https://docs.python.org/3/howto/argparse.html 
#https://www.reddit.com/r/learnpython/comments/obn1ig/argparse_how_do_i_add_a_flag_that_doesnt_require/

TEST_ARGS = True
#TEST_ARGS_PARAMS = ["missy", "-m", "single"]
TEST_HELP = ["missy", "-h"]

def user_input_parsed(input: list[str]):
    '''
    Where program Args should be processed, should return a error and failed exit code if formatted incorrectly. Should a list of args selected afterwards before proceeding to main code
    
    Should be implementing the arguments specified in the README.md (but only the ones that currently do anything (i.e implemented features))

    '''
    # Positional (mandatory)
    parser = argparse.ArgumentParser(input)
    parser.add_argument("-s", "--search", 
                help="The search term (NOTE: if a number is passed, will search by cID instead of name)",           
                )
    
    # Optional Args (with parameters)
    parser.add_argument("-m", "--mode",
        help="Searches AND downloads either using Album name/cID or Song name/cID, or downloads all songs, or downloads songs that don't exist on user hard drive.",
        type=utility.DownloadMethod, choices=list(utility.DownloadMethod),
        default= utility.DownloadMethod.SINGLE)
    parser.add_argument("-f", "--format", 
        help="Will convert downloaded music files to the following format",
        type=utility.FileFormat, choices=list(utility.FileFormat),
        default= utility.FileFormat.WAV)

    # Optional Flag Setting Args
    parser.add_argument("--noexact", 
        help="If flag is enabled, will search using the provided search term as a substring",
        action="store_true",
        default=False)
    parser.add_argument("-d", "--diff", 
        help="From found songs, only download those that don't exist in output directory",
        action="store_true",
        default=False)
    parser.add_argument("--nolyrics", 
        help="Will skip downloading any .lrc files if a song has it",
        action="store_false",
        default=True)

    parser.add_argument("-w", "--watermark", 
        help="Will skip downloading any .lrc files if a song has it",
        action="store_true",
        default=False)
    
    #COMMON ARGS ---
    parser.add_argument("-y", "--skipuser", 
        help="Will skip user confirmation after presenting found songs to user (and any other user input).",
        action="store_false",
        default=True)
    
    parser.args = parser.parse_args()
    return parser.args


def map_to_arg_class(args):
    '''
    Map from the parser namespace to actual explicitly defined data classes 
    '''
    arg_obj_search = utility.SearchArguments(
        search_term= args.search,
        mode= args.mode,
        exact= args.noexact)
    
    arg_obj_convert = utility.ConversionArguments(
        convert_format=args.format,
    )

    arg_obj_download = utility.DownloadArguments(
        lyrics=args.nolyrics,
    )

    arg_obj_metadata = utility.MetadataArguments(
        #watermark = args.watermark
    )

    arg_obj_common = utility.ProgramArguments(
        search_args= arg_obj_search,
        convert_args= arg_obj_convert,
        download_args= arg_obj_download,
        metadata_args= arg_obj_metadata,

        #common args,
        user_confirmation=args.skipuser
    )

    return arg_obj_common

def parse_args(input: list[str]):
    '''
    Main entry point for this file. Will parse CLI arguments, then map said arguments to dataclasses and returns it
    '''
    raw_args = user_input_parsed(input)
    #print (raw_args)

    parsed_args = map_to_arg_class(raw_args)
    #print (parsed_args)

    return parsed_args

parsed = parse_args(TEST_HELP)