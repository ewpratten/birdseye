import argparse

from . import dynmap
from . import ui

def main() -> int:

    # Get args
    ap = argparse.ArgumentParser(
        prog="birdseye", description="A tool for watching players on multiplayer Minecraft servers")
    ap.add_argument("dynmap_url", help="URL to a dynmap server")
    ap.add_argument("-t", "--test", help="Show a testing player", action="store_true")
    args = ap.parse_args()

    # Make configuration call
    try:
        config = dynmap.api.fetchServerConfiguration(args.dynmap_url)
    except dynmap.exceptions.InvalidEndpointException as e:
        print("Failed to contact server")
        print(e)
        return 1

    # Set up window
    window = ui.Window(f"{args.dynmap_url} {config.title}", args.dynmap_url)
    window.loadServerConfig(config)

    # Run main loop
    while True:

        # Handle quit
        if window.shouldQuit():
            return 0

        # Handle rendering
        if window.getTimeUntilNextFrame() <= 0:

            # Fetch any player positioning updates
            update = dynmap.api.fetchServerUpdate(args.dynmap_url, config)

            # Get and set the player list
            players = update.players

            if args.test:
                players.append(dynmap.models.DynmapPlayerModel({
                    "world": config.defaultworld,
                    "name":"TestAccount",
                    "account": "TestAccount",
                    "x": 0,
                    "y": 0,
                    "z": 0,
                }))

            window.updatePlayerList(players)

            # Actually render
            window.doRender()

    return 0


if __name__ == "__main__":
    exit(main())
