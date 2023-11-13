import time
import pandas as pd
import json

# Dictionary of city name and csv file name
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Month and day lists
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
DAYS_SHORT = ['mon', 'tue', 'wed', 'th', 'fri', 'sat', 'sun', 'all']

# Message length constants for printing
MSG_LENGTH = 50
EXTRA_MSG_SPACE = 20
DIVIDER_LENGTH = 150

def get_filters() -> tuple:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter a city name (Chicago, New York City or Washington):")
        city = city.lower().strip()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name. Please try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter a month name (January(1), February(2), March(3), April(4), May(5), June(6) or All(0 / n)):")
        month = month.lower().strip()
        if month.isdigit() and int(month) <= 6:
            month = MONTHS[int(month)]
            break
        elif month == 'n':
            month = 'all'
            break
        elif month in MONTHS:
            break
        else:
            print("Invalid month inoput. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day of week (Monday (mon), Tuesday (tue), Wednesday (wed), Thursday (th), Friday (fri), Saturday (sat), Sunday (sun) or All (n)):")
        day = day.lower().strip()
        if day in DAYS:
            day = day.title()
            break
        elif day == 'n':
            day = 'All'
            break
        elif day in DAYS_SHORT:
            day = DAYS[DAYS_SHORT.index(day)].title()
            break
        else:
            print("Invalid day of week. Please try again.")

    print(f"Chosen city: {city.title()}, month: {month.title()}, day: {day.title()}")
    print(f"\n > > > > > > > > > > > NOTE: Outputs are made to fit within {DIVIDER_LENGTH} characters."
          " Make sure to have wide enough terminal window ! ! ! < < < < < < < < < < <\n")
    print('-'*DIVIDER_LENGTH)
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

    # load selected csv data for the city
    df = pd.read_csv(CITY_DATA[city])

    # Get datetime pd series from start time column, save as new column, 
    # and reserve original time stamp column for later to print in json format
    df['Start Time Stamp'] = pd.to_datetime(df['Start Time'])

    # create month and day column
    df['Month'] = df['Start Time Stamp'].dt.month
    df['Day of week'] = df['Start Time Stamp'].dt.day_name()

    # filter by month if month is not ALL
    if month != 'all':
        month_num = MONTHS.index(month)
        df = df[df['Month'] == month_num]

    # filter by day if day is not ALL
    if day != 'All':
        df = df[df['Day of week'] == day]

    return df


def time_stats(df, filter: str) -> None:
    """Displays statistics on the most frequent times of travel."""

    print('\n- - - Stats on the Most Frequent Times of Travel - - -')
    # display chosen filter
    print(filter)
    start_time = time.time()

    # most common month
    if 'Month: All' in filter:
        most_common_month_num = df['Month'].mode().values[0]
        most_common_month = MONTHS[most_common_month_num]
        most_common_month_counts = df['Month'].value_counts()[most_common_month_num]
        
    
    # most common day of week
    if 'Day: All' in filter:
        most_common_day = df['Day of week'].mode().values[0]
        most_common_day_counts = df['Day of week'].value_counts()[most_common_day]
    
    # most common start hour
    hour_series = df['Start Time Stamp'].dt.hour
    most_common_hour = hour_series.mode().values[0]
    most_common_hour_counts = hour_series.value_counts()[most_common_hour]
    
    # Display the stats
    if 'Month: All' in filter:
        print_result("Most common month of ride:", most_common_month, 
                     make_count_info(most_common_month_counts, df['Month'].count()))
    if 'Day: All' in filter:
        print_result("Most common day of ride:", most_common_day, 
                     make_count_info(most_common_day_counts, df['Day of week'].count()))
    print_result("Most common hour:", most_common_hour, 
                 make_count_info(most_common_hour_counts, hour_series.count()))

    # Display elapsed time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DIVIDER_LENGTH)


def station_stats(df, filter: str) -> None:
    """Displays statistics on the most popular stations and trip."""

    print('\n- - - Stats on the Most Popular Stations and Trip - - -')
    print(filter)
    start_time = time.time()

    # Most commonly used start station
    most_used_start_station = df['Start Station'].mode().values[0]
    most_used_start_station_counts = df['Start Station'].value_counts()[most_used_start_station]
    
    # Most commonly used end station
    most_used_end_station = df['End Station'].mode().values[0]
    most_used_end_station_counts = df['End Station'].value_counts()[most_used_end_station]
    
    # Most frequent combination of start station and end station trip
    df_group = df.groupby(['Start Station', 'End Station'])
    most_freq_start_end_trip = df_group.size().idxmax()
    most_freq_start_end_trip_counts = df_group.size().max()

    # Display the stats
    print_result("Most used start station: ", most_used_start_station, 
                 make_count_info(most_used_start_station_counts, df['Start Station'].count()))
    print_result("Most used end station: ", most_used_end_station, 
                 make_count_info(most_used_end_station_counts, df['End Station'].count()))
    print_result("Most frequenct start end trip: ", most_freq_start_end_trip, 
                 make_count_info(most_freq_start_end_trip_counts, df_group.size().count()))

    # Display elpased time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DIVIDER_LENGTH)


