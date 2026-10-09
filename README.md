# LZ77 Text Compression App

A Python command-line application demonstrating **LZ77 (Lempel–Ziv 1977)** text compression and decompression using a sliding search window and a look-ahead window. It provides interactive text entry, `.txt` file selection, human-readable compression tags, and an optional decompression check.

> **Project status:** Educational prototype. In-memory compression and decompression work for ordinary text, but the current saved-tag format is **not reliably readable back** by the decompressor. See [Known limitations](#known-limitations) before using saved output.

## Features

- Compress text entered at the command line or loaded from a UTF-8 `.txt` file.
- Configure search-window and look-ahead-window sizes.
- Generate LZ77 tags of the form `<distance, length, next_symbol>`.
- Support overlapping matches when encoding repeated sequences.
- Decompress the in-memory tags immediately after compression.
- Optionally save compressed tags or decompressed text to a file.

## Requirements

- Python 3.8 or newer (recommended; no third-party packages are used).
- Tkinter, included with many Python distributions, for the graphical file picker.
- A desktop environment to use the file picker. Direct text entry works without selecting a file.

## Project structure

```text
.
├── main.py             # Interactive command-line menu and file input/output
├── compression.py      # TAG class, match search, compression, size estimate
├── decompression.py    # Decompression from tags or serialized text
└── README.md           # Project documentation
```

## Getting started

1. Download or clone the repository and open a terminal in its directory.
2. Run:

   ```bash
   python main.py
   ```

   On some systems use `python3 main.py` instead.
3. Choose **1** to compress or **2** to decompress.

### Compress text

1. Choose **1 — Compress Text**.
2. Enter text directly, or select a UTF-8 `.txt` file using the file picker.
3. Enter positive integer sizes for the **search window** and **look-ahead window** (for example, `8` and `8`).
4. View the generated tags and the displayed size estimate.
5. Optionally save the tags to `compressed.txt`.
6. Optionally decompress the **in-memory tags** to verify the recovered text.

### Decompress text

Choose **2 — Decompress Text** and enter tags or select a file. **Important:** the current text-tag parser has a known bug and typically raises `ValueError` on the format produced by the compressor. Until this is fixed, use the in-memory decompression prompt following compression to test a round trip.

## How it works

LZ77 scans the input from left to right. At each position, it searches a limited history (the **search window**) for the longest matching prefix of the upcoming text (the **look-ahead window**).

Each tag contains:

| Field | Meaning |
| --- | --- |
| `distance` | Number of characters to look backward in already processed text; `0` indicates a literal |
| `length` | Number of characters to copy from that previous position |
| `next_symbol` | Literal character after the match, or `None` when a match reaches the end |

For example, with a search window of `8` and a look-ahead window of `8`, `AAAAAA` is encoded as:

```text
<0, 0, A> <1, 5, None>
```

The second tag copies five characters using a distance of one. Copying is performed one character at a time, allowing **overlapping matches**.

## Modules

### `compression.py`

- `TAG`: represents one `(position, length, offset)` tuple. Here, `position` is a backward distance and `offset` stores the next symbol.
- `handle_repetition(text, i, sws, slh)`: finds the longest match at the current index.
- `lz77_compression(text, sws, slh)`: returns `(list_of_tags, serialized_tags)`.
- `size_after_compression(tags)`: computes an approximate fixed-width bit count **per tag**, not the real file size.
- `printTags(tags, text, tag_size)`: displays tags and estimated sizes.

### `decompression.py`

- `lz77_decompression(user_input)`: accepts a list of `TAG` objects or a string representation of tags. The list-of-objects path is suitable for in-memory round trips; the string parsing path needs repair.

### `main.py`

Provides the menu, keyboard input, Tkinter file selection, output printing, and optional file saving.

## Example: in-memory round trip

```python
from compression import lz77_compression
from decompression import lz77_decompression

text = "AAAAAA"
tags, serialized = lz77_compression(text, sws=8, slh=8)
restored = lz77_decompression(tags)

print(serialized)  # <0, 0, A> <1, 5, None>
print(restored)    # AAAAAA
assert restored == text
```

## License

No license has been specified. Add a `LICENSE` file if you want to define how others may use or contribute to the project.
