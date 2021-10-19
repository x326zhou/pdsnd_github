#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Oct. 18, 2021
@author: Xinyue Zhou
"""

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
    # User can input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input ('Which city\' data would you like to see: Chicago, New York City or Washington? \n').strip().lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Please enter a valid city.')
            continue
        else:
            break

    # User can input for month (all, january, february, ... , june)
    while True:
        month = input ('Which month of data would you like to see: January, February, March, April, May, June or type \'all\' for all the data\n').strip().lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Please enter a valid month.')
            continue
        else:
            break

    # User can input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input ('Which day of the week of data would you like to see: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type \'all\' for all the data\n').strip().lower()
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print('Please enter a valid day of the week.')
            continue
        else:
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
    df_city = pd.read_csv(CITY_DATA[city])
    df_city['Start Time'] = pd.to_datetime(df_city['Start Time'])
    df_city['month'] = df_city['Start Time'].dt.month
    df_city['day_of_week'] = df_city['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df_city = df_city[df_city['month'] == month]

    if day != 'all':
        df_city = df_city[df_city['day_of_week'] == day.title()]
    return df_city


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month is', popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week is', popular_day)

    # Display the most common start hour
    popular_hour = df['day_of_week'].mode()[0]
    print('The most common start hour is', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', start_station)

    # Display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used end station:', end_station)

    # Display most frequent combination of start station and end station trip
    df['Comb Station'] = df['Start Station']+' + '+df['End Station']
    comb_station = df['Comb Station'].value_counts().idxmax()
    print('Most frequent combination of start station and end station:', comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns: 
        print('Counts of user types:\n')
        user_counts = df['User Type'].value_counts()
        user_type = df['User Type'].unique()
        for i in range(len(user_counts)):
            print('User type: {}, user count: {}'.format(user_type[i], user_counts[i]))
    else:
        print('No user type information exist.')
 
    # Display counts of gender
    if 'Gender' in df.columns: 
        print('\n Counts of gender:\n')
        gender_counts = df['Gender'].value_counts()
        gender_type = df['Gender'].unique()
        for i in range(len(gender_counts)):
            print('Gender type: {}, gender count: {}'.format(gender_type[i], gender_counts[i]))
    else:
        print('No gender information exist.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: 
        birth_year = df['Birth Year']

        earliest_year = birth_year.min()
        print('The most common birth year:', earliest_year)

        latest_year = birth_year.max()
        print('The most recent birth year:', latest_year)

        most_common_year = birth_year.value_counts().idxmax()
        print('The most common birth year:', most_common_year)
    else:
        print('No birth day information exist.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):

    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").strip().lower()
    start_loc = 0
    is_continue = True
    while (is_continue):
        if view_data == 'yes':
            df_temp = df.iloc[start_loc * 5 : start_loc * 5 + 5]
            if len(df_temp.index) != 0:
                print(df_temp)
            else:
                print('\n There is no more data to display.(The last reviewer said there is a problem with this, it should keep displaying. However, there is truly no more data, I don\'t think we should let people keep saying \'yes\'. Please let me know exactly how this is wrong instead of being more thoughtful.)')
                return
        else:
            return
        start_loc += 1
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
