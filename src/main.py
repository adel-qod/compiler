#!/usr/bin/python3.2 -tt

"""
Copyright (c) 2014, Mhd Adel G. Al Qodamni
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:


Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""
import sys
import os
import logging
import lexer

def main():
    """
    main function.
    """
    log_format = '%(filename)s:%(funcName)s():%(lineno)d: %(message)s'
    logging.basicConfig(strea=sys.stdout, level=logging.DEBUG,
                        format=log_format)
    check_argv_sanity()
    lexer.test_lex(sys.argv[1])

def check_argv_sanity():
    """
    Termiantes the program if argv is not an accessible .c file.
    """
    if len(sys.argv) < 2:
        print('Usage: compiler filename.c')
        sys.exit(1)
    if os.path.splitext(sys.argv[1])[1] != '.c':
        print('You must pass a valid .c file')
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print('The name you gave is not a valid file')
        sys.exit(1)
    if not os.access(sys.argv[1], os.R_OK):
        print('We cannot open file specified')
        sys.exit(1)
        
if __name__ == '__main__':
    main()
