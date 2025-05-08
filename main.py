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

def main()
    # 1. Asking what the user wants.
    print("Struggling to decide where to eat? Let me help with that.")
    print("Don't know what to eat? I can help with that!")
    craving = input("Help me out here. Any specific things you're craving? If not, leave blank.) "
                    ).strip()

    #  2. If "No Idea"
    if not craving:
        print("Hmm... I see you don't know what you're craving...")
        while True:
            choice = input(
                "Would you like me to pick for you, or choose from a list? "
                "Enter 'me' if you'd like me to pick or 'list' if you'd like to see the list of available options: "
            ).strip().lower()
            if choice in ("me", "list"):
                break
            print("Invalid input. Please type 'me' or 'list'.")

        if choice == "list":
            print("\nDo any of these foods look inticing?")
            for idx, cat in enumerate(DEFAULT_CATEGORIES, start=1):
                print(f"  {idx}. {cat}")
            sel = input("Enter a number from 1–9: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(DEFAULT_CATEGORIES):
                craving = DEFAULT_CATEGORIES[int(sel) - 1]
            else:
                print("Oops! Invalid number. I'll pick for you.")
                craving = pick_random_craving()
        else:
            craving = pick_random_craving()

        print(f"\nWoo! Let's go with {craving}!\n")

    # 3. Location
    place = input("Where are you currently located? ").strip()

    # 4. Fetching up to 20 spots from Yelp
    spots = search_spots(craving, place, limit=20)
    if not spots:
        print("\nNo results. Try a different term or location.")
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
            print("\nNo more options available.")
            break

        print(f"\nShowing options {start+1}-{min(end, total)} of {total}:\n")
        for idx, biz in enumerate(chunk, start=start+1):
            name = biz["name"]
            addr = ", ".join(biz["location"]["display_address"])
            print(f"{idx}. {name} — {addr}")

        if end >= total:
            break

        more = input("\nNone of these hitting the spot? Want more options? (Y/n) ").strip().lower()
        if more in ("n", "no"):
            break

        page += 1

if __name__ == "__main__":
    main()