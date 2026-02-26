#ifndef HASHING_H
#define HASHING_H

#include <string>

// DJB2 Hashing Algorithm: highly efficient for system-level C++ apps
inline std::string calculateDJB2Hash(const std::string& input) {
    unsigned long hash = 5381;
    for (char c : input) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return std::to_string(hash);
}

#endif