## Cybersecurity assignment

* git pull
* cd Python
* pip install -r requirements.txt (make sure you have )

### Insecure implementation
* python lidar.py
* curl http://localhost:8007/mode/set/run : {"status": "Running"}
* python udp_sniffer.py :
Real LiDAR Pointcloud packet: Message number 36
Real LiDAR Pointcloud packet: Message number 37
Real LiDAR Pointcloud packet: Message number 38
* python udp_attacker.py :
{"status": "Running"}
Idle
Broadcasting on: 5044
* udp_sniffer.py output:
Real LiDAR Pointcloud packet: Message number 670
Real LiDAR Pointcloud packet: Message number 671
Spoofed LiDAR Pointcloud packet: Message number 0
Spoofed LiDAR Pointcloud packet: Message number 1

### Secure implementation
* python lidar_crt.py
* curl --insecure --cacert ca-crt.pem --key client.key --cert client.crt https://localhost:8007/mode/set/run : {"status": "Running"}
* python udp_sniffer.py (code still works without checking authentication for backwards compatibility):
Real LiDAR Pointcloud packet: Message number 634516C2DB1EE1050B85545531D764028A0D5C569981FE79CA147B641968BC784C
Real LiDAR Pointcloud packet: Message number 64347804A450742FAD5E32836D8AE2C1D1BAE45CF1080D76ED30BDEADFEDE0B480
Real LiDAR Pointcloud packet: Message number 650361F082D4013E3D44437F90DA3E8F7D5B9D626F681BF8F59C7C3B3D30435304
* python udp_sniffer_crt.py :
Real LiDAR Pointcloud packet: Message number 632
Real LiDAR Pointcloud packet: Message number 633
Real LiDAR Pointcloud packet: Message number 634
* python udp_attacker.py :
Can't access LiDAR REST API
Can't access LiDAR REST API
Broadcasting on: 5044
* udp_sniffer_crt.py output (The spoofed packets can be recognised and ignored):
Real LiDAR Pointcloud packet: Message number 1067
Authentication failed: Spoofed LiDAR Pointcloud packet: Message number 147
Real LiDAR Pointcloud packet: Message number 1068
Authentication failed: Spoofed LiDAR Pointcloud packet: Message number 148
Real LiDAR Pointcloud packet: Message number 1069
Authentication failed: Spoofed LiDAR Pointcloud packet: Message number 149


## FreeRTOS

## Getting started
The easiest way to use FreeRTOS is to start with one of the pre-configured demo application projects (found in the FreeRTOS/Demo directory).  That way you will have the correct FreeRTOS source files included, and the correct include paths configured.  Once a demo application is building and executing you can remove the demo application files, and start to add in your own application source files.  See the [FreeRTOS Kernel Quick Start Guide](https://www.freertos.org/FreeRTOS-quick-start-guide.html) for detailed instructions and other useful links.

Additionally, for FreeRTOS kernel feature information refer to the [Developer Documentation](https://www.freertos.org/features.html), and [API Reference](https://www.freertos.org/a00106.html).

### Getting help
If you have any questions or need assistance troubleshooting your FreeRTOS project, we have an active community that can help on the [FreeRTOS Community Support Forum](https://forums.freertos.org). Please also refer to [FAQ](http://www.freertos.org/FAQHelp.html) for frequently asked questions.

## Cloning this repository
This repo uses [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to bring in dependent components.

Note: If you download the ZIP file provided by GitHub UI, you will not get the contents of the submodules. (The ZIP file is also not a valid git repository)

To clone using HTTPS:
```
git clone https://github.com/xanderhendriks-uts/cyb-FreeRTOS.git --recurse-submodules
```
Using SSH:
```
git clone git@github.com:xanderhendriks-uts/cyb-FreeRTOS.git --recurse-submodules
```

If you have downloaded the repo without using the `--recurse-submodules` argument, you need to run:
```
git submodule update --init --recursive
```

## Repository structure
This repository contains the FreeRTOS Kernel, a number of supplementary libraries, and a comprehensive set of example applications.

### Kernel sources
The FreeRTOS Kernel Source is in [FreeRTOS/FreeRTOS-Kernel repository](https://github.com/FreeRTOS/FreeRTOS-Kernel), and it is consumed as a submodule in this repository.

The version of the FreeRTOS Kernel Source in use could be accessed at ```./FreeRTOS/Source``` directory.

A number of Demo projects can be found under ```./FreeRTOS/Demo``` directory.

### Supplementary library sources
The [FreeRTOS-Plus/Source](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Source) directory contains source code for some of the FreeRTOS+ components, as well as select partner provided libraries. These subdirectories contain further readme files and links to documentation.

[FreeRTOS-Labs](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Labs) contains libraries and demos that are fully functional, but undergoing optimizations or refactorization to improve memory usage, modularity,
documentation, demo usability, or test coverage.  At this time the projects ARE A WORK IN PROGRESS and will be released in the main FreeRTOS directories of the download following full review and completion of the documentation.

## Previous releases
Previous releases are available for download under [releases](https://github.com/FreeRTOS/FreeRTOS/releases).
