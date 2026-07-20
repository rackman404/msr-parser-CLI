"""
CLI Argument Parsing Module

TODO add unit tests
Refs:
https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module 
https://docs.python.org/3/howto/argparse.html 
https://www.reddit.com/r/learnpython/comments/obn1ig/argparse_how_do_i_add_a_flag_that_doesnt_require/
"""

import argparse
from msr_parser_code import utility

def _user_input_parsed(raw_args: list[str]) -> argparse.Namespace:
    '''
    Where program Args should be processed,
    Should be implementing the arguments specified in the README.md 
    (but only the ones that currently do anything (i.e implemented features))
    '''
    # Positional (mandatory)
    parser = argparse.ArgumentParser(raw_args)
    parser.add_argument("-s", "--search",
                help="The search term (NOTE: search by cID if number is used)",
                required=True
                )

    # Optional Args (with parameters)
    parser.add_argument("-m", "--mode",
        help="Searches AND downloads either using \
            Album name/cID or Song name/cID, or downloads all songs, \
            or downloads songs that don't exist on user hard drive.",
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
        help="Add a watermark to metadata comment field",
        action="store_true",
        default=False)

    #COMMON ARGS ---
    parser.add_argument("-y", "--skipuser",
        help="Will skip user confirmation after presenting found songs to user \
            (and any other user input).",
        action="store_false",
        default=True)
    parser.args = parser.parse_args()
    return parser.args


def _map_to_arg_class(namespace_args: argparse.Namespace) -> utility.ProgramArguments:
    '''
    Map from the parser namespace to actual explicitly defined data classes
    '''
    arg_obj_search = utility.SearchArguments(
        search_term= namespace_args.search,
        mode= namespace_args.mode,
        exact= namespace_args.noexact)

    arg_obj_convert = utility.ConversionArguments(
        convert_format=namespace_args.format,
    )

    arg_obj_download = utility.DownloadArguments(
        lyrics=namespace_args.nolyrics,
    )

    arg_obj_metadata = utility.MetadataArguments(
        watermark = namespace_args.watermark
    )

    arg_obj_common = utility.ProgramArguments(
        search_args= arg_obj_search,
        convert_args= arg_obj_convert,
        download_args= arg_obj_download,
        metadata_args= arg_obj_metadata,

        #common args,
        user_confirmation=namespace_args.skipuser
    )

    return arg_obj_common

def parse_args(raw_args: list[str]) -> utility.ProgramArguments:
    '''
    Main entry point for this file. 

    Will parse CLI arguments, then map said arguments to dataclasses and returns it

    Does not auto strip the very first argument (i.e program name).
    '''
    namespace_args = _user_input_parsed(raw_args)
    parsed_args = _map_to_arg_class(namespace_args)

    return parsed_args
