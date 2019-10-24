import time
import pandas as pd
import numpy as np
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',15)

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington").lower()
    while city not in ['chicago','new york city','washington']:
        print("invalid city name, please choose between 'Chicago', 'New York City','Washington'")
        city = input("Would you like to see data for Chicago, New York or Washington")
    print(city)
    # get user input for month (all, january, february, ... , june)
    month = input("Would you like to see data for 'January','February', 'March', 'April', 'May' or 'June'? Or enter 'all' if you don't wish to filter by month").lower()
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
         print("invalid month name or month does not exist, please choose between 'all','January', 'February', 'March', 'April', 'May', 'June'")
         month = input("Enter the month you would like to see data from, or enter 'all' if you don't wish to filter by month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter a day you would like to see data from, or enter 'all' if you don't wish to filter by day").lower()
    while day not in ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']:
        print("invalid day name, please choose between 'all','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'")
        day = input("Enter a day you would like to see data from, or enter 'all' if you don't wish to filter by day")

    print('-'*40)
    return city, month, day


def load_data(city,month,day):

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

    # display the most common month
    import  calendar
    popular_month = df['month'].mode()[0]
    popular_month = calendar.month_name[popular_month]
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print("Most common month when people travel is '{}'".format(popular_month))
    print("Most common day of week when people travel is '{}'".format(popular_day))
    print("Most common hour when people travel is '{}'".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return popular_month,popular_day,popular_hour

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    counts_popular_start_station = df['Start Station'].value_counts()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    counts_popular_end_station = df['End Station'].value_counts()[0]

    # display most frequent combination of start station and end station trip
    popular_station_combi = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]

    counts_popular_trip= df.groupby(['Start Station', 'End Station']).size().reset_index(name="Time").sort_values(by='Time',ascending=False)['Time'].max()

    print("Most popular start station is '{}' with {} visits".format(popular_start_station, counts_popular_start_station))
    print("Most popular end station is '{}' with {} visits".format(popular_end_station, counts_popular_end_station))
    print("Most popular trip is {} with {} trips".format(popular_station_combi, counts_popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return popular_start_station,popular_end_station,popular_station_combi,counts_popular_start_station,counts_popular_end_station,counts_popular_trip

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print("The total travel time was {}".format(total_travel_time))
    print("The average travel time was {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return total_travel_time,mean_travel_time


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df.groupby(['User Type']).size().reset_index(name = 'Amount').sort_values(by = 'Amount',ascending = False).to_string(index=False)
    print("The amount of people per user type is shown in the table below: \n{}".format(user_type_counts))

    # Display counts of gender
    while city != "washington":
        gender_counts = df.groupby(['Gender']).size().reset_index(name = 'Amount').sort_values(by = 'Amount',ascending = False).to_string(index=False)

    # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print("The amount of people per gender is shown in the table below: \n{}".format(gender_counts))
        print("The earliest birth year of users is {}".format(earliest_birth_year))
        print("The most recent birth year of users is {}".format(max_birth_year))
        print("The most common birth year of users is {}".format(common_birth_year))
        break

    while city == 'washington':
        print("\n !!!! Unfortunately there are no data on gender and birth year of users for the city of Washington")
        break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #return user_type_counts,gender_counts,earliest_birth_year,max_birth_year,common_birth_year


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Ask the user if they want to see the raw data before we display the descriptive statistics
        ask = input("Would you like to see the first 5 lines of raw data before displaying the descriptive statistics? Please enter yes or no").lower()
        x = 0
        while ask == 'yes':
            print(df.head(x + 5))
            x += 5
            ask = input("\nWould you like to see the next 5 lines of raw data before displaying the descriptive statistics? Please enter yes or no").lower()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()





