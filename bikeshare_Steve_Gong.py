import time
import datetime
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def get_filters():
    """
    Asks user to specify a city, month, day, and whether they want to see the raw data to analyze as well as whether or not the user want to see the raw data or not.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) raw_data - Yes or No input answer prompt from the user whether they want to see the raw data
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter a city: ")

    while city.lower() != 'chicago' and city.lower() != 'new york' and city.lower() != 'washington':
        city = input("Wrong City, Enter a city (your selections are New York, Chicago or washington): ")

    print("You selected City filter is "  + (city.lower()).title())


    # get user input for month (all, january, february, ... , june)
    month = input("Please enter a month you would like to filter by. \n Alternatively, please enter 'ALL' if you don't want to filter by month: ")

    while month.lower() != 'january' and month.lower() != 'january' and month.lower() != 'february' and month.lower() != 'march' and month.lower() != 'april' and month.lower() != 'may' and month.lower() != 'june' and month.lower() != 'july' and month.lower() != 'august' and month.lower() != 'august' and month.lower() != 'september' and month.lower() != 'october' and month.lower() != 'november' and month.lower() != 'december' and month.lower() != 'all':
        month = input("Wrong entry, please enter a month (ex. January, February) or enter 'ALL': ")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day of the week you would like to filter by. \n Alternatively, please enter 'ALL' if you don't want to filter by a day: ")
    print("You selected Month filter is " + (month.lower()).title())

    while day.lower() != 'monday' and day.lower() != 'tuesday' and day.lower() != 'wednesday' and day.lower() != 'thursday' and day.lower() != 'friday' and day.lower() != 'saturday' and day.lower() != 'sunday' and day.lower() != 'all':
        day = input("Wrong entry, please enter a day of a week (ex. Monday) or enter 'ALL': ")

    print("You selected Day filter is " + (day.lower()).title())

    #get user input if they want to see raw dataframe

    raw_data = input("Please answer yes if you want to see the raw data: ")
    while raw_data.lower() != 'yes' and raw_data.lower() != 'no':
        raw_data = input("Please only answer 'yes' or 'no'. Let's try again: ")

    print('-'*40)
    return city, month, day, raw_data


def load_data(city, month, day, raw_data):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) raw_data - user input whether or not he or she wants to see the raw data, which will be printed by this function
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    #print (df)

    if raw_data.lower() == 'yes':
        index = df.index
        number_of_rows = len (index)
        count = 5
        while raw_data == 'yes' and count <= number_of_rows:
            print (count)
            print(df.head (count))
            if count+5 > number_of_rows:
                count = (number_of_rows - count) + count
            else:
                count = count + 5
            raw_data = input ("Do you want to see more (answer 'yes' if you do)? ")


    #create a column of start and end station by concatnating the string value for start and end stations
    df['station_combo'] = df ['Start Station'].astype(str) + ' and ' + df ['End Station']

    # extract month and day of week from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month.lower() != 'all':
            month = MONTHS.index(month.lower()) + 1
            df = df[df['month'] == month]
    if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    df['hour'] = df['Start Time'].dt.hour
    start_time = time.time()
    popular_hour = df['hour'].mode()[0]
    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]

    # display the most common month
    print('Most common month:',  MONTHS[popular_month-1].title())


    # display the most common day of week
    print('Most common day of week:', popular_day)


    # display the most common start hour
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_station_combo = df['station_combo'].mode()[0]
    # display most commonly used start station
    print('Most commonly used start station:, ', popular_start_station)


    # display most commonly used end station
    print('Most commonly used end station:, ', popular_end_station)


    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start and end stations:, ', popular_station_combo)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #total_travel_time = total_travel_time // 24
    print ('Total travel time:, ', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print ('Mean travel time: ', int(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    gender_types = df['Gender'].value_counts()
    print(gender_types)
    # Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    recent_year = df['Birth Year'].max()
    common_year = df['Birth Year'].mode()[0]

    print ("Earlist birth year: ", int(earliest_year))
    print ("Most recent birth year: ", int(recent_year))
    print ("Most common birth year: ", int(common_year))

    #age calculation by substracting the current year to the birth year
    df['Current Year'] = datetime.date.today().year
    df['Age'] = df['Current Year'] - df['Birth Year']
    average_age = df['Age'].mean()
    print("Average age of a rider is: ", int(average_age))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, raw_data = get_filters()
        df = load_data(city, month, day, raw_data)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
