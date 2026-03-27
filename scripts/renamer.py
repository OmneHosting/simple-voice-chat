from pathlib import Path
import shutil

base = Path(__file__).resolve().parent.parent
src = base / "versions" / "voicechat-bukkit-folia-paper-purpur-spigot-1.21.x-1.20.x-1.19.x-1.18.x-1.17.x-1.16.x-1.12.x-1.8.8.jar"

names = ["bukkit", "folia", "paper", "purpur", "spigot"]
versions = ["1.21.x", "1.20.x", "1.19.x", "1.18.x", "1.17.x", "1.16.x", "1.12.x", "1.8.8"]

for name in names:
    for version in versions:
        dst = base / "versions" / f"voicechat-{name}-{version}.jar"
        shutil.copy2(src, dst)
        print(f"Created: {dst.name}")