`timescale 1ns / 1ps

module regmux3x1(in0, in1,in2,select, out);
    input wire [1:0] select; 
    input wire [4:0] in0;
    input wire [4:0] in1;
    input wire [4:0] in2;
    output reg[4:0] out;

    always @(*)
    begin
        if(select == 0)
        begin
            out <= in0;
        end
        else if(select == 1) 
        begin
            out <= in1;
        end else
        begin
            out <= in2;
        end
    end

endmodule
