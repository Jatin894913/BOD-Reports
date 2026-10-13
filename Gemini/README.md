# BOD Report Generator

A robust CLI tool designed for generating **Beginning of Day (BOD)** health check reports for various environments (Production and UAT). This tool helps monitor system resources, container status, data feeders, and file downloads.

## 📋 Features

- **Multi-Environment Support**: Generates tailored reports for W2W PROD, W2W UAT, and FTUAT.
- **Dynamic Configuration**: All thresholds and expected values are managed via a `common.env` file.
- **Automated Issue Detection**: Compares input data against pre-defined thresholds (e.g., RAM usage > 75%, missing containers) and flags issues automatically.
- **Robust Input Handling**: Includes built-in validation for integers, floats, and yes/no responses to prevent runtime errors.
- **Polymorphic Architecture**: Built on a modular base class (`ReportBase`) for easy extension to new environments.

## 📁 Project Structure

| File | Description |
| :--- | :--- |
| `ReportRunner.java` | The main entry point containing the CLI menu. |
| `ReportBase.java` | Abstract base class with shared utilities and data models. |
| `ReportConfig.java` | Centralized configuration management using environment variables. |
| `EnvLoader.java` | Utility to parse and load settings from `.env` files. |
| `W2WPRODReport.java` | Implementation for Way2Wealth Production (PS, NS, DR zones). |
| `W2WUATReport.java` | Implementation for Way2Wealth UAT environment. |
| `FTUATReport.java` | Implementation for FTUAT with specific file-level checks. |
| `common.env` | Configuration file for thresholds and expected counts. |

## ⚙️ Configuration

You can customize the reporting thresholds by editing `common.env`. Key parameters include:

- `STORAGE_THRESHOLD`: Percentage at which storage usage is flagged as an issue (default: 75).
- `RAM_THRESHOLD`: Percentage at which RAM usage is flagged as an issue (default: 75).
- `FEEDERS_COUNT`: Expected number of connected feeders.
- `EXTERNAL_FILES_COUNT`: Total number of external files expected to be downloaded.

## 🚀 Getting Started

### Prerequisites
- Java JDK 8 or higher.

### Compilation
Compile all files into the `bin` directory:
```bash
javac -d bin *.java
```

### Execution
Run the main generator using the `bin` classpath:
```bash
java -cp bin Gemini.ReportRunner
```

## 🛠️ Adding New Reports
To add a new environment report:
1. Create a new class extending `ReportBase`.
2. Implement the `execute()` method to collect data and print the report.
3. Register the new report in the `switch` statement in `ReportRunner.java`.
