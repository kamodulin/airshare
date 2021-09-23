# airshare

 airshare is a peer-to-peer socket utility that allows clipboard data to be continuously streamed between multiple computers. If continuity is enabled on Apple devices, an iPhone's clipboard can be shared to a Windows PC. 

## Features

## Installation
Clone this repo and enter this command from the root directory
```bash
pip install .
```

```
Usage:
    airshare [options]

Options:
    --host      Host ip address:port (default is None which leads to random port allocation)
    --remote    Remote ip address:port (default is None)

```

Example session:

Device 1: ```airshare --host "192.168.0.10:5000"```

Device 2: ```airshare --host "192.168.0.20:8000" --remote "192.168.0.10:5000"```