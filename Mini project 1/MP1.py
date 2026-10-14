import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import pandas as pd

### Handle data ###
file_path = r"H:\Uni\X3\bervet dataanalys\Mini project 1\LifeExpectancyData.csv"

data = pd.read_csv(file_path)

data.columns = data.columns.str.strip()

# Keep only the two columns
data = data[["Life expectancy", "Schooling"]]

data["Life expectancy"] = pd.to_numeric(
    data["Life expectancy"], errors="coerce"
)

data["Schooling"] = pd.to_numeric(
    data["Schooling"], errors="coerce"
)

cleaned_data = data[~np.isnan(data).any(axis=1)]

x = cleaned_data["Schooling"].to_numpy()
y = cleaned_data["Life expectancy"].to_numpy()


### Test cleaned data ###
def test_cleaned_data():
    tests_ok = 0

    if np.isnan(x).any() == False:
        tests_ok += 1

    if np.isnan(y).any() == False:
        tests_ok += 1

    if np.isfinite(x).all() == True:
        tests_ok += 1

    if np.isfinite(y).all() == True:
        tests_ok += 1

    if tests_ok == 4:
        return True
    else:
        return False


### Plot cleaned data ###
def plot_cleaned_data():

    plt.scatter(x, y, s=10)

    plt.title(
        "Life expectancy in relationship to schooling"
    )

    plt.xlabel("Years schooled")
    plt.ylabel("Life expectancy [years]")

    plt.legend(
        ["Years schooled vs Life expectancy"]
    )

    plt.show()
    plt.figure(1)


"""### Quadratic polynomial ###
A = np.column_stack((
    np.ones(len(x)),
    x,
    x**2
))"""

### improved version###

Pol_degree = 3

A_columns = [np.ones(len(x))]
for deg in range(1, Pol_degree + 1):
    A_columns.append(x**deg)

A = np.column_stack(A_columns)


### Normal equations ###
ATA = A.T @ A
ATy = A.T @ y

coefficients_normal = np.linalg.solve(
    ATA,
    ATy
)


"""def quad_normal(x):

    q2_norm = Polynomial([
        coefficients_normal[0],
        coefficients_normal[1],
        coefficients_normal[2]
    ])

    return q2_norm(x)"""

### improved version without hardlock ###

def quad_normal(x):
    q2_norm = Polynomial(coefficients_normal)
    return q2_norm(x)

### QR decomposition ###
Q, R = np.linalg.qr(A)

coefficients_qr = np.linalg.solve(
    R,
    Q.T @ y
)


"""def quad_qr(x):

    q2_qr = Polynomial([
        coefficients_qr[0],
        coefficients_qr[1],
        coefficients_qr[2]
    ])

    return q2_qr(x)"""

### improved version without hardlock ###

def quad_qr(x):
    q2_qr = Polynomial(coefficients_qr)
    return q2_qr(x)


### Plot quadratic fit using normal equations ###
def plot_quad_normal():

    plt.scatter(
        x,
        y,
        s=10,
        label="Raw data"
    )

    years_schooled = np.linspace(0, 20, 100)

    plt.plot(
        years_schooled,
        quad_normal(years_schooled),
        label="QuadNormal",
        color="green"
    )

    plt.title(
        "Life expectancy in relationship to schooling"
    )

    plt.xlabel("Years schooled")
    plt.ylabel("Life expectancy")

    plt.legend()
    plt.show()
    plt.figure(2)


### Plot quadratic fit using QR decomposition ###
def plot_quad_qr():

    plt.scatter(
        x,
        y,
        s=10,
        label="Raw data"
    )

    years_schooled = np.linspace(0, 20, 100)

    plt.plot(
        years_schooled,
        quad_qr(years_schooled),
        label="QuadQR",
        color="red"
    )

    plt.title(
        "Life expectancy in relationship to schooling"
    )

    plt.xlabel("Years schooled")
    plt.ylabel("Life expectancy")

    plt.legend()
    plt.show()
    plt.figure(3)

### Residual Analysis ###
def plot_residuals():
    y_predicted = quad_normal(x)
    residuals = y - y_predicted

    # Plot histogram of residuals
    plt.hist(residuals, bins=200)

    plt.title("Histogram of Residuals")
    plt.xlabel("Residual Value (y - y_predicted)")
    plt.ylabel("Frequency")

    plt.show()
    plt.figure(4)

### Condition Numbers ###
cond_A = np.linalg.cond(A)
cond_ATA = np.linalg.cond(ATA)

### Main function ###
def main():

    def _test_cleaned_data():

        if test_cleaned_data() == True:
            print("Cleaning of data ok.")
        else:
            print("Cleaning of data failed")

    _test_cleaned_data()

    print(
        "Visualize raw data by plotting cleaned data."
    )

    plot_cleaned_data()

    ### Comparing QR vs normal equations ###
    print(
        "Comparing the resulting quadratic functions "
        "from the normal equations and QR respectively."
    )

    print(
        f"The coefficients for the normal equation "
        f"approach are: {coefficients_normal}\n"
    )

    print(
        f"The coefficients for the QR approach are: "
        f"{coefficients_qr}\n"
    )

    print(
        "Visualize raw data alongside different "
        "quadratic fits."
    )

    plot_quad_normal()
    plot_quad_qr()
    plot_residuals()


    print(f"Condition number of matrix A (QR approach): {cond_A}")
    print(f"Condition number of matrix ATA (Normal equations): {cond_ATA}")


main()