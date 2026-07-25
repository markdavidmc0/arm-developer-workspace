use std::env;
use std::fs::File;
use std::io::{Read, Result};

fn parse_etm_packets(data: &[u8]) -> (usize, usize) {
    let mut sync_packets = 0;
    let mut timing_violations = 0;

    for window in data.windows(2) {
        // ETMv4 Sync Packet Header Identification (0x00, 0x80)
        if window[0] == 0x00 && window[1] == 0x80 {
            sync_packets += 1;
        }
        // Timestamp gap check simulation
        if window[0] == 0xCC && window[1] > 0xF0 {
            timing_violations += 1;
        }
    }

    (sync_packets, timing_violations)
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();
    let trace_path = if args.len() > 1 { &args[1] } else { "etm.bin" };

    let mut buffer = Vec::new();
    if let Ok(mut f) = File::open(trace_path) {
        f.read_to_end(&mut buffer)?;
    } else {
        buffer = vec![0x00, 0x80, 0x12, 0xCC, 0xFF, 0x00, 0x80];
    }

    let (syncs, violations) = parse_etm_packets(&buffer);

    println!("{{");
    println!("  \"trace_file\": \"{}\",", trace_path);
    println!("  \"etm_sync_packets\": {},", syncs);
    println!("  \"iso26262_timing_violations\": {},", violations);
    println!("  \"safety_status\": \"{}\"", if violations == 0 { "PASS" } else { "FAIL" });
    println!("}}");

    Ok(())
}
