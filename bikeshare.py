import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': "new_york_city.csv",
              'washington': "washington.csv" }
cities = ["chicago", "new york city", "washington"]
months = ["january", "february", "march", "april", "may", "june"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        city = input("Our cities: Chicago, New York City, Washington\n Which city do you want to explore?\n ").lower()
        #repeat input if it is wrong
        while city not in cities :
            print("\nPLEASE MAKE SURE THAT YOU WRITE WITH CORRECT SPELLING ONE OF OUR CITIES\n")
            city =input("Our cities: Chicago, New York City, Washington\n Which city do you want to explore?\n ").lower()
    except:
        print("\nPLEASE CHOOSE ONE OF OUR CITIES\n")

    # get user input for month (all, january, february, ... , june)
    try:
        month_choosed = input("Choose a month (January, February, ...,June). If you don't want to specify a month just write all\n Which month do you want to explore?\n ").lower()
        #repeat input if it is wrong
        while (month_choosed not in months) & (month_choosed!="all"):
            print("\nPLEASE CHECK THE SPELLING OF MONTH\n")
            month_choosed = input("Choose a month (January, February, ...,June). If you don't want to specify a month just write all\n Which month do you want to explore?\n ").lower()
    except:
        print("PLEASE CHECK THE SPELLING OF THE MONTH")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    try:
        day = input("Choose a day of week (Monday, Tuesday, ...,Sunday). If you don't want to specify a day just write all\n Which day of week do you want to explore?\n ").title()
        #repeat input if it is wrong
        while day not in days_of_week:
            print("\nPLEASE CHECK THE SPELLING OF THE DAY\n")
            day = input("Choose a day of week (Monday, Tuesday, ...,Sunday). If you don't want to specify a day just write all\n Which day of week do you want to explore?\n ").title()
    except:
        print("\nPLEASE CHECK THE SPELLING OF THE DAY\n")

    print('-.'*40)
    return city, month_choosed, day


def load_data(city, month_choosed, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data from selected file
    df = pd.read_csv(str(os.getcwd())+"/"+CITY_DATA[city])
    #convert start time column to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    #create new columns to apply filters and get mode
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour
    #to apply month filter
    if month_choosed != "all":
        # get the month in numbers
        month_choosed = months.index(month_choosed) + 1
        df = df[df["month"] == month_choosed]
    # to apply day filter
    if day != "All":
        df = df[df["day_of_week"] == day]
        
        
    return df


    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month if there is not month filter
    if df["month"].nunique()>1:
        popular_month = df["month"].mode()[0]
        #count no of trips per popular month
        count_popular_month = len(df[df["month"]==popular_month])
        print("The Most Popular Month Is: {}                         Number Of Trips: {} \n".format(months[popular_month-1].title(),count_popular_month))
    
    # display the most common day of week if there is not day filter
    if df["day_of_week"].nunique()>1:
        popular_day = df["day_of_week"].mode()[0]
        #count no of trips per popular day
        count_popular_day = len(df[df["day_of_week"]==popular_day])
        print("The Most Popular Day Of The Week Is: {}                   Number Of Trips: {} ".format(popular_day,count_popular_day))
    
    # display the most common start hour
    popular_hour = df["hour"].mode()[0]
    #count no of trips per popular hour
    count_popular_hour = len(df[df["hour"]==popular_hour])
    print("\nThe Most Popular Start Hour Is: {}                         Number Of Trips: {}".format(popular_hour, count_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-.'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    #create trip column from start -----> to end
    df["trip_stations"] = df["Start Station"] + " -----> " + df["End Station"]
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    #count no of trips per popular start station
    count_popular_start = len(df[df["Start Station"]==popular_start_station])
    print("The Most Popular Start Station Is: {}                   Number Of Trips: {} ".format(popular_start_station, count_popular_start))
        
    # display most commonly used end station            
    popular_end_station = df["End Station"].mode()[0]
    #count no of trips per popular end station
    count_popular_end = len(df[df["End Station"]==popular_end_station])
    print("\nThe Most Popular End Station Is: {}                    Number Of Trips: {} ".format(popular_end_station, count_popular_end))
        
    # display most frequent combination of start station and end station trip
    popular_compination = df["trip_stations"].mode()[0]
    #count no of trips per popular trip
    count_popular_trip = len(df[df["trip_stations"]==popular_compination])
    print("\nThe Most Popular Trip Is: {}             Number Of Trips: {}".format(popular_compination,count_popular_trip))
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-.'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()
    #get total trip duration in time format
    total_hours = pd.Timedelta(seconds=total_duration)
    print("Total Travel Time: {} \n ".format(total_hours))

    # display average trip duration
    average_duration = df["Trip Duration"].mean()
    #get average duration in time format
    Average_minutes = pd.Timedelta(seconds=average_duration)
    print("Average Trip Time: {} ".format(Average_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-.'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User Types:\n{} \n".format(user_types))

    # Display counts of gender
    if "Gender" in df.columns:
        gender= df["Gender"].value_counts()
        print("User Genders\n{} \n".format(gender))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        popular_birth_year = df["Birth Year"].mode()[0]
        print("The Most Popualr Year Of Birth Is: {}".format(int(popular_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-.'*40)


def ask_user(df):
    """to show every function by user request"""
   

def main():
    while True:
        city, month_choosed, day = get_filters()
        df = load_data(city, month_choosed, day)
        time_order = input("\n Are you excited about exploring most popular time to ride a bike? Enter yes or no\n")
        print('-.'*40)
        if time_order.lower()=="yes":
            time_stats(df)
    
        station_order = input("\n Are you excited about exploring most popular stations and trip? Enter yes or no\n")
        print('-.'*40)
        if station_order.lower()=="yes": 
            station_stats(df)

        trip_duration_order = input("\n Are you excited about exploring trip duration? Enter yes or no\n")
        print('-.'*40)
        if trip_duration_order.lower()=="yes":
            trip_duration_stats(df)

        user_order = input("\n Are you excited about exploring some user statistics? Enter yes or no\n")
        print('-.'*40)
        if user_order.lower()=="yes":
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
