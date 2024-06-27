`timescale 1ns / 1ps

module control_unit(
    input [31:0] instruction,
    output reg [1:0] RegDst,    // Destination for I and R type instruction
    output reg       ALUSrc,    // Decides between Register input to ALU and I Type add immediate
    output reg [1:0] MemToReg,  // Decides between SW and ALU output
    output reg       RegWrite,  // Write enable for Register File
    output reg       MemRead,   // Read from data memory
    output reg       MemWrite,  // Write to data memory
    output reg       Branch,    // 1 if instruction is beq and thus decides Program Counter
    output reg [3:0] ALUOp,     // ALU Opcode
    output reg       Push,       // 1
    output reg       Pop,       // 1 
    output reg       Mem_Wsel       // 1 

);

wire [5:0] opcode;
assign opcode = instruction [31:26];
reg [16:0]  controlSignals[63:0];

initial
begin
    controlSignals[6'b000000] = 16'b1000010000010000;   //rtype
    controlSignals[6'b000001] = 16'b0010010000000000;   //ADDI
    controlSignals[6'b000010] = 16'b0010010000001000;   //SUBI
    controlSignals[6'b000011] = 16'b0010010000100000;   //ANDI
    controlSignals[6'b000100] = 16'b0010010000101000;   //ORI
    controlSignals[6'b000101] = 16'b0010010000110000;   //XORI
    controlSignals[6'b000110] = 16'b0010010000111000;   //SLAI
    controlSignals[6'b000111] = 16'b0010010001000000;   //SRAI
    controlSignals[6'b001000] = 16'b0010010001001000;   //SRLI
    controlSignals[6'b001001] = 16'b0110110101010000;   //LD
    controlSignals[6'b001010] = 16'b0010001001010000;   //ST
    controlSignals[6'b001011] = 16'b0010100101010100;   //LDSP            ///Mem to reg will be passed to both stack and registers.
    controlSignals[6'b001100] = 16'b0010001001010011;   //STSP
    controlSignals[6'b001101] = 16'b0000000011011000;   //BR
    controlSignals[6'b001110] = 16'b0000000011011000;   //BMI
    controlSignals[6'b001111] = 16'b0000000011011000;   //BPL
    controlSignals[6'b010000] = 16'b0000000011011000;   //BZ
    controlSignals[6'b010001] = 16'b0100010001100000;   //MOVE
    controlSignals[6'b010010] = 16'b0000000001100100;   //PUSH
    controlSignals[6'b010011] = 16'b0001010000000010;   //POP
    controlSignals[6'b010100] = 16'b0000000001100100;   //CALL
    controlSignals[6'b010101] = 16'b0001010000000010;   //RET

end
    // controlSignals[6'b000000] = 10|0|00|1|0|0|0||0010|0|0|0
    
    // controlSignals[6'b000001] = 00|1|00|1|0|0|0||0000|0|0|0
    // controlSignals[6'b000010] = 00|1|00|1|0|0|0||0001|0|0|0
    // controlSignals[6'b000011] = 00|1|00|1|0|0|0||0100|0|0|0
    // controlSignals[6'b000100] = 00|1|00|1|0|0|0||0101|0|0|0
    // controlSignals[6'b000101] = 00|1|00|1|0|0|0||0110|0|0|0
    // controlSignals[6'b000110] = 00|1|00|1|0|0|0||0111|0|0|0
    // controlSignals[6'b000111] = 00|1|00|1|0|0|0||1000|0|0|0
    // controlSignals[6'b001000] = 00|1|00|1|0|0|0||1001|0|0|0

    // controlSignals[6'b001001] = 01|1|01|1|0|1|0||1010|0|0|0
    // controlSignals[6'b001010] = 00|1|00|0|1|0|0||1010|0|0|0
    // controlSignals[6'b001011] = 00|1|01|0|0|1|0||1010|1|0|0 ///Mem to reg will be passed to both stack and registers.
    // controlSignals[6'b001100] = 00|1|00|0|1|0|0||1010|0|1|1

    // controlSignals[6'b001101] = 00|0|00|0|0|0|1||1011|0|0|0
    // controlSignals[6'b001110] = 00|0|00|0|0|0|1||1011|0|0|0
    // controlSignals[6'b001111] = 00|0|00|0|0|0|1||1011|0|0|0
    // controlSignals[6'b010000] = 00|0|00|0|0|0|1||1011|0|0|0

    // controlSignals[6'b010001] = 01|0|00|1|0|0|0||1100|0|0|0

    // controlSignals[6'b010010] = 00|0|00|0|0|0|0||1100|1|0|0
    // controlSignals[6'b010011] = 00|0|10|1|0|0|0||0000|0|1|0
    // controlSignals[6'b000000] = 0

always @(instruction)
    begin
    #5;
        RegDst   = controlSignals[opcode][15:14];//2 bits
        ALUSrc   = controlSignals[opcode][13]; //1 bits
        MemToReg = controlSignals[opcode][12:11]; // 2bits 00->Alu , 01-> Mem out , 10-> stack_out
        RegWrite = controlSignals[opcode][10]; // 1 bits
        MemWrite = controlSignals[opcode][9]; // 1 bits
        MemRead  = controlSignals[opcode][8]; // 1 bits
        Branch   = controlSignals[opcode][7]; // 1 bits
        ALUOp    = controlSignals[opcode][6:3]; // 4 bits
        Push     = controlSignals[opcode][2];   // 1bits
        Pop      = controlSignals[opcode][1];   // 1bits
        Mem_Wsel = controlSignals[opcode][0];   // 1 bits
        $display("CONTROL UNIT :: control signals = %b,Instructions = %b ,opcode = %b ,RegDst = %d, MemtoReg = %d, Memwrite = %d, ALU = %d",controlSignals[opcode],instruction,opcode,RegDst,MemToReg,MemWrite,ALUOp);
    end
endmodule
