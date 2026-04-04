#pragma once

#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace camoufox {

/**
 * Thread-safe configuration reader for fingerprint spoofing.
 * Reads configuration from environment variables set by the Python launcher.
 */
class MaskConfig {
public:
    /**
     * Get the singleton instance of MaskConfig.
     * @return Reference to the singleton instance.
     */
    static MaskConfig& Get();

    /**
     * Initialize the configuration reader by parsing environment variables.
     * Should be called once at browser startup.
     */
    void Initialize();

    // Type-safe getter methods for various data types
    std::optional<std::string> GetString(const std::string& key);
    std::optional<int32_t> GetInt32(const std::string& key);
    std::optional<uint32_t> GetUint32(const std::string& key);
    std::optional<double> GetDouble(const std::string& key);
    std::optional<bool> GetBool(const std::string& key);
    std::optional<std::vector<std::string>> GetStringList(const std::string& key);

    /**
     * Check if a configuration key exists.
     * @param key The configuration key to check.
     * @return True if the key exists, false otherwise.
     */
    bool HasKey(const std::string& key);

    /**
     * Get all configuration keys.
     * @return Vector of all configuration keys.
     */
    std::vector<std::string> GetAllKeys() const;

private:
    MaskConfig() = default;
    ~MaskConfig() = default;
    MaskConfig(const MaskConfig&) = delete;
    MaskConfig& operator=(const MaskConfig&) = delete;

    /**
     * Read a value directly from environment variables.
     * @param key The environment variable name.
     * @return The value if found, std::nullopt otherwise.
     */
    static std::optional<std::string> ReadFromEnvironment(const std::string& key);

    // Internal storage for parsed configuration
    std::unordered_map<std::string, std::string> config_map_;

    // Thread safety
    mutable std::mutex mutex_;
};

} // namespace camoufox
