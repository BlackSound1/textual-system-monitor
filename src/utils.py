COLOR_MAP = {
    'textual-light': {
        'procs': "#FF8C00",
        'drives': "#FF0000",
        'mem': "#F3CD00",
        'cpu': "#7272f6",
        'net': "#008000",
        'gpu': "#FF1493",
    },
    'textual-dark': {
        'procs': "#FEA62B",
        'drives': "#FF0000",
        'mem': "#FFFF00",
        'cpu': "#ADD8E6",
        'net': "#90EE90",
        'gpu': "#FFC0CB",
    },
    'nord': {
        'procs': "#d08770",
        'drives': "#bf616a",
        'mem': "#ebcb8b",
        'cpu': "#88c0d0",
        'net': "#a3be8c",
        'gpu': "#b48ead",
    },
    'gruvbox': {
        'procs': "#fe8019",
        'drives': "#fb4934",
        'mem': "#fabd2f",
        'cpu': "#83a598",
        'net': "#8ec07c",
        'gpu': "#d3869b",
    },
    'catpuccin-mocha': {
        'procs': "#fab387",
        'drives': "#f38ba8",
        'mem': "#f9e2af",
        'cpu': "#89b4fa",
        'net': "#a6e3a1",
        'gpu': "#f5c2e7",
    },
    'catpuccin-latte': {
        'procs': "#fe640b",
        'drives': "#d20f39",
        'mem': "#df8e1d",
        'cpu': "#1e66f5",
        'net': "#40a02b",
        'gpu': "#ea76cb",
    },
    'dracula': {
        'procs': "#ffb86c",
        'drives': "#ff5555",
        'mem': "#f1fa8c",
        'cpu': "#8be9fd",
        'net': "#50fa7b",
        'gpu': "#ff79c6",
    },
    'tokyo-night': {
        'procs': "#ff9e64",
        'drives': "#f7768e",
        'mem': "#e0af68",
        'cpu': "#7aa2f7",
        'net': "#41a6b5",
        'gpu': "#9d7cd8",
    },
    'monokai': {
        'procs': "#ffb84d",
        'drives': "#ff56ad",
        'mem': "#ffff2f",
        'cpu': "#7effff",
        'net': "#d6ff53",
        'gpu': "#e4bfff",
    },
    'flexoki': {
        'procs': "#da702c",
        'drives': "#d14d41",
        'mem': "#d0a215",
        'cpu': "#4385be",
        'net': "#879a39",
        'gpu': "#ce5d97",
    },
    'solarized-light': {
        'procs': "#cb4b16",
        'drives': "#dc322f",
        'mem': "#b58900",
        'cpu': "#268bd2",
        'net': "#859900",
        'gpu': "#d33682",
    },
}


def get_pallette(name: str) -> dict[str, str]:
    """
    Get the current color pallette based on the current color theme.

    :param str name: The name of the current color theme.
    :return dict[str, str]: The color pallette as a dict.
    """
    return COLOR_MAP.get(name, COLOR_MAP['textual-dark'])
