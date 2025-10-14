import json
import os

USER_FILENAME = "user_data.json"

def get_user_data():
    name = input("Enter name: ").strip()
    if os.path.exists(USER_FILENAME):
        with open(USER_FILENAME, "r") as file:
            try: 
                users = json.load(file)
                existing_user = find_users(users, name)
                if existing_user:
                    print("\nFound existing data:")
                    for key, value in existing_user.items():
                        print(f"   {key.capitalize()}: {value}")
            except json.JSONDecodeError:
                print("File empty/corrupted, starting again.")
    else: 
        print("No existing data found, starting new file.")
        user_data = prompt_user_info(name)
        save_users(user_data)
        print("User sucessfully added to system!")

def save_users(users):
    # saves user info to file
    with open(USER_FILENAME, "w") as file:
        json.dump(users, file, indent=4)

def find_users(users, name):
    # finds users if file and name exist
    return next((user for user in users if user["name"].lower() == name.lower()), None)
            
def prompt_user_info(name):
    # prompts for user attributes
    expenditures = input("Enter how much you spend a month: ")
    food_expend = input("Monthly food expenditures: ")
    travel_expend = input("Monthly travel expenditures: ")
    return {"name": name, "expenditures": expenditures, "monthly_food": food_expend, "monthly_travel": travel_expend}

def main():
    get_user_data()

if __name__ == "__main__":
    main()