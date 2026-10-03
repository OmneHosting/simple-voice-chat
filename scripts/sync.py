#!/usr/bin/env python3
"""Mirror the latest Simple Voice Chat jars from Modrinth into versions/.

Stable raw.githubusercontent.com URLs for the panel Template Installer
(voicechat-<loader>-<mc>.jar). Stdlib only: python3 scripts/sync.py
Every download is checked against Modrinth's sha512 and for the loader's metadata
file before it is written. Release and beta builds are mirrored (Modrinth marks
most mod builds beta); alpha and snapshot builds are skipped.
"""
import hashlib, io, json, sys, urllib.parse, urllib.request, zipfile
from pathlib import Path

API = "https://api.modrinth.com/v2/project/simple-voice-chat/version"
UA = {"User-Agent": "OmneHosting/simple-voice-chat-mirror (https://github.com/OmneHosting/simple-voice-chat)"}
OUT = Path(__file__).resolve().parent.parent / "versions"

# Mod loaders: one jar per Minecraft version. Keys are what the template offers.
# 1.20.1 is deliberately not offered: NeoForge has no 1.20.1 build, and the
# template shares one version list across all three loaders.
MC = ["26.3", "26.2", "26.1", "1.21.11", "1.21.8", "1.21.4", "1.21.1", "1.20.6", "1.20.4"]
LOADERS = ["fabric", "forge", "neoforge"]

# Bukkit-family plugins ship ONE jar for every server and version; the many
# file names are copies so old and new template URLs keep resolving.
PLUGINS = ["bukkit", "folia", "paper", "purpur", "spigot"]
PLUGIN_LINES = ["26.x", "1.21.x", "1.20.x", "1.19.x", "1.18.x", "1.17.x", "1.16.x", "1.12.x", "1.8.8"]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def latest(loader, mc=None):
    q = {"loaders": json.dumps([loader])}
    if mc:
        q["game_versions"] = json.dumps([mc])
    for v in json.loads(get(f"{API}?{urllib.parse.urlencode(q)}")):  # newest first
        if v["version_type"] in ("release", "beta"):
            f = next((f for f in v["files"] if f["primary"]), v["files"][0])
            return v["version_number"], f
    raise SystemExit(f"no release/beta build for {loader} {mc or ''}")


# The file that proves a jar is for the loader we think it is.
# (NeoForge used mods.toml until 1.20.5, then neoforge.mods.toml.)
MARKER = {"bukkit": ("plugin.yml",), "fabric": ("fabric.mod.json",),
          "forge": ("META-INF/mods.toml",),
          "neoforge": ("META-INF/neoforge.mods.toml", "META-INF/mods.toml")}


def fetch(f, loader):
    data = get(f["url"])
    if hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
        raise SystemExit(f"sha512 mismatch for {f['filename']}")
    if not set(MARKER[loader]) & set(zipfile.ZipFile(io.BytesIO(data)).namelist()):
        raise SystemExit(f"{f['filename']} has none of {MARKER[loader]}, wrong loader?")
    return data


def write(path, data):
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


def main():
    OUT.mkdir(exist_ok=True)
    manifest, changed = {}, []

    ver, f = latest("bukkit")
    data = fetch(f, "bukkit")
    manifest["plugin"] = {"version": ver, "sha512": f["hashes"]["sha512"]}
    for name in PLUGINS:
        for line in PLUGIN_LINES:
            if write(OUT / f"voicechat-{name}-{line}.jar", data):
                changed.append(f"voicechat-{name}-{line}.jar")

    for loader in LOADERS:
        for mc in MC:
            ver, f = latest(loader, mc)
            dest = OUT / f"voicechat-{loader}-{mc}.jar"
            if write(dest, fetch(f, loader)):
                changed.append(dest.name)
            manifest[f"{loader}-{mc}"] = {"version": ver, "sha512": f["hashes"]["sha512"]}

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"{len(changed)} files written" if changed else "already up to date")
    for c in changed:
        print("  ", c)


if __name__ == "__main__":
    sys.exit(main())
