`timescale 1ns / 1ps

module InstructionMemoryModule(
    input wire clk,
    input wire [31:0] address,
    input wire readEnable,
    input wire writeEnable,
    input wire [31:0] dataIn,
    output reg [31:0] dataOut
    );
reg [31:0] memory[8191:0];

initial 
begin
    // memory[0] <= 32'b11000000000000000000000000000010;//jump
    // memory[0] <= 32'b01001100001000010000000000000001;// branch
    //memory[1] <= 32'b01011000100000100000000000000001; //sw value of R2 in memory address in R4 
    //memory[2] <= 32'b00000000001000100001100000000010;
    // memory[4] <= 32'b01001100001000100000000000000011;
    // memory[6] <= 32'b00000000100001010010100000000001;
    // memory[7] <= 32'b00000000100000010000100000000000;
    // memory[8] <= 32'b00000001000000010001000000000001;
    //memory[7] <= 32'b01001100010000000000000000000000; // 
    
    memory[0] <= 32'b00000000011000100000100000000000; //ADD $r1,$r2,$r3
    memory[1] <= 32'b00000000110001010010000000000000; //ADD $r4,$r5,$r6
    memory[2] <= 32'b00000000100000010000100000000001; //SUB $r1,$r1,$r4
    memory[3] <= 32'b00000100001000000000000001000000; //ADDI $r1,0x40
    memory[4] <= 32'b00111100001000000000000000000001;  //BPL $r1,branch
    memory[5] <= 32'b00000100101000000000000000010000;//ADDI $r5,0x10
    memory[6] <= 32'b01001000110000000000000000000000; // PUSH $r6
    memory[7] <= 32'b00000000010001100000100000000000; //ADD $r1,$r2,$r6
    memory[8] <= 32'b00101000000001000000000000000000; //ST $r4, 1($r0)
    memory[9] <= 32'b00100100000000010000000000000000; //LD $r1, 1($r0)
end
always @(address) 
    begin
    dataOut = memory[address]; 
    $display("INSTRUCT_MEM :: dataout - %b address- %d",dataOut,address); 
end


endmodule
