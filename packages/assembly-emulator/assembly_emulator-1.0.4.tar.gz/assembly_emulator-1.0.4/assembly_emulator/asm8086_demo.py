import math
import string
import sys
from pyfiglet import Figlet
import os

# TO DO LIST
"""

********************** URGENT **********************
1. ALLOW STRINGS ONLY INSIDE PARENTHESIS AND HANDLE EXCEPTIONS WHEN THE A WRONG STRING INPUT IS GIVEN.
2. SYNCHRONIZE 16 BIT REGISTER IN ALL OF THE METHODS
3. FIND OUT HOW TO REPRESENT NEGATIVE NUMBERS IN HEXADECIMAL BASE IN THE RIGHT WAY
4. IMPROVE FILE MODE AND ALLOW EXTRACTION OF CODE FROM CONSOLE MODE TO FILES
****************************************************
1. CHECK VALID FUNCTION IN THE FILE HANDLING AND TEXT EDITOR MODES
2. WORK ON SYNCHRONIZING BETWEEN THE 16 BIT REGISTERS AND THE 8 BITS REGISTER RESPECTIVELY ( AX = AH+AL)
3. IN HANDLE_COMMAND AND ASSIGN_VARIABLE : WHEN A VARIABLE IS A LIST - REFER TO HIM AS THE FIRST ONE .
4. LEARN HOW THE FLAG SYSTEM ACTUALLY WORKS SO I CAN USE CMP ..      UPDATE 7.09.20 : HALF DONE
5. PRINT MEMORY VALUES AS HEXADECIMAL ..
6.JMP SYSTEM : EXTEND AND ADD JMP COMMANDS  +  MAKE SURE IT WORKS ON FILE MODE 
7. OVERFLOW_CHECK() THAT RECEIVES THE DATA STRUCTURE IN A FORM OF A STR TYPE- DONE. IMPLEMENT IT IN THE PROGRAM 
8. CHECK REGISTER MATCH IN DIV,MUL ?
10.Fix analyze_errors() to match with emu8086
"""

# LISTS AND DICTIONARIES
commands = ['mov', 'xchg', 'add', 'sub', 'mul', 'div', 'lea', 'inc', 'dec', 'xor', 'or',
            'and', 'int', 'cmp', 'jmp', 'je', 'jne', 'jz', 'jnz', 'ja', 'jb', 'print', 'input', 'push', 'pop', 'pusha', 'popa', 'loop', 'proc','endp','call']
unary = ['inc', 'dec', 'int', 'div', 'mul', 'jmp','jmp', 'je', 'jne', 'jz', 'jnz', 'ja', 'jb', 'print', 'push', 'pop', 'loop', 'proc','call']
jmps = ['jmp', 'je', 'jne', 'jz', 'jnz', 'ja', 'jb', 'loop']
interrupts = ['21h', '16h', '10h']  # TO BE CONTINUED.
variable_declaration = ['db', 'dw', 'dd','dup']
lines = {}  # A list with commands with indices might be useful for JMP instructions. Perhaps It should be a dictionary, so that labels can be referenced..
special_commands = ['%finish', '%about', '%website', '%cmd', '%help']
ignore_code = 0 # If ignore_code equals 1 - then the code shall not be executed, only added to the list.
stack = []
procedures = {

}
register = {
    "al": 0,
    "ah": 0,
    'ax': 0,
    "bl": 0,
    "bh": 0,
    'bx': 0,
    "cl": 0,
    "ch": 0,
    'cx': 0,
    "dl": 0,
    "dh": 0,
    'dx': 0,
    "si": 0,
    "di": 0,
    "bp": 0,
    "sp": 0,
    "ds": 0,
    "cs": 0,
    "ss": 0,
    "ip": 0,
}
user_mode = 1  # 1 IS CONSOLE, 2 IS TEXT EDITOR, AND 3 IS FILE READING

variables = {
    'newvar': [0]
}

memory = {
    '100h': 0,
    '101h': 0,
}

flags = {
    "zf": 0,
    "cf": 0,
    "sf": 0,
    "of": 0,
    "af": 0,
    "if": 0,
    "df": 0.

}


