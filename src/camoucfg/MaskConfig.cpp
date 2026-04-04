#include "MaskConfig.hpp"
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <mutex>

namespace camoufox {

MaskConfig& MaskConfig::Get() {
    static MaskConfig instance;
    return instance;
}

void MaskConfig::Initialize() {
    std::lock_guard<std::mutex> lock(mutex_);

    // Read the number of configuration chunks
    auto count_str = ReadFromEnvironment("CAMOU_CONFIG_COUNT");
    if (!count_str) {
        std::cerr << "Warning: CAMOU_CONFIG_COUNT not set. No configuration loaded." << std::endl;
        return;
    }

    int count = std::stoi(*count_str);
    std::string full_config;

    // Reassemble the full JSON configuration from chunks
    for (int i = 1; i <= count; ++i) {
        std::string key = "CAMOU_CONFIG_" + std::to_string(i);
        auto chunk = ReadFromEnvironment(key);
        if (chunk) {
            full_config += *chunk;
        } else {
            std::cerr << "Warning: Missing configuration chunk " << i << std::endl;
        }
    }

    // TODO: Parse the full_config JSON and populate config_map_
    // This would use a JSON parser like nlohmann/json or RapidJSON
    // For now, we'll implement a simple parsing logic

    // Clear existing config
    config_map_.clear();

    // Example: Simple key-value parsing (replace with proper JSON parser)
    // parse_json_into_map(full_config, config_map_);

    std::cout << "MaskConfig initialized with " << config_map_.size() << " configuration entries" << std::endl;
}

std::optional<std::string> MaskConfig::ReadFromEnvironment(const std::string& key) {
    const char* val = std::getenv(key.c_str());
    if (val && val[0] != '\0') {
        return std::string(val);
    }
    return std::nullopt;
}

std::optional<std::string> MaskConfig::GetString(const std::string& key) {
    std::lock_guard<std::mutex> lock(mutex_);
    auto it = config_map_.find(key);
    if (it != config_map_.end()) {
        return it->second;
    }
    return std::nullopt;
}

std::optional<int32_t> MaskConfig::GetInt32(const std::string& key) {
    auto str_val = GetString(key);
    if (!str_val) {
        return std::nullopt;
    }
    try {
        return std::stoi(*str_val);
    } catch (const std::exception& e) {
        std::cerr << "Failed to convert " << key << " to int32: " << e.what() << std::endl;
        return std::nullopt;
    }
}

std::optional<uint32_t> MaskConfig::GetUint32(const std::string& key) {
    auto str_val = GetString(key);
    if (!str_val) {
        return std::nullopt;
    }
    try {
        return static_cast<uint32_t>(std::stoul(*str_val));
    } catch (const std::exception& e) {
        std::cerr << "Failed to convert " << key << " to uint32: " << e.what() << std::endl;
        return std::nullopt;
    }
}

std::optional<double> MaskConfig::GetDouble(const std::string& key) {
    auto str_val = GetString(key);
    if (!str_val) {
        return std::nullopt;
    }
    try {
        return std::stod(*str_val);
    } catch (const std::exception& e) {
        std::cerr << "Failed to convert " << key << " to double: " << e.what() << std::endl;
        return std::nullopt;
    }
}

std::optional<bool> MaskConfig::GetBool(const std::string& key) {
    auto str_val = GetString(key);
    if (!str_val) {
        return std::nullopt;
    }
    std::string lower_val = *str_val;
    std::transform(lower_val.begin(), lower_val.end(), lower_val.begin(), ::tolower);
    if (lower_val == "true" || lower_val == "1" || lower_val == "yes") {
        return true;
    }
    if (lower_val == "false" || lower_val == "0" || lower_val == "no") {
        return false;
    }
    return std::nullopt;
}

std::optional<std::vector<std::string>> MaskConfig::GetStringList(const std::string& key) {
    auto str_val = GetString(key);
    if (!str_val) {
        return std::nullopt;
    }

    std::vector<std::string> result;
    std::stringstream ss(*str_val);
    std::string item;

    // Assume comma-separated values
    while (std::getline(ss, item, ',')) {
        // Trim whitespace
        item.erase(0, item.find_first_not_of(" \t\n\r\f\v"));
        item.erase(item.find_last_not_of(" \t\n\r\f\v") + 1);
        if (!item.empty()) {
            result.push_back(item);
        }
    }

    return result;
}

bool MaskConfig::HasKey(const std::string& key) {
    std::lock_guard<std::mutex> lock(mutex_);
    return config_map_.find(key) != config_map_.end();
}

std::vector<std::string> MaskConfig::GetAllKeys() const {
    std::lock_guard<std::mutex> lock(mutex_);
    std::vector<std::string> keys;
    keys.reserve(config_map_.size());
    for (const auto& pair : config_map_) {
        keys.push_back(pair.first);
    }
    return keys;
}

} // namespace camoufox
