`timescale 1ns / 1ps

module ALU(clk,a, b, instruction,alufn, otp, zero, overflow);
    input wire clk;
    input wire [31:0] a;
    input wire [31:0] b;
    input wire [31:0] instruction;
    input wire [5:0] alufn; // choosing 6 bit op code
    output reg [31:0] otp;
    output reg zero; // set if the output of the alu is 0
    output reg overflow;
    wire [31:0] tempAuRes;
    wire [31:0] tempLuRes;
    wire [31:0] tempSuRes;
    wire tempAuZero,tempAuOverflow;
    wire tempLuZero,tempLuOverflow;
    wire tempSuZero,tempSuOverflow;
    
    always @(a or b or alufn or instruction)
    begin
        // $display("a%h - b%h",a,b);
        // $display("tempAuRes- %h",tempAuRes);
        casex(alufn)
            6'b0000xx: begin
        if(alufn[1:0] == 2'b00)
            begin //ADD
                otp = a + b;
                zero = (otp==0)?1:0;
                if ((a >= 0 && b >= 0 && otp < 0) || (a < 0 && b < 0 && otp >= 0))
                    overflow = 1;
                else
                    overflow = 0;
                // $display("a%h - b%h - otp %h",a,b,otp);
            end
        else if(alufn[1:0] == 2'b01) //SUB
            begin
                otp = a-b;
                zero = (otp==0)?1:0;
                if ((a >= 0 && b < 0 && otp < 0) || (a < 0 && b >= 0 && otp > 0))
                    overflow = 1;
                else
                    overflow = 0;
            end
        else if (alufn[1:0] == 2'b10) //PASS
            begin
                otp = a;
                zero = (otp==0)?1:0;
                overflow = 0;
            end
    end
        6'b0001xx: begin
        case (alufn[1:0])
        2'b00: //AND
            begin
                otp = a & b;
                overflow = 0;
                zero = (otp==0)?1:0;
            end
        2'b01: //OR
            begin
                otp = a | b;
                overflow = 0;
                zero = (otp==0)?1:0;
            end
        2'b10:  //XOR
                begin
                    otp = a ^ b;
                    overflow = 0;
                    zero = (otp==0)?1:0;
                end
        2'b11: //NOT
                begin
                    otp = ~a;
                    overflow = 0;
                    zero = (otp==0)?1:0;
                end
        endcase
    end
        6'b0010xx: begin
        case(alufn[1:0])
        2'b00: //SLA
            begin
                otp = a <<< b[0];
                zero = (otp == 0)?1:0;
                overflow = 0;
            end
        2'b01: //SRA
            begin
                otp = a >>> b[0];
                zero = (otp == 0)?1:0;
                overflow = 0;
            end
        2'b10: //SRL
            begin
                otp = a << b[0];
                zero = (otp == 0)?1:0;
                overflow = 0;
            end
        endcase
    end
        6'b0011xx: begin
        case(alufn[1:0])
        2'b00: //Zero = 1:: BZ
            begin
                otp = 1;
                zero = 1;
                overflow = 0;
            end
        2'b01: // a < 0
            begin
                otp = a;
                zero = (otp < 0)?1:0;
                overflow = 0;
            end
        2'b10: //a > 0
            begin
                otp = a ;
                zero = (otp > 0)?1:0;
                overflow = 0;
            end
        2'b11: //a = 0
            begin
                otp = a ;
                zero = (otp == 0)?1:0;
                overflow = 0;
            end
        endcase
    end
        default:
            begin 
                otp = {32{1'b0}};
            end
        endcase
        $display("ALU :: a%h (alufn%b) b%h = otp %h ",a,alufn,b,otp);
    end

endmodule

// module ArithmeticUnit(a,b,alufn,otp,zero,overflow);
//     input wire [31:0] a;
//     input wire [31:0] b;
//     input wire [1:0] alufn; // choosing 6 bit op code
//     output reg [31:0] otp;
//     output reg zero; // set if the output of the alu is 0
//     output reg overflow;
    
//     always @(alufn or a or b)
//     begin
//         $display("a%h - b%h - otp %h alufn %b",a,b,otp,alufn);
//         if(alufn == 2'b00)
//             begin //ADD
//                 otp = a + b;
//                 zero = (otp==0)?1:0;
//                 if ((a >= 0 && b >= 0 && otp < 0) || (a < 0 && b < 0 && otp >= 0))
//                     overflow = 1;
//                 else
//                     overflow = 0;
//                 $display("a%h - b%h - otp %h",a,b,otp);
//             end
//         else if(alufn == 2'b01) //SUB
//             begin
//                 otp = a-b;
//                 zero = (otp==0)?1:0;
//                 if ((a >= 0 && b < 0 && otp < 0) || (a < 0 && b >= 0 && otp > 0))
//                     overflow = 1;
//                 else
//                     overflow = 0;
//             end
//         else if (alufn == 2'b10) //MUL
//             begin
//                 otp = a*b;
//                 zero = (otp==0)?1:0;
//                 overflow = 0;
//             end
//     end
// endmodule

// module LogicalUnit(a,b,otp,alufn,zero,overflow);
//     input wire [31:0] a;
//     input wire [31:0] b;
//     input wire [1:0] alufn;
//     output reg zero;
//     output reg overflow;
//     output reg [31:0] otp;
    
//     always @(a,b,alufn)
//     begin
//         case (alufn)
//         2'b00: //AND
//             begin
//                 otp = a & b;
//                 overflow = 0;
//                 zero = (otp==0)?1:0;
//             end
//         2'b01: //OR
//             begin
//                 otp = a | b;
//                 overflow = 0;
//                 zero = (otp==0)?1:0;
//             end
//         2'b10:  //XOR
//                 begin
//                     otp = a ^ b;
//                     overflow = 0;
//                     zero = (otp==0)?1:0;
//                 end
//         endcase
//     end
// endmodule

// module ShiftUnit(a,b,otp,alufn,zero,overflow);
//     input wire [31:0] a;
//     input wire [31:0] b;
//     input wire [1:0] alufn;
//     output reg zero;
//     output reg overflow;
//     output reg [31:0] otp;
    
//     always @(a,b,alufn)
//     begin
//         case(alufn)
//         2'b00: //SHIFTLEFT
//             begin
//                 otp = a<<b;
//                 zero = (otp == 0)?1:0;
//                 overflow = 0;
//             end
//         2'b01: //shiftright
//             begin
//                 otp = a>>b;
//                 zero = (otp == 0)?1:0;
//                 overflow = 0;
//             end
//         2'b11: //slt
//             begin
//                 otp = (a<b)? 1:0;
//                 zero = (otp == 0)?1:0;
//                 overflow = 0;
//             end
//         endcase
//     end
// endmodule   
