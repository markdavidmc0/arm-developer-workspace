#include <stdio.h>
#include <stdlib.h>

typedef struct {
    size_t text_bytes;
    size_t data_bytes;
    size_t bss_bytes;
    size_t cmsis_scratchpad_bytes;
} ElfMemory;

int main(int argc, char** argv) {
    const char* elf_path = (argc > 1) ? argv[1] : "firmware.elf";
    int tcm_limit_kb = (argc > 2) ? atoi(argv[2]) : 128;

    // Simulate reading Cortex-M ELF sections
    ElfMemory mem = {
        .text_bytes = 48512,
        .data_bytes = 2048,
        .bss_bytes = 18432,
        .cmsis_scratchpad_bytes = 32768
    };

    size_t total_ram_used = mem.data_bytes + mem.bss_bytes + mem.cmsis_scratchpad_bytes;
    size_t tcm_limit_bytes = tcm_limit_kb * 1024;

    printf("{\n");
    printf("  \"elf_binary\": \"%s\",\n", elf_path);
    printf("  \"flash_text_kb\": %.2f,\n", mem.text_bytes / 1024.0);
    printf("  \"ram_total_kb\": %.2f,\n", total_ram_used / 1024.0);
    printf("  \"tcm_limit_kb\": %d,\n", tcm_limit_kb);
    printf("  \"tcm_overflow\": %s\n", (total_ram_used > tcm_limit_bytes) ? "true" : "false");
    printf("}\n");

    return 0;
}
