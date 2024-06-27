module StackMemory (
    input wire clk,        // Clock signal
    input wire reset,        // Reset signal
    input wire push,       // Push control signal (write data to stack)
    input wire pop,        // Pop control signal (read data from stack)
    input wire [31:0] data_in,  // Data to be written to the stack
    output reg [31:0] data_out  // Data read from the stack
);

    parameter DEPTH = 64;  // Depth of the stack memory
    reg [31:0] mem [0:DEPTH-1];  // Stack memory with 64 words of 32 bits each
    reg [5:0] stack_addr; // Address for stack memory

    // Initialize stack_addr to 0
    initial begin
        stack_addr = 6'b000000;
    end

    always @(posedge clk) begin
        // Write operation (push)
        if (push) begin
            mem[stack_addr] <= data_in;
            stack_addr <= stack_addr + 1;
        end
        // Read operation (pop)
        if (pop) begin
            stack_addr <= stack_addr - 1;
            data_out <= mem[stack_addr];
        end
        if (reset)begin
            stack_addr = 6'b000000;
        end
        $display("STACK :: Stack_add = %b, PUSH = %b, POP = %b, DATA_IN = %h",stack_addr,push,pop,data_in);
    end
endmodule
