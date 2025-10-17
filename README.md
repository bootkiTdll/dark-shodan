<div align="center">
  <img src="https://i.ibb.co/gL10KsMP/1760604184-1.png" width="30%" style="margin-bottom: 8px;">
  <h1 style="margin-top: 0; margin-bottom: 0;">DARK-SHODAN </h1>
  <code>❯ A modular tool for finding vulnerable devices using the Shodan API</code>
  <br><br>
  <img src="https://img.shields.io/github/last-commit/bootkiTdll/dark-shodan?style=for-the-badge&logo=git&logoColor=white&color=0080ff">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/GPL--3.0-red?style=for-the-badge">

</div>
<br>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Modules](#modules)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contributing](#contributing)

---

## Overview 

**DARK-SHODAN** is a lightweight Python CLI tool designed for automated scanning and discovery of vulnerable devices and services exposed on the internet using the Shodan API. It features a modular architecture for easy extension, multilingual interface support (English and Russian), and is ideal for security researchers and penetration testers conducting authorized reconnaissance.

<sub><sup>**This readme was generated using AI and may contain errors.**</sup></sub>
### Features

- **Modular Search System**: Easily extendable with custom modules for specific vulnerabilities (e.g., ComfyUI).
- **Structured Output**: Clean, formatted results for easy analysis.
- **Simple Configuration**: Easy setup via a single `config.json` file.

---

## Project Structure
```
└── dark-shodan/ # Main directory
    ├── LICENSE # GPL-3.0 License
    ├── README.md # Readme
    ├── config.json # Configuration file 
    ├── dark_shodan.py # Main script
    ├── eng.lng # English language strings  
    ├── requirements.txt # Python dependencies
    ├── ru.lng # Russian language strings
    ├── standart_filter.json # Standart filter config for "find" command
    │   └── modules/ # Modules directory
    │       ├── comfyui_module.py # Module for detecting vulnerable ComfyUI instances 
    │       ├── easy_example.py # Easy example module
    │       ├── eng_example.py # Example module (English)
    │       ├── ru_example.py # Example module (Russian)
    │       ├── ftp_anonymouse_login.py # A module for searching FTP servers with anonymous login enabled.
    │       ├── mongodb_disabledAuth.py # MongoDB server search module without authorization
    │       ├── vnc_disabledAuth.py # A module for searching for VNC servers without authorization.
    └───────|
```

---

## Getting Started

### Prerequisites

- **Python 3.6+** (tested on 3.13.9)
- **Pip** (Python package manager)
-  **Shodan API Key** ([Get it here](https://account.shodan.io/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bootkiTdll/dark-shodan
   cd dark-shodan
	```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
### Configuration

1.  Obtain your API key from your [Shodan account page](https://account.shodan.io/).
    
2.  Edit the `config.json` file:
    
```json
{
"language": "ru",
"default:max_results": 50,
"default:min_requests": 10,
"autoconnect:enable": false,
"autoconnect:api_key_file": "api_keys.txt",
"autoconnect:min_requests": 10,
"modules_path": "modules"
}
```
        
----------

## Usage

Run and use the tool from the directory:
```bash
python dark_shodan.py

connect <YOUR_API_KEY> // autoconnect <filename> <minimum available number of available requests>

search <request>

use <number/name>
```

----------

## Modules

DARK-SHODAN uses modules to search for specific vulnerabilities. The `modules/` directory contains:

-   **ComfyUI Module**: Searches for vulnerable instances of ComfyUI.
    
-   **Example Modules**: Provide a template for creating your own modules in both English and Russian.
    

**To create a new module:**

1.  Check out the example modules
    
2.  Follow the structure to define your search query and output.
    
3.  Place the new `.py` file in the `modules/` directory. It will be automatically detected.
    
----------

## Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.
1.  **Fork the Repository**
    
2.  **Clone your fork**:
```bash
git clone https://github.com/bootkiTdll/dark-shodan
```
3. **Create a Feature Branch**:
```bash
git checkout -b new-feature-x
```
4. **Commit your Changes**:
```bash
git commit -m 'Implemented new feature x.'
```
5. **Push to the Branch**:
```bash
git push origin new-feature-x
```
6.  **Open a Pull Request.**
   
----------

## Disclaimer

This tool is intended for **educational purposes and authorized security testing only**. The user is responsible for complying with all applicable laws. Unauthorized scanning and exploitation of computer systems is illegal. Use this tool responsibly and only on networks and devices you own or have explicit permission to test.
   
----------

## License

This project is distributed under the GPL-3.0 License. See the `LICENSE` file for more information.
   
----------

### Contributors

Thank you to all our contributors!

<a href="https://github.com/bootkiTdll/dark-shodan/graphs/contributors"> <img src="https://contrib.rocks/image?repo=bootkiTdll/dark-shodan" /> </a>
