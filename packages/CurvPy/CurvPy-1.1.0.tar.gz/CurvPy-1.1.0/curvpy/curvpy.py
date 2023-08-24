import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import scipy.optimize as optimize
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import warnings


# Function to calculate R-squared value
def r_squared(y_true, y_pred):
    residuals = y_true - y_pred
    ss_residuals = np.sum(residuals ** 2)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_residuals / ss_total)
    return r2

# Linear regression
def linear_regression(x, y):
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    equation = f'y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Polynomial regression
def polynomial_regression(x, y, degree):
    polynomial_features = PolynomialFeatures(degree=degree)
    x_poly = polynomial_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    y_pred = model.predict(x_poly)
    equation = 'y ='
    for i, coef in enumerate(model.coef_):
        equation += f' {coef:.2f}x^{i} +'
    equation += f' {model.intercept_:.2f}'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Logarithmic regression
def logarithmic_regression(x, y):
    def logarithmic_func(x, a, b):
        return a + b * np.log(x)
    params, _ = curve_fit(logarithmic_func, x, y)
    y_pred = logarithmic_func(x, *params)
    equation = f'y = {params[0]:.2f} + {params[1]:.2f} * log(x)'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Exponential regression
def exponential_regression(x, y):
    def exponential_func(x, a, b):
        return a * np.exp(b * x)
    params, _ = curve_fit(exponential_func, x, y)
    y_pred = exponential_func(x, *params)
    equation = f'y = {params[0]:.2f} * exp({params[1]:.2f} * x)'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Power law regression
def power_law_regression(x, y):
    def power_law_func(x, a, b):
        return a * np.power(x, b)
    params, _ = curve_fit(power_law_func, x, y)
    y_pred = power_law_func(x, *params)
    equation = f'y = {params[0]:.2f} * x^{params[1]:.2f}'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Sinusoidal regression
def sinusoidal_regression(x, y):
    def sinusoidal_func(x, a, b, c, d):
        return a * np.sin(b * x + c) + d
    params, _ = curve_fit(sinusoidal_func, x, y)
    y_pred = sinusoidal_func(x, *params)
    equation = f'y = {params[0]:.2f} * sin({params[1]:.2f} * x + {params[2]:.2f}) + {params[3]:.2f}'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Multiple linear regression
def multiple_linear_regression(x, y):
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    equation = 'y ='
    for i, coef in enumerate(model.coef_):
        equation += f' {coef:.2f}x{i+1} +'
    equation += f' {model.intercept_:.2f}'
    r2 = r_squared(y, y_pred)
    return equation, r2

# Data sleuth function
def datasleuth(x, y):
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7)

    # Reshape the data for PolynomialFeatures
    x_train_reshaped = x_train.reshape(-1, 1)
    x_test_reshaped = x_test.reshape(-1, 1)

    # Set the range of degrees to search
    param_grid = {'poly__degree': np.arange(1, 11)}

    # Create a pipeline with PolynomialFeatures and LinearRegression
    pipeline = Pipeline([
        ('poly', PolynomialFeatures()),
        ('model', LinearRegression())
    ])

    # Perform a grid search to find the best degree
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    grid_search.fit(x_train_reshaped, y_train)

    # Get the best degree and best model
    best_degree = grid_search.best_params_['poly__degree']
    best_model = grid_search.best_estimator_

    # Predict using the best model
    y_pred = best_model.predict(x_test_reshaped)

    # Calculate and print the best polynomial regression equation
    coefficients = best_model.named_steps['model'].coef_
    equation = f"y = {coefficients[0]:.4f}"
    for i in range(1, best_degree + 1):
        equation += f" + {coefficients[i]:.4f}x^{i}"

    # Linear regression
    linear_equation, linear_r2 = linear_regression(x.reshape(-1, 1), y)
    print("Linear Regression")
    print("Equation:", linear_equation)
    print("R-squared value:", linear_r2)
    print()
    print("=" * 40)


    # Polynomial regression
    poly_degree = best_degree
    poly_equation, poly_r2 = polynomial_regression(x.reshape(-1, 1), y, poly_degree)
    print("Polynomial Regression (Degree", poly_degree, ")")
    print("Equation:", poly_equation)
    print("R-squared value:", poly_r2)
    print()
    print("=" * 40)


    # Logarithmic regression
    log_equation, log_r2 = logarithmic_regression(x, y)
    print("Logarithmic Regression")
    print("Equation:", log_equation)
    print("R-squared value:", log_r2)
    print()
    print("=" * 40)


    # Exponential regression
    exp_equation, exp_r2 = exponential_regression(x, y)
    print("Exponential Regression")
    print("Equation:", exp_equation)
    print("R-squared value:", exp_r2)
    print()
    print("=" * 40)


    # Power law regression
    power_law_equation, power_law_r2 = power_law_regression(x, y)
    print("Power Law Regression")
    print("Equation:", power_law_equation)
    print("R-squared value:", power_law_r2)
    print()
    print("=" * 40)

    # Sinusoidal regression
    sinusoidal_equation, sinusoidal_r2 = sinusoidal_regression(x, y)
    print("Sinusoidal Regression")
    print("Equation:", sinusoidal_equation)
    print("R-squared value:", sinusoidal_r2)
    print()
    print("=" * 40)

    print("Polynomial Regression Equation (Machine learning):", equation)

    # Calculate and print the mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

    # Calculate and print the R-squared score
    r2 = r2_score(y_test, y_pred)
    print("R2 Score:", r2)
    print("=" * 40)



    warnings.filterwarnings("ignore", category=np.RankWarning)

    # Find the best degree based on R-squared score
    best_degree = None
    best_r2 = -float('inf')
    
    for degree in range(1, 51):
        # Fit a polynomial regression model
        coefficients = np.polyfit(x, y, degree)
        
        # Generate predictions
        y_pred = np.polyval(coefficients, x)
        
        # Compute R-squared score
        r2 = r2_score(y, y_pred)
        
        if r2 > best_r2:
            best_r2 = r2
            best_degree = degree
            best_equation = "f(x) = "
            degree_str = str(degree)
            for i, coef in enumerate(coefficients):
                power = degree - i
                term = f"{coef:.4f}x^{power}" if power > 0 else f"{coef:.4f}"
                best_equation += term
                if i < len(coefficients) - 1:
                    best_equation += " + "
    
    # Print the results
    print("Equation for Best Degree:")
    print(best_equation)
    print(f"Best Degree: {best_degree}")
    print(f"R-squared (R^2) for Best Degree: {best_r2}")
    
    return best_degree, best_r2

