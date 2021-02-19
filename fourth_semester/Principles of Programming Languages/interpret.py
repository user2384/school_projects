from xml.etree import ElementTree as ET
import os
import argparse
import re
import sys
import inspect
import getopt
from optparse import OptionParser

def exit_program(return_value, message):
    print("ERROR("+str(return_value)+"): "+ message, file=sys.stderr)
    sys.exit(return_value)

name_of_file_source = ""
name_of_file_input = ""
source_set = 1
input_set = 1
p = OptionParser()
p.add_option("--source", dest="name_of_file", help="write report to FILE", metavar="FILE")
p.add_option("--input", dest="name_of_file", help="write report to FILE", metavar="FILE")

try:
    (op, args) = p.parse_args()
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        raise SystemExit
    op_dic = vars(op)
    if len(sys.argv) == 2:
        aa = sys.argv[1]
        indx = aa.index("=")
        aa = aa[2:indx]
        if aa == "source":
            name_of_file_source = op_dic['name_of_file']
            source_set = 0
        if aa == "input":
            name_of_file_input = op_dic['name_of_file']
            input_set = 0
            name_of_file_source = sys.stdin.read()
            name_of_file_source = name_of_file_source.rstrip('\n')
    else:
        aa = sys.argv[1]
        indx = aa.index("=")
        aa = aa[2:indx]
        if aa == "source":
            name_of_file_source = sys.argv[1]
            name_of_file_source = name_of_file_source[3+len("source"):]
            source_set = 0
            bb = sys.argv[2]
            indx = bb.index("=")
            bb = bb[2:indx]
            if bb == "input":
                name_of_file_input = sys.argv[2]
                name_of_file_input = name_of_file_input[3+len("input"):]
                input_set = 0
            else:
                exit_program(10, "Invalid arguments used.")
        elif aa == "input":
            name_of_file_input = sys.argv[1]
            name_of_file_input = name_of_file_input[3+len("input"):]
            input_set = 0
            bb = sys.argv[2]
            indx = bb.index("=")
            bb = bb[2:indx]
            if bb == "source":
                name_of_file_source = sys.argv[2]
                name_of_file_source = name_of_file_source[3+len("source"):]
                source_set = 0
            else:
                exit_program(10, "Invalid arguments used.")
        else:
            exit_program(10, "Invalid arguments used.")



except SystemExit:
    if len(sys.argv) != 2:
        exit_program(10, "Invalid arguments used.")
    a = sys.argv[1]
    if a == "--help" or a == "--h":
        exit(0)
    else:
        exit_program(10, "Invalid arguments used.")

if source_set == 1 and input_set == 1:
    exit_program(10, "Invalid arguments used.")
if source_set == 0 and input_set == 1:
    if not (os.path.isfile(name_of_file_source) and os.access(name_of_file_source, os.R_OK) and os.path.exists(name_of_file_source)):
        exit_program(11, "Cannot open input file.")
    try:
        t = ET.parse(name_of_file_source).getroot()
    except Exception:
        exit_program(31, "Incorrect XML format.")

if source_set == 1 and input_set == 0:
    if not (os.path.isfile(name_of_file_input) and os.access(name_of_file_input, os.R_OK) and os.path.exists(name_of_file_input)):
        exit_program(11, "Cannot open input file.")
    try:
        t = ET.fromstring(name_of_file_source)
    except Exception:
        exit_program(31, "Incorrect XML format.")

if source_set == 0 and input_set == 0:
    if not (os.path.isfile(name_of_file_source) and os.access(name_of_file_source, os.R_OK) and os.path.exists(name_of_file_source)):
        exit_program(11, "Cannot open input file.")
    if not (os.path.isfile(name_of_file_input) and os.access(name_of_file_input, os.R_OK) and os.path.exists(name_of_file_input)):
        exit_program(11, "Cannot open input file.")
    try:
        t = ET.parse(name_of_file_source).getroot()
    except Exception:
        exit_program(31, "Incorrect XML format.")

arg_var_symb = 1
arg_none = 2
arg_var = 3
arg_var_label = 4
arg_var_symb_symb = 5
arg_var_symb = 6
arg_var_int = 7
arg_var_type = 8
arg_var_str = 9
arg_var_label = 10
arg_var_label_symb_symb = 11
arg_symb = 12

