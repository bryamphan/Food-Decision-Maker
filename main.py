# main.py
# used for when this was a terminal project, doesn't run on web server
import random
from yelp_client import search_spots

DEFAULT_CATEGORIES = [
    "Pizza", "Sushi", "Burgers",
    "Tacos", "Thai Food", "Korean Food",
    "Salads", "BBQ", "Coffee"
]

def pick_random_craving():
    """Choose a random category if the user truly has no idea."""
    return random.choice(DEFAULT_CATEGORIES)

def main():
    # 1. Asking what the user wants.
    print("Bot: Struggling to decide where to eat? Let me help with that.\n")
    craving = input("Bot: Any specific things you're craving? If not, leave blank.\n").strip()

    #  2. If "No Idea"
    if not craving:
        print("Bot: Hmm... I see you don't know what you're craving...\n")
        while True:
            choice = input(
                "Bot: Would you like me to pick for you, or choose from a list?\n"
                "\nBot: Enter 'me' if you'd like me to pick or 'list' if you'd like to see the list of available options: \n"
            ).strip().lower()
            if choice in ("me", "list"):
                break
            print("Bot: Invalid input. Please type 'me' or 'list'.\n")

        if choice == "list":
            print("\nBot: Do any of these foods look inticing?\n"
                  )
            for idx, cat in enumerate(DEFAULT_CATEGORIES, start=1):
                print(f"  {idx}. {cat}")
            sel = input("Bot: Enter a number from 1–9: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(DEFAULT_CATEGORIES):
                craving = DEFAULT_CATEGORIES[int(sel) - 1]
            else:
                print("Bot: Oops! Invalid number. I'll pick for you.\n")
                craving = pick_random_craving()
        else:
            craving = pick_random_craving()

        print(f"\nBot: Woo! Let's go with: {craving}!\n")

    # 3. Location
    place = input("Bot: Where are you currently located? \n").strip()

    # 4. Fetching up to 20 spots from Yelp
    spots = search_spots(craving, place, limit=20)
    if not spots:
        print("\nBot: No results. Try a different term or location.")
        return

    # 4) Display Results in 5
    page_size = 5
    total = len(spots)
    page = 0

    while True:
        start = page * page_size
        end = start + page_size
        chunk = spots[start:end]

        if not chunk:
            print("\nBot: Sorry! No more options available.")
            break

        print(f"\nBot: Showing options {start+1}-{min(end, total)} of {total}:\n")
        for idx, biz in enumerate(chunk, start=start+1):
            name = biz["name"]
            addr = ", ".join(biz["location"]["display_address"])
            print(f"{idx}. {name} — {addr}")

        if end >= total:
            break

        more = input("\nBot: Want more options? (Y/N)\n").strip().lower()
        if more in ("n", "no", "No", "N"):
            print("Bot: Hope you got to pick a spot!")
            break

        page += 1

if __name__ == "__main__":
    main()