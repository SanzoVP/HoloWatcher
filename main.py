import json
from youtube_api import YouTubeAPI
import webbrowser
import os
import time
import threading  # Import threading to handle background tasks

# ANSI escape codes for terminal coloring
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"

opened_streams_file = "opened_streams.json"

def load_vtubers():
    """Load VTubers data from JSON file."""
    vtubers_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "vtubers.json")
    
    # Check if the file exists, create directories if needed
    if not os.path.exists(vtubers_file):
        os.makedirs(os.path.dirname(vtubers_file), exist_ok=True)
        # Create default vtubers.json if it doesn't exist
        with open(vtubers_file, "w") as f:
            json.dump({}, f, indent=4)
        print(f"{YELLOW}Created empty vtubers.json file. Please update it with VTuber data.{RESET}")
        return {}
    
    try:
        with open(vtubers_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}Error reading vtubers.json. File may be corrupted.{RESET}")
        return {}

vtubers = load_vtubers()

def subscribe(step="main"):
    subscriptions = []
    try:
        with open("subscriptions.json", "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                subscriptions = data
            else:
                subscriptions = data.get("subscriptions", [])
    except (FileNotFoundError, json.JSONDecodeError):
        subscriptions = []

    if step == "main":
        print(f"{CYAN}Enter the names of the VTuber to subscribe/unsubscribe,\nExample: 'Hakos Baelz, Mori Calliope'\nor type 'browse' to navigate through branches and generations,\nor 'back' to go back:{RESET}")
        user_input = input().strip()

        if user_input.lower() == 'back':
            return  # Exit the function to go back to the previous menu

        if user_input.lower() == 'browse':
            # Navigate to branches selection
            subscribe("branches")
        else:
            # Handle direct subscription by name
            handle_direct_subscription(user_input, subscriptions)
    
    elif step == "branches":
        # Show available branches
        print(f"{CYAN}Select branch:{RESET}")
        branches = list(vtubers.keys())
        for i, branch in enumerate(branches, start=1):
            print(f"{YELLOW}{i}. {branch}{RESET}")

        branch_selection = input(f"{CYAN}Enter branch number or type 'back' to go back: {RESET}").strip()
        if branch_selection.lower() == 'back':
            subscribe("main")  # Go back to main menu
            return

        if branch_selection.isdigit() and 1 <= int(branch_selection) <= len(branches):
            selected_branch = branches[int(branch_selection) - 1]
            print(f"{GREEN}Selected Branch: {selected_branch}{RESET}")
            # Move to generation selection for this branch
            subscribe_generations(selected_branch, subscriptions)
        else:
            print(f"{RED}Invalid selection.{RESET}")
            subscribe("branches")  # Stay on branches menu

def subscribe_generations(selected_branch, subscriptions):
    # Show available generations for the selected branch
    generations = vtubers[selected_branch]
    generation_names = list(generations.keys())
    for i, gen in enumerate(generation_names, start=1):
        print(f"{YELLOW}{i}. {gen}{RESET}")

    generation_selection = input(f"{CYAN}\nEnter generation number or type 'back' to go back: {RESET}").strip()
    if generation_selection.lower() == 'back':
        subscribe("branches")  # Go back to branches selection
        return

    if generation_selection.isdigit() and 1 <= int(generation_selection) <= len(generation_names):
        selected_generation = generation_names[int(generation_selection) - 1]
        selected_vtubers = generations[selected_generation]
        print(f"{GREEN}Selected Generation: {selected_generation}{RESET}")
        # Move to VTuber selection for this generation
        subscribe_vtubers(selected_branch, selected_generation, selected_vtubers, subscriptions)
    else:
        print(f"{RED}Invalid generation selection.{RESET}")
        subscribe_generations(selected_branch, subscriptions)  # Stay on generations menu

def subscribe_vtubers(selected_branch, selected_generation, selected_vtubers, subscriptions):
    # Ask user to select VTubers from this generation
    print(f"{CYAN}Select VTubers to subscribe to from {selected_generation}:{RESET}")
    for i, vtuber in enumerate(selected_vtubers, start=1):
        print(f"{YELLOW}{i}. {vtuber['name']}{RESET}")

    selected_indices = input(f"{CYAN}Enter numbers separated by commas (e.g., 1,2,3) or type 'back' to go back: {RESET}")
    
    if selected_indices.strip().lower() == 'back':
        subscribe_generations(selected_branch, subscriptions)  # Go back to generations selection
        return

    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",") if i.strip().isdigit()]

    # Toggle subscription (subscribe/unsubscribe)
    for index in selected_indices:
        if 0 <= index < len(selected_vtubers):
            vtuber = selected_vtubers[index]
            if vtuber not in subscriptions:
                subscriptions.append(vtuber)  # Subscribe
                print(f"{GREEN}Subscribed to {vtuber['name']}{RESET}")
            else:
                subscriptions.remove(vtuber)  # Unsubscribe
                print(f"{RED}Unsubscribed from {vtuber['name']}{RESET}")
    
    # Save subscriptions to file
    with open("subscriptions.json", "w") as f:
        json.dump(subscriptions, f)
    
    # After subscription, go back to VTuber selection for this generation
    subscribe_vtubers(selected_branch, selected_generation, selected_vtubers, subscriptions)

