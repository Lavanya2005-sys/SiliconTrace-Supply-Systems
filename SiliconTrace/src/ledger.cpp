/**
 * @file ledger.cpp
 * @brief High-performance ledger for tracking semiconductor wafer batches.
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include "../include/hashing.h"

using namespace std;

// Struct to represent a batch of silicon wafers
struct WaferBatch {
    int batchID;
    string stage; 
    string timestamp;
    string prevHash;
    string currentHash;

    void generateHash() {
        stringstream ss;
        ss << batchID << stage << timestamp << prevHash;
        currentHash = calculateDJB2Hash(ss.str());
    }
};

class SiliconLedger {
private:
    vector<WaferBatch> chain;

public:
    SiliconLedger() {
        WaferBatch genesis = {1001, "Raw_Silicon_Ingot", "2026-02-26", "0", ""};
        genesis.generateHash();
        chain.push_back(genesis);

        cout << "[INIT] Genesis Block Created. Hash: "
             << genesis.currentHash << endl;
    }

    void addStage(string stageName) {
        WaferBatch nextBatch;
        nextBatch.batchID = chain.back().batchID;
        nextBatch.stage = stageName;
        nextBatch.timestamp = "2026-02-27";
        nextBatch.prevHash = chain.back().currentHash;
        nextBatch.generateHash();

        chain.push_back(nextBatch);

        cout << "[UPDATE] Stage: "
             << stageName
             << " | Hash: "
             << nextBatch.currentHash
             << endl;
    }

    void verifyLedger() {
        bool compromised = false;

        for (size_t i = 1; i < chain.size(); i++) {
            if (chain[i].prevHash != chain[i - 1].currentHash) {
                cout << "[ERROR] Ledger compromised at stage: "
                     << chain[i].stage << endl;
                compromised = true;
                break;
            }
        }

        ofstream jsonFile("ledger_output.json");

        if (!compromised) {
            cout << "[SUCCESS] Ledger integrity verified successfully." << endl;
            jsonFile << "{\n";
            jsonFile << "  \"status\": \"verified\",\n";
            jsonFile << "  \"total_stages\": " << chain.size() << "\n";
            jsonFile << "}";
        } else {
            jsonFile << "{\n";
            jsonFile << "  \"status\": \"compromised\",\n";
            jsonFile << "  \"total_stages\": " << chain.size() << "\n";
            jsonFile << "}";
        }

        jsonFile.close();
    }
};

int main() {
    cout << "=== SiliconTrace Provenance Engine ===" << endl;

    SiliconLedger supplyLedger;

    supplyLedger.addStage("5nm_Fabrication");
    supplyLedger.addStage("Advanced_Packaging");
    supplyLedger.addStage("Quality_Control");
    supplyLedger.addStage("Shipment_to_OEM");

    supplyLedger.verifyLedger();

    cout << "=== Ledger Verification Complete ===" << endl;

    return 0;
}