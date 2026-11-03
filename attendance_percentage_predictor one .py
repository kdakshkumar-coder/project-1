#
import numpy as np
import pandas as pd


def validate(attendance):
    """Return an error if attendance data is invalid, otherwise None."""
    if len(attendance) < 2:
        return "At least 2 weeks of data are required."

    try:
        values = [float(value) for value in attendance]
    except (TypeError, ValueError):
        return "Attendance values must be numeric."

    if any(not np.isfinite(value) for value in values):
        return "Attendance values must be finite numbers."

    if any(value < 0 or value > 100 for value in values):
        return "Attendance must be between 0 and 100."

    return None


def predict(attendance, future_week):
    """
    Fit a straight line to weekly attendance and predict a future week.

    """
    error = validate(attendance)
    if error:
        raise ValueError(error)

    if not isinstance(future_week, (int, np.integer)) or future_week < 1:
        raise ValueError("Future week must be a positive whole number.")
    if future_week <= len(attendance):
        raise ValueError("Future week must be after the weeks with attendance data.")

    attendance = np.asarray(attendance, dtype=float)
    weeks = np.arange(1, len(attendance) + 1)

    slope, intercept = np.polyfit(weeks, attendance, 1)
    raw_prediction = slope * future_week + intercept
    predicted = float(np.clip(raw_prediction, 0, 100))
    status = "Safe" if predicted >= 75 else "Warning: below 75%"

    return float(slope), float(intercept), predicted, status


def cap_note(slope, intercept, future_week):
    """Explain when the linear prediction was limited to the valid range."""
    raw_prediction = slope * future_week + intercept
    if raw_prediction > 100:
        return " (capped at 100)"
    if raw_prediction < 0:
        return " (capped at 0)"
    return ""


def load_attendance_from_csv(file_path):
    """Read attendance values from a CSV file using Pandas."""
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        raise ValueError("CSV file not found. Check the file path.")
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")

    if data.empty:
        raise ValueError("The CSV file has no attendance records.")

    # Prefer a column named 'attendance' (case-insensitive).
    matching_columns = [
        column for column in data.columns
        if str(column).strip().lower() == "attendance"
    ]

    if matching_columns:
        series = data[matching_columns[0]]
    elif len(data.columns) == 1:
        # A CSV with one column is also accepted, whatever its heading.
        series = data.iloc[:, 0]
    else:
        raise ValueError(
            "CSV must contain an 'attendance' column, or only one column."
        )

    if series.isna().any():
        raise ValueError("The CSV contains blank attendance values.")

    try:
        attendance = series.astype(float).tolist()
    except (TypeError, ValueError):
        raise ValueError("CSV attendance values must be numeric.")

    error = validate(attendance)
    if error:
        raise ValueError(error)

    return attendance


def run_test_cases():
    """Run the four test cases shown in the project specification."""
    tests = [
        {
            "name": "Test Case 1: Normal Input",
            "attendance": [90, 88, 86, 84, 82],
            "future_week": 10,
            "expected_slope": -2.0,
            "expected_intercept": 92.0,
            "expected_prediction": 72.0,
            "expected_status": "Warning: below 75%",
        },
        {
            "name": "Test Case 2: Boundary / Minimum Input",
            "attendance": [90, 80],
            "future_week": 3,
            "expected_slope": -10.0,
            "expected_intercept": 100.0,
            "expected_prediction": 70.0,
            "expected_status": "Warning: below 75%",
        },
        {
            "name": "Test Case 3(a): Invalid Input - One Week",
            "attendance": [90],
            "expected_error": "At least 2 weeks of data are required.",
        },
        {
            "name": "Test Case 3(b): Invalid Input - Above 100",
            "attendance": [90, 105, 80],
            "expected_error": "Attendance must be between 0 and 100.",
        },
        {
            "name": "Test Case 4: Different Attendance Scenario",
            "attendance": [70, 74, 78, 82, 86],
            "future_week": 9,
            "expected_slope": 4.0,
            "expected_intercept": 66.0,
            "expected_prediction": 100.0,
            "expected_status": "Safe",
        },
    ]

    print("\n" + "=" * 58)
    print("ATTENDANCE PREDICTOR - AUTOMATED TEST RESULTS")
    print("=" * 58)

    all_passed = True

    for test in tests:
        print(f"\n{test['name']}")

        if "expected_error" in test:
            error = validate(test["attendance"])
            passed = error == test["expected_error"]
            print(f"Expected error: {test['expected_error']}")
            print(f"Actual error:   {error}")
        else:
            slope, intercept, predicted, status = predict(
                test["attendance"], test["future_week"]
            )
            passed = (
                np.isclose(slope, test["expected_slope"], atol=0.01)
                and np.isclose(intercept, test["expected_intercept"], atol=0.01)
                and np.isclose(
                    predicted, test["expected_prediction"], atol=0.01
                )
                and status == test["expected_status"]
            )
            print(f"Slope: {slope:.2f} | Intercept: {intercept:.2f}")
            print(
                f"Predicted attendance for week {test['future_week']}: "
                f"{predicted:.2f}%"
                f"{cap_note(slope, intercept, test['future_week'])}"
            )
            print(status)

        print("Test result:", "PASS" if passed else "FAIL")
        all_passed = all_passed and passed

    print("\n" + "=" * 58)
    print("Overall result:", "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
    print("=" * 58)


def run_predictor():
    """Interactive mode for entering data or loading a CSV."""
    print("\nATTENDANCE PERCENTAGE PREDICTOR")
    print("-" * 35)
    print("1. Enter attendance manually")
    print("2. Load attendance from a CSV file")
    choice = input("Choose 1 or 2: ").strip()

    try:
        if choice == "1":
            raw = input(
                "Enter weekly attendance percentages separated by commas "
                "(example: 90, 88, 86, 84, 82): "
            )
            try:
                attendance = [float(item.strip()) for item in raw.split(",")]
            except ValueError:
                print("Error: Please enter numeric attendance values.")
                return
        elif choice == "2":
            file_path = input("Enter the CSV file path: ").strip()
            attendance = load_attendance_from_csv(file_path)
        else:
            print("Invalid choice. Please select 1 or 2.")
            return

        error = validate(attendance)
        if error:
            print("Error:", error)
            return

        try:
            future_week = int(input("Predict attendance for which future week? "))
        except ValueError:
            print("Error: Future week must be a positive whole number.")
            return

        slope, intercept, predicted, status = predict(attendance, future_week)

        print("\nPREDICTION RESULT")
        print("-" * 35)
        print(f"Slope: {slope:.2f} | Intercept: {intercept:.2f}")
        print(
            f"Predicted attendance for week {future_week}: "
            f"{predicted:.2f}%"
            f"{cap_note(slope, intercept, future_week)}"
        )
        print(status)

    except ValueError as error:
        print("Error:", error)


def main():
    print("ATTENDANCE PERCENTAGE PREDICTOR")
    print("1. Run interactive predictor")
    print("2. Run all project test cases")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        run_predictor()
    elif choice == "2":
        run_test_cases()
    else:
        print("Invalid choice. Please run the program again and choose 1 or 2.")


if __name__ == "__main__":
    main()
