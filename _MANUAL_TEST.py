import msr_parser_main
import msr_parser_code.utility as utility

import json

#NOTE not actually a unit test file or anything, just for manually checks
if __name__ == "__main__":
    #msr_parser_main.WORKING_FOLDER_PATHS, msr_parser_main.WORKING_DEPENDENCIES_PATHS = msr_parser_main.init()
    #msr_parser_main.main(download_method=utility.DownloadMethod.SINGLE, name="HUA YU", exact=False, file_format=utility.FileFormat.FLAC, lyrics=True) #should show the OST for obliteration

    print(json.load(open('coverage.json'))['totals']['percent_covered_display'])