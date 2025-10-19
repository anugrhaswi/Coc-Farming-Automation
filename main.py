from PIL import ImageGrab
import pyautogui
import easyocr
import cv2 
import numpy as np
import time
import os
import json
import sys


# ========== HARDCODED COORDINATES (DEFAULT VALUES) ==========

# Base search screen regions
DEFAULT_GOLD_COORD = (211, 148, 320, 176)
DEFAULT_ELIXIR_COORD = (211, 191, 330, 226)
DEFAULT_DARK_COORD = (210, 236, 291, 265)

# Results screen regions
DEFAULT_EXT_GOLD = (825, 440, 1028, 490)
DEFAULT_EXT_ELIXIR = (825, 500, 1028, 550)
DEFAULT_EXT_DELIXIR = (825, 570, 1028, 615)

# Action buttons
DEFAULT_SELECT_TROOP = (435, 943)
DEFAULT_END_BATTLE = (227, 799)
DEFAULT_CONFIRM_END = (1148, 634)
DEFAULT_RETURN_LOBBY = (1000, 868)
DEFAULT_ATTACK_BTN = (230, 916)
DEFAULT_FIND_MATCH = (380, 720)     # Button to START search from lobby
DEFAULT_NEXT_BTN = (1740, 777)      # Button to SKIP base during search

# Deployment zones (4 lines, start and end points)
DEFAULT_DEPLOY_LINE1 = [(571, 725), (880, 60)]
DEFAULT_DEPLOY_LINE2 = [(1080, 60), (1630, 445)]
DEFAULT_DEPLOY_LINE3 = [(1600, 570), (1260, 850)]
DEFAULT_DEPLOY_LINE4 = [(710, 840), (380, 580)]


