import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APap][Mm]\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_date': dates})

    df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
    # df['message_date'] = df['message_date'].astype(str).str.replace('\u202f', ' ')

    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce', dayfirst=True)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists
    users = []
    messages = []

    # Process messages
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)  # Split on first colon followed by space
        if len(entry) > 2:  # Valid user-message format
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:  # Group notification or no user
            users.append('group_notification')
            messages.append(message.strip())

    # Add new columns to DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original column
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    return df


