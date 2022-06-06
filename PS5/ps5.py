# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Daniel Castro
# Collaborators (discussion):
# Time:

import numpy as np
import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

# Testing class Climate
# year2000=Climate('PS5/data.csv').get_yearly_temp('BOSTON', 2000)
# print(year2000)
# somedate=Climate('PS5/data.csv').get_daily_temp('BOSTON', 2, 4, 2000)
# print(somedate)

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    output = []
    for deg in degs:
        output.append(pylab.polyfit(x,y,deg))
    return output

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    num = (y-estimated)**2
    num = num.sum()
    mean = pylab.mean(y)
    dem = (y-mean)**2
    dem = dem.sum()
    return 1-num/dem

# Testing r_squared  
# a=pylab.array([1961, 1962, 1963])
# b=pylab.array([1971, 1972, 1973])
# print(r_squared(a,b))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        pylab.scatter(x,y, label='Data points', color = 'b')
        est=[pylab.poly1d(model)(x_i) for x_i in x]
        pylab.plot(x,est, label='Model generated', color = 'r')
        pylab.legend()
        pylab.xlabel('Years')
        pylab.ylabel('Degrees (ºC)')
        r=r_squared(y, est)
        model_degree = len(model)-1

        # If degree of model is 1, then calculate se/slope and add to a string
        string_se=''
        if model_degree==1:
            string_se = 'se = %.3f' % se_over_slope(x, y, est, model)
        
        pylab.title('Degree ' + str(model_degree) \
            + '\n' + string_se+ \
                ' ; r^2 = %.3f' % r ) 
        pylab.show()

# Testing evaluate_models_on_training      
# x = pylab.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# y = pylab.array([15, 14, 13, 7, 5, 5, 8, 10, 16, 20])
# models=generate_models(x, y, [1,2,3])
# evaluate_models_on_training(x, y, models)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    year_avg=[]
    for year in years:
        cities_yearly_avg=[]
        for city in multi_cities:
            cities_yearly_avg.append(pylab.array(climate.get_yearly_temp(city, year)).mean())
        year_avg.append(pylab.array(cities_yearly_avg).mean())
    return pylab.array(year_avg)
    
def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg=[]
    for i in range(1,len(y)+1):
        window=range(max(0,i-window_length),i)
        window_temp=[]
        for window_index in window:
            window_temp.append(y[window_index])
        moving_avg.append(pylab.array(window_temp).mean())
    return pylab.array(moving_avg)
            
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    num = (y-estimated)**2
    num = num.sum()
    dem = y.shape[0]
    return (num/dem)**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    year_std=[]
    for year in years:
        cities_yearly=[]
        for city in multi_cities:
            temp_byyear_bycity=climate.get_yearly_temp(city, year)
            cities_yearly.append(temp_byyear_bycity)
        temp_city_avg=pylab.array(cities_yearly).mean(axis=0)
        # city_avg=np.mean(cities_yearly, axis=0)
        year_std.append(pylab.array(temp_city_avg).std())
    return pylab.array(year_std)
    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        pylab.scatter(x,y, label='Data points', color = 'b')
        est=[pylab.poly1d(model)(x_i) for x_i in x]
        pylab.plot(x,est, label='Model generated', color = 'y')
        pylab.legend()
        pylab.xlabel('Years')
        pylab.ylabel('STD')
        rmse_value=rmse(y, est)
        model_degree = len(model)-1

        
        pylab.title('Degree ' + str(model_degree) \
                    + ' ; rmse = %.3f' % rmse_value ) 
        pylab.show()