def trip_duration_stats(df, filter: str) -> None:
    """Displays statistics on the total and average trip duration."""

    print('\n- - - Stats on Trip Duration - - -')
    # display chosen filter
    print(filter)
    start_time = time.time()

    # Total travel time (seconds)
    total_travel_time = df['Trip Duration'].sum()
    
    # Mean travel time (seconds)
    avg_travel_time = int(df['Trip Duration'].mean())

    # Display the stats
    msg = "Total travel time:"
    hours, remainder = divmod(total_travel_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    res = "{} hours {} minutes and {} seconds".format(hours, minutes, seconds)
    print_result(msg, res)
    
    msg = "Average travel time:"
    minutes, seconds = divmod(avg_travel_time, 60)
    res = "{} minutes and {} seconds".format(minutes, seconds)
    print_result(msg, res)

    # Display elapsed time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DIVIDER_LENGTH)


def user_stats(df, filter: str) -> None:
    """Displays statistics on bikeshare users."""

    print('\n- - - Stats on Users - - -')
    # display chosen filter
    print(filter)
    start_time = time.time()

    # Counts of user types
    user_type_value_cnts = df['User Type'].value_counts()
    
    # Counts of gender (ONLY IF DATA EXISTS ! ! !)
    has_gender = False
    if 'Gender' in df.columns:
        has_gender = True
        gender_value_cnts = df['Gender'].value_counts()
    
    # Earliest, most recent, and most common year of birth (ONLY IF DATA EXISTS ! ! !)
    has_dob = False
    if 'Birth Year' in df.columns:
        has_dob = True
        earliest_birth_yr = df['Birth Year'].min()
        latest_birth_yr = df['Birth Year'].max()
        most_common_birth_yr = df['Birth Year'].mode().values[0]

    # Display the stats
    print_counts("- Counts of user types -", user_type_value_cnts)
    if has_gender:
        print_counts("\n- Counts of genders - ", gender_value_cnts)
    if has_dob:
        print('\n- Stats on birth year -')
        print_result("Earliest birth year: ", int(earliest_birth_yr))
        print_result("Latest birth year: ", int(latest_birth_yr))
        print_result("Most common birth year: ", int(most_common_birth_yr))

    # Display elapsed time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*DIVIDER_LENGTH)

def individual_view(df, filter: str) -> None:
    res = input("\nWould you like to view all individual trips? Enter yes (y) or no (n).\n"
                f"(WARNING: This may take a while if the filter is for all month and days ! ! ! {filter.strip().strip('(').strip(')')})\n")

    if (res and res.lower()[0] == 'y'):
        total = df.shape[0]
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_dict.pop('Unnamed: 0', None)
            row_dict.pop('Start Time Stamp', None)
            json_row = json.dumps(row_dict, indent = 4)
            print(json_row)
        print('total: ', total)
        print('-'*DIVIDER_LENGTH)

def raw_data_view(df, filter: str) -> None:
    res = input("\nWould you like to view raw data? Enter yes (y) or no (n).\n")
    row = 0
    total = len(df)
    if res and res.lower()[0] == 'y':
        print('The program will display raw data in chunks of 5 rows.')
    while row < total:
            print(df[row: min(row+5, total)])
            row += 5
            r = input('Press enter to see the next 5 rows or any key to exit.\n')
            if r:
                break


# Helper function to make a statement in the following format:
# msg1: result1, msg2: result2 . . .
def make_count_info(count: int, total: int) -> str:
    ratio = "{:.2f}".format(count / total * 100)
    return f'count: {count} ({ratio}%)   total: {total}'
    

# Helper function to print
def print_result(message: str, result, extras: str = '') -> None:
    result = str(result)
    if extras:
        result += ' ' * 4 + extras
        
    remain_cnt = MSG_LENGTH - len(message)
    if remain_cnt > 0:
        print(message + ' ' * remain_cnt + result)
    else:
        print(message + result)


# Helper function to print
def print_counts(header: str, pd_count_series: pd.Series) -> None:
    print(header)
    for idx, cnt in pd_count_series.items():
        msg = f"# of {idx}s:"
        print_result(msg, cnt)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        filter = f'(filter -> City: {city.title()}, Month: {month.title()}, Day: {day.title()})\n'

        time_stats(df, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        user_stats(df, filter)
        individual_view(df, filter)
        raw_data_view(df, filter)

        restart = input('\nWould you like to restart? Enter yes (y) or no (n).\n')
        if not restart or restart.lower()[0] != 'y':
            break


if __name__ == "__main__":
	main()
