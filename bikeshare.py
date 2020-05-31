import time
import pandas as pd
import calendar as cal
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello and Welcome to Ankit\'s bikeshare project submission')
    print('This is available at https://github.com/ankit1234us/pdsnd_github')
    print('Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city_user = input('Enter a City (Chicago, New York City or Washington): ')
        city = city_user.lower().strip()
        if city in CITY_DATA.keys():
            break
        else:
            print(
                'The city - {} - entered by you is not one of the allowed inputs. Please enter again'.format(city_user))

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Choose one from - All, January, February, March, April, May or June...')
        month_user = input('Enter a Month or ''All'' by which you would like to filter the data ')
        month = month_user.lower().strip()
        if month in MONTHS or month == 'all':
            break
        else:
            print(
                'The month input - {} - entered by you is not an allowed input. Please enter again'.format(month_user))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Choose one from - All, Mon, Tue, Wed, Thu, Fri, Sat or Sun...')
        day_user = input('Enter a day or ''All'' by which you would like to filter the data ')
        day = day_user.lower().strip()
        if day in DAYS or day == 'all':
            break
        else:
            print('The day input - {} - entered by you is not an allowed input. Please enter again'.format(day_user))

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = 'static\\' + CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        day = DAYS.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    comm_month = cal.month_name[df['month'].mode()[0]]

    print('The most common month of travel in the given data is: {}'.format(comm_month))

    # display the most common day of week
    comm_dow = cal.day_name[df['day_of_week'].mode()[0]]
    print('The most common day of travel in the given data is: {}'.format(comm_dow))

    # display the most common start hour
    # df['hour'] = df['Start Time'].dt.hour
    comm_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common hour of travel in the given data is: {}'.format(comm_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    comm_s_stn = df['Start Station'].mode()[0]
    print('The most common start station in the given data is: {}'.format(comm_s_stn))

    # display most commonly used end station
    comm_e_stn = df['End Station'].mode()[0]
    print('The most common end station in the given data is: {}'.format(comm_e_stn))

    # display most frequent combination of start station and end station trip
    df['combo station'] = df['Start Station'] + ' -> ' + df['End Station']
    comm_b_stn = df['combo station'].mode()[0]
    print('The most common combination of start and end station in the given data is: {}'.format(comm_b_stn))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total time of travel in the given data is: {}'.format(total_time))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('The average time of travel per trip in the given data is: {}'.format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_by_user = df['User Type'].value_counts()
    print('The number of user type and counts in the given data is: \n{}'.format(count_by_user))

    # Display counts of gender
    try:
        count_by_gender = df['Gender'].value_counts()
        print('The number of user type and counts in the given data is: \n{}'.format(count_by_gender))
    except KeyError:
        print('Sorry! The city you have chosen does not contain Gender Data')

    # Display earliest, most recent, and most common year of birth
    try:
        min_yob = df['Birth Year'].min()
        max_yob = df['Birth Year'].max()
        comm_yob = df['Birth Year'].mode()[0]
        print('The earliest year of birth is: {} '.format(min_yob))
        print('The most recent year of birth is: {} '.format(max_yob))
        print('The most common year of birth is: {}'.format(comm_yob))
    except KeyError:
        print('Sorry! The city you have chosen does not contain Birth Year Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    # city, month, day = 'washington', 'all', 'all'
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
