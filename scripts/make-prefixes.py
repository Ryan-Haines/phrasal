#!/usr/bin/env python
#
# Deterministically convert an input file
# into a prefix file for tuning. Output is written
# to stdout.
#
# The procedure selects prefixes by deterministic sampling of
# suffixes. Which prefixes are selected for an input depends on
# two parameters: the file length and the line number.
#
# NOTE: A prefix is defined as a target reference string
#       with length 1 <= n <= |e|.
#
# Author: Spence Green
#
import sys
import codecs
import os
from argparse import ArgumentParser

def make_prefixes(src_file, tgt_file, samples_per_sent):
    """
    Make a prefix file deterministically by selecting suffixes.
    """
    with codecs.open(src_file, encoding='utf-8') as infile:
        src = [x.strip() for x in infile.readlines()]
    with codecs.open(tgt_file, encoding='utf-8') as infile:
        tgt = [x.strip() for x in infile.readlines()]
    with codecs.open(src_file+'.out','w',encoding='utf-8') as srcout, codecs.open(tgt_file+'.out','w',encoding='utf-8') as tgtout, codecs.open(tgt_file+'.prefix','w',encoding='utf-8') as prfout:
        i = 1
        for j in xrange(0,samples_per_sent):
            for f,e in zip(src,tgt):
                e_tok = e.split()
                e_len = len(e_tok)
                # l := the suffix length
                l = i % e_len
                srcout.write(f + os.linesep)
                tgtout.write(e + os.linesep)
                prfout.write(' '.join(e_tok[0:e_len-l]) + os.linesep)
                i += 1
        print '# examples:', i-1

def main():
    """
    Main method
    """
    desc = 'Convert an source/target corpus to a prefix tuning corpus.'
    parser = ArgumentParser(description=desc)
    parser.add_argument('src_file',
                        help='Input file.')
    parser.add_argument('tgt_file',
                        help='Input file.')
    parser.add_argument('-s','--samples-per-sent',
                        dest='nsamples',
                        type=int,
                        default=1,
                        help='Number of samples per sentence (default: 1).')
    args = parser.parse_args()
    
    make_prefixes(args.src_file, args.tgt_file, args.nsamples)

if __name__ == '__main__':
    main()
