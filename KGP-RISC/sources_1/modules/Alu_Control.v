`timescale 1ns / 1ps

module alu_control(
    input      [31:0] instruction,
    input      [3:0]  ALUOp,
    output reg [5:0]  ALUFn
);

wire [5:0] opcde;
assign opcde = instruction[31:26];

always @(instruction or ALUOp)
begin
    if (ALUOp == 4'b0010) begin
        ALUFn <= instruction[5:0];
    end else if (ALUOp == 4'b0000) begin   //ADD
        ALUFn <= 6'b000000;
    end else if (ALUOp == 4'b1011 & opcde == 6'b001101 ) begin    //BRANCh all branches
        ALUFn <= 6'b001100;  // Z = 1
    end else if (ALUOp == 4'b1011 & opcde == 6'b001110 ) begin
        ALUFn <= 6'b001101;  // a>0 ? z= 1
    end else if (ALUOp == 4'b1011 & opcde == 6'b001111 ) begin
        ALUFn <= 6'b001110;
    end else if (ALUOp == 4'b1011 & opcde == 6'b010000 ) begin
        ALUFn <= 6'b001111; // z = 0;
    end else if (ALUOp == 4'b1100) begin    // Move
        ALUFn <= 6'b000010;  // PASS
    end else if (ALUOp == 4'b1010) begin    // LD, SW, LDSP, SWSP
        ALUFn <= 6'b000000;  // add
    end else if (ALUOp == 4'b0111) begin    // SLA
        ALUFn <= 6'b100000;  // shift
    end else if (ALUOp == 4'b1000) begin    // SRA
        ALUFn <= 6'b100001;  // shift
    end else if (ALUOp == 4'b1001) begin    // SRL
        ALUFn <= 6'b100010;  // sfhit
    end 

    
     else if (ALUOp == 4'b0001)begin  //SuB
        ALUFn <= 6'b000001; //Subtract
    end else if (ALUOp == 4'b0100)begin //AND
        ALUFn <= 6'b000100;
    end else if (ALUOp == 4'b0101)begin //OR
        ALUFn <= 6'b000101;
    end else if (ALUOp == 4'b0110)begin  //XOR
        ALUFn <= 6'b000110;
    end 
end

endmodule
