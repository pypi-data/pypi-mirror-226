import argparse
import command_funcs

parser = argparse.ArgumentParser(description="CLI tool for keeping changes to a file updated in different locations")
parser.add_argument("-add", "-a", dest="add", nargs=2, help="Add a pair of files")
parser.add_argument("-refresh", "-r", dest="refresh", action="store_true", help="Refresh current pairs to update changes")
parser.add_argument("-dir", "-d", dest="dir", nargs=2, help="Add a pair of directories")
parser.add_argument("-show", "-s", dest="show", action="store_true", help="Show the pairs of the current workspace")
parser.add_argument("-clear", "-c", dest="clear", action="store_true", help="Clear all the pairs from the current workspace")

def main():
    args = parser.parse_args()

    if args.add:
        command_funcs.add_pair_to_store(args.add[0], args.add[1])   
    elif args.refresh:
        to_refresh = command_funcs.find_changed()
        print("Pairs to be updated:")
        print(to_refresh)

        for pair in to_refresh:
            io = input(f"Do you want to refresh pair: {pair}? y/n or a for refreshing all pairs ")
            if io == "y":
                command_funcs.refresh_pair(pair)
            elif io == "a":
                command_funcs.refresh_pairs(to_refresh)
                break
    elif args.dir:
        command_funcs.add_pair_to_store(args.dir[0], args.dir[1])   
    elif args.show:
        command_funcs.show_pairs()
    elif args.clear:
        command_funcs.clear_file_pairs_file()

if __name__ == "__main__":
    main()

