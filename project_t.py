import os
import sys
import time
import random
from enum import Enum
""" 
A new Project!
"""
class GameState(Enum):
    EXPLORE = 1
    COMBAT = 2
    INVENTORY = 3
    TERMINAL = 4
    GAME_OVER = 5

class Player:
    def __init__(self):
        self.health = 100
        self.energy = 100
        self.level = 1
        self.exp = 0
        self.credits = 50
        self.inventory = ["Data Chip", "Energy Drink"]
        self.location = "Main Hub"
        self.weapon = "Plasma Pistol"
        self.armor = "Light Jacket"
        self.cybernetics = []
        
    def display_stats(self):
        print(f"\n┌{'─'*30}┐")
        print(f"│ {'HEALTH':<10}: {'█'*int(self.health//10):<20} │")
        print(f"│ {'ENERGY':<10}: {'█'*int(self.energy//10):<20} │")
        print(f"│ {'LEVEL':<10}: {self.level:<20} │")
        print(f"│ {'CREDITS':<10}: {self.credits:<20} │")
        print(f"│ {'WEAPON':<10}: {self.weapon:<20} │")
        print(f"│ {'ARMOR':<10}: {self.armor:<20} │")
        print(f"│ {'LOCATION':<10}: {self.location:<20} │")
        print(f"└{'─'*30}┘")
        
    def use_item(self, item):
        if item == "Energy Drink" and "Energy Drink" in self.inventory:
            self.energy = min(100, self.energy + 30)
            self.inventory.remove("Energy Drink")
            print("\nYou chug the Energy Drink. +30 ENERGY!")
            return True
        return False

