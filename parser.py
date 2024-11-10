import argparse
'''
The input file may contain instructions in the following types:

R type - add, sub, sll, srl, slt
I-Type - addi, beq, bne, lw, sw

'''
def dec_reg_to_binary(num): #Number parsed from register number
    num = num.replace('$','')
    num = num.replace(',','')
    if ord(num[0]) >= 0x30 or ord(num[0]) <= 0x39: #Check if the register is written as a number
        if int(num) <= 31 and int(num) >= 0: #Check if its a valid register
            num = str(bin(int(num)))
            num = num.replace('b','') #bin() adds 0b to the start of the string, so removing it
            num = num.replace('0','',1)
            if len(num) < 5:
                 for i in range(0,5-len(num)):
                    num = "0" + num
            return num #Valid Register, Return Binary Encoding
        else:
            return -1 #Error, Invalid Register 
    else:
        return -1 #Invalid Register
def get_register_binary(string): #For when the alias of a register is used
    str(string)
    string = string.replace(',', '')
    if string[0] != "$":
        return -1 #Invalid Register Name
    else:
        registers = {
            "$zero" : "00000",
            "$v0" : "00010",
            "$v1" : "00011",
            "$a0" : "00100",
            "$a1" : "00101",
            "$a2" : "00110",
            "$a3" : "00111",
            "$t0" : "01000",
            "$t1" : "01001",
            "$t2" : "01010",
            "$t3" : "01011",
            "$t4" : "01100",
            "$t5" : "01101",
            "$t6" : "01110",
            "$t7" : "01111",    
            "$s0" : "10000",
            "$s1" : "10001",
            "$s2" : "10010",
            "$s3" : "10011",
            "$s4" : "10100",
            "$s5" : "10101",
            "$s6" : "10110",
            "$s7" : "10111",
            "$t8" : "11000",
            "$t9" : "11001",
            "$gp" : "11100",
            "$sp" : "11101",
            "$fp" : "11110",
            "$ra" : "11111"
        }
        if string in registers:
            return registers[string] #Return the binary encoding of the register alias
        else: 
            return dec_reg_to_binary(string) #Try converting a register to binary through a number

def get_op_code(op):
    op_codes = {
        "addi" : "001000",
        "beq" : "000100",
        "bne" : "000101",
        "lw" :  "100011",
        "sw" : "101011"
    }
    if op in op_codes:
        return op_codes[op]
    else:
        return -1

def decimal_to_binary(val):
    valIsNeg = False
    
    val = str(val)
    if val[0] == '-':
        valIsNeg = True
        val = val[1:]
    for i in range(0,len(val)): #Check if all the characters in val are numeric
        if (ord(val[i]) >= 0x30 and ord(val[i]) <= 0x39):
            continue#if character is numeric continue
        else:
            return -1 #else return error
    val = int(val)
    if val < (-(2**15)) or val > ((2**15) - 1):
        return -1 #Val cannot be expressed in 16 bit twos compliment
    binaryVal = str(bin(val))
    binaryVal = binaryVal[2:]
    while len(binaryVal) < 16: #Make binary val 16 bits if it isn't already
        binaryVal = '0' + binaryVal
    if valIsNeg: #Find twos compliment
        newBinVal = [] #Make a list as python strings don't support item assignment 
        for i in range (0,len(binaryVal)): #newBinVal = ~binaryVal
            if binaryVal[i] == '0':
               newBinVal.append('1')
            else:
                newBinVal.append('0')
        i = len(newBinVal) - 1 #newBinVal += 1
        while newBinVal[i] != '0':
            i-= 1 #i--
            newBinVal[i+1] = '0' #add 1 to what was newBinVal[i], 1 + 1 = 10 in binary
        newBinVal[i] = '1'
        tempString = ''
        for i in range (0,len(newBinVal)):
            tempString = tempString + newBinVal[i]
        binaryVal = tempString
    return binaryVal
        
        

    
def determine_instruction(line):
    valid_instructions = { 
        #Instruction Name : Type
        "add" : "r", 
        "sub" : "r",
        "sll" : "r1",
        "srl" : "r1",
        "slt" : "r",
        "addi" : "i",
        "beq" : "i",
        "bne" : "i",
        "lw" : "i",
        "sw" : "i",
        }
    #Split the string
    parts = line.split(' ')
    newparts = []
    for part in parts: #Remove Excess Spaces
        if part != '' and part != '\n':
            newparts.append(part)
    temp = newparts[1].split(',')
    newparts.pop(1)
    for val in temp:
        newparts.append(val)
    newparts[len(newparts)-1] = newparts[len(newparts)-1].replace('\n','')

    
    parts = newparts;
    if parts[0] in valid_instructions:
        if valid_instructions[parts[0]] == "r":
            return parse_r_type(parts) #If R-Type parse as an R-type
        elif valid_instructions[parts[0]] == "r1":
            return parse_r1_type(parts) #SRL or SLL
        elif valid_instructions[parts[0]] == "i":
            return parse_i_type(parts) #If I-Type parse an I type
        else:
            return -1  #Invalid Instruction, Return error
    else:
        return -1 #Invalid Instruction Return Error
    
