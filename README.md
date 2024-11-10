# ECPE-170-MIPS-assembly-parser
Made this for a project in ECPE 170 at UOP where we create a python program that takes MIPS assembly instructions **add**, **sub**, **sll**, **srl**, **slt**, **addi**, **beq**, **bne**, **lw**, and **sw** then outputs the binary encoding. If there is an error in the assembly code input file the program writes "!!! invalid input!!!" to the text file and stops the program.

# Usage
In a terminal in the directory where the parser is located run `python3 parser.py --file <input>`

Your output will be in a plaintext file called `out_code.txt` in the directory of the parser.
