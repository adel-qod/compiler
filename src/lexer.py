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

import io
import os
import sys
import logging

class Tokens:
    """
    This class represents the set of tokens this lexer returns.

    DO NOT CHANGE THEIR VALUES
    """
    ## Data types
    VOID_T = 0
    INT_T = 1
    CHAR_T = 2
    FLOAT_T = 3
    AUTO_T = 4
    ## Possible values
    INT = 5
    CHAR = 6
    FLOAT = 7
    ## Identifier and common reserved words
    ID = 8
    RET = 9
    SIZEOF = 10
    STRUCT = 11
    UNION = 12
    ## Modifiers
    CONST = 13
    STATIC = 14
    EXTERN = 15
    ## Conditional statements
    IF = 16
    ELSE = 17
    WHILE = 18
    FOR = 19
    BREAK = 20
    CONT = 21
    IN = 22
    ## Arithemtic operators
    ADD = 23
    MINUS = 24
    ASTER = 25
    DIVID = 26
    MOD = 27
    ASSIGN = 28  # =
    ## Comparision operators
    LT = 29  # < 
    MT = 30
    LE = 31  # <=
    ME = 32  # >=
    EQ = 33  # ==
    NEQ = 34  # !=
    ## Logical operators
    AND = 35  # &&
    OR = 36
    NOT = 37  # !
    ## bit operators
    BIT_AND = 38
    BIT_OR = 39
    BIT_NOT = 40  # ~
    ## Access operators
    DOT_ACC = 41  # .
    DASH_ACC = 42  # ->
    # grouping
    LPARAN = 43  # (
    RPARAN = 44
    LCURL = 45  # {
    RCURL = 46
    LBRACKET = 47  # [
    RBRACKET = 48
    # Misc
    COL = 51  # ,
    SEM_COL = 52
    AT = 53  # @
    STR = 54  # "adsda"
    CMNT = 55

    @staticmethod
    def tok_to_str(tok):
        '''
        Returns a string to tell what the token is.

        Arguments:
            tok: The number of the token
        Returns:
            a string to describe what the token passed is e.g if tok == 1
                                                                 return 'int'
            returns None if the tok is not a token
        '''
        dic = { 0 : 'VOID_T', 1 : 'INT_T', 2 : 'CHAR_T', 3 : 'FLOAT_T',
                4 : 'AUTO_T', 
                5 : 'INT' , 6 : 'CHAR LIT', 7 : 'FLOAT',
                8 : 'ID', 9 : 'RET', 10 : 'SIZEOF', 11 : 'STRUCT',
                12 : 'UNION', 13 : 'CONST', 14 : 'STATIC',
                15 : 'EXTERN', 16 : 'IF', 17 : 'ELSE',
                18 : 'WHILE', 19 : 'FOR', 20 : 'BREAK',
                21 : 'CONT', 22 : 'IN', 23 : 'ADD',
                24 : 'MINUS', 25 : 'ASTER', 26 : 'DIVID',
                27 : 'MOD', 28 : 'ASSIGN', 29 : 'LT',
                30 : 'MT', 31 : 'LE', 32 : 'ME', 33 : 'EQ',
                34 : 'NEQ', 35 : 'AND', 36 : 'OR', 37 : 'NOT',
                38 : 'BIT_AND', 39 : 'BIT_OR', 40 : 'BIT_NOT',
                41 : 'DOC_ACC', 42 : 'DASH_ACC', 43 : 'LPARAN',
                44 : 'RPARAN', 45 : 'LCURL', 46 : 'RCURL',
                47 : 'LBRACKET', 48 : 'RBRACKET',
                51 : 'COL', 52 : 'SEM_QOL', 53 : 'AT',
                54 : 'STR', 55 : 'CMNT'
            }
        if tok in dic:
            return dic[tok]
        return None

