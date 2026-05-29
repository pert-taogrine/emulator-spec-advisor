#!/usr/bin/env python3
"""Recommend Android-emulator settings from your PC's CPU cores and RAM."""
import argparse, os


def recommend(cores: int, ram_gb: float):
    alloc_cores = max(2, min(cores // 2, 4))
    alloc_ram = 2 if ram_gb <= 8 else (4 if ram_gb <= 16 else 6)
    instances = max(1, min(int(ram_gb // 3), cores // 2))
    res = "1280x720" if ram_gb <= 8 else "1920x1080"
    renderer = "DirectX"
    return {
        "cpu_cores": alloc_cores,
        "ram_mb": alloc_ram * 1024,
        "resolution": res,
        "renderer": renderer,
        "max_instances": instances,
        "enable_vt": True,
    }


def detect():
    cores = os.cpu_count() or 4
    ram_gb = 8.0
    try:
        if hasattr(os, "sysconf"):
            ram_gb = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3)
    except (ValueError, OSError):
        pass
    return cores, round(ram_gb, 1)


def main():
    ap = argparse.ArgumentParser(description="Android emulator settings advisor")
    ap.add_argument("--cores", type=int)
    ap.add_argument("--ram", type=float, help="RAM in GB")
    a = ap.parse_args()
    cores, ram = detect()
    cores = a.cores or cores
    ram = a.ram or ram
    print(f"Detected: {cores} cores, {ram} GB RAM")
    for k, v in recommend(cores, ram).items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
