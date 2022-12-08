from realtime_detect import *

TEXT = "1) Using Model XML\n2) Using Background Subtraction\n: "


def main():
    choice = input(TEXT).strip()
    num_count = []

    for video in [1, 2]:
        if choice == '1':
            count = count_using_model_xml(video)
            num_count.append(count)
            print(f"Detected {count} vehicles.")
            if video == 1:
                print(f"Ground truth: {ground_truth1} vehicles.")
            else:
                print(f"Ground truth: {ground_truth2} vehicles.")

        elif choice == '2':
            show_detect = input("Show detector (Yes/No)? ").lower().strip()
            count = count_using_bg_sub(show_detect, video)
            num_count.append(count)
            if video == 1:
                print(f"Ground truth: {ground_truth1} vehicles.")
            else:
                print(f"Ground truth: {ground_truth2} vehicles.")

        else:
            print("invalid choice")

    # Calculate MAE
    print('MAE =', (abs(num_count[0] - ground_truth1) +
                    abs(num_count[1] - ground_truth2)) / 2.0)


if __name__ == '__main__':
    main()
