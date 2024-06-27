`timescale 1ns / 1ps

module mux2x1(in0, in1,select, out);
    input wire select;
    input wire [31:0] in0;
    input wire [31:0] in1;
    output reg[31:0] out;

    always @(*)
    begin
        if(select == 2'b00)
        begin
            out <= in0;
        end
        else 
        begin
            out <= in1;
        end
    end


endmodule