def handle_command(command, operand1='0', operand2='0'):
    """ Receives a command and the operands , and returns the result"""
    register['ip'] += 3
    operand1 = clean_input(operand1)
    operand2 = clean_input(operand2)
    global ignore_code
    if ignore_code == 1:  # code inside a procedure ...
        if command == 'endp':  # IF YOU REACH THE END OF THE PROCEDURE, TURN THE EXECUTION ON ...
            ignore_code = 0

    elif command == 'mov':  # ******************************** MOV METHOD *************************************
        if operand2 == '0':
            flags['zf'] = 1
        if operand1 in register:  # FIRST IS REGISTER
            if operand2 in register:  # BOTH ARE REGISTERS
                if check_register_match(operand1, operand2):
                    register[operand1] = int(register[operand2])
                else:
                    print(f'(19) wrong parameters: MOV {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST IS REGISTER AND SECOND IS A VARIABLE
                register[operand1] = int(variables[operand2[0]])
            elif operand2 in memory:
                register[operand1] = int(memory[operand2])  # FIRST IS A REGISTER AND THE SECOND IS A MEMORY
            else:
                register[operand1] = int(operand2)  # FIRST IS REGISTER AND THE SECOND IS A NUMBER
            if operand1.endswith('x'):
                synchronize_8_bit(f'{operand1}')
            elif operand1.endswith('h') or operand1.endswith('l'):
                synchronize_16_bit(operand1,register[operand1])
        elif operand1 in variables:  # FIRST IS A VARIABLE
            if operand2 in register:  # FIRST IS A VARIABLE AND SECOND IS A REGISTER
                variables[operand1][0] = int(register[operand2])
            elif operand2 in variables:  # THE FIRST IS A VARIABLE AND THE SECOND IS A VARIABLE
                variables[operand1][0] = int(variables[operand2][0])
            elif operand2 in memory:  # FIRST IS A VARIABLE AND THE SECOND IS A MEMORY
                variables[operand1][0] = int(memory[operand2])
            else:
                variables[operand1][0] = int(operand2)  # THE FIRST IS A VARIABLE AND THE SECOND IS A NUMBER
        elif operand1 in memory:  # FIRST IS A MEMORY ADDRESS
            if operand2 in register:  # FIRST IS A MEMORY ADDRESS AND THE SECOND IS A REGISTER
                memory[operand1] = int(register[operand2])
            elif operand2 in variables:  # FIRST IS A MEMORY AND THE SECOND IS A VARIABLE
                memory[operand1] = int(variables[operand2][0])
            elif operand2 in memory:
                memory[operand1] = int(memory[operand2])
            else:
                memory[operand1] = int(operand2)  # FIRST IS A MEMORY AND THE SECOND IS A NUMBER
        else:
            return 'Something went wrong. Please re-check your input.'

    elif command == 'add':  # **************************** ADD METHOD **************************************
        #print(f'operand1 : {operand1}, operand2: {operand2}')
        if operand1 in register:  # FIRST IS REGISTER
            if operand2 in register:  # BOTH ARE REGISTERS
                if check_register_match(operand1, operand2):
                    register[operand1] += int(register[operand2])
                else:
                    print(f'(19) wrong parameters: ADD {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST IS REGISTER AND SECOND IS VARIABLE
                register[operand1] += int(variables[operand2][0])
            elif operand2 in memory:  # FIRST IN REGISTERS AND SECOND IN MEMORY
                register[operand1] += int(memory[operand2])
            else:
                register[operand1] += int(operand2)  # FIRST IS REGISTER AND SECOND IS NUMBER
            if operand1.endswith('x'):
                synchronize_8_bit(f'{operand1}')
            if operand1.endswith('h') or operand1.endswith('l'):
                synchronize_16_bit(operand1, register[operand1])
        elif operand1 in variables:  # FIRST IS A VARIABLE

            if operand2 in register:
                variables[operand1][0] += int(register[operand2])
            elif operand2 in variables:
                variables[operand1][0] += int(variables[operand2][0])
            elif operand2 in memory:
                variables[operand1][0] += int(memory[operand2])
            else:
                variables[operand1][0] += int(operand2)

        elif operand1 in memory:
            if operand2 in register:
                memory[operand1] += int(register[operand2])
            elif operand2 in variables:
                memory[operand1] += int(variables[operand2][0])
            elif operand2 in memory:
                memory[operand1] += int(memory[operand2])
            else:
                memory[operand1] += int(operand2)

    elif command == 'sub':  # ******************************  SUB METHOD ***********************************
        second = ' '
        if operand1 in register:  # FIRST: REGISTER
            if operand2 in register:  # BOTH REGISTERS
                if check_register_match(operand1, operand2):
                    change_flags(command, register[operand1], int(register[operand2]))
                    register[operand1] -= int(register[operand2])
                else:
                    print(f'(19) wrong parameters: SUB {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST: REGISTER,SECOND: VARIABLE
                register[operand1] -= int(variables[operand2][0])
            else:
                second = int(operand2)
                change_flags(command, register[operand1], second)
                register[operand1] -= second
            if operand1.endswith('x'): # SYNCHRONIZE THE 8 BITS REGISTER IF YOU CHANGE A 16 BITS REGISTER
                synchronize_8_bit(f'{operand1}')
            if operand1.endswith('h') or operand1.endswith('l'):  # SYNCHRONIZE THE 16 BIT REGISTER IF YOU CHANGE 8 BITS REGISTER
                synchronize_16_bit(operand1, register[operand1])
        elif operand1 in variables:  # FIRST : VARIABLE
            if operand2 in register:  # FIRST : VARIABLE , SECOND : REGISTER
                change_flags(command, variables[operand1][0], int(register[operand2]))
                variables[operand1][0] -= int(register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                change_flags(command, int(variables[operand1]), int(variables[operand2]))
                variables[operand1] -= int(variables[operand2])
            elif operand2 in memory:  # FIRST : VARIABLE , SECOND : MEMORY
                change_flags(command, variables[operand1], int(memory[operand2]))
                memory[operand1] -= int(memory[operand2])
            else:
                second = int(operand2)
                if variables[operand1] == second:
                    flags['zf'] = 1
                variables[operand1] -= second
        elif operand1 in memory:
            if operand2 in register:
                memory[operand1] -= int(register[operand2])
            elif operand2 in variables:
                memory[operand1] -= int(variables[operand2])
            else:
                second = int(operand2)
                if memory[operand1] == second:
                    flags['zf'] = 1
                memory[operand1] -= second

    elif command == 'xchg':  # ********************************* XCHG METHOD ******************************
        if operand1 in register:  # FIRST IS A REGISTER
            if operand2 in register:  # BOTH ARE REGISTERS
                if check_register_match(operand1, operand2):
                    register[operand1], register[operand2] = register[operand2], register[operand1]
                else:
                    print(f'(19) wrong parameters: XCHG {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST IS A REGISTER AND SECOND IS A VARIABLE
                register[operand1], variables[operand2] = variables[operand2], register[operand1]
            elif operand2 in memory:  # FIRST IS A REGISTER AND SECOND IS A MEMORY ADDRESS
                register[operand1], memory[operand2] = memory[operand2], register[operand1]
            else:
                print('Invalid operand for xchg')
            if operand1.endswith('x'):
                synchronize_8_bit(operand1)
            if operand2.endswith('x'):
                synchronize_8_bit(operand2)
            if operand1.endswith('l') or operand1.endswith('h'):
                synchronize_16_bit(operand1, register[operand1])
            if operand2.endswith('l') or operand1.endswith('h'):
                synchronize_16_bit(operand2, register[operand2])
        elif operand1 in variables:  # FIRST IS A VARIABLE
            if operand2 in register:  # FIRST IS A VARIABLE AND SECOND IS REGISTER
                variables[operand1], register[operand2] = register[operand2], variables[operand1]
            elif operand2 in variables:  # BOTH ARE VARIABLES
                variables[operand1], variables[operand2] = variables[operand2], variables[operand1]
            elif operand2 in memory:  # FIRST IS A VARIABLE AND SECOND IS MEMORY
                variables[operand1], memory[operand2] = memory[operand2], variables[operand1]
            else:
                print('Invalid operand for xchg')

        elif operand1 in memory:  # FIRST IS A MEMORY
            if operand2 in register:  # FIRST : MEMORY, SECOND: REGISTER
                memory[operand1], register[operand2] = register[operand2], memory[operand1]
            elif operand2 in variables:  # FIRST : MEMORY , SECOND : VARIABLE
                memory[operand1], variables[operand2] = variables[operand2], memory[operand1]
            elif operand2 in memory:  # BOTH ARE MEMORY
                memory[operand1], memory[operand2] = memory[operand2], memory[operand1]
    elif command == 'inc':  # ********************************  INC METHOD  *************************************
        if operand1 in register:
            register[operand1] += 1
            if operand1.endswith('x'):
                synchronize_8_bit(operand1)
            if operand1.endswith('l') or operand1.endswith('h'):
                synchronize_16_bit(operand1, register[operand1])
        elif operand1 in variables:
            variables[operand1] += 1
        elif operand1 in memory:
            memory[operand1] += 1
        else:
            print(f'INC METHOD ERROR . NOT FOU ND {operand1} ')
    elif command == 'dec':  # ********************************  DEC METHOD  **************************************
        if operand1 in register:  # DECREASE A REGISTER VALUE
            register[operand1] -= 1
            if operand1.endswith('x'):
                synchronize_8_bit(f'{operand1}')
        elif operand1 in variables: # DECREASE A VARIABLE VALUE
            variables[operand1] -= 1
        elif operand1 in memory:  # DECRAEASE A MEMORY VALUE
            memory[operand1] -= 1
        else:
            print(f'(19) wrong parameters: DEC {operand1} ')
    elif command == 'xor':  # ********************************  XOR METHOD ******************************************
        if operand1 == operand2:
            flags['zf'] = 1
        if operand1 in register:  # FIRST: REGISTER
            if operand2 in register:  # BOTH REGISTER
                if check_register_match(operand1, operand2):  # if they have the same number of bits, proceed
                    register[operand1] ^= int(register[operand2])
                else:
                    print(f'(19) wrong parameters: XOR {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST : REGISTER, SECOND: VARIABLE
                register[operand1] ^= int(variables[operand2][0])
            elif operand2 in memory:
                register[operand1] ^= int(memory[operand2])  # FIRST : REGISTER, SECOND : MEMORY
            else:
                register[operand1] ^= int(operand2)  # FIRST : REGISTER, SECOND : NUMBER
            if operand1.endswith('x'):
                synchronize_8_bit(operand1)
            elif operand1.endswith('l') or operand1.endswith('h'):
                synchronize_16_bit(operand1,register[operand1])
        elif operand1 in variables:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST: REGISTER, SECOND :VARIABLE
                variables[operand1][0] ^= int(register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                variables[operand1][0] ^= int(variables[operand2][0])
            elif operand2 in memory:
                variables[operand1][0] ^= int(memory[operand2])  # FIRST:VARIABLE, SECOND : MEMORY
            else:
                variables[operand1][0] ^= int(operand2)  # FIRST : VARIABLE, SECOND : NUMBER

        elif operand1 in memory:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST : MEMORY , SECOND : REGISTER
                memory[operand1] ^= int(register[operand2])
            elif operand2 in variables:  # FIRST: MEMORY, SECOND : VARIABLE
                memory[operand1] ^= int(variables[operand2][0])
            elif operand2 in memory:  # BOTH MEMORY
                memory[operand1] ^= int(memory[operand2])
            else:  # FIRST: MEMORY, SECOND : NUMBER
                memory[operand1] ^= int(operand2)
    elif command == 'or':  # ********************************  OR METHOD ******************************************
        result = -1
        if operand1 in register:  # FIRST: REGISTER
            if operand2 in register:  # BOTH REGISTER
                if check_register_match(operand1,operand2):  # if they have the same number of bits, proceed
                    register[operand1] |= int(register[operand2])
                else:
                    print(f'(19) wrong parameters: OR {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST : REGISTER, SECOND: VARIABLE
                register[operand1] |= int(variables[operand2])
            elif operand2 in memory:
                register[operand1] |= int(memory[operand2])  # FIRST : REGISTER, SECOND : MEMORY
            else:
                register[operand1] |= int(operand2)  # FIRST : REGISTER , SECOND : NUMBER
            if operand1.endswith('x'):
                synchronize_8_bit(operand1)
            elif operand1.endswith('l') or operand1.endswith('h'):
                synchronize_16_bit(operand1, register[operand1])
        elif operand1 in variables:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST: REGISTER, SECOND :VARIABLE
                variables[operand1] |= int(register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                variables[operand1] |= int(variables[operand2])
            elif operand2 in memory:
                variables[operand1] |= int(memory[operand2])  # FIRST:VARIABLE, SECOND : MEMORY
            else:
                variables[operand1] |= int(operand2)  # FIRST : VARIABLE, SECOND : NUMBER

        elif operand1 in memory:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST : MEMORY , SECOND : REGISTER
                memory[operand1] |= int(register[operand2])
            elif operand2 in variables:  # FIRST: MEMORY, SECOND : VARIABLE
                memory[operand1] |= int(variables[operand2])
            elif operand2 in memory:  # BOTH MEMORY
                memory[operand1] |= int(memory[operand2])
            else:  # FIRST: MEMORY, SECOND : NUMBER
                memory[operand1] |= int(operand2)

    elif command == 'and':  # ********************************  AND METHOD ******************************************

        if operand1 in register:  # FIRST: REGISTER
            if operand2 in register:  # BOTH REGISTER
                if check_register_match(operand1, operand2):
                    register[operand1] &= int(register[operand2])
                else:
                    print(f'(19) wrong parameters: AND {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST : REGISTER, SECOND: VARIABLE
                register[operand1] &= int(variables[operand2])
            elif operand2 in memory:
                register[operand1] &= int(memory[operand2])  # FIRST : REGISTER, SECOND : MEMORY
            else:
                register[operand1] &= int(operand2)  # FIRST : REGISTER, SECOND : NUMBER

        elif operand1 in variables:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST: REGISTER, SECOND :VARIABLE
                variables[operand1] &= int(register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                variables[operand1] &= int(variables[operand2])
            elif operand2 in memory:
                variables[operand1] &= int(memory[operand2])  # FIRST:VARIABLE, SECOND : MEMORY
            else:
                variables[operand1] &= int(operand2)  # FIRST : VARIABLE, SECOND : NUMBER

        elif operand1 in memory:  # FIRST : VARIABLE:
            if operand2 in register:  # FIRST : MEMORY , SECOND : REGISTER
                memory[operand1] &= int(register[operand2])
            elif operand2 in variables:  # FIRST: MEMORY, SECOND : VARIABLE
                memory[operand1] &= int(variables[operand2])
            elif operand2 in memory:  # BOTH MEMORY
                memory[operand1] &= int(memory[operand2])
            else:  # FIRST: MEMORY, SECOND : NUMBER
                memory[operand1] &= int(operand2)

    elif command == 'div':  # ***********************************  DIV METHOD  ****************************************
        second = -1
        if operand1 in register:
            second = register[operand1]
        elif operand1 in variables:
            second = variables[operand1][0]
        elif operand1 in memory:
            second = memory[operand1]
        else:
            print('not found')
            return -1
        if second == 0:
            print(' divide error - overflow.')
            return -1
        if register['ax'] == 0:
            flags['zf'] = 1
        register['ax'] //= second
        synchronize_8_bit('ax')
    elif command == 'mul':  # ***********************************  MUL METHOD  ****************************************
        second = -1
        if operand1 in register:
            second = register[operand1]
        elif operand1 in variables:
            second = variables[operand1][0]
        elif operand1 in memory:
            second = memory[operand1]
        else:
            print('not found')
            return -1
        if register['ax'] == 0 or second == 0:
            flags['zf'] = 1
        register['ax'] *= second
        synchronize_8_bit('ax')

    elif command == 'int':  # ************************************ INTERRUPTS  ****************************************
        if operand1 == '21h':
            if register['ah'] == 9:
                try:
                    value = get_value_from_offset(register['dl'])  # DO IT FOR DL OR DX ????
                    print(value)  # Needs to be converted to ascii. chr() method not working ...
                except TypeError:
                    print('Type Error occurred..')
                except IndexError:
                    print('Invalid Syntax')
                except KeyError:
                    print('A key error has occurred for some reason')
            elif register['ah'] == 2:
                print(chr(register['dl']))
            if register['ah'] == 1:
                received_char = input(' ')
                if len(received_char) != 1:
                    return -1
                else:
                    register['al'] = ord(received_char)
            elif register['ah'] == 76:  # Should be 4CH
                print("exit the program was executed")
            else:
                pass
    elif command == 'lea':  # ***********************************  LEA & OFFSET ****************************************
        offset, sub = get_offset(operand2)
        if offset < 0 or sub < 0 or sub > offset:
            print(f'INDEX ERROR OF OFFSET {offset}')
        else:
            # offset -= sub
            if operand1 in register:
                register[operand1] = offset
                if operand1.endswith('h') or operand1.endswith('l'):
                    synchronize_16_bit(operand1,register[operand1])
                    pass
                    pass
                elif 'a' <= operand1[0] <= 'd':
                    synchronize_8_bit(operand1)
            elif operand2 in variables:
                variables[operand1] = offset
            elif operand2 in memory:
                memory[operand1] = offset
            else:
                print('first operand invalid')
    elif command == 'cmp':  # ***********************************  CMP COMMAND  ****************************************

        if operand1 in register:  # FIRST : REGISTER
            if operand2 in register:  # BOTH REGISTER
                if check_register_match(operand1, operand2):
                    change_flags('sub', register[operand1], register[operand2])
                else:
                    print(f'(19) wrong parameters: CMP {operand1},{operand2}')
                    print(f'>>> (19) operands do not match: 16 bit and 8 bit register ')
            elif operand2 in variables:  # FIRST: REGISTER, SECOND: VARIABLE
                change_flags('sub', register[operand1], variables[operand2])
            elif operand2 in memory:
                change_flags('sub', register[operand1], memory[operand2])  # FIRST : REGISTER, SECOND: MEMORY
            else:
                change_flags('sub', register[operand1], int(operand2))  # FIRST: REGISTER, SECOND: NUMBER
        elif operand1 in variables:  # FIRST : VARIABLES
            if operand2 in register:  # FIRST : VARIABLE, SECOND: REGISTER
                change_flags('sub', variables[operand1], register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                change_flags('sub', variables[operand1], variables[operand2])
            elif operand2 in memory:
                change_flags('sub', variables[operand1], memory[operand2])
            else:
                change_flags('sub', variables[operand1], int(operand2))

        elif operand1 in memory:
            if operand2 in register:  # FIRST : VARIABLE, SECOND: REGISTER
                change_flags('sub', memory[operand1], register[operand2])
            elif operand2 in variables:  # BOTH VARIABLES
                change_flags('sub', memory[operand1], variables[operand2])
            elif operand2 in memory:
                change_flags('sub', memory[operand1], memory[operand2])
            else:
                change_flags('sub', memory[operand1], int(operand2))

        else:
            print(f'{operand1} must be a register, a variable or a memory address ')
            return -1
    elif command == 'jmp':  # ***********************************   JMP METHOD  ***************************************
        operand1 = clean_input(operand1) # OPERAND1 SHOULD BE THE NAME OF THE LABEL
        if not operand1.endswith(':'):
            operand1 += ':'
        try:
            index = 0
            operand1 = clean_input(operand1)
            for value in lines:
                if lines[value] == operand1:
                    # print('equal')
                    return index
                index += 1

            print('Not found!')
        except Exception as e:
            print(e.__class__)
    elif command == 'je' or command == 'jz':  # ********************************  JE & JZ  *****************************
        if flags['zf'] == 1:  # OPERAND1 SHOULD BE THE NAME OF THE LABEL
            operand1 = clean_input(operand1)
            if not operand1.endswith(':'):
                operand1 += ':'
            try:
                index = 0
                operand1 = clean_input(operand1)
                for value in lines:
                    if lines[value] == operand1:
                        return index
                    index += 1

                print('Not found!')
            except Exception as e:
                print(e.__class__)
                return -1
        else:
            return -1
    elif command == 'jne' or command == 'jnz':  # ******************************  JNE & JNZ ****************************
        if flags['zf'] == 0:  # OPERAND1 SHOULD BE THE NAME OF THE LABEL
            operand1 = clean_input(operand1)
            if not operand1.endswith(':'):
                operand1 += ':'
            try:
                index = 0
                operand1 = clean_input(operand1)
                for value in lines:
                    if lines[value] == operand1:
                        print('equal')
                        return index
                    index += 1

                print('Not found!')
            except Exception as e:
                print(e.__class__)
                return -1
        else:
            return -1

    elif command == 'ja':  # ************************************** JA COMMAND ****************************************
        if flags['sf'] == 0 and flags['zf'] == 0:  # EXAMPLE : 5-3 = 2 ; SIGNED FLAG = 0, ZERO FLAG = 0
            operand1 = clean_input(operand1)
            if not operand1.endswith(':'):
                operand1 += ':'
            try:
                index = 0
                operand1 = clean_input(operand1)
                for value in lines:
                    # lines[value] = clean_input(lines[value])
                    # print(f'value:  {lines[value]} , operand1: {operand1}')
                    # print(f'JE METHOD SAYS : \n operand1: {operand1} value: {lines[value]}')
                    if lines[value] == operand1:
                        #  print('equal')
                        return index
                    index += 1

                print('Not found!')
            except Exception as e:
                print(e.__class__)
                return -1
        else:
            return -1
    elif command == 'loop':  # ******************************* LOOP ***************************************************
        operand1 = clean_input(operand1)
        register['cx'] -= 1
        if register['cx'] > 0:
            if not operand1.endswith(':'):
                operand1 += ':'
            try:
                index = 0
                for value in lines:
                    # lines[value] = clean_input(lines[value])
                    # print(f'value:  {lines[value]} , operand1: {operand1}')
                    # print(f'JE METHOD SAYS : \n operand1: {operand1} value: {lines[value]}')
                    if lines[value] == operand1:
                        #  print('equal')
                        return index
                    index += 1

                print('Not found!')
            except Exception as e:
                print(e.__class__)
                return -1
        else:
            return -1

    elif command == 'push':  # *******************************************  PUSH  **************************************
        result = 0
        if operand1 in register:
            if operand1.endswith('l') or operand1.endswith('h'):
                print(f'(19) Wrong parameters: PUSH {operand1}')
            else:
                result = register[operand1]
                stack.append(result)
        elif operand1 in variables:
            result = variables[operand1][0]
            stack.append(result)
        elif operand1 in memory:
            result = memory[operand1]
            stack.append(result)
        else:
            if only_numbers(operand1):
                result = int(operand1)
                if -65536 < result < 65536:  # VALID 16 BIT VALUE
                    stack.append(result)
                else:
                    print(f'(19) overflow! - cannot be evaluated: push {operand1}')
            else:
                print(f'(19) wrong parameters: PUSH  {operand1}')

    elif command == 'pop':  # *****************************************  POP  ****************************************
        if len(stack) == 0:
            print('Stack is empty!')
        else:
            popped = stack.pop(len(stack)-1)  # FOR EXAMPLE : POP AX - > POPPED = AX - >  CHANGE AX
            if operand1 in register:
                if operand1.endswith('l') or operand1.endswith('h'):
                    print(f'(19) Wrong parameters: PUSH {operand1}')
                else:
                    register[operand1] = popped
                    if operand1.endswith('x'):  # synchronize it in case it is ax, bx, cx, dx
                        synchronize_8_bit(operand1)

            elif operand1 in variables:
                variables[operand1][0] = popped
            elif operand1 in memory:
                memory[operand1] = popped
            else:
                print(f'(19) Wrong parameters: POP {operand1}')

    elif command == 'pusha':  # ************************************** PUSHA ******************************************
        for key in register:
            stack.append(register[key])
    elif command == 'popa':
        for key in register:
            if len(stack) == 0:
                break
            register[key] = stack.pop(0)
    elif command == 'proc':  # ************************************* PROC *********************************************
        index = 0
        found = False
        if len(lines) == 0:
            index = 0
        else:
            for line in lines:
                if lines[line] == 'proc {}'.format(operand1):
                    break
                index += 1

        procedures[index] = operand1

        ignore_code = 1
    elif command == 'endp':  # ************************************* ENDP *********************************************
        ignore_code = 0
    elif command == 'call':
        current_index = len(lines)-1
        start_index = -1
        for routine_index in procedures:
            if procedures[routine_index] == operand1:
                start_index = routine_index
                break
        if start_index == -1:
            print(f'Procedure {operand1} not found')
        else:
            ignore_code = 0
            index = 0
            for line in lines:
                if lines[line] == 'endp':
                    print('reached the end of the procedure')
                    break
                elif index > start_index:
                    # print(f'executing {lines[line]}')
                    cmd,op1,op2 = extract_command(lines[line])
                    handle_command(cmd,op1,op2)
                index += 1

    elif command == 'print':  # ********************************* PRINT MACRO ******************************************
        if user_mode == 1:  # IF THE MODE IS CONSOLE
            # print('got here')
            handle_wrapper_for_console('mov ah,9')
            variable_wrapper(f'tempvar db {operand1}')
            handle_wrapper_for_console('mov dl, offset tempvar')
            handle_wrapper_for_console('int 21h')
            del variables['tempvar']  # DELETING THE TEMPORARY VARIABLE...
            # ADD THESE 3 COMMANDS TO THE LINES LIST?
            # DO VERSIONS FOR TEXT EDITOR MODE , ETC ..
    elif command == 'input':  # *******************************  INPUT MACRO *******************************************
        if user_mode == 1:  # IF THE MODE IS CONSOLE
            handle_wrapper_for_console('mov ah,1h')
            handle_wrapper_for_console('int 21h')


def check_data_overflow(item, structure):
    """ Returns True if there's an overflow , otherwise returns False """
    if structure == 'register':
        if item.endwith('l'):
            if register[item] > 255 or register[item] < -255:  # If the register is 8 bit
                return True
        else:
            if register[item] > 65535 or register[item] < -65535:  # If the register is 16 bit
                return True
    elif structure == 'variables':
        # Somehow extract the data ( dd or db ). Perhaps use object oriented programming to represent data structures?
        pass
    elif structure == 'memory':
        if memory[item] > 255 or memory[item] < -255:  # Memory is referred as a byte
            return True

    return False


def check_register_match(register1, register2):
    """  You can perform actions only on registers with the same number of bits . For example : mov ax,dl will be invalid in assembly language ."""
    register1 = clean_input(register1)
    register2 = clean_input(register2)
    if register1.endswith('x') and not register2.endswith('x'):
        return False
    elif not register1.endswith('x') and register2.endswith('x'):
        return False
    return True


# ****************************   TO DO!!!  **************************************

def restart_flags():
    """ restarts all the flags each command ."""
    for i in flags:
        flags[i] = 0


def change_flags(command, one, two):
    """ compares two values to know which flag to turn"""
    if command == 'sub':
        if one == two:
            flags['zf'] = 1
        elif one < two:
            flags['cf'] = 1  # I think so..
            flags['sf'] = 1
        else:
            flags['sf'] = 0
            flags['zf'] = 0
            flags['cf'] = 0
    elif command == 'add':
        if one + two == 0:
            flags['zf'] = 1
        else:
            flags['zf'] = 1
    elif command == 'mov':
        if two == 0:
            flags['zf'] = 1
        else:
            flags['zf'] = 0
    elif command == 'xor':
        if one == two:
            flags['zf'] = 1
        else:
            flags['zf'] = 0
    elif command == 'or':
        if one | two == 0:
            flags['zf'] = 1
        else:
            flags['cf'] = 0
    elif command == 'and':
        if one & two == 0:
            flags['zf'] = 1
        else:
            flags['cf'] = 0


def synchronize_8_bit(big_register):
    """RECEIVES A 16 REGISTER NAME - IF IT IS AX,BX,CX,DX - SYNCHRONIZES THE OTHERS."""
    value = register[big_register]
    value = hex(value)
    if value[0] == '-':
        value = value[1:]
    value = value[2:]
    higher_nibble = value[:len(value)-2]
    lower_nibble = value[len(value)-2:]
    if 'a' <= big_register[0] <= 'd':  # CHECK ANOTHER TIME THAT THE REGISTERS ARE ACTUALLY VALID JUST IN CASE
        high_register = big_register[:-1]+'h'
        low_register = big_register[:-1]+'l'
        register[high_register] = convert_to_decimal('0' + higher_nibble + 'h')
        register[low_register] = convert_to_decimal('0' + lower_nibble + 'h')


def synchronize_16_bit(small_register, data=''):
    """ RECEIVES A 8 BIT NAME ( AL, BL, CL, DL ) """
    value = register[small_register]
    value = hex(value)
    # print(value)
    if value[0] == '-':
        value = value[1:]
    value = value[2:]
    big_register = small_register[:-1]+'x'
    if big_register not in register:
        print('Register was not found')
    else:
        value = hex(register[big_register])
        value = value[value.find('x')+1:]
        if -256 < register[big_register] < 256:
            lower_nibble = value[:1] + value[2:]
            higher_nibble = '00'
            # print(f'lower nibble is {lower_nibble}')
        else:
            higher_nibble = value[:len(value) - 2]
            lower_nibble = value[len(value) - 2:]
            # print(f'higher nibble is {higher_nibble} and lower nibble is {lower_nibble}')

        if small_register.endswith('h'):
            higher_nibble = hex(data)[2:]
            print(higher_nibble)
            register[big_register] = convert_to_decimal( higher_nibble + '0'+lower_nibble + 'h')
        elif small_register.endswith('l'):
            lower_nibble = hex(data)[2:]
            register[big_register] = convert_to_decimal(higher_nibble + '0' + lower_nibble + 'h')


def extract_command(inserted):
    # print('got here')
    """ Extracts the command from the given string. Returns True/False """
    inserted = inserted.strip().lower()
    command = inserted[0:(inserted.find(' '))]
    # print(command)
    if inserted == 'pusha' or inserted == 'input' or inserted == 'popa' or inserted == 'endp' or inserted == 'endm':
        # AL AND 0 ARE JUST DEFAULT VALUES TO PREVENT VALID FUNCTIONS TO CAUSE ERRORS
        return inserted, 'al', '0'
    if command not in unary:
        operand1 = inserted[inserted.find(' '):inserted.find(',')]
        operand1 = clean_input(operand1)
        if operand1.startswith('[') and operand1.endswith(']'):
            operand1 = operand1[1:len(operand1) - 1]
        if operand1 not in memory and operand1 + 'h' in memory:
            operand1 = operand1 + 'h'
        operand2 = inserted[inserted.find(',') + 1:]
        operand2 = operand2.strip()
        if check_empty_line(operand2):  # IF THE FIRST IS EMPTY , IGNORE
            return command, operand1, ' '
        else:
            if operand2 in register:
                return command,operand1,operand2
            if operand2[-1] == 'h':
                try:
                    operand2 = convert_to_decimal(operand2)
                    operand2 = str(operand2)
                except Exception as e:
                    print(f'Error code: {e.__class__}')

            if operand2.startswith('offset'):
                command = 'lea'
                operand2 = inserted[inserted.rfind(' '):]
                operand2 = clean_input(operand2)

                return command, operand1, operand2
                #  OPERAND 2 = GET_OFFSET(OPERAND2[OPERAND2.RFIND(''):] = > RETURNS THE MEMORY LOCATION
            if operand2.startswith('[') and operand2.endswith(']'):  # [100] -> 100 -> 100h => valid
                operand2 = operand2[1:len(operand2) - 1]
            if operand2 not in memory and operand2 + 'h' in memory:
                operand2 = operand2 + 'h'
        # print(operand2)
        #  print(command, ' , ', operand1, ' , ', operand2)
            """
            if operand2[0] == "'" and operand2[2] == "'":  # ALLOWS THIS FEATURE: E.G : MOV AX, 'F' - > 97 ( 61h) in ascii
                if len(operand2) == 3:
                    operand2 = str(ord(operand2[1]))
                else:
                    print('syntax error ...')
                    return -1
            """

            if operand2[0] == '"' and operand2[len(operand2)-1] == '"' or ( operand2[0]=="'" and operand2[len(operand2)-1] == "'"):
                if operand1 in register: # A REGISTER..
                    if operand1.endswith('l') or operand1.endswith('h'):  # 8 BITS REGISTERS
                        if len(operand2) < 3:  # THE LENGTH MUST BE 1 - BECAUSE 1 LETTER = 8 BITS. EACH LETTER IS 4.
                            print(f'(19) cannot convert  to 8 bit value: {operand2}')
                            return "", "", ""
                        elif len(operand2) > 3: # THE LENGTH MUST BE 1 - BECAUSE 1 LETTER = 8 BITS. EACH LETTER IS 4.
                            print(f'(19) wrong parameters: {inserted} ')
                            print(f'operands do not match: second operand is over 8 bits!')
                        else:
                            operand2 = str(ord(operand2[1]))
                    else:  # 16 BITS REGISTERS
                        if len(operand2) < 3:  # must be at least one letter
                            print(f'(19) cannot convert  to 16 bit value: {operand2}')
                            return "", "", ""
                        elif len(operand2) > 4:
                            print(f'(19) cannot convert  to 16 bit value: {operand2}')
                            return "", "", ""
                        else:
                            operand2 = operand2[1:len(operand2)-1]
                            temp = ""
                            for letter in operand2:
                                temp += str(ord(letter))
                            operand2 = temp
                elif operand1 in variables:
                    operand2 = operand2[1:len(operand2) - 1]
            return command, operand1, operand2
    else:
        # EXTRACT THE UNARY COMMAND , AND THE SINGLE OPERAND
        operand1 = inserted[inserted.rfind(' '):]
        operand1 = clean_input(operand1)
        if operand1.startswith('[') and operand1.endswith(']'):
            operand1 = operand1[1:len(operand1) - 1]
        if operand1 not in memory and operand1 + 'h' in memory:  # TRY ADDING IT H AS FOR HEXADECIMAL
            operand1 = operand1 + 'h'
        return command, operand1, '0'


def get_offset(value):
    """ Receives a data type and checks where it belongs. then returns the offset from the specified dictionary """
    value = clean_input(value)
    index = 0
    location = 'u'  # unknown location. we don't know yet if the offset is for a register or a variable or even memory
    if value in register:  # if it is a register
        # print('register found !!')
        for cell in register:
            # print(str(index)+ ' is the index ')
            if value == cell:  # When there's a match between a register and the value, return the index of the register
                location = 'r'
                return index, 0
            index += 1  # Increment the index , because the index is actually the offset we're looking for ...
        return -1  # If somehow the value is a register but it cannot be found, it'll reach here and return -1. UNLIKELY

    elif value in variables:  # if it is a variable
        for cell in variables:
            if value == cell:  # When there's a match between a variable and the value, return the index of the variable
                location = 'v'
                return index + 1000, 1000  # CLASSIFICATION: 0-999 - REGISTERS, 1000-1999- VARIABLES , 3000-3999 MEMORY
            index += 1  # Increment the index , because the index is actually the offset we're looking for ...
        return -1  # If somehow the value is a variable but it cannot be found, it'll reach here and return -1. UNLIKELY

    elif value in memory:  # if it is a memory value
        for cell in memory:
            if value == cell:  # When there's a match between a memory and the value, return the index of the memory
                location = 'm'
                return index + 2000, 2000  # CLASSIFICATION: 0-999 - REGISTERS, 1000-1999- VARIABLES , 3000-3999 MEMORY
            index += 1  # Increment the index , because the index is actually the offset we're looking for ...
        return -1  # If somehow the value is a variable but it cannot be found, it'll reach here and return -1. UNLIKELY
    else:
        return -5  # COULDN'T RELATE THE VALUE TO ANYTHING ... NOT A REGISTER , NOR VARIABLE , NOR A MEMORY ADDRESS.


def get_value_from_offset(offset):  # To be used in the handle_command method , in interrupts mainly. *** TO BE DONE ***
    """ Gets the value from the offset """
    if 0 < offset < 1000:
        found_cell = find_from_index(register, offset)  # for example 'ax'
        return register[found_cell]
    elif 1000 <= offset < 2000:
        offset -= 1000
        found_cell = find_from_index(variables, offset)
        return variables[found_cell][0]
    elif 2000 <= offset < 3000:
        offset -= 2000
        found_cell = find_from_index(memory, offset)
        return memory[found_cell]
    else:
        return -1


def find_from_index(structure, offset):
    """ returns the value from a structure given an index ( offset )"""
    index = 0
    for cell in structure:
        if index == offset:
            return cell  # FOUND : RETURN THE GODAMN VALUE
        index += 1
    return -1  # NOT FOUND


def convert_to_decimal(value):  # TO ADD OPTIONS OF BINARY TO DECIMAL TOO. And to add it in other methods .
    """ Converts from Hexadecimal Base to Decimal Base. """
    if value.endswith('h'):  # If it ends with 'h' convert to hexadecimal counting base
        value = '0x' + str(value)[:-1]
        value = int(value, 0)
        return value


def first_is_valid(inserted):
    """ Checks if the given input is valid . Returns True / False """
    if check_empty_line(inserted):
        return True
    for char in inserted:
        if char not in string.ascii_letters and char not in string.punctuation and char not in string.digits and char!= ' ':
            return False
    return True


def get_number_of_repeats(inserted, character):
    """ Receives a string and a character and returns how many times does the char appear in the string . """
    inserted = clean_input(inserted)
    counter = 0
    for char in inserted:
        if char == character:
            counter += 1
    return counter


def second_is_valid(command, operand1, operand2):
    """add a limit to the numbers according to bytes ??  """
    if check_empty_line(command) and check_empty_line(operand1) and check_empty_line(operand2):  # IF IT IS EMPTY
        return True

    if command not in commands:  # check the commands , RETURN FALSE IF IT'S NOT FOUND
        # print('not in commands ')
        return False

    operand1 = clean_input(operand1)
    if command != 'int' and command not in jmps and command not in unary:  # DEAL WITH NORMAL COMMANDS
        if operand1 not in register and operand1 not in variables and operand1 not in memory:
            return False
        if check_empty_line(operand2):
            return False
        operand2 = clean_input(operand2)
        if operand2 in register or operand2 in variables or operand2 in memory:
            return True

        for char in operand2:
            if char not in string.digits and char != ' ' and char != '-' and char not in string.ascii_letters:
                return False
        return True
    else:
        #HANDLE INTERRUPTS AND JMPS
        # PERHAPS DO A SPECIAL CHECK TO INTERRUPTS BECAUSE IT HAS H -E.G 21H, OR MODIFY IT SO CONVERSION WORKS FOR ALL
        # IN A THE EXTRACT METHOD . CAUTION NEEDED SINCE IT TENDS TO MESS WITH THINGS IN DIFFERENT PART OF THE CODE
        return True


def clean_input(inserted):
    """ Turns to lower, Trims from both sides the spaces"""
    return inserted.lower().strip()


def print_info():
    """ prints the current data about the registers in conversion to hexadecomal counting base at every line"""
    print('REGISTERS : ', end=' ')
    temp_dict = {}
    for reg in register:
        converted = hex(register[reg])
        add_in_start = ''
        if converted.startswith('-'):
            add_in_start = '-'
            converted = converted[:2] + converted[3:]
        converted = converted[2:]
        converted = add_in_start + '0' + converted + 'h'
        temp_dict[reg] = converted

    print(temp_dict)
    print('>>> MEMORY :  ' + str(memory))
    print('VARIABLES : ', end=' ')
    temp_dict.clear()
    for var in variables:
        for value in variables[var]:
            try:
                converted = hex(value)
                add_in_start = ''
                if converted.startswith('-'):
                    add_in_start = '-'
                    converted = converted[:2] + converted[3:]
                converted = converted[2:]
                converted = add_in_start + '0' + converted + 'h'
            except TypeError as tp:
                pass
            temp_dict[var] = value
    print(temp_dict)
    print('>>> Flags : ' + str(flags))
    print(f'''>>> code: {lines}''')
    print(f'Stack :{stack}')
    print(f'Procedures: {procedures}')


def determine_input_type(inserted):
    """determines if it is a command, an assignment of a variable , or an assignment of a label"""
    inserted = clean_input(inserted)
    words = extract_words(inserted)
    # print(words)
    for word1 in words:
        if word1 in commands:
            return 1  # 1 MEANS IT IS A COMMAND

    for word1 in words:
        if word1 in variable_declaration:
            return 0  # 0 MEANS IT IS A DECLARATION

    if len(words) == 1 and ':' in words[0]:
        return -1  # -1 MEANS THIS IS A LABEL DECLARATION
    else:
        return -2  # -2 MEANS A TOTAL ERROR!


def extract_words(inserted):
    """ accepts a string value and returns a list with all the words. delimiter : ' ' , ', ' ......................."""
    inserted = clean_input(inserted)
    words = []
    collector = ""
    index = 0
    inserted = inserted + ' '
    for char in inserted:
        if (char == ' ' or char == ',') and collector != '' and collector != ' ':
            collector = collector.strip()
            words.append(collector)
            collector = ''
        else:
            collector += char

    return words


def check_empty_line(line):
    for char in line:
        if char != ' ':
            return False
    return True


def handle_wrapper(command):
    """ A method that handles all of the  processing: INPUT CHECK 1, INPUT CHECK 2 , HANDLE_COMMAND(), ETC FOR COMMANDS ."""
    if first_is_valid(command) and get_number_of_repeats(command, ',') <= 1:
        # print('valid1')
        real_cmnd, operand1, operand2 = extract_command(command)
        # print(operand2)
        if second_is_valid(real_cmnd, operand1, operand2):
            handle_command(real_cmnd, operand1, operand2)

            return 1
        else:
            return -1
    return 0


def handle_wrapper_for_console(command):
    """ A method that handles all of the  processing: INPUT CHECK 1, INPUT CHECK 2 , HANDLE_COMMAND(), ETC FOR COMMANDS ."""
    if first_is_valid(command) and get_number_of_repeats(command, ',') <= 1:
        # print('valid1')
        real_cmnd, operand1, operand2 = extract_command(command)
        # print(operand2)
        if second_is_valid(real_cmnd, operand1, operand2):
            if real_cmnd == 'jmp':
                index = handle_command(real_cmnd, operand1, operand2)
                return 1, index
            handle_command(real_cmnd, operand1, operand2)
            return 1, -1
        else:
            return -1, -1
    return 0, -1


def handle_wrapper_for_files(command):
    """ A method that handles all of the  processing: INPUT CHECK 1, INPUT CHECK 2 , HANDLE_COMMAND(), ETC FOR COMMANDS ."""
    if first_is_valid(command) or True:
        # print('valid1')
        real_cmnd, operand1, operand2 = extract_command(command)
        # print(real_cmnd,operand1,operand2)
        if second_is_valid(real_cmnd, operand1, operand2):
            # print('valid2')
            handle_command(real_cmnd, operand1, operand2)
            return 1
        else:
            return -1
    return 0


# ***************************** TO BE DONE **************************************************************


def only_numbers(value):
    """ checks if a string value is constructed only from digits """
    for char in value:
        if char not in string.digits:
            return False
    return True


def assembly_string(value):
    """ Checks if a string value is constructed only from English letters """
    dollar = value.rfind('$')
    if dollar == -1:
        return False

    for index in range(dollar):
        if value[index] not in string.ascii_letters and value[index] != '$' and value[index] != ' ' and value[
            index] not in string.digits:
            return False

    if value.rfind('$') != len(value) - 1:
        after_space = value[value.rfind('$') + 1:]
        if not check_empty_line(after_space):
            return False
    return True


def valid_value(value):
    if only_numbers(value) or assembly_string(value):
        return True
    return False


def valid_variable_declaration(declaration):  # ADD A CHECK FOR AN ARRAY VARIABLE
    """ checks if the variable declaration is valid , (len = 3 first of all ) """
    # print(declaration)
    words = extract_words(declaration)
    # print(words)
    try:
        if words[1] not in variable_declaration:  # words[1] should be the size of the variable; db,dw or dd
            return False
    except IndexError:
        print('Out of range exception !')
        return False
    except TypeError:
        print('Wrong type ..')
    return True


def extract_from_variable(inserted):
    """ extracts the name and values from the variable declaration """
    values = extract_words(inserted)
    return values[0], values[2:]


def convert_to_ascii(values):
    """ turns things to ascii if it's not a number"""
    for value in values:
        if not isinstance(value, int):
            for char in value:
                char = ord(char)
    return values


def assign_variable(name, value):
    """adds a new value to the variable dictionary structure"""

    if name in variables:
        print(f'Variable {name} already exists')
    elif name in register:
        print(f'Variable name cannot be the same as register {name}')
    elif name in memory:
        print(f'Variable name cannot be the same as the memory address {name}')
    elif 'dup' in value:
        print('detected this ')
        pass
    elif isinstance(value, str):  # if the value is a string
        lst = list(value)
        for char in lst:
            lst.append(ord(char))
    else:
        # print(value)
        for i in range(len(value)):
            if only_numbers(value[i]):
                value[i] = int(value[i])
        variables[name] = value
        # print(value)


# This method is not actually needed yet, however it might be useful as this code continues .
def number_of_words(value):
    """ Returns the number of words in a string, separated by ',' or ' ' ."""
    value = clean_input(value)
    counter = 0
    for i in range(1, len(value)):
        if (value[i] == ' ' or value[i] == ',') and value[i - 1] != ' ' and value[i - 1] != ',':
            counter += 1
    return counter


def variable_wrapper(inserted):
    if valid_variable_declaration(inserted):
        name, value = extract_from_variable(inserted)
        # Valid 2 ?
        assign_variable(name, value)
        return True
    else:
        return False


def display_list_of_methods():
    """ hey there """
    current_module = sys.modules[__name__]
    functions = dir(current_module)
    docs = current_module.__doc__
    print('section1')
    print(docs)
    print(help(current_module))


def save_to_file(file_name,code_list):
    """ creates a new file with the name given and inserts the given code list into it """
    if not file_name.lower().endswith('.txt') and not file_name.lower().endswith('.asm'):
        file_name += '.asm'
    if not os.path.isfile(file_name):  # If the file exists
        f = open(file_name,'wt')  # CREATING AND CHECKING BY THAT IF THE FILE NAME ALREADY TAKEN
        for line1 in code_list:
            f.write(code_list[line1]+'\n')
        f.close()
    else:
        print(f'File {file_name} already exists !')
        choice = input("Press 1 to overwrite ( original file won't be saved) , 2 to create a file with a different name"
                       " \n or press any other key to skip  ")
        choice = choice.strip()
        if choice == '1':  # OVERWRITE
            f = open(file_name, 'wt')
            for line1 in code_list:
                f.write(line1 + '\n')
            f.close()
        elif choice == '2':  # RE-ENTER
            file_name = input('File name:  ')
            if not file_name.lower().endswith('.txt') and not file_name.lower().endswith('.asm'):
                file_name += '.asm'
            while os.path.isfile(file_name):
                file_name = input('File name:  ')
                if not file_name.lower().endswith('.txt') and not file_name.lower().endswith('.asm'):
                    file_name += '.asm'
# *****************************************************************************************************


def analyze_errors(error_number):  # add line number as optional
    """ prints a message according to the error's serial number : 0 - syntax error , 1 - No Error , -1 - Not found """
    if error_number == -1:
        print(f'(19) wrong parameters ')
    elif error_number == 0:
        print('Syntax Error')
    else:
        pass


def analyze_special_commands(command):
    """ Performs actions according to the specified command . Returns True,Running if the command, else False,Running"""
    help_message = ''' 
       These are the supported commands in this emulator:
       mov <register/variable/address> , <register,variable,address,value> A = B
       add <register/variable/address> , <register,variable,address,value> A = A+B
       sub <register/variable/address> , <register,variable,address,value> - A = A-B
       xchg <register/variable/address> , <register,variable,address> - swaps between 2 values
       inc <register/variable/address> - increments by 1
       dec <register/variable/address> - decrements by 1
       print <register/variable/address> - a macro that prints 

       '''
    about = '''
       This is Emu++, the python powered emulator. 
       Clean, simple and effective . Full version in 100$
       To buy this, enter www.emuplusplus.com/scam/full/ 
       '''  # add a link to a real C:\ website with bootstrap about this !

    special_cmd = '''
       %finish - exit
       %help - displays all of the built in methods
       %about - displays an about message
       %cmd - displays the special commands list
       %display - lists all functions and their roles in this program using the help() built in method .
       '''
    command_attempt = True  # If the user entered a command , or started with the '%' key -it'll stay true .
    running = True
    if command == '%finish':
        running = False
    elif command == '%help':
        print(help_message)
    elif command == '%about':
        print(about)
    elif command == '%cmd':
        print(special_cmd)
    elif command == '%display':
        display_list_of_methods()
    elif command.startswith('%') and command not in special_commands:
        print('Command Not Found')
    else:
        command_attempt = False
    return command_attempt, running


def main():
    """ The main method, where all of the above methods are executed according to the user's input"""
    # ENTRY MESSAGE
    intro_font = Figlet(font='standard')
    print(intro_font.renderText('EMU++ '))
    del intro_font
    # SPECIAL MESSAGES TO THE USER
    # webbrowser.open('file://' + os.path.realpath('C:\\Users\\user\\PycharmProjects\\pythonProject\\website.html'))
    input_way = input(
        '>>> | Enter C for console mode | F to upload a file | T for text editor mode |  ')
    input_way = clean_input(input_way)
    if input_way == 'f':  # ***************************   FILE MODE   **************************************
        file_name = clean_input(input('>>> Enter the name of the file:  '))  # RECEIVE THE FILE'S NAME
        if not file_name.endswith('.txt'):
            file_name += '.txt'
        try:
            file = open(file_name, 'rt')  # TRY TO OPEN IT
            for line in file:  # ADD EACH LINE TO THE LIST
                lines[line] = line[:-1]
            print(lines)
            for line in lines:
                command_attempt, running = analyze_special_commands(line)
                if not command_attempt and running:
                    mode = determine_input_type(line)
                    if mode == 1:  # ******** EXECUTING COMMANDS ***********
                        is_valid = handle_wrapper_for_files(line)
                        if is_valid == 1:
                            # print_info()
                            # print('Valid line')
                            pass
                        else:
                            analyze_errors(is_valid)  # PRINTS THE APPROPRIATE MESSAGE
                    elif mode == 0:  # ******** VARIABLE DECLARATION **********
                        # DECLARE A VARIABLE ( DON'T FORGET A VALID_VARIABLE_DECLARATION METHOD )
                        variable_wrapper(line)
                        # print_info()
                    elif mode == -1:
                        # DECLARE A LABEL
                        pass
                    else:
                        print(f"(19) illegal instruction:  or wrong parameters.") # insert parameter here

            print('Your code is : ')
            for line in lines:
                print(line)
            print_info()
        except Exception as e:
            print(e.__class__)
            pass

    elif input_way == 'c':  # ************************** CONSOLE MODE *************************************
        running = True
        index = 0
        while running:
            print('>>>', end=' ')
            command = clean_input(input(' '))
            command_attempt, running = analyze_special_commands(command)
            if not command_attempt and running:
                mode = determine_input_type(command)
                if mode == 1:  # ******** EXECUTING COMMANDS ***********
                    is_valid, number = handle_wrapper_for_console(command)
                    if is_valid == 1:
                        lines[index] = command
                        print_info()
                        if number != -1 and 'jmp' in command:  # INFINITE LOOP FEATURE
                            i = number
                            while i < len(lines):
                                real_cmnd,operand1,operand2 = extract_command(lines[i])
                                handle_command(real_cmnd,operand1,operand2)
                                if i == len(lines)-1:
                                    i = number
                                print_info()
                                i += 1

                    else:
                        analyze_errors(is_valid)  # PRINTS THE APPROPRIATE MESSAGE
                elif mode == 0:  # ******** VARIABLE DECLARATION **********
                    # DECLARE A VARIABLE ( DON'T FORGET A VALID_VARIABLE_DECLARATION METHOD )
                    variable_wrapper(command)
                    print_info()
                    # lines.append(command)
                elif mode == -1:
                    # DECLARE A LABEL
                    lines[index] = command
                    pass
                else:
                    if not check_empty_line(command):
                        print(f"(19) illegal instruction: {command} or wrong parameters.")
                index += 1

        print('Your code is : ')
        for i in range(len(lines)):
            print(lines[i])
        input('Press any key to continue ...')
    elif input_way == 't':  # *****************************  TEXT EDITOR MODE  ***************************************
        running = True
        i = 0
        while running:
            line_of_code = input('>>> {}.'.format(i + 1))
            line_of_code = clean_input(line_of_code)
            command_attempt, running = analyze_special_commands(line_of_code)
            if not running:
                break
            lines[i] = line_of_code
            i += 1
        index = 0
        for i in range(len(lines)):  # RUN TO CHECK IF THERE ARE ANY SYNTAX ERROR . "COMPILATION STAGE 1"
            command_attempt, running = analyze_special_commands(lines[index])
            mode = determine_input_type(lines[index])
            if not command_attempt:
                if not first_is_valid(lines[index]):
                    print(f' Error in line {index+1}')
                    return -1
                else:
                    command, operand1, operand2 = extract_command(lines[index])
                    if mode == 1:
                        pass
                    elif mode == 0:
                        pass
                        #  declaration valid check here ..
                    elif mode == -1:
                        #print('label detected')
                        pass

            index += 1
        errors = 0
        i = 0
        while i < len(lines):  # STAGE 2 - RUN IT !
            command_attempt, running = analyze_special_commands(lines[i])
            if not command_attempt:
                command, operand1, operand2 = extract_command(lines[i])
                # print(command)
                # print(operand1)
                # print(operand2)
                mode = determine_input_type(lines[i])
                if mode == 1:
                    try:
                        if command in jmps:
                            i1 = handle_command(command, operand1, operand2)
                            if i1 != -1:
                                i = i1
                        else:
                            handle_command(command, operand1, operand2)
                    except Exception as e:
                        print(f'ERROR: {e.__class__}')  # NOT INSERTING THE PROBLEMATIC LINES TO THE LINE LIST
                        errors += 1
                elif mode == 0:
                    variable_wrapper(lines[i])
                elif mode == -1:
                    pass
                else:
                    if command not in commands and command not in variable_declaration:
                        print(f" {command}  not found")
                    else:
                        print(f"{command} does not exist in this context.")
            else:
                pass
            i += 1
        print_info()
        print(f'>>> {errors} errors was found')
        answer = input('Do you want to save your work ?  Y / N  ')
        if answer.strip().lower() == 'y':
            file_name = input("File's name:  ")
            file_name = file_name.strip()
            save_to_file(file_name, lines)
    else:
        print("You didn't follow the instructions, therefore you get thrown out")
    input('Press any key to continue ...')


if __name__ == '__main__':
    main()