arg_var_symb_num = 2
arg_var_symb_type = ['^var$', "^(var|int|bool|string)$"]
arg_var_symb_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$","^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)"]
arg_none_num = 0
arg_var_num = 1
arg_var_type = ['^var$']
arg_var_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$"]
arg_var_int_num = 2
arg_var_int_type = ['^var$','^int$']
arg_var_int_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$", "^(\+|\-)?\d+$"]
arg_var_type_num = 2
arg_var_type_type = ['^var$', '^type$']
arg_var_type_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$", "^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)"]
arg_var_str_num = 2
arg_var_str_type = ['^var$','^string$']
arg_var_str_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$", "([^#\s\\\\]|\\\\[0-9]{3})*$"]
arg_var_symb_symb_num = 3
arg_var_symb_symb_type = ['^var$',"^(var|int|bool|string)$","^(var|int|bool|string)$"]
arg_var_symb_symb_patt = ["^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$", "^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)", "^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)"]
arg_symb_num = 1
arg_symb_type = ["^(var|int|bool|string)$"]
arg_symb_patt = ["^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)"]
arg_var_label_num = 1
arg_var_label_type = ['^label$']
arg_var_label_patt = ["^([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$"]
arg_var_label_symb_symb_num = 3
arg_var_label_symb_symb_type = ['^label$',"^(var|int|bool|string)$","^(var|int|bool|string)$"]
arg_var_label_symb_symb_patt = ["^([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$", "^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)","^((LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(((\+|\-)?\d+)$|((true|false)$)|(([^#\s\\\\]|\\\\[0-9]{3})*)$)"]

opcodes = {
  'MOVE':arg_var_symb,
  'CREATEFRAME':arg_none,
  'PUSHFRAME':arg_none,
  'POPFRAME':arg_none,
  'DEFVAR':arg_var,
  'CALL':arg_var_label,
  'RETURN':arg_none,

  'PUSHS': arg_symb,
  'POPS':  arg_var,

  'ADD':arg_var_symb_symb,
  'SUB':arg_var_symb_symb,
  'MUL':arg_var_symb_symb,
  'IDIV':arg_var_symb_symb,

  'LT':arg_var_symb_symb,
  'GT':arg_var_symb_symb,
  'EQ':arg_var_symb_symb,

  'AND':arg_var_symb_symb,
  'OR':arg_var_symb_symb,
  'NOT':arg_var_symb,

  'INT2CHAR': arg_var_int,
  'STRI2INT':arg_var_symb_symb,

  'READ': arg_var_type,
  'WRITE': arg_symb,

  'CONCAT':arg_var_symb_symb,
  'STRLEN':arg_var_str,
  'GETCHAR':arg_var_symb_symb,
  'SETCHAR':arg_var_symb_symb,

  'TYPE': arg_var_symb,

  'LABEL':arg_var_label,
  'JUMP':arg_var_label,
  'JUMPIFEQ':arg_var_label_symb_symb,
  'JUMPIFNEQ':arg_var_label_symb_symb,
  'EXIT':arg_symb,

  'DPRINT':arg_symb,
  'BREAK':arg_none
}

def opcode_num(op):
    if op == arg_var_symb:
        return arg_var_symb_num
    if op == arg_none:
        return arg_none_num
    if op == arg_var:
        return arg_var_num
    if op == arg_var_int:
        return arg_var_int_num
    if op == arg_var_type:
        return arg_var_type_num
    if op == arg_var_str:
        return arg_var_str_num
    if op == arg_var_symb_symb:
        return arg_var_symb_symb_num
    if op == arg_symb:
        return arg_symb_num
    if op == arg_var_label:
        return arg_var_label_num
    if op == arg_var_label_symb_symb:
        return arg_var_label_symb_symb_num

lbs = []
temporary_frame_list = []
frame_list = []

# Checks 'program' element
if not 'program' in t.tag:
    exit_program(31, "Program is missing.")

tree_attr_count = len(t.attrib)


if not 'language' in t.attrib:
    exit_program(31, "Language not found.")
if t.attrib['language'] != "IPPcode19":
    exit_program(32, "Incorrect language.")

if tree_attr_count == 2:
    if not 'name' in t.attrib:
        if not 'description' in t.attrib:
            exit_program(32, "Unknown attribute found.")

if tree_attr_count == 3:
    if not 'name' in t.attrib:
        exit_program(31, "Name not found.")
    if not 'description' in t.attrib:
        exit_program(31, "Description not found.")

if tree_attr_count > 3 or tree_attr_count < 1:
    exit_program(32, "Number is too big.")

# Data stack
stack = []

# Global frame
global_frame = {'frame': 'GF'}
frame_list.append(global_frame)

# Instruction counter
instruction_counter = 0

# Instruction list
instruction_list = []

#Fill instruction list and checks structure of XML tree and elements values
for instruction in t:
  instruction_counter = instruction_counter + 1
  if not 'instruction' in instruction.tag:
      exit_program(31, "Instruction element is not named correctly.") # 31 or 32
  instruction_attr_count = len(instruction.attrib)
  if len(instruction.attrib) != 2:
      exit_program(32, "Too much or too little attributes used for instruction element.") # 31 or 32
  if not 'order' in instruction.attrib:
      exit_program(31, "Order not found in instruction element.") # 31 or 32
  if not 'opcode' in instruction.attrib:
      exit_program(31, "Opcode not found in instruction element.") # 31 or 32
  if instruction.attrib['order'] != str(instruction_counter):
      exit_program(32, "Order does not contain values.") # 31 or 32
  instruction_opcode = instruction.attrib['opcode']
  instruction_arg_count = len(instruction)
  if not instruction_opcode in opcodes.keys():
      exit_program(32, "Unknown opcode used.")  # 31 or 32
  else:
      if instruction_arg_count != opcode_num(opcodes[instruction_opcode]):
          exit_program(32, "Incorrect number of arguments used with instruction.")
      idx = 0
      idx_p = 1
      argument_list = []
      for argument in instruction:
          if not 'arg' + str(idx_p) in argument.tag:
              exit_program(31, "Not increasing arguments.") #31 or 32
          if len(argument.attrib) != 1:
              exit_program(32, "Incorrect number of attributes.") #31 or 32
          if not 'type' in argument.attrib:
              exit_program(31, "Attribute type missing in instruction argument.") #31 or 32
          if instruction_opcode == 'LABEL':
              for each in lbs:
                  if argument.text in each.keys():
                      exit_program(52, "Same name defined for more labels.")
              lbs.append({argument.text: instruction.attrib['order']})
          if not argument.text:
              argument.text = ""
          check_p = ""
          if "var" == argument.attrib['type']:
              check_p = "^(LF|TF|GF)@([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$"
          elif "int" == argument.attrib['type']:
              check_p = "^(\+|\-)?\d+$"
          elif "bool" == argument.attrib['type']:
              check_p = "^(true|false)$"
          elif "string" == argument.attrib['type']:
              check_p = "([^#\s\\\\]|\\\\[0-9]{3})*$"
          elif "type" == argument.attrib['type']:
              check_p = "^(int|bool|string)$" #nil
          elif "label" == argument.attrib['type']:
              check_p = "^([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$"
          elif "nil" == argument.attrib['type']:
              check_p = "^(nil)$" #nil
          else:
              exit_program(32, "Unknown type used.")
          p_c = re.compile(check_p)
          m = bool(p_c.match(argument.text))
          if m == False:
              exit_program(32, "Type does not match value.")
          argument = {'type': argument.attrib['type'], 'value': argument.text}
          argument_list.append(argument)
          idx = idx + 1
          idx_p = idx_p + 1

      new_instruction = {
          'order': instruction.get('order'),
          'opcode': instruction.get('opcode'),
          'argnum': len(instruction),
          'args' : argument_list}
  instruction_list.append(new_instruction)

f_back = []
f_call = []
p_counter = 0
drist = 0
while (p_counter < instruction_counter):
    ins = instruction_list[p_counter]
    p_counter = p_counter + 1
    if ins['opcode'] == "DEFVAR":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame = temporary_frame_list[0]

        if frame:
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                gotframe = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                gotframe = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                gotframe = temporary_frame_list[0]
            if name_variable in gotframe:
                booln = True
            else:
                booln = False
            if not booln:
                frame[name_variable] = {'type': 'Unknown', 'value': 'Unknown'}
            else:
                exit_program(52, "Same name for more than one variable used.")
        else:
            exit_program(55, "Not existing frame" + frame_variable + ".")
    elif ins['opcode'] == "MOVE":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame_where = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame_where = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame_where = temporary_frame_list[0]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            result = True
        else:
            result = False
        if result:
            argument_type = ins['args'][1]['type']
            if argument_type == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument = to_split[0]
                name_argument = to_split[1]

                if frame_argument == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument in gotframe:
                    result = True
                else:
                    result = False
                if result:
                    if frame_argument == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        frame_f = global_frame
                    elif frame_argument == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        frame_f = frame_list[-1]
                    elif frame_argument == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        frame_f = temporary_frame_list[0]
                    frame_where[name_variable] = {'type': frame_f[name_argument]['type'], 'value': frame_f[name_argument]['value']}
                else:
                    exit_program(54, "Variable does not exist.")
            else:
                argument_value = ins['args'][1]['value']
                if argument_type == "int":
                    argument_value = str(int(argument_value))
                frame_where[name_variable] = {'type': argument_type,'value': argument_value}
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "CREATEFRAME":
        frame_n = {'frame': 'TF'}
        if not temporary_frame_list:
            temporary_frame_list.append(frame_n)
        else:
            temporary_frame_list.remove(temporary_frame_list[0])
            temporary_frame_list.append(frame_n)
    elif ins['opcode'] == "PUSHFRAME":
        if not temporary_frame_list:
            exit_program(55, "TF does not exist.")
        else:
            frame_list.append(temporary_frame_list[0])
            temporary_frame_list.remove(temporary_frame_list[0])
            frame_list[-1]['frame'] = "LF"
    elif ins['opcode'] == "POPFRAME":
        if len(frame_list) != 1:
            if temporary_frame_list:
                temporary_frame_list.remove(temporary_frame_list[0])
            temporary_frame_list.append(frame_list[-1])
            frame_list.remove(frame_list[-1])
            temporary_frame_list[0]['frame'] = "TF"
        else:
            exit_program(55, "LF does not exist.")
    elif ins['opcode'] == "CALL":
        argument_type = ins['args'][0]['type']
        argument_value = ins['args'][0]['value']
        f = False
        idx = 0
        for each in lbs:
            if argument_value in each.keys():
                f = True
                instruction_label = argument_value
                instruction_order = int(lbs[idx][argument_value])
            idx =  idx + 1

        if f == True:
            if p_counter < instruction_order:
                while (p_counter < instruction_order):
                    p_counter = p_counter + 1
            else:
                while (p_counter > instruction_order):
                    p_counter = p_counter - 1
        else:
            exit_program(52, "Unknown label.")
    elif ins['opcode'] == "RETURN":
        if not f_call:
            exit_program(56, "Return outside the function.")
        else:
            p_counter = f_back[-1]
            f_call.remove(f_call[-1])
            f_back.remove(f_back[-1])
    elif ins['opcode'] == "PUSHS":
        argument_type = ins['args'][0]['type']
        argument_value = ins['args'][0]['value']

        if argument_type == "var":
            to_split = ins['args'][0]['value'].split('@')
            frame_variable = to_split[0]
            if len(to_split) == 1:
                exit_program(32, "Invalid xml.")
            name_variable = to_split[1]
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                gotframe = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                gotframe = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                gotframe = temporary_frame_list[0]
            if name_variable in gotframe:
                result = True
            else:
                result = False
            if result:
                if frame[name_variable]['type'] == "Unknown":
                    exit_program(56, "Variable with unknown value and type used with instruction PUSHS.")
                else:
                    if frame[name_variable]['type'] == "int":
                        push_int = str(int(frame[name_variable]['value']))
                        stack.append({'type': frame[name_variable]['type'], 'value': push_int})

                    elif frame[name_variable]['type'] == "bool":
                        stack.append({'type': frame[name_variable]['type'], 'value': frame[name_variable]['value']})

                    elif frame[name_variable]['type'] == "nil":
                        stack.append({'type': frame[name_variable]['type'], 'value': frame[name_variable]['value']})

                    elif frame[name_variable]['type'] == "string":
                        stack.append({'type': frame[name_variable]['type'], 'value': frame[name_variable]['value']})
            else:
                exit_program(55, "Variable used with instruction PUSHS does not exist.")
        else:
            if argument_type == "Unknown":
                exit_program(56, "Variable with unknown value and type used with instruction PUSHS.")
            else:
                if argument_type == "int":
                    push_int = str(int(argument_value))
                    stack.append({'type': argument_type, 'value': push_int})

                elif argument_type == "bool":
                    stack.append({'type': argument_type, 'value': argument_value})

                elif argument_type == "nil":
                    stack.append({'type': argument_type, 'value': argument_value})

                elif argument_type == "string":
                    stack.append({'type': argument_type, 'value': argument_value})
    elif ins['opcode'] == "POPS":
        argument_type = ins['args'][0]['type']
        argument_value = ins['args'][0]['value']

        if argument_type != "var":
            exit_program(53, "First argument need to be defined variable.")
        else:
            to_split = ins['args'][0]['value'].split('@')
            frame_variable = to_split[0]
            if len(to_split) == 1:
                exit_program(32, "Invalid xml.")
            name_variable = to_split[1]

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                gotframe = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                gotframe = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                gotframe = temporary_frame_list[0]
            if name_variable in gotframe:
                result = True
            else:
                result = False
            if result:
                if not stack:
                    exit_program(56, "Instruction POPS was called even when data stack is empty.")
                else:
                    frame[name_variable]['type'] = stack[-1]['type']
                    frame[name_variable]['value'] = stack[-1]['value']
                    del stack[-1]
            else:
                exit_program(54, "Variable used with instrucstion POPS does not exist.")
    elif ins['opcode'] == "ADD":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_first = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "int":
                operand_first = int(argument_value_first)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_second = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                operand_second = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")

            result = operand_first + operand_second
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "int";
            frame[name_variable]['value'] = str(result)
    elif ins['opcode'] == "SUB":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_first = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "int":
                operand_first = int(argument_value_first)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_second = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                operand_second = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")

            result = operand_first - operand_second
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "int";
            frame[name_variable]['value'] = str(result)
    elif ins['opcode'] == "MUL":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_first = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "int":
                operand_first = int(argument_value_first)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_second = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                operand_second = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")

            result = operand_first * operand_second
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "int";
            frame[name_variable]['value'] = str(result)
    elif ins['opcode'] == "IDIV":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_first = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "int":
                operand_first = int(argument_value_first)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_second = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers in arithmetic operation.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                operand_second = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers in arithmetic operation.")

            if operand_second == 0:
                exit_program(57, "Division by zero.")
            else:
                result = operand_first // operand_second
            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "int";
            frame[name_variable]['value'] = str(result)
    elif ins['opcode'] == "LT":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_first = argument_frame[name_argument_variable]['type']
                    operand_first_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_first = argument_type_first
                operand_first_value = argument_value_first

            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_second = argument_frame[name_argument_variable]['type']
                    operand_second_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_second = argument_type_second
                operand_second_value = argument_value_second

            if operand_type_first != operand_type_second:
                exit_program(53, "Relational type collision.")

            else:
                opcode = ins['opcode']
                if operand_type_first== "int":
                    operand_first_value = int(operand_first_value)
                    operand_second_value = int(operand_second_value)

                elif operand_type_first == "bool":
                    if operand_first_value == "false":
                        if operand_second_value == "false":
                            operand_first_value = 0
                            operand_second_value = 0
                        else:
                            operand_first_value = 0
                            operand_second_value = 1
                    else:
                        if operand_second_value == "false":
                            operand_first_value = 1
                            operand_second_value = 0
                        else:
                            operand_first_value = 1
                            operand_second_value = 1
                elif operand_type_first == "nil":
                    exit_program(53, "Relation with nil operand.")
                elif operand_type_second == "nil":
                    exit_program(53, "Relation with nil operand.")
                elif operand_type_first == "string":
                    operand_first_value = operand_first_value
                    operand_second_value = operand_second_value
                if opcode == "LT":
                    result = operand_first_value < operand_second_value
                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                frame[name_variable]['type'] = "bool";
                if result == True:
                    frame[name_variable]['value'] = "true"
                elif result == False:
                    frame[name_variable]['value'] = "false"
                else:
                    exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "GT":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_first = argument_frame[name_argument_variable]['type']
                    operand_first_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_first = argument_type_first
                operand_first_value = argument_value_first

            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_second = argument_frame[name_argument_variable]['type']
                    operand_second_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_second = argument_type_second
                operand_second_value = argument_value_second

            if operand_type_first != operand_type_second:
                exit_program(53, "Relational type collision.")

            else:
                opcode = ins['opcode']
                if operand_type_first == "int":
                    operand_first_value = int(operand_first_value)
                    operand_second_value = int(operand_second_value)

                elif operand_type_first == "bool":
                    if operand_first_value == "false":
                        if operand_second_value == "false":
                            operand_first_value = 0
                            operand_second_value = 0
                        else:
                            operand_first_value = 0
                            operand_second_value = 1
                    else:
                        if operand_second_value == "false":
                            operand_first_value = 1
                            operand_second_value = 0
                        else:
                            operand_first_value = 1
                            operand_second_value = 1
                elif operand_type_first == "nil":
                    exit_program(53, "Relation with nil operand.")
                elif operand_type_second == "nil":
                    exit_program(53, "Relation with nil operand.")
                elif operand_type_first == "string":
                    operand_first_value = operand_first_value
                    operand_second_value = operand_second_value
                if opcode == "GT":
                    result = operand_first_value > operand_second_value
                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                frame[name_variable]['type'] = "bool";
                if result == True:
                    frame[name_variable]['value'] = "true"
                elif result == False:
                    frame[name_variable]['value'] = "false"
                else:
                    exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "EQ":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_first = argument_frame[name_argument_variable]['type']
                    operand_first_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_first = argument_type_first
                operand_first_value = argument_value_first

            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    operand_type_second = argument_frame[name_argument_variable]['type']
                    operand_second_value = argument_frame[name_argument_variable]['value']
            else:
                operand_type_second = argument_type_second
                operand_second_value = argument_value_second

            if operand_type_first != operand_type_second:
                exit_program(53, "Relational type collision.")

            else:
                opcode = ins['opcode']
                if operand_type_first == "int":
                    operand_first_value = int(operand_first_value)
                    operand_second_value = int(operand_second_value)

                elif operand_type_first == "bool":
                    if operand_first_value == "false":
                        if operand_second_value == "false":
                            operand_first_value = 0
                            operand_second_value = 0
                        else:
                            operand_first_value = 0
                            operand_second_value = 1
                    else:
                        if operand_second_value == "false":
                            operand_first_value = 1
                            operand_second_value = 0
                        else:
                            operand_first_value = 1
                            operand_second_value = 1
                elif operand_type_first == "nil":
                    operand_first_value = 0
                    operand_second_value = 0
                elif operand_type_second == "nil":
                    operand_first_value = 0
                    operand_second_value = 0
                elif operand_type_first == "string":
                    operand_first_value = operand_first_value
                    operand_second_value = operand_second_value
                if opcode == "EQ":
                    result = operand_first_value == operand_second_value
                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                frame[name_variable]['type'] = "bool"
                if result == True:
                    frame[name_variable]['value'] = "true"
                elif result == False:
                    frame[name_variable]['value'] = "false"
                else:
                    exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "AND":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_number = ins['argnum']

        if argument_number == 3:
            argument_type_second = ins['args'][2]['type']
            argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    if argument_frame[name_argument_variable]['type'] == "bool":
                        operand_first = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not boolean.")
            elif argument_type_first == "bool":
                operand_first = argument_value_first
            else:
                exit_program(53, "Operands are not boolean.")
            operand_second = None
            if argument_number == 3:
                if argument_type_second == "var":
                    to_split = ins['args'][2]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if not res:
                        exit_program(54, "Variable does not exist.")
                    else:
                        if argument_frame[name_argument_variable]['type'] == "bool":
                            operand_second = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not boolean.")
                elif argument_type_second == "bool":
                    operand_second = argument_value_second
                else:
                    exit_program(53, "Operands are not boolean.")
            if operand_first == "false":
                operand_first = False
            elif operand_first == "true":
                operand_first = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            if operand_second == "false":
                operand_second = False
            elif operand_second == "true":
                operand_second = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            result = operand_first and operand_second

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "bool"
            if result == True:
                frame[name_variable]['value'] = "true"
            elif result == False:
                frame[name_variable]['value'] = "false"
            else:
                exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "OR":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_number = ins['argnum']

        if argument_number == 3:
            argument_type_second = ins['args'][2]['type']
            argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    if argument_frame[name_argument_variable]['type'] == "bool":
                        operand_first = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not boolean.")
            elif argument_type_first == "bool":
                operand_first = argument_value_first
            else:
                exit_program(53, "Operands are not boolean.")
            operand_second = None
            if argument_number == 3:
                if argument_type_second == "var":
                    to_split = ins['args'][2]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if not res:
                        exit_program(54, "Variable does not exist.")
                    else:
                        if argument_frame[name_argument_variable]['type'] == "bool":
                            operand_second = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not boolean.")
                elif argument_type_second == "bool":
                    operand_second = argument_value_second
                else:
                    exit_program(53, "Operands are not boolean.")
            if operand_first == "false":
                operand_first = False
            elif operand_first == "true":
                operand_first = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            if operand_second == "false":
                operand_second = False
            elif operand_second == "true":
                operand_second = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            result = operand_first or operand_second

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "bool"
            if result == True:
                frame[name_variable]['value'] = "true"
            elif result == False:
                frame[name_variable]['value'] = "false"
            else:
                exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "NOT":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_number = ins['argnum']

        if argument_number == 3:
            argument_type_second = ins['args'][2]['type']
            argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if not res:
            exit_program(54, "Variable does not exist.")
        else:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if not res:
                    exit_program(54, "Variable does not exist.")
                else:
                    if argument_frame[name_argument_variable]['type'] == "bool":
                        operand_first = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not boolean.")
            elif argument_type_first == "bool":
                operand_first = argument_value_first
            else:
                exit_program(53, "Operands are not boolean.")
            operand_second = None
            if argument_number == 3:
                if argument_type_second == "var":
                    to_split = ins['args'][2]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if not res:
                        exit_program(54, "Variable does not exist.")
                    else:
                        if argument_frame[name_argument_variable]['type'] == "bool":
                            operand_second = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not boolean.")
                elif argument_type_second == "bool":
                    operand_second = argument_value_second
                else:
                    exit_program(53, "Operands are not boolean.")
            if operand_first == "false":
                operand_first = False
            elif operand_first == "true":
                operand_first = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            if operand_second == "false":
                operand_second = False
            elif operand_second == "true":
                operand_second = True
            else:
                exit_program(53, "Argument is not string representing bool.")
            result = not operand_first

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            frame[name_variable]['type'] = "bool"
            if result == True:
                frame[name_variable]['value'] = "true"
            elif result == False:
                frame[name_variable]['value'] = "false"
            else:
                exit_program(53, "Wrong argument to bool function.")
    elif ins['opcode'] == "INT2CHAR":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            booln = True
        else:
            booln = False
        if booln:
            operand_type_first = argument_type_first
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_first_value = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not integers.")
                else:
                    exit_program(54, "Variable doesnot exist.")
            elif argument_type_first == "int":
                operand_first_value = argument_value_first
            else:
                exit_program(53, "Operands are not integers.")
            if operand_first_value in range(0, 256):
                result = chr(operand_first_value)
                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]
                frame[name_variable]['type'] = "string"
                frame[name_variable]['value'] = result
            else:
                exit_program(58, "ASCII is different than it should be.")
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "STRI2INT":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            result = True
        else:
            result = False
        if result:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]
                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "string":
                        operand_string = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not strings.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "string":
                operand_string = argument_value_first
            else:
                exit_program(53, "Operands are not strings.")

            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]
                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        operand_index = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(53, "Operands are not integers.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                operand_index = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers.")

            escaped_pattern = "\\\\[0-9]{3}"
            escaped = re.findall(escaped_pattern, operand_string)
            regular = re.split(escaped_pattern, operand_string)
            operand_string_len = 0
            for each in escaped:
                operand_string_len += 1

            for each in regular:
                operand_string_len += len(each)

            operand_string_len = operand_string_len

            character_counter = 0
            escape_counter = 0
            escape_sequence = False
            c = []
            if operand_index < operand_string_len and operand_index >= 0:

                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                while (character_counter <= operand_index):
                    if operand_string[character_counter] == "\\":
                        if character_counter == operand_index:
                            escape_sequence = True
                            escape_counter += 1
                            while (escape_counter < 3):
                                c.append(operand_string[operand_index + escape_counter])
                                escape_counter += 1
                        character_counter += 3
                        operand_index += 3
                    else:
                        if character_counter == operand_index:
                            c.append(operand_string[operand_index])
                        character_counter += 1

                c = "".join(c)
                if escape_sequence:
                    c = int(c)
                else:
                    c = ord(c)

                frame[name_variable]['type'] = "int";
                frame[name_variable]['value'] = str(c);
            else:
                exit_program(58, "Index out of range.")
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "READ":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type = ins['args'][1]['value']
        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if res:
            if source_set == 0 and input_set == 1:
                try:
                    argument_value = input()
                except EOFError:
                    argument_value = ""

                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                if argument_type == "string":
                    pattern_compared = re.compile("([^#\s\\\\]|\\\\[0-9]{3})*$")
                    m = bool(pattern_compared.match(argument_value))
                    if m == True:
                        booln = True
                    else:
                        booln = False
                    if argument_value and booln:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = str(argument_value)
                    else:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = ""
                elif argument_type == "int":
                    try:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = str(int(argument_value))
                    except:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = "0"
                elif argument_type == "bool":
                    if argument_value.lower() == "true":
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "true"
                    else:
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "false"
                else:
                    exit_program(54, "Variable does not exist.")
            elif source_set == 1 and input_set == 0:
                lista = []
                z = open(name_of_file_input)
                lista = z.read().splitlines()
                ll = 0
                argument_value = ""
                while ll < len(lista):
                    argument_value = argument_value + lista[ll]
                    ll = ll+1

                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                if argument_type == "string":
                    pattern_compared = re.compile("([^#\s\\\\]|\\\\[0-9]{3})*$")
                    m = bool(pattern_compared.match(argument_value))
                    if m == True:
                        booln = True
                    else:
                        booln = False
                    if argument_value and booln:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = str(argument_value)
                    else:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = ""
                elif argument_type == "int":
                    try:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = str(int(argument_value))
                    except:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = "0"
                elif argument_type == "bool":
                    if argument_value.lower() == "true":
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "true"
                    else:
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "false"
                else:
                        exit_program(54, "Variable does not exist.")
            elif source_set == 0 and input_set == 0:
                lista = []
                z = open(name_of_file_input)
                lista = z.read().splitlines()
                ll = 0
                argument_value = ""
                while ll < len(lista):
                    argument_value = argument_value + lista[ll]
                    ll = ll + 1

                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                if argument_type == "string":
                    pattern_compared = re.compile("([^#\s\\\\]|\\\\[0-9]{3})*$")
                    m = bool(pattern_compared.match(argument_value))
                    if m == True:
                        booln = True
                    else:
                        booln = False
                    if argument_value and booln:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = str(argument_value)
                    else:
                        frame[name_variable]['type'] = "string"
                        frame[name_variable]['value'] = ""
                elif argument_type == "int":
                    try:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = str(int(argument_value))
                    except:
                        frame[name_variable]['type'] = "int"
                        frame[name_variable]['value'] = "0"
                elif argument_type == "bool":
                    if argument_value.lower() == "true":
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "true"
                    else:
                        frame[name_variable]['type'] = "bool"
                        frame[name_variable]['value'] = "false"
                else:
                    exit_program(54, "Variable does not exist.")
        else:
            exit_program(54, "Variable does not exist.")

    elif ins['opcode'] == "WRITE":
        argument_type = ins['args'][0]['type']
        argument_value = ins['args'][0]['value']

        if argument_type == "var":
            to_split = ins['args'][0]['value'].split('@')
            frame_variable = to_split[0]
            name_variable = to_split[1]

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                frame = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                frame = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                frame = temporary_frame_list[0]

            if frame_variable == "GF":
                if not global_frame:
                    exit_program(55, "GF does not exist.")
                gotframe = global_frame
            elif frame_variable == "LF":
                if frame_list[-1]:
                    if not frame_list[-1]['frame'] == "LF":
                        exit_program(55, "LF does not exist.")
                gotframe = frame_list[-1]
            elif frame_variable == "TF":
                if not temporary_frame_list:
                    exit_program(55, "TF does not exist.")
                gotframe = temporary_frame_list[0]
            if name_variable in gotframe:
                res = True
            else:
                res = False
            if res:
                if frame[name_variable]['type'] != "Unknown":
                    if frame[name_variable]['type'] == "int":
                        integer_to_print = frame[name_variable]['value']
                        pattern_compared = re.compile("\+")
                        match = bool(pattern_compared.match(frame[name_variable]['value']))
                        if match == True:
                            booln = True
                        else:
                            booln = False
                        if booln:
                            integer_to_print = frame[name_variable]['value'].split("+")[1]
                        print(integer_to_print, end='')
                    elif frame[name_variable]['type'] == "bool":
                        print(frame[name_variable]['value'], end='')
                    elif frame[name_variable]['type'] == "string":
                        hex_list = []
                        esc_pattern = "\\\\[0-9]{3}"
                        escaped = re.findall(esc_pattern, frame[name_variable]['value'])
                        regular = re.split(esc_pattern, frame[name_variable]['value'])

                        for each in escaped:
                            int_value = re.split("\\\\", each)
                            hex_list.append(int(int_value[1]))

                        counter = 0
                        for escape in hex_list:
                            print(regular[counter], chr(hex_list[counter]), sep='', end="")
                            counter += 1

                        if len(hex_list) < len(regular):
                            print(regular[counter], sep='', end="")
                        print("\n", sep='', end="")
                else:
                    exit_program(56, "Value is missing.")
            else:
                exit_program(54, "Variable does not exist.")
        else:
            if argument_type != "Unknown":
                if argument_type == "int":
                    integer_to_print = argument_value
                    pattern_compared = re.compile("\+")
                    match = bool(pattern_compared.match(argument_value))
                    if match == True:
                        booln = True
                    else:
                        booln = False
                    if booln:
                        integer_to_print = argument_value.split("+")[1]
                    print(integer_to_print, end='')
                elif argument_type == "bool":
                    print(argument_value, end='')
                elif argument_type == "string":
                    hex_list = []
                    esc_pattern = "\\\\[0-9]{3}"
                    escaped = re.findall(esc_pattern, argument_value)
                    regular = re.split(esc_pattern, argument_value)

                    for each in escaped:
                        int_value = re.split("\\\\", each)
                        hex_list.append(int(int_value[1]))

                    counter = 0
                    for escape in hex_list:
                        print(regular[counter], chr(hex_list[counter]), sep='', end="")
                        counter += 1

                    if len(hex_list) < len(regular):
                        print(regular[counter], sep='', end="")
                    print("\n", sep='', end="")
            else:
                exit_program(56, "Value is missing.")
    elif ins['opcode'] == "CONCAT":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame = temporary_frame_list[0]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if res:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "string":
                        operand_first = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(56, "Operands are not strings.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "string":
                 operand_first = argument_value_first
            else:
                exit_program(53, "Operands are not strings.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "string":
                        operand_second = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not strings.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "string":
                operand_second = argument_value_second
            else:
                exit_program(53, "Operands are not strings.")
            result = operand_first + operand_second

            frame[name_variable]['type'] = "string"
            frame[name_variable]['value'] = result
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "STRLEN":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type = ins['args'][1]['type']
        argument_value = ins['args'][1]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame = temporary_frame_list[0]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if res:
            if argument_type == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "string":
                        op_string = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(53, "Operands are not strings.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type == "string":
                 op_string = argument_value
            else:
                exit_program(53, "Operands are not strings.")
            escaped_pattern = "\\\\[0-9]{3}"
            escaped = re.findall(escaped_pattern, op_string)
            regular = re.split(escaped_pattern, op_string)
            operand_string_length = 0
            for each in escaped:
                operand_string_length += 1

            for each in regular:
                operand_string_length += len(each)

            string_operand_length = operand_string_length
            frame[name_variable]['type'] = "int"
            frame[name_variable]['value'] = str(string_operand_length)
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "GETCHAR":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if res:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "string":
                        op_string = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(56, "Operands are not strings.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "string":
                 op_string = argument_value_first
            else:
                exit_program(53, "Operands are not strings.")
            if argument_type_second == "var":
                to_split = ins['args'][2]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    if argument_frame[name_argument_variable]['type'] == "int":
                        op_index = int(argument_frame[name_argument_variable]['value'])
                    else:
                        exit_program(56, "Operands are not integers.")
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_second == "int":
                op_index = int(argument_value_second)
            else:
                exit_program(53, "Operands are not integers.")

            escaped_pattern = "\\\\[0-9]{3}"
            escaped = re.findall(escaped_pattern, op_string)
            regular = re.split(escaped_pattern, op_string)
            operand_string_length = 0
            for each in escaped:
                operand_string_length += 1

            for each in regular:
                operand_string_length += len(each)

            string_operand_length = operand_string_length

            counter_for_characters = 0
            counter_esc = 0
            c = []
            if op_index < string_operand_length and op_index >= 0:
                if frame_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    frame = global_frame
                elif frame_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    frame = frame_list[-1]
                elif frame_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    frame = temporary_frame_list[0]

                while (counter_for_characters <= op_index):
                    if op_string[counter_for_characters] == "\\":
                        if counter_for_characters == op_index:
                            while (counter_esc < 3):
                                c.append(op_string[op_index + counter_esc])
                                counter_esc += 1
                        counter_for_characters += 3
                        op_index += 3
                    else:
                        if counter_for_characters == op_index:
                            c.append(op_string[op_index])
                        counter_for_characters += 1

                c = "".join(c)
                frame[name_variable]['type'] = "string";
                frame[name_variable]['value'] = c
            else:
                exit_program(58, "Index out of range.")
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "SETCHAR":
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame = temporary_frame_list[0]
        var_type = frame[name_variable]['type']
        var_value = frame[name_variable]['value']

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            res = True
        else:
            res = False
        if res:
            if var_type == "string":
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "int":
                            op_index = int(argument_frame[name_argument_variable]['value'])
                        else:
                            exit_program(53, "Operands are not integers.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_first == "int":
                    op_index = int(argument_value_first)
                else:
                    exit_program(53, "Operands are not integers.")

                if argument_type_second == "var":
                    ato_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "string":
                            op_string = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(58, "Operands are not strings.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_second == "string":
                    op_string = argument_value_second
                else:
                    exit_program(53, "Operands are not strings. here i am now")
                string_variable_length = len(var_value)
                string_operand_length = len(op_string)

                if string_operand_length > 0:
                    if op_index < string_variable_length and op_index >= 0:
                        var_value = list(var_value)

                        if var_value[op_index] == "\\":
                            if op_string[0] == "\\":
                                for i in range(1, 4):
                                    var_value[op_index + i] = op_string[i]
                            else:
                                for i in range(1, 4):
                                    del var_value[op_index + 1]
                                var_value[op_index] = op_string[0]
                        else:
                            if op_string[0] == "\\":
                                var_value[op_index] = "\\"
                                for i in range(1, 4):
                                    var_value.insert(op_index + i, op_string[i])
                            else:
                                var_value[op_index] = op_string[0]

                        var_value = "".join(var_value)
                        frame[name_variable]['value'] = str(var_value)
                    else:
                        exit_program(58, "Index not in range.")
                else:
                    exit_program(58, "Empty string.")
            else:
                exit_program(53, "No string in variable.")
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "TYPE": #nil
        to_split = ins['args'][0]['value'].split('@')
        frame_variable = to_split[0]
        if len(to_split) == 1:
            exit_program(32, "Invalid xml.")
        name_variable = to_split[1]

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']
        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            frame = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            frame = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            frame = temporary_frame_list[0]

        if frame_variable == "GF":
            if not global_frame:
                exit_program(55, "GF does not exist.")
            gotframe = global_frame
        elif frame_variable == "LF":
            if frame_list[-1]:
                if not frame_list[-1]['frame'] == "LF":
                    exit_program(55, "LF does not exist.")
            gotframe = frame_list[-1]
        elif frame_variable == "TF":
            if not temporary_frame_list:
                exit_program(55, "TF does not exist.")
            gotframe = temporary_frame_list[0]
        if name_variable in gotframe:
            booln = True
        else:
            booln = False
        if booln:
            if argument_type_first == "var":
                to_split = ins['args'][1]['value'].split('@')
                frame_argument_variable = to_split[0]
                name_argument_variable = to_split[1]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    argument_frame = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    argument_frame = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    argument_frame = temporary_frame_list[0]

                if frame_argument_variable == "GF":
                    if not global_frame:
                        exit_program(55, "GF does not exist.")
                    gotframe = global_frame
                elif frame_argument_variable == "LF":
                    if frame_list[-1]:
                        if not frame_list[-1]['frame'] == "LF":
                            exit_program(55, "LF does not exist.")
                    gotframe = frame_list[-1]
                elif frame_argument_variable == "TF":
                    if not temporary_frame_list:
                        exit_program(55, "TF does not exist.")
                    gotframe = temporary_frame_list[0]
                if name_argument_variable in gotframe:
                    res = True
                else:
                    res = False
                if res:
                    var_type = argument_frame[name_argument_variable]['type']
                else:
                    exit_program(54, "Variable does not exist.")
            elif argument_type_first == "int":
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "int":
                            argument_value_first = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not integers.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_first == "int":
                    argument_value_first = argument_value_first
                else:
                    exit_program(53, "Operands are not integers.")
            elif argument_type_first == "bool":
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "bool":
                            argument_value_first = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not booleans.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_first == "bool":
                    argument_value_first = argument_value_first
                else:
                    exit_program(53, "Operands are not booleans.")
            elif argument_type_first == "nil":
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "nil":
                            argument_value_first = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not nils.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_first == "nil":
                    argument_value_first = argument_value_first
                else:
                    exit_program(53, "Operands are not nils.")
            elif argument_type_first == "string":
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        if argument_frame[name_argument_variable]['type'] == "string":
                            argument_value_first = argument_frame[name_argument_variable]['value']
                        else:
                            exit_program(53, "Operands are not strings.")
                    else:
                        exit_program(54, "Variable does not exist.")
                elif argument_type_first == "string":
                    argument_value_first = argument_value_first
                else:
                    exit_program(53, "Operands are not strings.")
            else:
                exit_program(52, "Unknown type.")
            var_type = argument_type_first
            if var_type == "Unknown":
                var_type = ""

            frame[name_variable]['type'] = "string";
            frame[name_variable]['value'] = var_type
        else:
            exit_program(54, "Variable does not exist.")
    elif ins['opcode'] == "LABEL":
        ...
    elif ins['opcode'] == "JUMP":
        argument_type = ins['args'][0]['type']
        argument_value = ins['args'][0]['value']
        f = False
        idx = 0
        for each in lbs:
            if argument_value in each.keys():
                f = True
                instruction_label = argument_value
                instruction_order = int(lbs[idx][argument_value])
            idx += 1

        if f == True:
            if p_counter < instruction_order:
                while (p_counter < instruction_order):
                    p_counter += 1
                p_counter = p_counter
            else:
                while (p_counter > instruction_order):
                    p_counter -= 1
                p_counter = p_counter
        else:
            exit_program(52, "Unknown label.")
    elif ins['opcode'] == "JUMPIFEQ":
        argument_type_zero = ins['args'][0]['type']
        argument_value_zero = ins['args'][0]['type']

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']
        if argument_type_zero == "label":
            pattern_compared = re.compile("^([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$")
            m = bool(pattern_compared.match(argument_value_zero))
            if m == True:
                booln = True
            else:
                booln = False
            if booln:
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        operand_type_first = argument_frame[name_argument_variable]['type']
                        operand_first_value = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(54, "Variable does not exist.")
                else:
                    operand_type_first = argument_type_first
                    operand_first_value = argument_value_first
                if argument_type_second == "var":
                    to_split = ins['args'][2]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        operand_type_second = argument_frame[name_argument_variable]['type']
                        operand_second_value = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(54, "Variable does not exist.")
                else:
                    operand_type_second = argument_type_second
                    operand_second_value = argument_value_second
                if operand_type_first == operand_type_second:
                    if operand_first_value == operand_second_value:
                        argument_type = ins['args'][0]['type']
                        argument_value = ins['args'][0]['value']
                        f = False
                        idx = 0
                        for each in lbs:
                            if argument_value in each.keys():
                                f = True
                                instruction_label = argument_value
                                instruction_order = int(lbs[idx][argument_value])
                            idx += 1

                        if f == True:
                            if p_counter < instruction_order:
                                while (p_counter < instruction_order):
                                    p_counter += 1
                                p_counter = p_counter
                            else:
                                while (p_counter > instruction_order):
                                    p_counter -= 1
                                p_counter = p_counter
                        else:
                            exit_program(52, "Unknown label.")
                    else:
                        p_counter = p_counter
                else:
                    exit_program(53, "Relational type collision.")
            else:
                exit_program(54, "Variable does not exist.")
        else:
            exit_program(53, "Label is not valid type.")
    elif ins['opcode'] == "JUMPIFNEQ":
        argument_type_zero = ins['args'][0]['type']
        argument_value_zero = ins['args'][0]['type']

        argument_type_first = ins['args'][1]['type']
        argument_value_first = ins['args'][1]['value']

        argument_type_second = ins['args'][2]['type']
        argument_value_second = ins['args'][2]['value']

        if argument_type_zero == "label":
            pattern_compared = re.compile("^([a-zA-Z]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$")
            m = bool(pattern_compared.match(argument_value_zero))
            if m == True:
                booln = True
            else:
                booln = False
            if booln:
                if argument_type_first == "var":
                    to_split = ins['args'][1]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        operand_type_first = argument_frame[name_argument_variable]['type']
                        operand_first_value = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(54, "Variable does not exist.")
                else:
                    operand_type_first = argument_type_first
                    operand_first_value = argument_value_first
                if argument_type_second == "var":
                    to_split = ins['args'][2]['value'].split('@')
                    frame_argument_variable = to_split[0]
                    name_argument_variable = to_split[1]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        argument_frame = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        argument_frame = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        argument_frame = temporary_frame_list[0]

                    if frame_argument_variable == "GF":
                        if not global_frame:
                            exit_program(55, "GF does not exist.")
                        gotframe = global_frame
                    elif frame_argument_variable == "LF":
                        if frame_list[-1]:
                            if not frame_list[-1]['frame'] == "LF":
                                exit_program(55, "LF does not exist.")
                        gotframe = frame_list[-1]
                    elif frame_argument_variable == "TF":
                        if not temporary_frame_list:
                            exit_program(55, "TF does not exist.")
                        gotframe = temporary_frame_list[0]
                    if name_argument_variable in gotframe:
                        res = True
                    else:
                        res = False
                    if res:
                        operand_type_second = argument_frame[name_argument_variable]['type']
                        operand_second_value = argument_frame[name_argument_variable]['value']
                    else:
                        exit_program(54, "Variable does not exist.")
                else:
                    operand_type_second = argument_type_second
                    operand_second_value = argument_value_second
                if operand_type_first == operand_type_second:
                    if operand_first_value != operand_second_value:
                        argument_type = ins['args'][0]['type']
                        argument_value = ins['args'][0]['value']
                        f = False
                        idx = 0
                        for each in lbs:
                            if argument_value in each.keys():
                                f = True
                                instruction_label = argument_value
                                instruction_order = int(lbs[idx][argument_value])
                            idx += 1

                        if f == True:
                            if p_counter < instruction_order:
                                while (p_counter < instruction_order):
                                    p_counter += 1
                                p_counter = p_counter
                            else:
                                while (p_counter > instruction_order):
                                    p_counter -= 1
                                p_counter = p_counter
                        else:
                            exit_program(52, "Unknown label.")
                    else:
                        p_counter = p_counter
                else:
                    exit_program(53, "Relational type collision.")
            else:
                exit_program(54, "Variable does not exist.")
        else:
            exit_program(53, "Label is not valid type.")
    elif ins['opcode'] == "EXIT":
        ...
    elif ins['opcode'] == "DPRINT":
        ...
    elif ins['opcode'] == "BREAK":
        ...











