# simple-voice-chat

Stable download links for the [Simple Voice Chat](https://modrinth.com/plugin/simple-voice-chat) jars,
used by the OmneHosting panel's **SimpleVoiceChat** Template Installer template.

Modrinth has no "latest for this loader and Minecraft version" URL, so the jars are mirrored here under predictable names:

    https://raw.githubusercontent.com/OmneHosting/simple-voice-chat/main/versions/voicechat-<type>-<version>.jar

| Type | Versions | Notes |
|---|---|---|
| `fabric`, `forge`, `neoforge` | `26.3`, `26.2`, `26.1`, `1.21.11`, `1.21.8`, `1.21.4`, `1.21.1`, `1.20.6`, `1.20.4` | One build per Minecraft version. |
| `bukkit`, `spigot`, `paper`, `purpur`, `folia` | `26.x`, `1.21.x`, `1.20.x`, `1.19.x`, `1.18.x`, `1.17.x`, `1.16.x`, `1.12.x`, `1.8.8` | Upstream ships one Java 8 jar for all of them (Modrinth lists 1.8.8 through current). The names are identical copies so old links keep working. |

`versions/manifest.json` records the upstream version and sha512 behind each file.

## Updating

    python3 scripts/sync.py

Downloads the newest release or beta build from Modrinth (alpha and snapshot builds are skipped; Modrinth marks most mod builds beta), checks its sha512 and loader metadata, and rewrites only files that changed.
The `sync` workflow runs this weekly and opens a pull request when something changed. Review and merge it; nothing reaches `main` unreviewed.

To offer another Minecraft version, add it to `MC` in `scripts/sync.py` and to the template's version list in `omne-panel`.
