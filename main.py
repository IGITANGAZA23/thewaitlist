import sys
from waitlist import Waitlist
from ingabotool import mask_email, truncate

def run_demonstration():
    print("=" * 60)
    print("      PROJECT WAITLIST - AUTOMATED FEATURE DEMONSTRATION")
    print("=" * 60)

    waitlist = Waitlist()

    print("\n[1] Testing User Registration with Valid Inputs:")
    test_users = [
        ("Alice In Wonderland", "alice@wonderland.com"),
        ("Bob Builder", "bob.builder@construction.org"),
        ("Charlie Brown", "charlie@peanuts.com"),
    ]
    for username, email in test_users:
        res = waitlist.join(username, email)
        print(f" -> {res['message']} (Code: {res.get('referral_code')})")

    print("\n[2] Testing Email Validation (via ingabotool.is_valid_email):")
    bad_emails = ["invalid-email", "test@", "@domain.com", "spaces in@mail.com"]
    for bad in bad_emails:
        res = waitlist.join("TestUser", bad)
        print(f" -> Input: '{bad}' => {res['message']}")

    print("\n[3] Testing Duplicate Prevention:")
    dup_res = waitlist.join("Alice Two", "alice@wonderland.com")
    print(f" -> Duplicate Email check: {dup_res['message']}")

    dup_uname = waitlist.join("alice-in-wonderland", "newalice@example.com")
    print(f" -> Duplicate Username check: {dup_uname['message']}")

    print("\n[4] Displaying Public Waitlist (Emails masked via ingabotool.mask_email):")
    waitlist.display_waitlist(as_admin=False)

    print("\n[5] Displaying Admin Waitlist (Full Details):")
    waitlist.display_waitlist(as_admin=True)

    print("\n[6] Checking Waitlist Statistics:")
    stats = waitlist.get_statistics()
    print(f" -> Total Registered Users: {stats['total_users']}")

    print("\n[7] Testing Admin Removal:")
    removed = waitlist.remove_entry("bob.builder@construction.org")
    print(f" -> Removed Bob: {removed}")
    print(f" -> Updated Total Count: {waitlist.get_statistics()['total_users']}")

    print("\n[8] Privacy Notice:")
    print(" -> We collect your email solely to notify you when the product launches.")
    print(" -> Public leaderboards will always mask your email for privacy.")
    print("\n" + "=" * 60)
    print("            DEMONSTRATION COMPLETE")
    print("=" * 60)

def interactive_menu():
    waitlist = Waitlist()
    while True:
        print("\n=== Project Launch Waitlist Menu ===")
        print("1. Join Waitlist")
        print("2. Check My Queue Position")
        print("3. View Public Waitlist")
        print("4. View Waitlist (Admin)")
        print("5. View Stats")
        print("6. Remove User (Admin)")
        print("7. Run Automated Demo")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            referral = input("Enter referral code (optional, press Enter to skip): ").strip() or None
            res = waitlist.join(username, email, referral)
            print("\nResult:", res["message"])
        elif choice == "2":
            email = input("Enter your registered email: ").strip()
            pos = waitlist.get_position(email)
            if pos > 0:
                print(f"\nUser with email {mask_email(email)} is at Position #{pos}")
            else:
                print("\nEmail not found in waitlist.")
        elif choice == "3":
            waitlist.display_waitlist(as_admin=False)
        elif choice == "4":
            waitlist.display_waitlist(as_admin=True)
        elif choice == "5":
            stats = waitlist.get_statistics()
            print(f"\nTotal registrations: {stats['total_users']}")
        elif choice == "6":
            email = input("Enter email to remove: ").strip()
            if waitlist.remove_entry(email):
                print(f"Successfully removed {email}.")
            else:
                print("Email not found.")
        elif choice == "7":
            run_demonstration()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-8.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demonstration()
    else:
        interactive_menu()