if __name__ == '__main__':

    climate = Climate('PS5/data.csv')
    years = pylab.array(range(1961,2009+1))

    # Part A.4
    # temp_jan_10 = [climate.get_daily_temp('NEW YORK', 1, 10, year) for year in years]
    # temp_jan_10 = pylab.array(temp_jan_10)
    # models=generate_models(years, temp_jan_10, [1])
    # evaluate_models_on_training(years, temp_jan_10, models)
    # temp_anual=[climate.get_yearly_temp('NEW YORK', year).mean() for year in years]
    # temp_anual=pylab.array(temp_anual)
    # models=generate_models(years, temp_anual, [1])
    # evaluate_models_on_training(years, temp_anual, models)
    
    """
    ● What difference does choosing a specific day to plot the data for versus calculating 
    the yearly average have on our graphs (i.e., in terms of the R 2 values and the fit of 
    the resulting curves)? Interpret the results. 
    
    By choosing the a specific day, the variance of the temperature is higher. The distance 
    between points and the model slope is bigger. Therefore, the R 2 value is worst (smaller)
    
    ● Why do you think these graphs are so noisy? Which one is more noisy?
    Because temperature varies depending on the year. Temperature on the January 10th is more noisy
    because on the anual temperature the differences between years get averaged out. 
    
    ● How do these graphs support or contradict the claim that global warming is leading to an increase 
    in temperature? The slope and the standard error-to-slope ratio could be helpful in thinking about this.
    
    The graphs support the claim that global warning is leading to an increase in temperature. In both graphs 
    there is a positive trend, validated by the standard error-to-slope ratio.
    """
    
    # Part B

    # national_yearly_avg=gen_cities_avg(climate, CITIES , list(years))
    # models=generate_models(years, national_yearly_avg, [1])
    # evaluate_models_on_training(years, national_yearly_avg, models)

    """
    ● How does this graph compare to the graphs from part A (i.e., in terms of
    the R 2 values, the fit of the resulting curves, and whether the graph
    supports/contradicts our claim about global warming)? Interpret the
    results.

    The model for the graph Part B4 has a higher r², which means that slope has less error for predicting
    the values of yearly tempeatures averaged by city.
    Therefore we can assert with more certainty the claim about the global warning.

    ● Why do you think this is the case?
    The data points, that represented the averaged yearly temperatures, have less variance between years 
    making it easier for the model to minimize the distance from the slope to the data points.


    ● How would we expect the results to differ if we used 3 different cities?
    What about 100 different cities?
    If we used only 3 cities the r² would be significantly smaller, around 0.2 or 0.3.
    When we increased the number o cities the variability year-to-year of the temperature decreases
    because it the outliers get averaged out. Therefore the r² increases. 


    ● How would the results have changed if all 21 cities were in the same region
    of the United States (for ex., New England)?
    There would be less variability of temperature between cities, assuming that all cities in 
    New England have a similar temperature along the year. Not sure what would happen to r².
    If you know please make a suggestion to modify the code.
    """
    
    # Part C
    # national_yearly_avg=gen_cities_avg(climate, CITIES , list(years))
    # mov_avg=moving_average(national_yearly_avg, 5)
    # models=generate_models(years, mov_avg, [1])
    # evaluate_models_on_training(years, mov_avg, models)

    """
    ● How does this graph compare to the graphs from part A and B ( i.e., in
    terms of the R 2 values, the fit of the resulting curves, and whether the
    graph supports/contradicts our claim about global warming)? Interpret the
    results.
    Using the moving average the r² value get even higher.

    ● Why do you think this is the case?
    Same reason as before. Yearly temperatures get even more averaged out that
    results in less variability between consecutive years.

    """

    # Part D.2.I
    # training_years=pylab.array(TRAINING_INTERVAL)
    # national_yearly_avg=gen_cities_avg(climate, CITIES , list(TRAINING_INTERVAL))
    # mov_avg=moving_average(national_yearly_avg, 5)
    # models=generate_models(training_years, mov_avg, [1,2,20])
    # evaluate_models_on_training(training_years, mov_avg, models)
    
    """
    ● How do these models compare to each other?
    These use different degrees of a polynomial to fit the training data.

    ● Which one has the best R2? Why?
    The model of degree 20 because it overfits the data.

    ● Which model best fits the data? Why?

    """
    # Part D.2.I
    # training_years=pylab.array(TRAINING_INTERVAL)
    # national_yearly_avg=gen_cities_avg(climate, CITIES , list(TRAINING_INTERVAL))
    # mov_avg=moving_average(national_yearly_avg, 5)
    # models=generate_models(training_years, mov_avg, [1,2,20])
    # testing_years=pylab.array(TESTING_INTERVAL)
    # national_yearly_avg_testing=gen_cities_avg(climate, CITIES , list(TESTING_INTERVAL))
    # mov_avg_testing=moving_average(national_yearly_avg_testing, 5)
    # evaluate_models_on_testing(testing_years, mov_avg_testing, models)
    """
    ● How did the different models perform? How did their RMSEs compare?
    
    ● Which model performed the best? Which model performed the worst? 
    Are they the same as those in part D.2.I? Why?

    Degree 1 model perfomed best which proves it the best suited to 
    predict the temperature rises in the following year.
    Degree 20 model perfomed worst, it is clearly overfitting the data.
    RMSEs values are better in the models with worst r² in D.2.I.

    ●If we had generated the models using the A.4.II data 
    (i.e. average annual temperature of New York City) 
    instead of the 5-year moving average over 22 cities, 
    how would the prediction results 2010-2015 have changed?

    """


    # Part E
    training_years=pylab.array(TRAINING_INTERVAL)
    national_yearly_std= gen_std_devs(climate, CITIES , list(TRAINING_INTERVAL))
    mov_std=moving_average(national_yearly_std, 5)
    models=generate_models(training_years, mov_std, [1])
    evaluate_models_on_training(training_years, mov_std, models)
    
    """
    ●Does the result match our claim (i.e., temperature variation is getting 
    larger over these years)?
    No, actually it is getting smaller. 

    ●Can you think of ways to improve our analysis?
    Measure the standard deviation along different years. 
    """


# temp_array=[6.8007729489975439, 6.9344723094071865, 7.2965004501815818, 6.8077243598168549, 6.5055948680511539, 6.959087494608867, 6.4889799240243695, 6.9510430337868963, 7.0585431115159478, 7.0977420580318782, 6.8386579785236048, 6.731347077523127, 6.6616225764762902, 6.4092396746786013, 6.6214217100011084, 6.7136104957814435, 7.2575482189983553, 7.263276360210706, 7.1787611973720633, 7.0859352578611796, 6.8736741252762821, 6.7957043866857889, 7.0815549177622765, 6.7249974778654433, 7.2162729580931124, 6.4560372283957266, 6.7288306794528907, 6.9720986945202927, 6.922958341746317, 6.3033645588306086, 6.5330170805999908, 6.2777429551963237, 6.8488629387504032, 6.8257830274740625, 6.7856101061465059, 6.7592782215870484, 6.6634050127541604, 6.4486321701001552, 6.3413248952817742, 6.7637674361128752, 6.5519930751275384, 6.6831654464946064, 6.7751550280705839, 6.7435411127318146, 6.8720508861149154, 6.381528250607194, 6.9707944558310109, 6.7582457290380731, 6.7451346848899991]
# pylab.scatter(y=temp_array, x=TRAINING_INTERVAL)
# pylab.show()
