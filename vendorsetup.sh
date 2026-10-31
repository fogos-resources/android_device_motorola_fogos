#!/bin/bash

echo "--- Initializing Source Sync ---"

clone_if_missing() {
    local repo_url=$1
    local branch=$2
    local target_dir=$3

    if [ -d "$target_dir/.git" ] || [ -d "$target_dir" ]; then
        echo "Skipping: $target_dir already exists"
        return 0
    fi

    echo "Cloning: $target_dir"

    if [ -n "$branch" ]; then
        git clone --branch "$branch" "$repo_url" "$target_dir"
    else
        git clone "$repo_url" "$target_dir"
    fi

    if [ $? -eq 0 ]; then
        echo "Successfully cloned $target_dir"
    else
        echo "Error: Failed to clone $target_dir"
        return 1
    fi
}

# Device
clone_if_missing "https://github.com/fogos-resources/android_device_motorola_fogos.git" "mist" "device/motorola/fogos"
# Vendor
clone_if_missing "https://github.com/fogos-resources/proprietary_vendor_motorola_fogos.git" "17" "vendor/motorola/fogos"
# Kernel
clone_if_missing "https://github.com/fogos-resources/android_kernel_motorola_sm6375.git" "17" "kernel/motorola/sm6375"
# Hardware
clone_if_missing "https://github.com/fogos-resources/android_hardware_motorola.git" "17" "hardware/motorola"
clone_if_missing "https://github.com/fogos-resources/android_hardware_dolby.git" "17" "hardware/dolby"

echo "--- Source Sync Complete ---"