class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        
    def display(self):
        print(f"\nENCOUNTERED: {self.name}")
        print(f"HEALTH: {'█'*int(self.health//10)}")
        
    def attack(self):
        return random.randint(self.damage//2, self.damage)

class ProjectT:
    def __init__(self):
        self.player = Player()
        self.state = GameState.EXPLORE
        self.current_enemy = None
        self.terminals_hacked = 0
        self.cybernetics_available = ["Neural Interface", "Optical Enhancer", "Subdermal Armor"]
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_title(self):
        print(r"""
   ___                  _        _____ 
  / _ \ _ __  ___ _ __ | |_ ___ |_   _|
 / /_)/| '_ \/ _ \ '_ \| __/ _ \  | |  
/ ___/ | |_) | __/ | | | || (_) | | |  
\/     | .__/\___|_| |_|\__\___/  |_|  
       |_|                             
        """)
        
    def display_main_menu(self):
        self.clear_screen()
        self.display_title()
        print("\n1. NEW GAME")
        print("2. CONTINUE")
        print("3. ABOUT PROJECT T")
        print("4. QUIT")
        
    def display_about(self):
        self.clear_screen()
        print("PROJECT T - TERMINAL TEXT ADVENTURE")
        print("----------------------------------")
        print("A cyberpunk-themed text adventure game")
        print("where you explore a dystopian city,")
        print("battle rogue AIs, hack terminals,")
        print("and upgrade your cybernetics.")
        print("\nFeatures:")
        print("- Turn-based combat")
        print("- Exploration system")
        print("- Inventory management")
        print("- Terminal hacking mini-game")
        print("- Cybernetic enhancements")
        print("\nPress ENTER to return...")
        input()
        
    def display_location(self):
        locations = {
            "Main Hub": "The central hub of the arcology. Neon signs flicker overhead as drones zip by.",
            "Market Sector": "A bustling marketplace filled with vendors selling tech, cybernetics, and suspicious-looking noodles.",
            "Tech District": "The technology center of the arcology. Filled with research labs and tech shops.",
            "Undercity": "The dark underbelly of the city. Home to hackers, rebels, and things best avoided.",
            "Corporate Tower": "The imposing headquarters of the powerful OmniCorp. Security is tight here.",
            "Server Farm": "Rows upon rows of humming servers. The air is cold and filled with the smell of ozone."
        }
        
        print(f"\nLOCATION: {self.player.location}")
        print(locations.get(self.player.location, "Unknown location"))
        print("\nWhat do you want to do?")
        
    def display_inventory(self):
        print("\nINVENTORY:")
        if not self.player.inventory:
            print("Empty")
        else:
            for i, item in enumerate(self.player.inventory, 1):
                print(f"{i}. {item}")
                
    def explore_menu(self):
        self.clear_screen()
        self.player.display_stats()
        self.display_location()
        
        options = {
            "Main Hub": [
                "Go to Market Sector",
                "Go to Tech District",
                "Go to Undercity",
                "Use item",
                "Check inventory"
            ],
            "Market Sector": [
                "Buy Energy Drink (15 credits)",
                "Go to Main Hub",
                "Go to Corporate Tower",
                "Use item",
                "Check inventory"
            ],
            "Tech District": [
                "Buy Cybernetic Implant (50 credits)",
                "Go to Main Hub",
                "Go to Server Farm",
                "Use item",
                "Check inventory"
            ],
            "Undercity": [
                "Fight Security Bot",
                "Go to Main Hub",
                "Hack Terminal",
                "Use item",
                "Check inventory"
            ],
            "Corporate Tower": [
                "Fight Corporate Guard",
                "Go to Market Sector",
                "Steal Data",
                "Use item",
                "Check inventory"
            ],
            "Server Farm": [
                "Hack Mainframe",
                "Go to Tech District",
                "Fight Security Drone",
                "Use item",
                "Check inventory"
            ]
        }
        
        location_options = options.get(self.player.location, [])
        for i, option in enumerate(location_options, 1):
            print(f"{i}. {option}")
            
        choice = input("\nSelect an option: ")
        return choice, location_options
        
    def handle_explore(self, choice, options):
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid choice!")
            time.sleep(1)
            return
        
        choice_index = int(choice) - 1
        action = options[choice_index]
        
        if "Go to" in action:
            destination = action.split("Go to ")[1]
            self.player.location = destination
            print(f"\nMoving to {destination}...")
            time.sleep(1)
            
            # Random encounter chance
            if random.random() < 0.3 and destination not in ["Main Hub", "Market Sector"]:
                enemies = [
                    Enemy("Rogue Drone", 40, 15),
                    Enemy("Corporate Guard", 60, 20),
                    Enemy("Security Bot", 80, 25),
                    Enemy("Cybernetic Thug", 50, 18)
                ]
                self.current_enemy = random.choice(enemies)
                self.state = GameState.COMBAT
                print("\n!!! ENEMY ENCOUNTER !!!")
                time.sleep(1)
                
        elif action == "Use item":
            self.display_inventory()
            item_choice = input("\nSelect item to use (or 0 to cancel): ")
            if item_choice.isdigit() and int(item_choice) > 0 and int(item_choice) <= len(self.player.inventory):
                item = self.player.inventory[int(item_choice)-1]
                if not self.player.use_item(item):
                    print(f"Cannot use {item} right now.")
            time.sleep(1)
            
        elif action == "Check inventory":
            self.display_inventory()
            input("\nPress ENTER to continue...")
            
        elif "Buy" in action:
            item = action.split("Buy ")[1].split(" (")[0]
            cost = int(action.split("(")[1].split(" ")[0])
            
            if self.player.credits >= cost:
                self.player.credits -= cost
                self.player.inventory.append(item)
                print(f"\nPurchased {item} for {cost} credits!")
            else:
                print("\nNot enough credits!")
            time.sleep(1)
            
        elif "Fight" in action:
            enemy_type = action.split("Fight ")[1]
            enemies = {
                "Security Bot": Enemy("Security Bot", 80, 25),
                "Corporate Guard": Enemy("Corporate Guard", 60, 20),
                "Security Drone": Enemy("Rogue Drone", 40, 15)
            }
            self.current_enemy = enemies.get(enemy_type, Enemy("Thug", 30, 10))
            self.state = GameState.COMBAT
            
        elif "Hack" in action:
            print("\nAccessing terminal...")
            time.sleep(1)
            self.state = GameState.TERMINAL
            
        elif action == "Steal Data":
            if random.random() < 0.4:
                print("\nYou successfully steal valuable corporate data!")
                self.player.credits += 75
                self.player.exp += 25
            else:
                print("\nSecurity caught you! You barely escape.")
                self.player.health -= 20
            time.sleep(2)
            
        elif action == "Hack Mainframe":
            if self.terminals_hacked >= 3:
                print("\nYou hack the mainframe and access critical data!")
                print("You win! Project T is complete!")
                self.state = GameState.GAME_OVER
            else:
                print("\nMainframe security is too strong. Hack more terminals first!")
                time.sleep(2)
                
        elif "Buy Cybernetic Implant" in action:
            if self.player.credits >= 50 and self.cybernetics_available:
                self.clear_screen()
                print("CYBERNETIC IMPLANTS AVAILABLE:")
                for i, implant in enumerate(self.cybernetics_available, 1):
                    print(f"{i}. {implant}")
                    
                choice = input("\nSelect implant to purchase (or 0 to cancel): ")
                if choice.isdigit() and int(choice) > 0 and int(choice) <= len(self.cybernetics_available):
                    implant = self.cybernetics_available[int(choice)-1]
                    self.player.cybernetics.append(implant)
                    self.player.credits -= 50
                    self.cybernetics_available.remove(implant)
                    
                    if implant == "Neural Interface":
                        print("\nNeural Interface installed! +20 MAX ENERGY")
                    elif implant == "Optical Enhancer":
                        print("\nOptical Enhancer installed! +15% combat accuracy")
                    elif implant == "Subdermal Armor":
                        print("\nSubdermal Armor installed! +25 MAX HEALTH")
                        
                    time.sleep(2)
            else:
                print("\nNot enough credits or no implants available!")
                time.sleep(1)
    
    def combat_menu(self):
        self.clear_screen()
        self.player.display_stats()
        self.current_enemy.display()
        
        print("\nCOMBAT OPTIONS:")
        print("1. Attack")
        print("2. Use item")
        print("3. Attempt to flee")
        
        choice = input("\nSelect an option: ")
        return choice
        
    def handle_combat(self, choice):
        if choice == "1":  # Attack
            player_damage = random.randint(15, 30)
            self.current_enemy.health -= player_damage
            print(f"\nYou attack with your {self.player.weapon} for {player_damage} damage!")
            
            if self.current_enemy.health <= 0:
                print(f"\nYou defeated the {self.current_enemy.name}!")
                credits_earned = random.randint(20, 50)
                exp_earned = random.randint(15, 30)
                self.player.credits += credits_earned
                self.player.exp += exp_earned
                print(f"Earned: {credits_earned} credits and {exp_earned} XP!")
                
                # Level up check
                if self.player.exp >= self.player.level * 50:
                    self.player.level += 1
                    self.player.health = 100
                    self.player.energy = 100
                    print(f"\nLEVEL UP! You are now level {self.player.level}!")
                    
                self.state = GameState.EXPLORE
                time.sleep(2)
                return
            
            # Enemy attack
            enemy_damage = self.current_enemy.attack()
            self.player.health -= enemy_damage
            print(f"The {self.current_enemy.name} attacks you for {enemy_damage} damage!")
            
            if self.player.health <= 0:
                print("\nYou have been defeated...")
                self.state = GameState.GAME_OVER
                
            time.sleep(1.5)
            
        elif choice == "2":  # Use item
            self.display_inventory()
            item_choice = input("\nSelect item to use (or 0 to cancel): ")
            if item_choice.isdigit() and int(item_choice) > 0 and int(item_choice) <= len(self.player.inventory):
                item = self.player.inventory[int(item_choice)-1]
                if self.player.use_item(item):
                    self.player.inventory.remove(item)
            time.sleep(1)
            
        elif choice == "3":  # Flee
            if random.random() < 0.6:
                print("\nYou successfully flee from combat!")
                self.state = GameState.EXPLORE
            else:
                print("\nEscape failed!")
                enemy_damage = self.current_enemy.attack()
                self.player.health -= enemy_damage
                print(f"The {self.current_enemy.name} attacks you for {enemy_damage} damage!")
                
                if self.player.health <= 0:
                    print("\nYou have been defeated...")
                    self.state = GameState.GAME_OVER
                    
            time.sleep(1.5)
    
    def terminal_hacking(self):
        self.clear_screen()
        print("TERMINAL HACKING MINI-GAME")
        print("--------------------------")
        print("Decrypt the security protocol by guessing the correct number sequence.")
        
        target = random.randint(1000, 9999)
        attempts = 3
        
        while attempts > 0:
            print(f"\nAttempts remaining: {attempts}")
            try:
                guess = int(input("Enter 4-digit code: "))
            except ValueError:
                print("Invalid input! Enter numbers only.")
                continue
                
            if guess == target:
                print("\nACCESS GRANTED!")
                print("Terminal hacked successfully!")
                self.terminals_hacked += 1
                self.player.credits += 40
                self.player.exp += 20
                print(f"+40 credits, +20 XP! Terminals hacked: {self.terminals_hacked}/3")
                time.sleep(2)
                self.state = GameState.EXPLORE
                return
                
            # Give hints
            correct_digits = sum(1 for g, t in zip(str(guess).zfill(4), str(target)) if g == t)
            print(f"Correct digits: {correct_digits}")
            
            attempts -= 1
            
        print("\nHACKING FAILED! Security protocols triggered!")
        self.player.health -= 15
        time.sleep(1.5)
        self.state = GameState.EXPLORE
    
    def start_game(self):
        self.clear_screen()
        print("\nInitializing Project T...")
        time.sleep(1)
        print("Booting neural interface...")
        time.sleep(1)
        print("Establishing connection to city network...")
        time.sleep(1)
        print("\nWelcome to Neo Arcadia - 2087")
        print("You are a freelance hacker known only as 'Cipher'")
        print("Your mission: Infiltrate OmniCorp and expose their secrets")
        input("\nPress ENTER to begin your journey...")
        
        self.game_loop()
    
    def game_loop(self):
        while True:
            if self.state == GameState.GAME_OVER:
                self.clear_screen()
                if self.player.health <= 0:
                    print("GAME OVER")
                    print("Your systems have been compromised...")
                else:
                    print("PROJECT T COMPLETE")
                    print("You've successfully hacked OmniCorp and exposed their secrets!")
                    print("Neo Arcadia will never be the same...")
                
                print("\nPlay again? (y/n)")
                choice = input().lower()
                if choice == 'y':
                    self.__init__()
                    self.start_game()
                else:
                    break
                
            elif self.state == GameState.EXPLORE:
                choice, options = self.explore_menu()
                self.handle_explore(choice, options)
                
            elif self.state == GameState.COMBAT:
                choice = self.combat_menu()
                self.handle_combat(choice)
                
            elif self.state == GameState.TERMINAL:
                self.terminal_hacking()
    
    def main_menu(self):
        while True:
            self.display_main_menu()
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                self.start_game()
            elif choice == "2":
                if hasattr(self, 'player'):
                    self.game_loop()
                else:
                    print("\nNo saved game found! Starting new game...")
                    time.sleep(1)
                    self.start_game()
            elif choice == "3":
                self.display_about()
            elif choice == "4":
                print("\nExiting Project T...")
                time.sleep(1)
                break
            else:
                print("\nInvalid choice! Please select 1-4.")
                time.sleep(1)

if __name__ == "__main__":
    game = ProjectT()
    game.main_menu()
