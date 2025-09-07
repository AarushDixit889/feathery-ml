# FeatheryML

A sophisticated AI-powered statistical analysis tool with a modern CLI interface.

## Features

- 🤖 AI-Powered Analysis: Generates code for statistical analysis from natural language queries
- 📊 Interactive Analysis: Chat-based interface for continuous data exploration
- 🎨 Modern UI: Rich terminal interface with custom styling
- 🔄 Version Control: Automatic git integration for tracking analysis history
- 📝 History Management: Maintains QnA history for future reference
- ⚡ Fast Dependencies: Uses `uv` for efficient package management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/feathery-ml.git
cd feathery-ml
```

2. Set up the environment:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Project Structure

```
feathery-ml/
├── src/
│   ├── ai_engine/         # AI code generation and processing
│   ├── chat_manager/      # Interactive chat interface
│   ├── cli/              # Command line interface
│   ├── config_manager/   # Configuration handling
│   ├── data_handlers/    # Data processing utilities
│   ├── git_manager/      # Git integration
│   ├── project_manager/  # Project initialization and management
│   └── utils/           # Common utilities
├── tests/               # Test suites
├── data/               # Data storage
│   ├── raw/           # Raw input data
│   └── processed/     # Processed data
└── docs/              # Documentation
```

## Usage

1. Start the interactive analysis:
```bash
python -m src.cli.main
```

2. Use natural language queries for analysis:
```
Analysis Query> Calculate mean and standard deviation of column A
```

3. View help and available commands:
```
Analysis Query> help
```

## Development

1. Install development dependencies:
```bash
uv pip install -r requirements.txt
```

2. Run tests:
```bash
pytest
```

## Configuration

The tool can be configured through `.feathers` configuration file:

- `output_format`: Preferred output format (text/table)
- `auto_commit`: Enable/disable automatic git commits
- `save_history`: Enable/disable QnA history saving

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
