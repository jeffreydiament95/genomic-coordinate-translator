SOLUTION DETAILS
----------------
solution.py takes in two input files:

-A four-column tab-separated file that contains transcript name, chromosome name, 0-based starting position on the chromosome, and CIGAR string indicating mapping.
-A two-column tab-separated file that contains transcript name and 0-based transcript coordinate.
The script then translates transcript coordinates to genomic coordinates and writes the output into a new four-column tab-separated file with the columns:

-transcript name
-0-based transcript coordinate
-chromosome name
-chromosome coordinate

To run the script, you need to pass three arguments:

-input_path_1: the path to the first input file
-input_path_2: the path to the second input file
-output_path: the path to the output file

The script contains the following functions:

-make_index_map(pos, cigar): Converts chromosome starting position and CIGAR string into transcript->chromosome index map.
-is_valid_cigar(s): Checks if a string is a valid CIGAR string.
-get_chrom(df_transcript_info, row): Given a transcript_info DataFrame and a row of a different DataFrame, extracts the chromosome information associated with the transcript of the row, if available.
-get_chrom_index(df_transcript_info, row): Returns the chromosomal index of the transcript given its index on the transcript.
-solve(input_path_1, input_path_2, output_path): Translates transcript coordinates to genomic coordinates.

Note that this script requires the pandas, re, sys, and argparse libraries.

ASSUMPTIONS
-----------

This solution is a minimum viable product that depends on many assumptions in order to work properly. Some of these are outlined below:

-The input files are tab-separated files.
-The first input file has exactly four columns in the order of transcript name, chromosome name, 0-based starting position on chromosome, and CIGAR string indicating mapping.
-The second input file has exactly two columns in the order of transcript name and 0-based transcript coordinate.
-The output file will be a tab-separated file with four columns in the order of transcript name, 0-based transcript coordinate, chromosome name, and chromosome coordinate.
-The CIGAR string in the first input file follows the format described in the SAM format specification.
-The input files have no missing values.
-The transcripts in the second input file match those in the first input file.
-The transcript indices in the second input file are 0-based.
-The chromosome index map returned by make_index_map is also 0-based.

ERROR HANDLING
--------------

The program will handle errors in the following ways:
-Exceptions caused reading from input files/output cause the program to abort with the corresponding exception printed to the command line.
-Improper CIGAR strings will also cause the program to abort with an error message instructing the user of the location of the improper string.
-If a transcript in the second input file is missing a corresponding chromosome in the first file, the program will label the chromosome field in the output file as "NA".
-If a transcript in the second input file has a coordinate that is out of range of the specified CIGAR string, the program will print an error message and set the corresponding chromosome coordinate to -1.

STRENGTHS/ WEAKNESSES/ FUTURE IMPROVEMENTS
--------------------------------------------

-The solution is relatively simple and easy to understand.
-It uses an array to map transcript coordinates to chromosome coordinates, which is a good time/space optimization.
-It returns the correct output for the given problem statement.

Note, this solution is most efficient when there are a high number of queries for a given transcript. It  assembles the transcript->chromosome map for every transcript in the input, and then uses this map as a lookup table for all queries. Thus, if N is the length of the transcript, it takes O(N) time and O(N) space to assemble the data structure, and then O(1) time to answer the query.

There are some potential downsides to this implementation:
-If there is superfluous information in the transcript info file (e.g., transcripts with no corresponding queries) , maps will be created needlessly.
-->Future improvement: only make transcript->chromosome map for transcripts with corresponding queries.

-If there are long transcripts, with coordinate queries near the start, the full map will be created needlessly.
-->Future improvement: instead of assembling a transcript->chromosome map, a just-in-time approach could be used as follows: All transcript queries are grouped together and sorted. The CIGAR string is then iterated through in real time (with no auxiliary data structure), and queries are answered in order. Once all queries are answered, progression through the CIGAr string will halt.


TESTING
-------
The python unittest library was used to develop unit tests to evaluate nominal performance and edge cases for all major functions.
The tests are outlined in test_solution.py and an example output of running these tests is shown below:

% python test_solution.py -v
test_invitae_full_solution (__main__.TestFullSolution.test_invitae_full_solution) ... ok
test_invalid_strings (__main__.TestIsValidCigar.test_invalid_strings) ... ok
test_valid_cigars (__main__.TestIsValidCigar.test_valid_cigars) ... ok
test_invitae_example (__main__.TestMakeIndexMap.test_invitae_example) ... ok
test_max_base_cases (__main__.TestMakeIndexMap.test_max_base_cases) ... ok
test_min_base_cases (__main__.TestMakeIndexMap.test_min_base_cases) ... ok
test_offset (__main__.TestMakeIndexMap.test_offset) ... ok
test_wikipedia_example (__main__.TestMakeIndexMap.test_wikipedia_example) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.010s