class Lexer:
    """
    Retrieve tokens from a .c file.
    """

    def __init__(self, path):
        """
        Initates the class with the path.
        """
        self._file = io.open(path, 'r', os.stat(path).st_blksize)
        logging.debug('file block size: ' + str(os.stat(path).st_blksize))
        self._res = { }
        self._init_reserved()
        self._col = -1
        self._row = 1
        self._peek = None
        self._readch()

    def scan(self):
        """
        Reads the next token.

        Returns: - The token number, the row & col numbers where it appeared,
                   [value: either the number or the ID itself as a string]
                 - None when it cannot read anything anymore
                 - -1 When an error is encountered
        """
        self._ignore_spaces()
        tmp = []
        start_row = self._row
        start_col = self._col
        if self._peek.isalpha() or self._peek == '_':
            return self._tokenize_res_id()
        elif self._peek.isnumeric():
            return self._tokenize_number()
        elif self._peek == "'":
            return self._tokenize_char_literal()
        elif self._peek == '"':
            return self._tokenize_str_literal()
        elif self._peek == '+':
            self._readch()  # move to next char
            return Tokens.ADD, start_row, start_col
        elif self._peek == '-':
            self._readch()  # move to next char
            if self._peek == '>':
                self._readch()
                return Tokens.DASH_ACC, start_row, start_col
            return Tokens.MINUS, start_row, start_col
        elif self._peek == '*':
            self._readch()  # move to next char
            return Tokens.ASTER, start_row, start_col
        elif self._peek == '/':
            self._readch()  # move to next char
            if self._peek == '/':
                return self._tokenize_comment()
            return Tokens.DIVID, start_row, start_col
        elif self._peek == '%':
            self._readch()  # move to next char
            return Tokens.MOD, start_row, start_col
        elif self._peek == '=':
            self._readch()  # move to next char
            if self._peek == '=':
                self._readch()
                return Tokens.EQ, start_row, start_col
            return Tokens.ASSIGN, start_row, start_col
        elif self._peek == '<':
            self._readch()  # move to next char
            if self._peek == '=':
                self._readch()
                return Tokens.LE, start_row, start_col
            return Tokens.LT, start_row, start_col
        elif self._peek == '>':
            self._readch()
            if self._peek == '=':
                self._readch()
                return Tokens.ME, start_row, start_col
            return Tokens.MT, start_row, start_col
        elif self._peek == '!':
            self._readch()
            if self._peek == '=':
                self._readch()
                return Tokens.NEQ, start_row, start_col
            return Tokens.NOT, start_row, start_col
        elif self._peek == '&':
            self._readch()
            if self._peek == '&':
                self._readch()
                return Tokens.AND, start_row, start_col
            return Tokens.BIT_AND, start_row, start_col
        elif self._peek == '|':
            self._readch()
            if self._peek == '|':
                self._readch()
                return Tokens.OR, start_row, start_col
            return Tokens.BIT_OR, start_row, start_col
        elif self._peek == '~':
            self._readch()
            return Tokens.BIT_NOT, start_row, start_col
        elif self._peek == '.':
            self._readch()
            return Tokens.DOT_ACC, start_row, start_col
        elif self._peek == '(':
            self._readch()
            return Tokens.LPARAN, start_row, start_col
        elif self._peek == ')':
            self._readch()
            return Tokens.RPARAN, start_row, start_col
        elif self._peek == '{':
            self._readch()
            return Tokens.LCURL, start_row, start_col
        elif self._peek == '}':
            self._readch()
            return Tokens.RCURL, start_row, start_col
        elif self._peek == '[':
            self._readch()
            return Tokens.LBRACKET, start_row, start_col
        elif self._peek == ']':
            self._readch()
            return Tokens.RBRACKET, start_row, start_col
        elif self._peek == ',':
            self._readch()
            return Tokens.COL, start_row, start_col
        elif self._peek == ';':
            self._readch()
            return Tokens.SEM_COL, start_row, start_col
        elif self._peek == '@':
            self._readch()
            return Tokens.AT, start_row, start_col
        elif self._peek == '':
            return None  # stream is done
        logging.debug('peek = %s\n' % self._peek)
        logging.debug(tmp)
        return -1 ## in case of error return -1
    
    def _ignore_spaces(self):
        """ Reads from the file as long as the char read is whitespace. """
        while self._peek.isspace():
            self._readch()

    def _tokenize_res_id(self):
        """
        Tokenizes reserved words and IDs.

        Returns: The token number, the row & col numbers where it appeared,
                 [value: the ID itself as a string]
        """
        assert self._peek.isalpha() or self._peek == '_'
        tmp = []
        start_row = self._row
        start_col = self._col 
        while self._peek.isalnum() or self._peek == '_':
            tmp.append(self._peek)
            self._readch()
        lexeme = ''.join(tmp)
        if lexeme in self._res:
            return self._res[lexeme], start_row, start_col
        return Tokens.ID, start_row, start_col, lexeme

    def _tokenize_number(self):
        """
        Tokenizes numbers (integers and floating point).

        Returns: The token number, the row & col numbers where it appeared,
                 the number itself
        """
        assert self._peek.isnumeric()
        tmp = []
        start_row = self._row
        start_col = self._col
        while self._peek.isnumeric():
            tmp.append(self._peek)
            self._readch()
        if self._peek != '.':
            lexeme = int(''.join(tmp))
            return Tokens.INT, start_row, start_col, lexeme
        tmp.append('.')
        self._readch()
        if not self._peek.isnumeric():
            self.lex_err('floating point numbers should be of the form x.y')
        while self._peek.isnumeric():
            tmp.append(self._peek)
            self._readch()
        lexeme = float(''.join(tmp))
        return Tokens.FLOAT, start_row, start_col, lexeme

    def _tokenize_char_literal(self):
        """
        Tokenizes single char literals (e.g 'h' or '\t').
        
        Returns: The token number, the row & col numbers where it appeared,
                 the ascii value of the char literal as an int 
        """
        assert self._peek == "'"
        start_row = self._row
        start_col = self._col
        self._readch()
        lexeme = self._peek
        #  logging.debug(tok)
        if lexeme == "'":  # empty character literals '' are not allowed
            self.lex_err("Char literals cannot be empty (i.e '')")
        elif lexeme == '\\':  # if what we read is a skip character (e.g \t)
            skip_char = {
                '0' : 0, 'a' : 7, 'b' : 8, 't' : 9, 'n' : 10, 'v' : 11,
                'f' : 12, 'r' : 13, '\\' : 28, "'" : 39
                }
            self._readch()
            lexeme = self._peek
            if lexeme not in skip_char:
                self.lex_err('Char followed by \ is not an ascii skip char')
            lexeme = get_ascii_skip_val(lexeme)
        else:
            lexeme = ord(lexeme)
        self._readch()
        if self._peek != "'":
            self.lex_err("Char literals contain one char (e.g 'a' or '\\a')")
        # we need to advance the peek to the begining of the next char
        # beyond this token                
        self._readch()
        return Tokens.CHAR, start_row, start_col, lexeme               

    def _tokenize_str_literal(self):
        """
        Tokenizes string literals.

        Returns: The token number, the row & col numbers where it appeared,
                 the lexeme as a string (i.e 'abcde')
        Note that empty strings are allowed.
        """
        assert self._peek == '"'
        start_row = self._row
        start_col = self._col
        self._readch()  # now we're at the first char in the str
        tmp = []
        while self._peek != '"':
            if self._peek == '':
                self.lex_err('Encountered EOF before string termination')
            if self._peek == '\n':
                self.lex_err('string literals can span only one line')
            tmp.append(self._peek)
            self._readch()
        self._readch()  # just consume the trailing "
        lexeme = ''.join(tmp)
        return Tokens.STR, start_row, start_col, lexeme

    def _tokenize_comment(self):
        """
        Tokenizes comments.

        We might need comments later if we wanna add debug symbols.
        Return:
            Token ID, row, col, the comment as a string
        """
        start_row = self._row
        start_col = self._col -1  # col is at the 2nd /
        self._readch()  # now we're past the //
        tmp = []
        while self._peek != '\n':
            tmp.append(self._peek)
            self._readch()
        lexeme = ''.join(tmp)
        return Tokens.CMNT, start_row, start_col, lexeme
    
    def _init_reserved(self):
        """
        Init the dic _res with the reserved keywords
        """
        self._res = {
            'void' : Tokens.VOID_T, 'int' : Tokens.INT_T,
            'char' : Tokens.CHAR_T, 'float' : Tokens.FLOAT_T,
            'auto' : Tokens.AUTO_T,
            'return' : Tokens.RET, 'sizeof' : Tokens.SIZEOF,
            'struct' : Tokens.STRUCT, 'union' : Tokens.UNION,
            'const' : Tokens.CONST, 'static' : Tokens.STATIC,
            'extern' : Tokens.EXTERN, 'if' : Tokens.IF,
            'else' : Tokens.ELSE, 'while' : Tokens.WHILE,
            'for' : Tokens.FOR, 'break' : Tokens.BREAK,
            'continue' : Tokens.CONT, 'in' : Tokens.IN
            }
        
    def _readch(self):
        """
        Reads the next character from the file into peek.

        It reads the next char from the file into peek and sets the values
        of the _col and _row to the col number and row number respectively of
        where the char was read
        """
        self._peek = self._file.read(1)
        if self._peek == '\n':
            self._col = -1
            self._row = self._row + 1
        else:
            self._col = self._col + 1
        
    def lex_err(self, err):
        """
        Prints err and exits program on code 2.

        Arguments:
            err: the err message to be printed
        """
        print('Lexical error - line: %d  col: %d' % (self._row, self._col))
        print(err)
        sys.exit(2)
        
