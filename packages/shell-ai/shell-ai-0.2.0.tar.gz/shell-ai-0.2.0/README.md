# Shell-AI: Your Intelligent Command-Line Companion

Shell-AI (`shai`) is a CLI utility that brings the power of natural language understanding to your command line. Simply input what you want to do in natural language, and `shai` will suggest single-line commands that achieve your intent. Under the hood, Shell-AI leverages the [LangChain](https://github.com/langchain-ai/langchain) for LLM use and builds on the excellent [InquirerPy](https://github.com/kazhala/InquirerPy) for the interactive CLI.

## Installation

You can install Shell-AI directly from PyPI using pip:

```bash
pip install shell-ai
```

After installation, you can invoke the utility using the `shai` command.

## Usage

To use Shell-AI, open your terminal and type:

```bash
shai run terraform dry run thingy
```

Shell-AI will then suggest 3 commands to fulfill your request:
- `terraform plan`
- `terraform plan -input=false`
- `terraform plan`

## Features

- **Natural Language Input**: Describe what you want to do in plain English (or other supported languages).
- **Command Suggestions**: Get single-line command suggestions that accomplish what you asked for.
- **Cross-Platform**: Works on Linux, macOS, and Windows.

## Contributing

This implementation can be made much smarter! Contribute your ideas as Pull Requests and make AI Shell better for everyone.

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Shell-AI is licensed under the MIT License. See [LICENSE](LICENSE) for details.
