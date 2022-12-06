from realtime_detect import *


def main():
    choice = input("1) Using Model\n2) Using Background\n: ").strip()
    if choice == '1':
        count = count_using_model_xml()
        print(f"Detected {count} vehicles.")
    elif choice == '2':
        show_detect = input("Show detector (Yes/No)? ").lower().strip()
        count = count_using_bg_sub(show_detect)
        print(f"Detected {count} vehicles.")
    else:
        print("invalid choice")


if __name__ == '__main__':
    main()