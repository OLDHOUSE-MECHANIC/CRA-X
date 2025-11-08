# CRA X — Contextual Response Agent X

**A local-first, modular framework for contextual automation and intelligent response handling.**

---

## Overview
CRA X Mk1 is a lightweight, offline framework for building interactive command-response systems. It’s designed for users who want more than simple scripts — offering a structured, extensible way to create context-aware automation without relying on cloud services.

CRA X focuses on clarity, modularity, and control — giving developers a foundation to build responsive logic systems that can grow over time.

---

## Features
- Local-first: Fully offline, runs anywhere Python does.
- Modular structure: Swap, extend, or replace any component easily.
- Plugin-ready: Add new commands or behaviors without altering the core.
- Interactive shell mode: Use CRA X like a personal command console.
- Transparent logic: No hidden ML layers — everything is inspectable and editable.

---

## Quick Start

### Requirements
- Python 3.10+
- Linux / macOS (Windows support planned)

### Installation
```bash
git clone https://github.com/OLDHOUSE-MECHANIC/CRAX-Mk1
cd CRAX-Mk1
pip install -r requirements.txt
```

### Run
```bash
python crax/cli.py -i
```

Example session:
```bash
$ crax -i
> hello
[CRA X] Hello, Operator. Ready when you are.
```

---

## Architecture

CRA X is built around a simple modular pipeline:

```
┌────────────┐
│  CLI / UI  │  ← Input from user
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Parser    │  → Breaks input into commands or tokens
├────────────┤
│  Resolver  │  → Maps recognized input to known actions
├────────────┤
│  Executor  │  → Safely performs the requested operation
├────────────┤
│  Responder │  → Formats and returns the output
└────────────┘
```

Each module is independent and can be swapped or extended via configuration or plugins.

For detailed module design, see [`docs/architecture.md`](docs/architecture.md).

---

## Configuration
CRA X supports runtime configuration through `.toml` or `.yaml` files.

| Key | Description | Default | Example |
|-----|--------------|----------|----------|
| `log_level` | Logging level | `info` | `debug` |
| `plugins_path` | Path to plugin modules | `./plugins` | `/usr/local/share/crax/plugins` |
| `persona` | Output tone or style | `default` | `quiet`, `verbose`, `friendly` |

Example:
```toml
[core]
log_level = "debug"
plugins_path = "./plugins"
```


---

## Contributing
Contributions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-logic`
3. Commit using [Conventional Commits](https://www.conventionalcommits.org)
4. Submit a pull request with a clear description

See [`CONTRIBUTING.md`](docs/contributing.md) for details.

---

## Documentation---Pending
- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [Architecture Overview](docs/architecture.md)
- [Configuration Reference](docs/configuration.md)
- [API Reference](docs/api_reference.md)

---

## Design Philosophy
CRA X was built around one core belief:

**Complex behavior can come from simple, transparent logic.**

It’s a framework for experimenting with contextual responses, structured automation, and human-like interaction — without requiring heavy infrastructure or opaque AI models.

---

## License
MIT License — see [`LICENSE`](LICENSE) for details.

---

## Maintainers
**OLDHOUSE-MECHANIC**  
Local systems, modular automation, and experimental tools.

Contributors are welcome — share your ideas or improvements through GitHub discussions or pull requests.
