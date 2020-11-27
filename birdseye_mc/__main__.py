import argparse
import threading
import time

from . import dynmap
from . import ui

notice_kill = False

def handleServerUpdates(window: ui.Window, dynmap_url: str, config: dynmap.models.DynmapConfigurationModel, test: bool):
    global notice_kill
    while not notice_kill:
        # Fetch any player positioning updates
        update = dynmap.api.fetchServerUpdate(dynmap_url, config)

        # Get and set the player list
        players = update.players

        if test:
            players.append(dynmap.models.DynmapPlayerModel(**{
                "world": config.defaultworld,
                "name": "TestAccount",
                "account": "TestAccount",
                "x": 0,
                "y": 0,
                "z": 0,
                "test": True
            }))

        window.updatePlayerList(players)

        time.sleep(int((config.updaterate/2) / 1000))


def main() -> int:
    global notice_kill

    # Get args
    ap = argparse.ArgumentParser(
        prog="birdseye", description="A tool for watching players on multiplayer Minecraft servers")
    ap.add_argument("dynmap_url", help="URL to a dynmap server")
    ap.add_argument("-t", "--test", help="Show a testing player",
                    action="store_true")
    args = ap.parse_args()

    # Make configuration call
    try:
        config = dynmap.api.fetchServerConfiguration(args.dynmap_url)
    except dynmap.exceptions.InvalidEndpointException as e:
        print("Failed to contact server")
        print(e)
        return 1

    # Set up window
    window = ui.Window(f"{args.dynmap_url} {config.title}",
                       args.dynmap_url, debug=args.test)
    window.loadServerConfig(config)

    # Set up update thread
    update_thread = threading.Thread(
        target=handleServerUpdates, args=(window, args.dynmap_url, config, args.test))
    update_thread.start()

    # Run main loop
    while True:

        # Handle quit
        if window.shouldQuit():
            notice_kill = True
            print("Waiting for HTTP connection to close")
            update_thread.join()
            return 0

        # Handle rendering
        window.doRender()

        time.sleep(0.5)

    return 0


if __name__ == "__main__":
    exit(main())
