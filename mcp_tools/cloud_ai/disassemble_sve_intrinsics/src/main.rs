use std::env;
use std::fs::File;
use std::io::{Read, Result};

fn analyze_elf_bytes(bytes: &[u8]) -> (usize, usize, Vec<String>) {
    let mut sve_count = 0;
    let mut hardcoded_z_regs = 0;
    let mut warnings = Vec::new();

    // Basic opcode scanner detecting Arm64 SVE instruction patterns
    for chunk in bytes.chunks(4) {
        if chunk.len() == 4 {
            let insn = u32::from_le_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]);
            // SVE Encoding mask check: Bits [31:24] match SVE class pattern (0x04000000)
            if (insn & 0x0E000000) == 0x04000000 {
                sve_count += 1;
                // Check if instruction fixes Z register size instead of VLA usage
                if (insn & 0x000001F0) == 0x00000010 {
                    hardcoded_z_regs += 1;
                }
            }
        }
    }

    if hardcoded_z_regs > 0 {
        warnings.push(format!("Found {} potential hardcoded vector length assumptions.", hardcoded_z_regs));
    }

    (sve_count, hardcoded_z_regs, warnings)
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: disassemble_sve_intrinsics <elf_path>");
        std::process::exit(1);
    }

    let mut file = File::open(&args[1])?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    let (sve_count, hardcoded, _warnings) = analyze_elf_bytes(&buffer);

    println!("{{");
    println!("  \"binary\": \"{}\",", args[1]);
    println!("  \"sve_instruction_count\": {},", sve_count);
    println!("  \"hardcoded_z_reg_warnings\": {},", hardcoded);
    println!("  \"is_vla_compliant\": {}", hardcoded == 0);
    println!("}}");

    Ok(())
}
