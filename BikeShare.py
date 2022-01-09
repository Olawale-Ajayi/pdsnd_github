import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


CITY_DATA = {key.upper():value for (key, value) in CITY_DATA.items()}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
   
    while True:
        data = input("Please choose from any of the following cities: Washington, Chicago or New york City   \n" ).upper()
        if not data in CITY_DATA:
            print("please choose from the options specified Below")
            continue
        else:
            df = pd.read_csv(CITY_DATA[data])
            

            


           
        df["Months"] = pd.to_datetime(df["Start Time"]).dt.month_name().str.upper()
        df["Days"] = pd.to_datetime(df["Start Time"]).dt.day_name().str.upper()
        Unique_Month = [x for x in df["Months"].unique()]
        Unique_Days = [x for x in df["Days"].unique()]


        while True:
            choice = input("Do You want to filter by a particular Month, Day, or Both or all Months: Enter  Month, Day, both or None if you dont want to apply filter \n").upper()
            
            if choice.startswith("M"):
                month = input("Please choose from the following months: January, february, March, April, May, June \n").upper()
                Day = None
                if not month in Unique_Month:
                    print("Please choose from the specified months above")
                    continue
                               

                else:
                    df = df[df["Months"]==month]
                    

                    

                return df, month, Day, data.title()
                break

            elif choice.startswith("D"):
                    Day = input("Please choose any day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday \n ").upper()
                    month = None
            
                    if not Day in Unique_Days:
                        print("Please choose from the specified Days above")
                        #Day
                        continue
                    
                    else:
                        df = df[df["Days"]==Day]

                    return df, month, Day, data.title()
                    break
                

            
            elif choice.startswith("B"):
                Day = input("Please choose any day of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday \n ").upper()
                month = input("Please choose from the following months: January, february, March, April, May, June \n ").upper()
                if not Day in Unique_Days and not month in Unique_Month:
                    print("Please choose from the specified Days above")
                    continue
                else:
                    df = df[(df["Days"]==Day) & (df["Months"]==month)]

                return df,  month, Day, data.title()
                break

            elif choice.startswith("N"):
                month = None
                Day = None
        

                return df, month, Day, data.title()
                break
            else:
                print("Please enter a valid entry from the options below ")
                continue
                 



                







 
        break                    
def Time_Stats():
    #print('Time Statistics of duration')
    start = time.time()
    df, month, day, city = get_filters()

# Getting The Filter for the Datasets
    

    if month == None and day == None:
        filter = "No filter" 
    elif month is not None and day is  None:
        filter = "month"
    elif day is not None and month is None:
        filter = "Day"
    else:
        filter = "Day and Month"


    Freq_Month = df["Months"].mode()[0]
    Freq_Days = df["Days"].mode()[0]
    Freq_Start_Hour = pd.to_datetime(df["Start Time"]).dt.hour.mode()[0]
    Freq_Travel_time = pd.to_datetime(df["Start Time"]).dt.time.mode()[:1][0].strftime("%H:%M:%S")
    df1 = pd.DataFrame(df.groupby("User Type")['Trip Duration'].sum()).reset_index().rename(columns = {"Trip Duration": "Total Trip Duration"})

    print(f"Getting you start for analysis of {city} filter by: {filter.title()}" )
    print()
    print("Duration time Analysis")




    print(f"The Most Common Day of the week is : {Freq_Days}")
    print(f"The Most Common month is : {Freq_Month}")
    print(f"The Most Common Starting Hour is : {str(Freq_Start_Hour)}:00H")
    print(f"The Most Frequent travel time is: {Freq_Travel_time}")
    print("Total duration of trip by User Type:")
    print(df1)




    print("_" * 50)

    Freq_Start_Station = df["Start Station"].mode()[0]
    Freq_End_Station = df["End Station"].mode()[0]
    Freq_Trip = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending = False).index[0]

    print()
    print("Station Analysis")
    print(f"Most common start station is: {Freq_Start_Station}")
    print(f"Most common End station is: {Freq_End_Station}")
    print(f" The Most Frequent Trip is from {Freq_Trip[0]} --> {Freq_Trip[1]}")


    print("_" * 50)
    print()

    print("Travel Time analysis")
    Max_Travel_time = df["Trip Duration"].max()
    Avg_Travel_time = df["Trip Duration"].mean()

    print(f"Maximum Duration Time is {np.round(Max_Travel_time,1)}")
    print(f"Average Duration Time is {np.round(Avg_Travel_time, 1)}")

    print("_" * 50)
    print()

    print('User Gender and Birth Analysis')

    df2 = pd.DataFrame(df.groupby("User Type").size()).reset_index().rename(columns = {0: "Total Number"})
    missing_columns = ["Gender", "Birth Year"]
    if "Gender" not in df.columns:
        df3 = "There is no Gender and Birth Year Data for Washington City"
        Earliest_Year = None
        most_recent_Year = None
        most_common_year = None

        
     
    else:
        
        df3 = pd.DataFrame(df.groupby("Gender").size()).reset_index().rename(columns = {0: "Total Number"})
        Earliest_Year = df["Birth Year"].dropna().sort_values().values[0].astype(int)
        most_recent_Year = df["Birth Year"].dropna().sort_values(ascending = False).values[0].astype(int)
        most_common_year = df["Birth Year"].mode()[0].astype(int)






    


    print("Users Distribution") 
    print(df2)
    print()
    print("Gender Distribution")
    print(df3)
    print()
    print(f"Earliest Year of birth is: {Earliest_Year}")
    print(f"Recent Year of birth is: {most_recent_Year }")
    print(f"Most Common Year of birth is: {most_common_year}")



    print("_" * 50)


    print(f"This Program took  {np.round(time.time() - start,1)} Seconds")



def display_raw_data(df):
    i = 0
    raw = input("Do you want to see 5 lines of raw data: Please enter yes/no  \n ").lower()
    while True:
        if raw.startswith("n"):
            break
        elif raw.startswith("y"):
            print(df[:(i+5)])
            raw = input("Do you want to see another 5 lines of raw data: Please enter yes/no  \n").lower()
            i+=5
        else:
            raw = input("Your input is invalid, Please enter only yes or no \n").lower()








    
def main():
    while True:
        print("Welcome to Bike Share Exploratory Analysis!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print()
        display = display_raw_data(get_filters()[0])
        result = Time_Stats()
        print()
        
        restart = input("Do you wants to restart the program: Enter Yes/no  \n").upper()

        # if not restart.startswith("Y") or not restart.startswith("N"):
        #     print("Please enter yes or no")
            
        if restart.startswith("N"):
                break
        else:
            continue
                    
if __name__ == "__main__":

    main()





                        

               

                        


    

        
        



                









      
    



    