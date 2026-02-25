[![PyPI version](https://badge.fury.io/py/keygen.svg)](https://badge.fury.io/py/keygen)

keygen v0.1.0
======================================

A tiny, dependency-free CLI for generating strong keys, tokens, and password-like strings with flexible symbol sets.

Installation
--------------------------------------
```bash
> pip install keygen
```

Command line parameters
--------------------------------------
```bash
> keygen [-s SYMBOLS] [-l LENGTH] [-v]
    -s, --symbols     # Character set for generation:
                         u - ASCII uppercase letters
                         l - ASCII lowercase letters
                         d - digits
                         p - punctuation symbols
                         h - HEX digits
                         o - OCT digits
                         b - BIN digits
                         Default: uldp
    -l, --length      # Generated key length
                         Default: 32
    -e, --emulate     # Emulate encryption algorithm output
                         Supported algorithms:
                           md5, sha1, sha224, sha256, sha384, sha512, uuid
                         Default: None
    --unsafe          # Allow potentially problematic symbols (including ;, ", ', \\, `, $)
                         Default: False (safe mode enabled)
```

Usage
--------------------------------------
```bash
# Generate a 32-character key
> keygen

# Generate a 64-character key using HEX symbols
> keygen -s h -l 64

# Generate a 128-character key using all available symbols
> keygen -s uldp -l 128

# Generate a key that looks like UUID
> keygen -e uuid

# Generate a key with unsafe symbols
> keygen --unsafe
```

Changelog
--------------------------------------
* **v0.1.0** \[_25.02.2026_\]

    - Added safe mode by default and `--unsafe` flag.
    - Removed potentially problematic symbols from the default generation.

* **v0.0.3** \[_27.05.2020_\]

    - Random algorithm switched to system one.
    - Added ability to generate keys that look like crypto function outputs.
    - Removed extra output mode.
    
* **v0.0.2** \[_22.03.2018_\]

    - Added input parameter validation.
    
* **v0.0.1** \[_20.03.2018_\]

    - Initial release.
