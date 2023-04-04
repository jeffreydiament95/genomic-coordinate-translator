import pandas as pd
import re
import sys
import argparse


class Solution:
    @staticmethod
    def make_index_map(pos, cigar):
        """
        Converts chromosome starting position and CIGAR string into transcript->chromosome index map

        Parameters:
            pos (int): The starting index on the chromosome.
            cigar (str): The CIGAR string describing the transcript.

        Returns:
            array: the transcript->chromosome index map
            (i.e. value at position N is chromosome coordinate corresponding to transcript coordinate N
        """
        trans_to_chrom_map = []
        chrom_index = pos

        matches = re.findall(r'\d+[MIDNSHPX=]', cigar)

        for match in matches:
            num = int(match[:-1])
            op = match[-1]

            # alignment match (can be a sequence match or mismatch)
            if op == 'M':
                consumes_trans = True
                consumes_chrom = True

            # insertion to the reference
            elif op == 'I':
                consumes_trans = True
                consumes_chrom = False

            # deletion from the reference
            elif op == 'D':
                consumes_trans = False
                consumes_chrom = True

            # skipped region from the reference
            elif op == 'N':
                consumes_trans = False
                consumes_chrom = True

            # soft clipping (clipped sequences present in SEQ)
            elif op == 'S':
                consumes_trans = True
                consumes_chrom = False

            # hard clipping (clipped sequences NOT present in SEQ)
            elif op == 'H':
                consumes_trans = False
                consumes_chrom = False

            # padding (silent deletion from padded reference)
            elif op == 'P':
                consumes_trans = False
                consumes_chrom = False

            # sequence match
            if op == '=':
                consumes_trans = True
                consumes_chrom = True

            # sequence mismatch
            if op == 'X':
                consumes_trans = True
                consumes_chrom = True

            for _ in range(0, num):
                if consumes_trans:
                    trans_to_chrom_map.append(chrom_index)
                if consumes_chrom:
                    chrom_index += 1

        return trans_to_chrom_map

    @staticmethod
    def is_valid_cigar(s):
        """
        Checks if a string is a valid CIGAR string.

        Parameters:
            s (str): The string to be tested.

        Returns:
            bool: True if it's a CIGAR string, False if not
        """
        cigar_pattern = r'^([1-9]\d*[MIDNSHPX=])+$'
        return bool(re.match(cigar_pattern, s))

    @staticmethod
    def get_chrom(df_transcript_info, row):
        """
        Given a transcript_info DataFrame and a row of a different DataFrame, extracts the chromosome information
        associated with the transcript of the row, if available.

        Parameters:
            df_transcript_info (pd.DataFrame): DataFrame containing transcript information, with at least the columns
                                             "trans" and "chrom".
            row (pd.Series): A row of a different DataFrame that has a "trans" column with values matching those in
                             the "trans" column of the transcript_info DataFrame.

        Returns:
            str: The chromosome information associated with the transcript of the row, if found in the df_transcript_info
                 DataFrame. Otherwise, returns the string "NA".
        """

        try:
            chrom = df_transcript_info["chrom"].loc[df_transcript_info["trans"] == row["trans"]].iloc[0]
        except IndexError:
            chrom = "NA"
        return chrom

    @staticmethod
    def get_chrom_index(df_transcript_info, row):
        """
        Returns the chromosomal index of the transcript given its index on the transcript.

        Parameters:
            df_transcript_info (pandas.DataFrame): A DataFrame containing transcript information, including
                the transcript ID, chromosome name, and an index map that maps transcript indices to
                chromosomal indices.
            row (pandas.Series): A row of a DataFrame containing information about a single transcript, including
                the transcript ID and its index on the transcript.

        Returns:
            int: The chromosomal index of the transcript corresponding to the input transcript index. Returns -1
            if the input transcript index is out of range.
        """

        index_map = df_transcript_info["index_map"].loc[df_transcript_info["trans"] == row["trans"]].iloc[0]
        trans_index = row["trans_index"]

        try:
            chrom_index = index_map[trans_index]
        except IndexError:
            print("Transcript {} index {} out of range.".format(row["trans"], row["trans_index"]))
            chrom_index = -1
        return chrom_index

    @staticmethod
    def solve(input_path_1, input_path_2, output_path):
        """
        Translates transcript coordinates to genomic coordinates

        Parameters:
            input_path_1 (str): Path to four column, tab-separated file with columns for:
                transcript name, chromosome name, 0-based starting position on chromosome, CIGAR string indicating mapping
            input_path_2 (st): Path to two column, tab-separated file with columns for:
                transcript name, 0-based transcript coordinate
            output_path(str): Path for newly created four column, tab-separated file with columns for:
                transcript name, 0-based transcript coordinate, chromosome name, chromosome coordinate

        Returns:
            None
        """

        # read first input file into dataframe
        try:
            df_transcript_info = pd.read_csv(input_path_1, delimiter="\t", header=None,
                                             names=["trans", "chrom", "chrom_index", "cigar"],
                                             dtype={0: str, 1: str, 2: int, 3: str})

            valid_cigars = df_transcript_info['cigar'].apply(Solution.is_valid_cigar)
            invalid_indices = valid_cigars[~valid_cigars].index
            if len(invalid_indices) > 0:
                raise ValueError("Invalid CIGAR strings found at indices: {}".format(invalid_indices))
            print("Input 1 successfully read from: {}".format(input_path_1))
        except Exception as e:
            print("Error reading input file 1: {}. Please fix file and re-run.".format(input_path_1))
            print((str(e)))
            sys.exit(1)

        # read second input file into dataframe
        try:
            df_queries = pd.read_csv(input_path_2, delimiter="\t", header=None,
                                     names=["trans", "trans_index"])
            print("Input 2 successfully read from: {}".format(input_path_2))
        except Exception as e:
            print("Error reading input file 2: {}. Please fix file and re-run.".format(input_path_2))
            print((str(e)))
            sys.exit(1)

        # add transcript->chromosome map to transcript info dataframe
        df_transcript_info["index_map"] = df_transcript_info.apply(
            lambda row: Solution.make_index_map(row["chrom_index"], row["cigar"]), axis=1)

        # create output dataframe and populate with transcript chromosome name and coordinates
        df_output = df_queries.copy()
        df_output["chrom"] = df_output.apply(lambda row: Solution.get_chrom(df_transcript_info, row), axis=1)
        df_output["chrom_index"] = df_output.apply(lambda row: Solution.get_chrom_index(df_transcript_info, row), axis=1)

        # write to output file
        try:
            df_output.to_csv(output_path, sep='\t', header=False, index=False)
            print("Output file successfully written to: {}.".format(output_path))
        except Exception as e:
            print("Error writing to output file: {}. Please address issue and re-run.".format(output_path))
            print((str(e)))
            sys.exit(1)


if __name__ == '__main__':
    """
    Parse arguments from command line and pass them to main(). See comments above for more details on inputs.

    Returns:
        None
    """

    # if run from the command line, parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path_1', type=str, help='Path to input file 1 (transcript information)')
    parser.add_argument('input_path_2', type=str, help='Path to input file 2 (transcript coordinate queries)')
    parser.add_argument('output_path', type=str, help='Path to output file (to be created)')
    args = parser.parse_args()
    Solution.solve(args.input_path_1, args.input_path_2, args.output_path)