def optifit(func, x_data, y_data, guess_params):
    # Perform curve fitting
    fitted_params, _ = optimize.curve_fit(func, x_data, y_data, guess_params)
    y_pred = func(x_data, *fitted_params)

    # Calculate metrics
    residuals = y_data - y_pred
    sse = np.sum(residuals ** 2)
    rmse = np.sqrt(sse / len(x_data))
    r_squared = 1 - (sse / np.sum((y_data - np.mean(y_data)) ** 2))
    chi_square = np.sum((residuals / y_pred) ** 2)
    
    # Perform statistical tests
    ks_statistic, ks_pvalue = stats.kstest(residuals, 'norm')
    ad_statistic, ad_critical_values, ad_significance_levels = stats.anderson(residuals, 'norm')
    
    # Print results
    print("Fitting results:")
    print("Parameters:", fitted_params)
    print("Number of data points:", len(x_data))
    print("Number of parameters:", len(fitted_params))
    print("SSE:", sse)
    print("RMSE:", rmse)
    print("R-squared:", r_squared)
    print("Chi-square:", chi_square)
    print("KS Test - Statistic:", ks_statistic)
    print("KS Test - p-value:", ks_pvalue)
    print("AD Test - Statistic:", ad_statistic)
    print("AD Test - Critical Values:", ad_critical_values)
    print("AD Test - Significance Levels:", ad_significance_levels)
    
    # Plot data and fitted function
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label='Data')
    plt.plot(x_data, y_pred, label='Fit')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Data and Fitted Function')
    plt.show()
    
    # Generate heatmap of parameter values
    param_range = np.linspace(-1, 1, 100)  # Adjust the range as needed
    param1_range, param2_range = np.meshgrid(param_range, param_range)
    param_values = np.zeros_like(param1_range)
    for i in range(len(param_range)):
        for j in range(len(param_range)):
            params = fitted_params.copy()
            params[0] = param1_range[i, j]
            params[1] = param2_range[i, j]
            y_pred = func(x_data, *params)
            residuals = y_data - y_pred
            param_values[i, j] = np.sum(residuals ** 2)
    
    # Plot heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(param_values, extent=[-1, 1, -1, 1], cmap='hot', aspect='auto')
    plt.colorbar()
    plt.xlabel('Parameter 1')
    plt.ylabel('Parameter 2')
    plt.title('Heatmap of Parameter Values')
    plt.show()

def optifit_v2(func, initial_parameters, x, y):
    def ask_user_input(prompt, default=None):
        if default is not None:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        value = input(prompt)
        if value == '':
            return default
        if value == "-inf":
            return -np.inf
        if value == "inf":
            return np.inf
        return eval(value)



    
    lower_bounds_input = ask_user_input("Enter the lower bounds (optional): ", default=None)
    upper_bounds_input = ask_user_input("Enter the upper bounds (optional): ", default=None)
    maxfev = ask_user_input("Enter the number of function evaluations (optional): ", default=None)
    
    lower_bounds = lower_bounds_input if lower_bounds_input is not None else -np.inf
    upper_bounds = upper_bounds_input if upper_bounds_input is not None else np.inf
    
    if maxfev is None:
        maxfev = 10000
    
    popt, pcov = curve_fit(func, x, y, p0=initial_parameters, bounds=(lower_bounds, upper_bounds), maxfev=maxfev)
    
    return popt
