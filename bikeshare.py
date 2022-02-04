import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

"""define support lists for for get_filters() function"""
city_list = list(CITY_DATA.keys())
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    str_cities = ', '.join(map(str,city_list))
    while True: 
        city = input('\nFor which city do you want to explore data? \n' + 'The available cities are:\n' + str_cities + '\n').strip().lower()
        if city  in city_list:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    str_months = ', '.join(map(str,months))
    while True:
        month = input('\nFor which month do you want to explore data (enter "all" to select all available months)? \n' + 'The available months are:\n' + str_months + '\n').strip().lower()
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    str_days = ', '.join(map(str,days))
    while True:
       day = input('\nFor which day do you want to explore data (enter "all" to select all available days)? \n' + 'The available days are:\n' + str_days + '\n').strip().lower()
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # create start/end combination column
    df['start_end'] = df['Start Station'] + ',' + df['End Station']
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month: ', months[most_common_month].title())

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', most_common_day)

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour: ', most_common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combination = df['start_end'].mode()[0]
    stations = most_frequent_combination.split(',')
    print('Most frequent start/end station combination:\n - Start Station: {}\n - End Station: {}'.format(stations[0],stations[1]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_seconds(seconds):
    """converts an input in seconds into a string with the corresponding days, hours and minutes"""
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) / seconds_in_minute
    
    return str('{} days, {} hours, {} minutes'.format(days, hours, round(minutes,1)))
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_converted = convert_seconds(total_travel_time)
    print('Total travel time: {} seconds (= {})'.format(total_travel_time, total_travel_time_converted))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_converted = convert_seconds(mean_travel_time)
    print('Average travel time: {} seconds (= {})'.format(mean_travel_time, mean_travel_time_converted))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts() 
    print('Count of user types:', )
    for index, user_type_count in enumerate(user_types):
        print(' - {}: {}'.format(user_types.index[index], user_type_count))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns: 
        genders = df['Gender'].value_counts() 
        print('\nCount of gender:')
        for index, gender_count in enumerate(genders):
            print(' - {}: {}'.format(genders.index[index], gender_count))
    else: print('\nNo Gender data avalailable')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year: ', int(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year: ', int(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year: ', int(most_common_birth_year))
    else: print('\nNo Birth Year data avalailable')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def reviewdata(df):
    """asks user if he/she wants to cycle through the loaded data 5 rows at a time """
    print(df.head())
    row = 0
    while True:
        show_next = input('\nWould you like to show the next 5 rows of data(yes/no).\n').strip().lower()
        if show_next.strip().lower() != 'yes':
            return
        row = row + 5
        print(df.iloc[row:row+5])
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        """ asks the user if he/she wants to display the 1st 5 rows of the loaded data"""
        while True:
            show_data = input('\nWould you like to view the first five rows of data (yes/no)?.\n')
            if show_data.strip().lower() != 'yes':
                break
            reviewdata(df)
            break
            
        """ asks the user if he/she wants to restart the program"""
        restart = input('\nWould you like to restart? (yes/no).\n')
        if restart.strip().lower() != 'yes':
            break        

if __name__ == "__main__":
	main()
