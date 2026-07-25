#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>

struct PipelineStats {
    int total_instructions = 0;
    int sve_instructions = 0;
    int memory_hazards = 0;
    int estimated_stall_cycles = 0;
};

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: analyze_neoverse_sve_pipeline <assembly_file>\n";
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open assembly file: " << argv[1] << "\n";
        return 1;
    }

    PipelineStats stats;
    std::string line;
    std::regex sve_regex(R"(\b(ptrue|ld1w|st1w|fmla|z[0-9]+|p[0-9]+)\b)", std::regex::icase);
    std::regex mem_hazard_regex(R"(\b(ldr|str|ld1w|st1w)\b)", std::regex::icase);

    bool prev_was_mem = false;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '.' || line[0] == '/') continue;

        stats.total_instructions++;
        if (std::regex_search(line, sve_regex)) {
            stats.sve_instructions++;
        }

        bool is_mem = std::regex_search(line, mem_hazard_regex);
        if (is_mem && prev_was_mem) {
            stats.memory_hazards++;
            stats.estimated_stall_cycles += 2; // Neoverse load-store unit pipeline conflict
        }
        prev_was_mem = is_mem;
    }

    std::cout << "{\n"
              << "  \"total_instructions\": " << stats.total_instructions << ",\n"
              << "  \"sve_instructions\": " << stats.sve_instructions << ",\n"
              << "  \"memory_hazards\": " << stats.memory_hazards << ",\n"
              << "  \"estimated_stall_cycles\": " << stats.estimated_stall_cycles << "\n"
              << "}\n";
    return 0;
}
