`timescale 1ns / 1ps

module Register_File(
        clk,
        read_addr1,
        read_addr2,
        read_data1,
        read_data2,
        write_addr,
        write_data,
        write_enable
    );

/***************************
******** PARAMETERS ********
***************************/

input wire clk;

input wire [4:0]  read_addr1;
input wire [4:0]  read_addr2;
input wire [4:0]  write_addr;

input wire [31:0] write_data;
input wire        write_enable;

output reg [31:0] read_data1;
output reg [31:0] read_data2;


// REGISTER FILE

reg [31:0] Register_File [31:0]; // 32 - 32 Bit Registers


/*************************
********* LOGIC **********
**************************/


initial
begin
        Register_File[0]=32'h00000000;
        Register_File[1]=32'h00000001;
        Register_File[2]=32'h00000010;
        Register_File[3]=32'h00000100;
        Register_File[4]=32'h00000001;
        Register_File[5]=32'h00000040;
        Register_File[6]=32'h00000200;
        Register_File[7]=32'h0000050;
        Register_File[8]=32'h00000006;
end

always @(read_addr1 or read_addr2)
    begin
    // $display("read_addr1 %d - read_addr2 -%d write_data -%h clk%b",read_addr1,read_addr2,write_data,clk);
    read_data1 = 32'h00000000;
    read_data2 = 32'h00000000;
    if (read_addr1 != 5'b11111) begin
        read_data1 = Register_File[read_addr1];
    end 
    if (read_addr2 != 5'b11111) begin
        read_data2 = Register_File[read_addr2]; 
    end
    
    end
always @(posedge clk)
    begin
    
    if (write_enable) begin
//    $display("write_addr- %d - write_enable -%d write_data -%h clk%b",write_addr,write_enable,write_data,clk);
        if (write_addr != 5'b11111) begin
            Register_File[write_addr] = write_data; 
        end
    end
    $display("REGISTER :: WRITE_ADDRESS = %d  WRITE_ENABLE = %d WRITE_DATA -%h clk%b",write_addr,write_enable,write_data,clk);  
   end
endmodule
