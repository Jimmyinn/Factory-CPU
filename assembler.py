def convert(instruction):
    instruction = instruction.split();
    bin_instruct = 0b0000000000000000
    ops = {"ADD":0b00100, "SUB":0b01100, "LOAD":0b10110, "STORE":0b11001}
    registers = {"r0":0b00, "r1":0b01, "r2":0b10, "r3":0b11}
    
    operation = instruction[0]
    dst = instruction[1]
    
    # 16-12th bits
    if operation in ops:
        bin_instruct = (ops[operation] << 11) | bin_instruct
    
    if operation == "ADD" or operation == "SUB":
        # check for immediate, 11th bit
        #print(instruction)
        if len(instruction) > 3 and instruction[3] not in registers:
            bin_instruct = (1 << 10) | bin_instruct
            
            # 10-9th bits, dst 1
            bin_instruct = (registers[instruction[1]] << 8) | bin_instruct
            
            # 8-7th bits, src 1
            bin_instruct = (registers[instruction[2]] << 6) | bin_instruct
            
            # 6-1st bits, immediate
            imm = int(instruction[3])
            bin_instruct = imm | bin_instruct
        else:
            bin_instruct = (0 << 10) | bin_instruct
            
            # 10-9th bits, dst 1
            bin_instruct = (registers[instruction[1]] << 8) | bin_instruct
            
            # 8-7th bits, src 1
            bin_instruct = (registers[instruction[2]] << 6) | bin_instruct
            
            # 6-5th bits, src 2
            bin_instruct = (registers[instruction[3]] << 4) | bin_instruct
            # last four bits are 0s
    if operation == "LOAD" or operation == "STORE":
        # check for immediate, 10th bit
        if instruction[2] not in registers:
            bin_instruct = (1 << 10) | bin_instruct
    
            # 10-9th bits, dst/src
            bin_instruct = (registers[instruction[1]] << 8) | bin_instruct
            
            # next two bits are left as 0s
            
            # 6-1st bits, immediate
            imm = int(instruction[2])
            bin_instruct = imm | bin_instruct      
        else:
            # this block can only be reached by LOAD
            bin_instruct = (0 << 10) | bin_instruct
            
            # 10-9th bits, dst
            bin_instruct = (registers[instruction[1]] << 8) | bin_instruct
            
            # 8-7th bits, src 1
            bin_instruct = (registers[instruction[2]] << 6) | bin_instruct
            
            # last 6 bits are 0s for LOAD
    print(instruction, hex(bin_instruct))
    return hex(bin_instruct)

if __name__ == "__main__":
    instructions = open("project2.txt", 'r')
    assembled_instructions = open("assembled.txt", 'w')
    
    assembled_instructions.write("v3.0 hex words addressed\n00: 0000 ")
    
    pc = 1
    for instruction in instructions:
        if instruction == "" or instruction == "\n":
            continue
        if pc != 0 and pc % 16 == 0 and pc <= 0xf0:
            assembled_instructions.write("\n" + hex(pc)[2:] + ": ")
        assembled_instructions.write(convert(instruction)[2:] + " ")
        pc += 1
    
    instructions.close()
    assembled_instructions.close()