def parse_r_type(instruction):
    if len(instruction) != 4: #If there isn't 4 parts: op, $r1 ,$r2, $r3 exit with error
        return -1
    rs = get_register_binary(instruction[2])
    rt = get_register_binary(instruction[3])
    rd = get_register_binary(instruction[1])
    shamt = get_funct(instruction[0])
    if rs == -1:  #If one of the sub steps returns an error, return an error 
        return -1
    elif rt == -1:
        return -1
    elif rd == -1:
        return -1
    elif shamt == -1:
        return -1
    else:
        return "000000" + rs + rt + rd + shamt

def parse_r1_type(instruction): 
    if len(instruction) != 4:
        return -1
    rt = get_register_binary(instruction[2])
    rd = get_register_binary(instruction[1])
    shamt = ''
    if rt == -1:
        return -1
    if rd == -1:
        return -1
    string = instruction[3]
    for i in range (0,len(string)):
         if ord(string[i]) >= 0x30 or ord(string[i]) <= 0x39: #Ensure that all of the characters are a number.
             continue
         else:
             return -1 #If non-numeric character in string, return error
    if int(instruction[3]) > 32 or int(instruction[3]) < 0:
        return -1 #Number out of range
    else:
        shamt = str(bin(int(instruction[3])))
        shamt = shamt[2:]
        while len(shamt) < 5:
            shamt = '0' + shamt
    if instruction[0] == "sll":
        return '000000' + '00000' + rt + rd + shamt + '000000'
    else:
        return '000000' + '00000' + rt + rd + shamt + '000010'

def parse_i_type(instruction):
    i_type = ["addi", "beq", "bne", "lw", "sw"]
    if instruction[0] in i_type: 
        if instruction[0] == "lw" or instruction[0] == "sw":
            #Process for sw and lw
            temp = instruction[2].split('(')
            temp[1] = temp[1].replace(')','')
            instruction.pop()
            for val in temp:
                instruction.append(val)
            rt = get_register_binary(instruction[1])
            rs = get_register_binary(instruction[3])
            offset = decimal_to_binary(instruction[2])
            if instruction[0] == "lw":
                return "100011" + rs + rt + offset
            else:
                return "101011" + rs + rt + offset
        elif instruction[0] == "addi":
            opcode = get_op_code(instruction[0])
            rt = get_register_binary(instruction[1])
            rs  = get_register_binary(instruction[2])
            immid = decimal_to_binary(instruction[3])
            if opcode == -1:
                return -1
            elif rt == -1:
                return -1
            elif rs == -1:
                return -1
            elif immid == -1:
                return -1
            else:
                return str(opcode) + str(rs) + str(rt) + str(immid)
        elif instruction[0] == "beq" or instruction[0] == "bne":
            opcode = get_op_code(instruction[0])
            rt = get_register_binary(instruction[2])
            rs  = get_register_binary(instruction[1])
            immid = decimal_to_binary(int(int(instruction[3])/4))
            if opcode == -1:
                return -1
            elif rt == -1:
                return -1
            elif rs == -1:
                return -1
            elif immid == -1:
                return -1
            else:
                return str(opcode) + str(rs) + str(rt) + str(immid)

    else:
        return -1 #instruction isn't in i-type somehow.
    
    
    

def get_funct(rtype):
    codes = {
        "add" : "00000100000", #Funct = x20,
        "sub" : "00000100010",  #Funct = x22,
        "slt" : "00000101010" #Funct = x2A
    }
    if rtype in codes:
        return codes[rtype]
    else:
        return -1 #If somehow invalid instruction, return -1


def main():
    parser = argparse.ArgumentParser(prog = "Mips Assembly Binary Encoder", description="Takes in an input file of MIPs assembly, and")
    parser.add_argument('--file',type=str,help="Provide the filename and filepath of the input file. Example: -i ~/ecpe170-worksheet.txt")
    args = parser.parse_args()
    #Print both of the filenames and paths to the files 
    print("Input File: " + args.file)
    print("Output File: " + "out_code.txt")
    #Open both files
    inFile = open(args.file,"r")
    outFile = open("out_code.txt","w")
    #Conversion Process: converts one line at a time, 
    for line in inFile:
        if line == "\n":
            continue
        else:
            output = determine_instruction(line)
            if output == -1:
                outFile.write("!!! invalid input !!!\n")
                break
            else:
                outFile.write(str(output) +"\n")

main()
