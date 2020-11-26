import argparse


def main() -> int:

    # Get args
    ap = argparse.ArgumentParser(
        prog="birdseye", description="A tool for watching players on multiplayer Minecraft servers")
    ap.add_argument("dynmap_url", help="URL to a dynmap server")
    args = ap.parse_args()

    return 0


if __name__ == "__main__":
    exit(main())
