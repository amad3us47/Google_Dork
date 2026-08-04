# Google Dorking Tool

A simple Google dorking tool that runs a database of ~8,000 dorks against a target domain to surface publicly exposed pages, files, and information. Useful for OSINT, reconnaissance, and security assessments.

## Requirements

- Python 3

## Usage

Run all dorks against a target domain:

```bash
python3 search.py -d "example.com"
```

Launch browser mode:

```bash
python3 search.py -brows
```

## Disclaimer

This tool queries only publicly indexed information. It is intended for education, OSINT research, and authorized security testing. Only use it against domains you own or have explicit permission to test. You are responsible for how you use it.

## License

Add a license of your choice (e.g. MIT).