def handle_direct_subscription(user_input, subscriptions):
    # Split user input by commas and strip only leading/trailing spaces
    vtuber_names = [name.strip() for name in user_input.split(',')]

    # Iterate over each VTuber name
    for vtuber_name in vtuber_names:
        found = False
        for branch_name, generations in vtubers.items():
            for gen_name, vtuber_list in generations.items():
                for vtuber in vtuber_list:
                    if vtuber['name'].lower() == vtuber_name.lower():
                        found = True
                        if vtuber not in subscriptions:
                            subscriptions.append(vtuber)  # Subscribe
                            print(f"{GREEN}Subscribed to {vtuber['name']}{RESET}")
                        else:
                            subscriptions.remove(vtuber)  # Unsubscribe
                            print(f"{RED}Unsubscribed from {vtuber['name']}{RESET}")
                        break
                if found:
                    break
            if found:
                break

        if not found:
            print(f"{RED}VTuber '{vtuber_name}' not found. Please check the name and try again.{RESET}")
    
    # Save subscriptions to file
    with open("subscriptions.json", "w") as f:
        json.dump(subscriptions, f, indent=4)

def check_live():
    with open("subscriptions.json", "r") as f:
        data = json.load(f)
        channel_ids = [vtuber["channel_id"] for vtuber in data]

    youtube_api = YouTubeAPI()

    if os.path.exists(opened_streams_file):
        with open(opened_streams_file, "r") as f:
            opened_streams = json.load(f)
    else:
        opened_streams = []

    max_streams = 100

    for channel_id in channel_ids:
        live_status = youtube_api.get_live_status(channel_id)
        
        if 'live' in live_status and live_status['live']:
            live_url = live_status['live'][0]['url']
            if live_url not in opened_streams:
                print(f"{GREEN}Opening live stream: {live_url}{RESET}")
                webbrowser.open_new_tab(live_url)
                opened_streams.append(live_url)

                if len(opened_streams) > max_streams:
                    opened_streams.pop(0)  # Keep list within the max limit

    with open(opened_streams_file, "w") as f:
        json.dump(opened_streams, f, indent=4)


def delete_lives():
    with open(opened_streams_file, "w") as f:
        json.dump([], f, indent=4)
    print(f"{GREEN}Live stream data deleted.{RESET}")


def automation_loop():
    """Handles the automation in the background."""
    while automation:
        check_live() 
        time.sleep(300)  # Delay for 5 minutes

def view_subscriptions():
    """Display all current subscriptions organized by branch and generation."""
    try:
        with open("subscriptions.json", "r") as f:
            data = json.load(f)
            subscriptions = data if isinstance(data, list) else data.get("subscriptions", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"{RED}No subscription data found.{RESET}")
        return

    if not subscriptions:
        print(f"{YELLOW}You are not subscribed to any VTubers.{RESET}")
        return

    # Organize subscriptions by branch and generation
    organized_subs = {}
    
    for vtuber in subscriptions:
        name = vtuber['name']
        found = False
        
        # Find which branch and generation the VTuber belongs to
        for branch_name, branch_data in vtubers.items():
            if found:
                break
                
            for gen_name, gen_list in branch_data.items():
                for v in gen_list:
                    if v['name'] == name:
                        if branch_name not in organized_subs:
                            organized_subs[branch_name] = {}
                        
                        if gen_name not in organized_subs[branch_name]:
                            organized_subs[branch_name][gen_name] = []
                            
                        organized_subs[branch_name][gen_name].append(name)
                        found = True
                        break
                        
                if found:
                    break

    print(f"{BOLD}{CYAN}       YOUR SUBSCRIPTIONS       {RESET}")
    
    total_subs = len(subscriptions)
    
    for branch_name, branch_data in organized_subs.items():
        print(f"{BOLD}{YELLOW}┌─ {branch_name}{RESET}")
        
        for gen_name, members in branch_data.items():
            print(f"{YELLOW}│  ├─ {gen_name}{RESET}")
            
            for member in members:
                print(f"{YELLOW}│  │  └─ {GREEN}{member}{RESET}")
    
    print(f"\n{BOLD}{CYAN}Total Subscriptions: {total_subs}{RESET}")


def main():
    global automation
    automation = False
    while True:
        doing = input(f"\n{GREEN}type help for commands{RESET}\nType what you want to do:\n\n")

        if doing in {'sub', 'subscribe'}:
            subscribe()
        elif doing in {'check', 'lives', 'check lives'}:
            check_live()
        elif doing in {'delete', 'del'}:
            delete_lives()
        elif doing in {'list', 'view', 'subs', 'subscriptions'}:
            view_subscriptions()
        elif doing in {'auto', 'automation'}:
            automation = not automation  # Toggle the automation flag
            if automation:
                print(f"{GREEN}Automation enabled. Checking live streams every 5 minutes...{RESET}")
                automation_thread = threading.Thread(target=automation_loop)
                automation_thread.daemon = True
                automation_thread.start()
            else:
                print(f"{RED}Automation disabled.{RESET}")
        elif doing == 'exit':
            break
        elif doing == 'help':
            print(f"\n'{YELLOW}sub{RESET}' to subscribe\n'{YELLOW}check{RESET}' to check live streams\n'{YELLOW}delete{RESET}' to reset live stream data\n'{YELLOW}list{RESET}' to view subscriptions\n'{YELLOW}automation{RESET}' to toggle auto checking\n'{YELLOW}exit{RESET}' to quit")
        else:
            print(f'{RED}Invalid option. Please try again.{RESET}')

if __name__ == "__main__":
    main()