def clear_console():
    """Clears the console screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def set_region(region_name, instruction=""):
    """Interactive region selection (2 corners)"""
    print(f"\n--- Setting {region_name} ---")
    if instruction:
        print(f"ℹ️  {instruction}")
    
    pyautogui.alert(f'Move mouse to TOP-LEFT corner of {region_name} and press Enter')
    tl = pyautogui.position()
    print(f"  Top-Left: {tl}")
    
    pyautogui.alert(f'Move mouse to BOTTOM-RIGHT corner of {region_name} and press Enter')
    br = pyautogui.position()
    print(f"  Bottom-Right: {br}")
    
    coords = (tl[0], tl[1], br[0], br[1])
    print(f"  ✓ Region saved: {coords}")
    return coords


def set_button(button_name, instruction=""):
    """Interactive button position selection"""
    print(f"\n--- Setting {button_name} ---")
    if instruction:
        print(f"ℹ️  {instruction}")
    
    pyautogui.alert(f'Move mouse to {button_name} and press Enter')
    pos = pyautogui.position()
    print(f"  ✓ Position saved: {pos}")
    return pos


def set_deploy_line(line_number):
    """Interactive deployment line selection"""
    print(f"\n--- Setting Deployment Line {line_number} ---")
    
    pyautogui.alert(f'Move mouse to START point of Line {line_number} and press Enter')
    start = pyautogui.position()
    print(f"  Start: {start}")
    
    pyautogui.alert(f'Move mouse to END point of Line {line_number} and press Enter')
    end = pyautogui.position()
    print(f"  End: {end}")
    
    print(f"  ✓ Line {line_number} saved: {start} → {end}")
    return [start, end]


def save_config(config_data):
    """Save all coordinates to cache.json"""
    with open('cache.json', 'w') as f:
        json.dump(config_data, f, indent=4)
    print("\n✓ Configuration saved to cache.json!\n")


def load_config():
    """Load all coordinates from cache.json"""
    try:
        with open('cache.json', 'r') as f:
            config = json.load(f)
        
        # Convert lists to tuples where needed
        result = {}
        for key, value in config.items():
            if isinstance(value, list):
                if len(value) == 2 and not isinstance(value[0], list):
                    # Button coordinate
                    result[key] = tuple(value)
                elif len(value) == 4:
                    # Region coordinate
                    result[key] = tuple(value)
                elif len(value) == 2 and isinstance(value[0], list):
                    # Deployment line
                    result[key] = [tuple(value[0]), tuple(value[1])]
                else:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None


def setup_menu():
    """Interactive setup menu"""
    clear_console()
    print("=" * 65)
    print("🔧 COORDINATE SETUP MODE 🔧")
    print("=" * 65)
    print("\nWhat do you want to configure?\n")
    
    print("[1] Resource Regions (Base Search Screen)")
    print("    └─ Gold, Elixir, Dark Elixir regions")
    print("    └─ Selections needed: 6 clicks (3 regions × 2 corners)\n")
    
    print("[2] Result Screen Regions (Loot Earned)")
    print("    └─ Gold earned, Elixir earned, Dark Elixir earned")
    print("    └─ Selections needed: 6 clicks (3 regions × 2 corners)\n")
    
    print("[3] Action Buttons")
    print("    └─ Select Troop, End Battle, Confirm End, Return Lobby,")
    print("       Attack Button, Find Match Button, Next Button")
    print("    └─ Selections needed: 7 clicks (7 buttons)\n")
    
    print("[4] Attack Deployment Zones")
    print("    └─ 4 drag lines (start and end points)")
    print("    └─ Selections needed: 8 clicks (4 lines × 2 points)\n")
    
    print("[5] Everything (All Above)")
    print("    └─ Selections needed: 27 clicks total\n")
    
    print("[6] Cancel")
    print("=" * 65)
    
    while True:
        choice = input("\nEnter your choice (1-6): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return int(choice)
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


def setup_resource_regions(config):
    """Setup option 1: Resource regions"""
    print("\n" + "=" * 65)
    print("📊 CONFIGURING RESOURCE REGIONS (BASE SEARCH SCREEN)")
    print("=" * 65)
    print("\nℹ️  Go to the base search screen in CoC (attack mode).\n")
    input("Press Enter when ready...")
    
    config['gold'] = set_region("Gold", "The gold amount shown on the base you're searching")
    config['elixir'] = set_region("Elixir", "The elixir amount shown on the base")
    config['dark_elixir'] = set_region("Dark Elixir", "The dark elixir amount shown on the base")
    
    print("\n✓ Resource regions configured!")


def setup_result_regions(config):
    """Setup option 2: Result screen regions"""
    print("\n" + "=" * 65)
    print("💰 CONFIGURING RESULT SCREEN REGIONS (LOOT EARNED)")
    print("=" * 65)
    print("\nℹ️  Complete an attack and go to the RESULTS SCREEN.\n")
    input("Press Enter when you're on the results screen...")
    
    config['ext_gold'] = set_region("Gold Earned", "The gold amount you earned (results screen)")
    config['ext_elixir'] = set_region("Elixir Earned", "The elixir amount you earned")
    config['ext_delixir'] = set_region("Dark Elixir Earned", "The dark elixir amount you earned")
    
    print("\n✓ Result screen regions configured!")


def setup_action_buttons(config):
    """Setup option 3: Action buttons"""
    print("\n" + "=" * 65)
    print("🎯 CONFIGURING ACTION BUTTONS")
    print("=" * 65)
    
    print("\nℹ️  Navigate to each screen as prompted.\n")
    input("Press Enter when ready...")
    
    print("\n📍 Go to ATTACK SCREEN (with troops ready)")
    input("Press Enter when ready...")
    config['select_troop_btn'] = set_button("Select Troop Button", "The button to select/activate troops")
    
    print("\n📍 Stay on ATTACK SCREEN")
    config['end_battle_btn'] = set_button("End Battle Button", "The button to end/surrender the attack")
    
    print("\n📍 Click End Battle to see confirmation screen")
    input("Press Enter when you see the confirmation dialog...")
    config['confirm_end_btn'] = set_button("Confirm End Battle Button", "The button that confirms ending battle")
    
    print("\n📍 Go to RESULTS SCREEN (after an attack)")
    input("Press Enter when you're on the results screen...")
    config['return_lobby_btn'] = set_button("Return to Lobby Button", "The button to return home")
    
    print("\n📍 Go to MAIN HOME SCREEN")
    input("Press Enter when you're on the home screen...")
    config['attack_btn'] = set_button("Attack Button", "The main Attack button on home screen")
    
    print("\n📍 Click Attack button, you'll see a matchmaking screen")
    input("Press Enter when you see 'Find a Match' button...")
    config['find_match_btn'] = set_button("Find Match Button", "The button to START searching for bases")
    
    print("\n📍 After clicking Find Match, you'll see a base")
    input("Press Enter when you're viewing a base in search mode...")
    config['next_btn'] = set_button("Next Button", "The button to SKIP to next base")
    
    print("\n✓ Action buttons configured!")


def setup_deployment_zones(config):
    """Setup option 4: Deployment zones"""
    print("\n" + "=" * 65)
    print("⚔️  CONFIGURING DEPLOYMENT ZONES")
    print("=" * 65)
    print("\nℹ️  Go to ATTACK MODE with troops ready to deploy.")
    print("You'll set 4 drag lines covering all sides of the base.\n")
    input("Press Enter when ready...")
    
    config['deploy_line1'] = set_deploy_line(1)
    config['deploy_line2'] = set_deploy_line(2)
    config['deploy_line3'] = set_deploy_line(3)
    config['deploy_line4'] = set_deploy_line(4)
    
    print("\n✓ Deployment zones configured!")


def setup_mode():
    """Main setup mode with menu"""
    choice = setup_menu()
    
    if choice == 6:
        print("\n❌ Setup cancelled.")
        return
    
    # Load existing config or start fresh
    config = load_config() or {}
    
    # Execute chosen setup
    if choice == 1:
        setup_resource_regions(config)
    elif choice == 2:
        setup_result_regions(config)
    elif choice == 3:
        setup_action_buttons(config)
    elif choice == 4:
        setup_deployment_zones(config)
    elif choice == 5:
        # Setup everything
        setup_resource_regions(config)
        setup_result_regions(config)
        setup_action_buttons(config)
        setup_deployment_zones(config)
    
    # Save configuration
    save_config(config)
    
    print("=" * 65)
    print("✓ Setup Complete!")
    print("=" * 65)
    print("\nYour coordinates have been saved to cache.json")
    print("Run the bot normally: python main.py\n")


# ========== CHECK FOR SETUP FLAG ==========

if "--setup" in sys.argv:
    setup_mode()
    sys.exit(0)


# ========== LOAD COORDINATES ==========

clear_console()
print("Loading coordinates...")

cached = load_config()

if cached:
    # Use cached coordinates
    gold_coord = cached.get('gold', DEFAULT_GOLD_COORD)
    elixir_coord = cached.get('elixir', DEFAULT_ELIXIR_COORD)
    dark_elixir_coord = cached.get('dark_elixir', DEFAULT_DARK_COORD)
    
    ext_gold = cached.get('ext_gold', DEFAULT_EXT_GOLD)
    ext_elixir = cached.get('ext_elixir', DEFAULT_EXT_ELIXIR)
    ext_delixir = cached.get('ext_delixir', DEFAULT_EXT_DELIXIR)
    
    select_troop_btn = cached.get('select_troop_btn', DEFAULT_SELECT_TROOP)
    end_battle_btn = cached.get('end_battle_btn', DEFAULT_END_BATTLE)
    confirm_end_btn = cached.get('confirm_end_btn', DEFAULT_CONFIRM_END)
    return_lobby_btn = cached.get('return_lobby_btn', DEFAULT_RETURN_LOBBY)
    attack_btn = cached.get('attack_btn', DEFAULT_ATTACK_BTN)
    find_match_btn = cached.get('find_match_btn', DEFAULT_FIND_MATCH)
    next_btn = cached.get('next_btn', DEFAULT_NEXT_BTN)
    
    deploy_line1 = cached.get('deploy_line1', DEFAULT_DEPLOY_LINE1)
    deploy_line2 = cached.get('deploy_line2', DEFAULT_DEPLOY_LINE2)
    deploy_line3 = cached.get('deploy_line3', DEFAULT_DEPLOY_LINE3)
    deploy_line4 = cached.get('deploy_line4', DEFAULT_DEPLOY_LINE4)
    
    print("✓ Using cached coordinates from cache.json\n")
else:
    # Use hardcoded defaults
    gold_coord = DEFAULT_GOLD_COORD
    elixir_coord = DEFAULT_ELIXIR_COORD
    dark_elixir_coord = DEFAULT_DARK_COORD
    
    ext_gold = DEFAULT_EXT_GOLD
    ext_elixir = DEFAULT_EXT_ELIXIR
    ext_delixir = DEFAULT_EXT_DELIXIR
    
    select_troop_btn = DEFAULT_SELECT_TROOP
    end_battle_btn = DEFAULT_END_BATTLE
    confirm_end_btn = DEFAULT_CONFIRM_END
    return_lobby_btn = DEFAULT_RETURN_LOBBY
    attack_btn = DEFAULT_ATTACK_BTN
    find_match_btn = DEFAULT_FIND_MATCH
    next_btn = DEFAULT_NEXT_BTN
    
    deploy_line1 = DEFAULT_DEPLOY_LINE1
    deploy_line2 = DEFAULT_DEPLOY_LINE2
    deploy_line3 = DEFAULT_DEPLOY_LINE3
    deploy_line4 = DEFAULT_DEPLOY_LINE4
    
    print("✓ Using default hardcoded coordinates\n")
    print("  💡 Run 'python main.py --setup' to configure custom coordinates\n")


# ========== LOAD EASYOCR ==========

print("Loading EasyOCR reader...")
start_time = time.time()
reader = easyocr.Reader(['en'], gpu=False)
end_time = time.time()
execution_time = end_time - start_time
clear_console()
print(f"✓ Reader loaded in {execution_time:.2f} seconds\n")


# ========== HELPER FUNCTIONS ==========

def capture_region(coord):
    """Capture screenshot of specified region"""
    if coord is None:
        raise ValueError("Coordinates not set!")
    return ImageGrab.grab(bbox=coord)


def image_to_cv2(im):
    """Convert PIL Image to OpenCV format (BGR)"""
    if im.mode != 'RGB':
        im = im.convert('RGB')
    numpy_image = np.array(im)
    cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return cv2_image


def extract_text_from_region(coord, resource_name="Unknown"):
    """Extract text from a screen region using OCR"""
    screenshot = capture_region(coord)
    cv2_image = image_to_cv2(screenshot)
    results = reader.readtext(cv2_image, allowlist='0123456789,. ')
    
    extracted = []
    for detection in results:
        text = detection[1]
        confidence = detection[2]
        extracted.append((text, confidence))
    
    return extracted


# Resource coordinate mappings
resources_coord = [
    ("Gold", gold_coord),
    ("Elixir", elixir_coord),
    ("Dark Elixir", dark_elixir_coord)
]

extracted_res_coord = [
    ("Gold", ext_gold),
    ("Elixir", ext_elixir),
    ("Dark Elixir", ext_delixir)
]

# Global dictionaries
found_resources = {}
extracted_res = {}


def get_resource_value(resource_list, res_dict):
    """Read resource values from screen"""
    for resource_name, coord in resource_list:
        try:
            results = extract_text_from_region(coord, resource_name)
            
            if results:
                for text, confidence in results:
                    cleaned_text = text.replace(',', '').replace(' ', '').replace('.', '')
                    
                    if cleaned_text.isdigit():
                        number = int(cleaned_text)
                        res_dict[resource_name] = number
                        print(f"  {resource_name}: {number:,}")
                    else:
                        print(f"  ⚠ {resource_name}: Could not parse '{text}'")
                        res_dict[resource_name] = 0
            else:
                print(f"  ⚠ {resource_name}: No text detected!")
                res_dict[resource_name] = 0
                
        except Exception as e:
            print(f"  ❌ {resource_name} Error: {e}")
            res_dict[resource_name] = 0


def checkif(gold_threshold, elixir_threshold, dark_threshold, req_resource):
    """Check if any resource meets threshold"""
    try:
        if req_resource.get('Gold', 0) >= gold_threshold:
            return True
        elif req_resource.get('Elixir', 0) >= elixir_threshold:
            return True
        elif req_resource.get('Dark Elixir', 0) >= dark_threshold:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in checkif: {e}")
        return False


def find_base(gold_threshold, elixir_threshold, dark_threshold):
    """Search for a base that meets loot requirements"""
    print("\n=== SEARCHING FOR GOOD BASE ===")
    search_count = 0
    
    while True:
        search_count += 1
        print(f"\n--- Checking Base #{search_count} ---")
        
        get_resource_value(resources_coord, found_resources)
        
        if checkif(gold_threshold, elixir_threshold, dark_threshold, found_resources):
            print(f"\n✓✓✓ GOOD BASE FOUND! ✓✓✓")
            print(f"  Gold: {found_resources.get('Gold', 0):,}")
            print(f"  Elixir: {found_resources.get('Elixir', 0):,}")
            print(f"  Dark Elixir: {found_resources.get('Dark Elixir', 0):,}")
            return True
        else:
            print("  ✗ Not enough loot, clicking Next...")
            pyautogui.click(next_btn)
            time.sleep(4)


def check_loot_earned():
    """Read loot from results screen"""
    print("\n=== CHECKING LOOT EARNED ===")
    get_resource_value(extracted_res_coord, extracted_res)
    
    gold = extracted_res.get('Gold', 0)
    elixir = extracted_res.get('Elixir', 0)
    dark = extracted_res.get('Dark Elixir', 0)
    
    print(f"💰 Earned:")
    print(f"   Gold: {gold:,}")
    print(f"   Elixir: {elixir:,}")
    print(f"   Dark: {dark:,}")
    
    return gold, elixir, dark


def deploy_troops():
    """Deploy troops using configured deployment zones"""
    pyautogui.click(deploy_line1[0])
    pyautogui.dragTo(deploy_line1[1], button='left')
    
    pyautogui.click(deploy_line2[0])
    pyautogui.dragTo(deploy_line2[1], button='left')
    
    pyautogui.click(deploy_line3[0])
    pyautogui.dragTo(deploy_line3[1], button='left')
    
    pyautogui.click(deploy_line4[0])
    pyautogui.dragTo(deploy_line4[1], button='left')


def farm_loop(target_gold=5000000, target_elixir=5000000, target_dark=50000):
    """Main farming loop"""
    print("\n" + "=" * 60)
    print("🤖 FARMING BOT STARTED 🤖")
    print("=" * 60)
    
    gold_threshold = 500000
    elixir_threshold = 500000
    dark_threshold = 50000
    
    total_gold = 0
    total_elixir = 0
    total_dark = 0
    attack_count = 0
    
    while True:
        if (total_gold >= target_gold and 
            total_elixir >= target_elixir and 
            total_dark >= target_dark):
            print("\n✓ ALL GOALS REACHED!")
            break
        
        found = find_base(gold_threshold, elixir_threshold, dark_threshold)
        
        if found:
            attack_count += 1
            print(f"\n⚔️  ATTACK #{attack_count} ⚔️")
            
            print("🎯 Selecting troop...")
            pyautogui.click(select_troop_btn)
            time.sleep(0.5)
            
            print("🚀 Deploying troops...")
            for i in range(15):
                deploy_troops()
            
            print("⏳ Attacking...")
            time.sleep(15)
            
            print("🛑 Ending battle...")
            pyautogui.click(end_battle_btn)
            time.sleep(0.25)
            
            print("🛑 Confirming...")
            pyautogui.click(confirm_end_btn)
            time.sleep(4)
            
            earned_gold, earned_elixir, earned_dark = check_loot_earned()
            total_gold += earned_gold
            total_elixir += earned_elixir
            total_dark += earned_dark
            
            print(f"\n📊 Total Progress:")
            print(f"   Gold: {total_gold:,} / {target_gold:,}")
            print(f"   Elixir: {total_elixir:,} / {target_elixir:,}")
            print(f"   Dark: {total_dark:,} / {target_dark:,}")
            
            print("\n🏠 Returning to lobby...")
            pyautogui.click(return_lobby_btn)
            time.sleep(5)
            
            print("🔍 Opening attack menu...")
            pyautogui.click(attack_btn)
            time.sleep(1)
            
            print("🔍 Finding next match...")
            pyautogui.click(find_match_btn)
            time.sleep(5)


# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    clear_console()
    print("\n🎮 CLASH OF CLANS BOT 🎮")
    print("=" * 60)
    print("💡 Tip: Run 'python main.py --setup' to configure coordinates\n")
    
    input('Press Enter to start farming...')
    clear_console()
    
    starting_time = time.time()

    farm_loop(
        target_gold=14000000,
        target_elixir=14000000,
        target_dark=500
    )
    ending_time = time.time()
    time_taken = ending_time-starting_time
    print(time_taken/60,'Minutes')
    
