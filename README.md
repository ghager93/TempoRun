# Tempo Run

Tempo Run is a command-line interface (CLI) application that analyses the tempo of music files in a directory and helps you find ideal tracks to run to.

Currently only works on Linux.

## Installation

To install Tempo Run, run the following command:

```bash
python setup.py install
```

This will install the necessary dependencies and make the `temporun` command available in your terminal.

## Usage

Tempo Run reads audio files from the directory specified in the `audio_dir` variable in the `config.yaml` file. To analyse the tempos of the audio files in this directory, run the following command:

```bash
temporun analyse
```

This will analyse the tempo of each music file in the `audio_dir` directory and output a list of tempos. The track names and tempos are saved in an SQLite3 database.

To find ideal tracks to run to, run the following command:

```bash
temporun suggest
```

This will analyse the tempo of each music file in the `audio_dir` directory and suggest a list of tracks around the ideal tempo for running. The track names and tempos are saved in the SQLite3 database.

## Contributions

If you encounter any bugs or have suggestions for new features, feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/yourusername/your-repo-name).

Thank you for using Tempo Run!
