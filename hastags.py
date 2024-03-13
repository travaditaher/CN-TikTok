import pandas as pd
import re

# Read the Excel file
file_path = '/Users/tahers/Documents/Python_prep/CN-TikTok/TIkTok Web Scrapping.xlsx'
excel_data = pd.ExcelFile(file_path)

# Read the first sheet to get initial hashtags
first_sheet = excel_data.sheet_names[0]
first_sheet_data = pd.read_excel(excel_data, sheet_name=first_sheet)
initial_hashtags = set(first_sheet_data['Hashtags'].str.findall(r'#\w+').sum())

# Function to extract hashtags from video descriptions
def extract_hashtags(text):
    hashtags = re.findall(r'#\w+', str(text))
    return hashtags

# Iterate through other sheets
new_hashtags = set()
for sheet_name in excel_data.sheet_names[1:]:
    sheet_data = pd.read_excel(excel_data, sheet_name=sheet_name)
    hashtags_hashtags = sheet_data['Hashtags'].apply(lambda x: re.findall(r'#\w+', str(x))).sum()
    hashtags_desc = sheet_data['video_description'].apply(extract_hashtags).tolist()
    all_hashtags = set(tag for sublist in hashtags_desc + hashtags_hashtags for tag in sublist) # Flatten the lists
    new_hashtags.update(all_hashtags - initial_hashtags)


# Append new hashtags to the first sheet
first_sheet_data['New_Hashtags'] = ''
first_sheet_data.at[0, 'New_Hashtags'] = ', '.join(new_hashtags)

# Write the updated data back to the Excel file
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
    first_sheet_data.to_excel(writer, sheet_name='New_Hash', index=False)

print("New hashtags appended to 'HashTags' sheet:", new_hashtags)
