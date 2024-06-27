`timescale 1ns / 1ps

module MainMemoryModule(
    input wire clk,
    input wire [31:0] instruction,
    input wire [31:0] address,
    input wire readEnable,
    input wire writeEnable,
    input wire [31:0] dataIn,
    output reg [31:0] dataOut
    );
reg [31:0] memory[1024*1024*1024*4-1:0];

always @(address or readEnable or writeEnable) 
    begin
    if(readEnable)
    begin
        dataOut = memory[address];
    end
    else if(writeEnable)
    begin
        memory[address] = dataIn;
    end
    else begin
        dataOut = 0;
    end
    // $display("DATA_OUT = %h , read_Enable = %b write_enable = %b,address main memory - %b",dataOut,readEnable,writeEnable,address);  
end

endmodule
