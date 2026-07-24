#include <vector>
#include <iostream>
#include <chrono>
#include <cstdint>

struct CacheLine {
    bool valid = false;
    uint64_t tag = 0;
    uint64_t last_used = 0;
};

// Naive Set-Associative Cache Simulation Loop (Target for Architecture & Modeling Engineers)
// Simulates cache hits/misses for a sequence of memory addresses.
void simulate_cache_accesses(const std::vector<uint64_t>& addresses, std::vector<std::vector<CacheLine>>& cache, 
                             int num_sets, int associativity, uint64_t& hits, uint64_t& misses) {
    uint64_t cycle = 0;
    for (uint64_t addr : addresses) {
        cycle++;
        uint64_t set_index = (addr >> 6) % num_sets; // 64-byte cache lines
        uint64_t tag = addr >> (6 + 8); // Assuming 256 sets (8 bits set index)
        
        bool hit = false;
        std::vector<CacheLine>& set = cache[set_index];
        
        // Linear scan through set lines (Associativity) - target for optimization
        for (int i = 0; i < associativity; ++i) {
            if (set[i].valid && set[i].tag == tag) {
                hit = true;
                set[i].last_used = cycle;
                hits++;
                break;
            }
        }
        
        if (!hit) {
            misses++;
            // Find victim (LRU replacement)
            int victim_idx = 0;
            uint64_t min_cycle = cycle;
            for (int i = 0; i < associativity; ++i) {
                if (!set[i].valid) {
                    victim_idx = i;
                    break;
                }
                if (set[i].last_used < min_cycle) {
                    min_cycle = set[i].last_used;
                    victim_idx = i;
                }
            }
            set[victim_idx].valid = true;
            set[victim_idx].tag = tag;
            set[victim_idx].last_used = cycle;
        }
    }
}

int main() {
    const int NUM_SETS = 256;
    const int ASSOCIATIVITY = 8; // 8-way set associative
    const size_t NUM_ACCESSES = 100000;
    
    std::vector<uint64_t> addresses(NUM_ACCESSES);
    // Generate a sequence of memory accesses with temporal and spatial locality
    for (size_t i = 0; i < NUM_ACCESSES; ++i) {
        if (i % 10 < 7) {
            addresses[i] = (i % 50) * 64; // High temporal locality
        } else {
            addresses[i] = i * 1024; // Strided accesses (misses)
        }
    }

    std::vector<std::vector<CacheLine>> cache(NUM_SETS, std::vector<CacheLine>(ASSOCIATIVITY));
    uint64_t hits = 0, misses = 0;

    auto start = std::chrono::high_resolution_clock::now();
    simulate_cache_accesses(addresses, cache, NUM_SETS, ASSOCIATIVITY, hits, misses);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Cache Simulator executed in: " << duration.count() << " ms" << std::endl;
    std::cout << "Total Hits: " << hits << " | Total Misses: " << misses << std::endl;
    return 0;
}
