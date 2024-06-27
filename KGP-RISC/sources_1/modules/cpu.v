`timescale 1ns / 1ps

module cpu(
    input clk,
    input rst
);
    wire [31:0] alu_operand;
    wire [31:0] alu_otp;
    wire [31:0] pc_instaddr;
    wire [31:0] instruction;
    wire [31:0] sign_extend;
    wire [31:0] reg1data;
    wire [31:0] reg2data;
    wire [31:0] regwrdata;
    wire [31:0] data_mem_in;
    wire [31:0] data_mem_out;  
    wire [31:0] st_mem_out;
    wire [31:0] mem_write_data;
    wire [1:0]  pcControl;
    wire [3:0]  alu_op;
    wire [4:0]  reg_radd0;
    wire [4:0]  reg_radd1;
    wire [4:0]  reg_waddr;
    wire [5:0]  alu_control_otp;
    wire [1:0]  reg_wr_add_control; // updated
    wire [1:0]  datawr_select;      // updated
    wire        datamem_readen;
    wire        datamemwriteen;
    wire        alusrcselect;
    wire        reg_wr_en;
    wire        branch_control;
    // wire        jump_control;
    wire        alu_zero;
    wire        overflow_signal;
    wire        push;
    wire        pop;
    wire        mem_wsel;

    
    ProgramCounter prcount (
        .clk(clk),
        .reset(rst),
        .zero(alu_zero),
        .branch(branch_control),
        // .jump(jump_control),
        .jumpAddress(instruction[25:0]),
        .branchOffset(instruction[15:0]),
        .regAddress(reg1data),
        .pc(pc_instaddr)
    );
        
    InstructionMemoryModule instructionMemory(
        .clk(clk),
        .address(pc_instaddr),
        .readEnable(1'b1),
        .writeEnable(1'b0),
        .dataIn(32'h000000),
        .dataOut(instruction)
    );
        
    control_unit signals(
        .instruction(instruction),
        .RegDst(reg_wr_add_control),
        .MemRead(datamem_readen),
        .MemToReg(datawr_select),
        .ALUOp(alu_op),
        .MemWrite(datamemwriteen),
        .ALUSrc(alusrcselect),
        .RegWrite(reg_wr_en),
        .Branch(branch_control),
        .Push(push_en),
        .Pop(pop_en),
        .Mem_Wsel(mem_wsel)
    );

    assign reg_radd0 = instruction[25:21];

    assign reg_radd1 = instruction[20:16];
    
    
    regmux3x1 reg_wr_dst(
        .select(reg_wr_add_control),
        .in0(reg_radd0),                        //rs = 0, rt = 1, rd = 2
        .in1(reg_radd1),                        //There should be reg_radd0
        .in2(instruction[15:11]),
        .out(reg_waddr)
    );

    Register_File regfile(
        .clk(clk),
        .read_addr1(reg_radd0),
        .read_addr2(reg_radd1),
        .write_addr(reg_waddr),
        .write_data(regwrdata),
        .write_enable(reg_wr_en),
        .read_data1(reg1data),
        .read_data2(reg2data)
    );

    signExtension sign(
        .in(instruction[15:0]),
        .out(sign_extend)
    );

    mux2x1 alusrc_select(
        .select(alusrcselect),
        .in0(reg2data),
        .in1(sign_extend),
        .out(alu_operand)
    );
        
    alu_control alucntrl(
        .instruction(instruction),
        .ALUOp(alu_op),
        .ALUFn(alu_control_otp)
    );
        
    ALU alu(
        .clk(clk),
        .instruction(instruction),
        .a(reg1data),
        .b(alu_operand),
        .alufn(alu_control_otp),
        .otp(alu_otp),
        .zero(alu_zero),
        .overflow(overflow_signal)
    );
    mux2x1 mem_write(
        .select(mem_wsel),  //Control signals for that
        .in0(reg2data),
        .in1(st_mem_out),
        .out(mem_write_data)

    );
    
    MainMemoryModule data_mem(.clk(clk),
        .address(alu_otp),
        .instruction(instruction),
        .readEnable(datamem_readen),
        .writeEnable(datamemwriteen),
        .dataIn(data_mem_in),
        .dataOut(data_mem_out)
    );

    mux3x1 write_select(.select(datawr_select),
        .in0(alu_otp),
        .in1(data_mem_out),
        .in2(st_mem_out),  
        .out(regwrdata)
    );
    
    StackMemory data_stack(
        .clk(clk),
        .reset(rst),
        .push(push_en),
        .pop(pop_en),
        .data_in(regwrdata),
        .data_out(st_mem_out)  // *********** Important ***************
    );

    
    assign data_mem_in = mem_write_data;
    always @(posedge clk)
        begin
            $display("reg_radd0- %d - reg_radd1 - %d",reg_radd0,reg_radd1);
            $display("INSTRUCTION=%h - reg1data=%h - reg2data=%h  - alu_control_otp=%d - datamemwriteen=%d - data_mem_in=%d - alu_otp=%h",
                instruction, 
                reg1data, 
                reg2data,
                alu_control_otp,
                datamemwriteen,
                data_mem_in,
                alu_otp);
        end
endmodule
