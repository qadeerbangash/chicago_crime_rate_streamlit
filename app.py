# data======= https://www.kaggle.com/datasets/adelanseur/crimes-2001-to-present-chicago


import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns



def load_data():
    df = pd.read_csv("Crimes_2001_to_Present.csv")
    df=df.dropna()
    return df


def get_location(df):
    return sorted(df['Block'].unique())


def main():
    # Load data
    df = load_data()

    crime_data = pd.read_csv('Crimes_2001_to_Present.csv')
    crime_data.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'}, inplace=True)
    st.sidebar.title('Crime Data Analysis')
    selected_crime_type = st.sidebar.selectbox('Select Crime Type', crime_data['Primary Type'].unique())
    selected_year = st.sidebar.slider('Select Year', min_value=int(crime_data['Year'].min()), max_value=int(crime_data['Year'].max()))

    # Filter the data based on user selection
    filtered_data = crime_data[(crime_data['Primary Type'] == selected_crime_type) & (crime_data['Year'] == selected_year)]

    # Show filtered data in a table
    st.write(f'### {selected_crime_type} Crimes in {selected_year}')
    st.dataframe(filtered_data)

    # Calculate and display crime statistics
    total_crimes = len(filtered_data)
    st.write(f'Total {selected_crime_type} crimes in {selected_year}: {total_crimes}')

    # Create a bar chart to visualize crime counts by month
    st.write(f'### {selected_crime_type} Crimes by Month')
    monthly_crime_counts = filtered_data['Date'].str.slice(0, 2).value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_crime_counts.index, y=monthly_crime_counts.values, color='blue')
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    st.pyplot(plt)
    st.write(f'### Map of {selected_crime_type} Crimes in {selected_year}')
    st.map(filtered_data[['LAT', 'LON']].dropna())



 



    location=get_location(df)
    st.title('Chicago Crime Rate- 2001 to Present')
    st.subheader('Crime Data Set')




    # Add a drop-down widget to select state
    selected_block=st.sidebar.selectbox("LOCATION", location)
    filtered_data = df[df["Block"] == selected_block]
    st.subheader('Selected Specific Block')

    st.write(filtered_data.head(200))


    col1, col2, col3, col4, col5= st.columns(5)
    col1.metric(label="Total number of Crimes", value=filtered_data["Case Number"].nunique())
    # Calculate the number of people arrested
    arrested_count = filtered_data['Arrest'].sum()
    col2.metric(label="Total No. of Arrests", value=arrested_count)

    total_crimes = filtered_data["Case Number"].nunique()
    # Calculate the percentage of crimes for each type (THEFT, BATTERY, and Other)
    theft_count = filtered_data[filtered_data['Primary Type'] == 'THEFT'].shape[0]
    battery_count = filtered_data[filtered_data['Primary Type'] == 'BATTERY'].shape[0]
    other_count = total_crimes - theft_count - battery_count

    theft_percentage = (theft_count / total_crimes) * 100
    battery_percentage = (battery_count / total_crimes) * 100
    other_percentage = (other_count / total_crimes) * 100

    col3.metric(label="THEFT Percentage", value=f"{theft_percentage:.2f}")
    col4.metric(label="BATTERY Percentage", value=f"{battery_percentage:.2f}")
    col5.metric(label="Other Crimes Percentage", value=f"{other_percentage:.2f}")




    st.subheader("Horizontal Bar Plot of Number of Crimes by Primary Type")
    histogram_chart= filtered_data.groupby("Primary Type").size()
    st.bar_chart(histogram_chart)




    # Sidebar for user input
    st.sidebar.title('Crime Selection')
    crime_list = filtered_data['Primary Type'].unique()
    selected_crime = st.sidebar.selectbox('Select a Crime Type with Respect to Block:', crime_list)
    crime_df = filtered_data[filtered_data['Primary Type'] == selected_crime]
    crime_df['Time'] = pd.to_datetime(crime_df['Date']).dt.time
    crime_count_by_time = crime_df.groupby('Time').size().reset_index(name='Count')
    fig = px.line(crime_count_by_time, x='Time', y='Count', title=f'Trend of {selected_crime} Over Time')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Number of Crimes')
    st.plotly_chart(fig)









    st.title('Crime Hotspots in Chicago')

    # Filter out rows with missing latitude and longitude values
    hotspot = filtered_data.dropna(subset=['Latitude', 'Longitude'])

    # Plot the hotspots on a map using Plotly Express
    fig = px.scatter_mapbox(
        hotspot,
        lat='Latitude',
        lon='Longitude',
        color='Primary Type',
        hover_name='Primary Type',
        hover_data=['Description'],
        mapbox_style='carto-positron',
        zoom=10,
        title='Crime Hotspots in Chicago'
    )

    # Customize the map layout
    fig.update_layout(
        mapbox=dict(
            accesstoken='YOUR_MAPBOX_ACCESS_TOKEN',  # Replace with your own Mapbox access token
            bearing=0,
            center=dict(lat=41.8781, lon=-87.6298),  # Chicago's latitude and longitude
            pitch=0,
            zoom=10
        ),
    )
    st.plotly_chart(fig)















    # Convert 'Date' column to datetime type
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], errors='coerce')

    # Extract the time component and create a new column 'Time'
    filtered_data['Time'] = filtered_data['Date'].dt.time

    # Convert the 'Time' column to datetime format (if needed) to access the 'hour' attribute
    filtered_data['Time'] = pd.to_datetime(filtered_data['Time'], format='%H:%M:%S').dt.hour

    # Group the data by 'Time' and 'Primary_type', and count the occurrences
    crime_type_counts = filtered_data.groupby(["Time", "Primary Type"]).size().reset_index(name='Frequency')

    # Create a bar plot using Plotly Express
    fig = px.bar(
        crime_type_counts,
        x='Time',
        y='Frequency',
        color='Primary Type',
        labels={'Time': 'Time of Day (Hour)', 'Frequency': 'Crimes'},
        title='Hourly Crime Rate',
    )

    # Customize the x-axis labels and range
    fig.update_xaxes(tickvals=list(range(24)), dtick=1)

    # Show the plot in the Streamlit app
    st.plotly_chart(fig)






   # Create a pie chart to visualize the distribution of crime types for the selected year
    st.write(f'### Crime Type Distribution in {selected_year}')
    crime_type_counts = filtered_data['Primary Type'].value_counts().nlargest(10)
    plt.figure(figsize=(6, 8))
    plt.pie(crime_type_counts, labels=crime_type_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(plt)

















# Run the app
if __name__ == "__main__":
    main()
