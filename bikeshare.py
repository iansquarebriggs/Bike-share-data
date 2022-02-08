import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        cities = ['new york city', 'chicago', 'washington']
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

        city = input("Enter 'new york city', 'chicago' or 'washington': ").lower()
        if city in cities:
            break

    while True:
        month = input("Enter any of the first 6 months or 'all' to select all 6 months: ").lower()
        if month in months:
            break

    while True:
        day = input("Enter any day of the week or 'all' for all days: ").lower()
        if day in days:
            break

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
       df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('The most common month: ', common_month)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]
    print('The most common day: ', common_day)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour: ', common_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].value_counts()[:1]
    print('The most common start station: ', start_station)

    end_station = df['End Station'].value_counts()[:1]
    print('The most common end station: ', end_station)

    start_end_station = df['Start Station'].value_counts()[:1] + df['End Station'].value_counts()[:1]
    print('The most frequent combination of start station and end station: ', start_end_station)

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = round((df['Trip Duration'].sum() / 60) / 24, 2)
    print('The total travel time: {} hours'.format(trip_duration))

    avg_duration = round(df['Trip Duration'].mean() / 60, 2)
    print('The average trip duration: {} minutes'.format(avg_duration))

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()
    print('The counts of user types: ', user_type)

    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('The counts of gender: ', gender)
    else:
        print('No gender data available')

    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].value_counts().reset_index().min()[:1]
        print('The earliest year of birth: ', int(earliest_year))
    else:
        print('No earliest birth year data available')

    if 'Birth Year' in df:
        recent_year = df['Birth Year'].value_counts().reset_index().max()[:1]
        print('The most recent year of birth: ', int(recent_year))
    else:
        print('No most recent birth year data available')

    if 'Birth Year' in df:
        common_year = df['Birth Year'].value_counts().reset_index()[:1]
        print('The most common year of birth: ', common_year)
    else:
        print('No most common birth year data available')

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def row_data(df):
    ''' Asks user if they want to see 5 rows of data and
        repeats 5 rows of raw data everytime user input is yes. '''

    row = 0
    while True:
        rowData = input('Would you like to se the raw data? Type yes or no: ').lower()
        if rowData == 'yes':
            rows = df.iloc[row:row + 5]
            pd.set_option('display.max_columns', 200)
            print(rows)
            row += 5
        else:
            break


def main():
    """ When city, month, day are entered all functions are displayed.
        If user doesn't want to see raw data, user is asked if they want to restart. """

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
