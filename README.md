# Attendance Percentage Predictor

This Python console project reads weekly attendance data from a CSV or accepts percentages manually. It uses NumPy to fit a least-squares line, predicts a future week, limits the prediction to 0–100%, and marks results as **Safe** at 75% or higher.

## Open and run in VS Code

1. Open this project folder in VS Code.
2. Install or enable the Microsoft Python extension. VS Code is set to use the Python interpreter already installed on this computer; if you open the project on another computer, choose its Python 3 interpreter from the Command Palette.
3. In the VS Code integrated terminal, run `python -m pip install -r requirements.txt`.
4. Press **F5** and select **Run Attendance Predictor**.
5. Choose `1` for manual attendance or `2` for CSV. For the included CSV, enter `attendance.csv`; enter `10` for the future week.

The project includes a VS Code launch profile and unittest discovery settings.

## Run the automated tests

Use the VS Code Testing panel, or run this in the integrated terminal:

```text
python -m unittest -v
```

The automated tests cover all four assignment cases, CSV loading, and future-week validation. The program also has a menu option to print the assignment cases as pass/fail results.

## CSV format

Use a header named `Attendance`, followed by one percentage per row. Every percentage must be between 0 and 100, and at least two weeks are required.