def get_ascii_skip_val(char):
    """
    returns the ascii value of the skip character \char.

    Returns None if given a char that doesn't carry a special meaning if
    \ proceeds it such as g
    """
    assert len(char) == 1
    skip_char = {
        '0' : 0, 'a' : 7, 'b' : 8, 't' : 9, 'n' : 10, 'v' : 11, 'f' : 12,
        'r' : 13, '\\' : 28, "'" : 39
        }
    if char in skip_char:
        return skip_char[char]
    return None

def test_lex(path):
    """
    Runs the lexer on the file and prints out the results found
    
    Arguments:
        path: The file path to be tokenized
    """
    lex = Lexer(path)
    tok = lex.scan()
    print(type(tok))
    while tok is not None:
        if tok == -1:
            print("Error encountered")
            return
        elif tok[0] == Tokens.ID:
            s = '%s %d %d %s' % (Tokens.tok_to_str(tok[0]), tok[1],
                                tok[2], tok[3])
            print(s)
        elif tok[0] == Tokens.INT or tok[0] == Tokens.CHAR:
            s = '%s %d %d %d' % (Tokens.tok_to_str(tok[0]), tok[1],
                                tok[2], tok[3])
            print(s)
        elif tok[0] == Tokens.FLOAT:
            s = '%s %d %d %f' % (Tokens.tok_to_str(tok[0]), tok[1],
                                 tok[2], tok[3])
            print(s)
        elif tok[0] == Tokens.STR:
            s = '%s %d %d %s' % (Tokens.tok_to_str(tok[0]), tok[1],
                                 tok[2], tok[3])
            print(s)
        elif tok[0] == Tokens.CMNT:
            s = '%s %d %d %s' % (Tokens.tok_to_str(tok[0]), tok[1],
                                 tok[2], tok[3])
            print(s) 
        else: # reserved word
            s = '%s %d %d' % (Tokens.tok_to_str(tok[0]), tok[1], tok[2])
            print(s)
        tok = lex.scan()
