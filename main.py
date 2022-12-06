from realtime_detect import *

TEXT = "1) Using Model XML\n2) Using Background Subtraction\n: "

def main():
    choice = input(TEXT).strip()
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