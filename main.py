# %%
from pathlib import Path
import pandas as pd
import requests


def get_input_files():
    input_folder = Path("input")
    files = list(input_folder.glob("*.csv"))
    return [file for file in files if file.name != "example_contacts.csv"]


def check_columns(df, example_df):
    required_columns = [
        col for col in example_df.columns if not example_df[col].isnull().all()
    ]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
    return True


def load_example_contacts():
    example_file_path = Path("input/example_contacts.csv")
    example_df = pd.read_csv(example_file_path)
    return example_df


def read_inputs():
    input_files = get_input_files()

    if len(input_files) > 1:
        print("Multiple files found. Please select one:")
        for i, file in enumerate(input_files):
            print(f"{i+1}. {file.name}")

        choice = int(input("Enter the number of your chosen file: ")) - 1
        selected_file = input_files[choice]
    elif len(input_files) == 1:
        selected_file = input_files[0]
    else:
        raise ValueError("No CSV files found in 'input' folder")

    example_df = load_example_contacts()
    df = pd.read_csv(selected_file)

    check_columns(df, example_df)

    print(f"File '{selected_file.name}' loaded successfully.")

    return df

def download_photos(df_in):
    contact_photos_dir = Path('contact_photos')
    if not contact_photos_dir.exists():
        contact_photos_dir.mkdir()
    
    for index, row in df_in.iterrows():
        if not pd.isnull(row['Photo']):
            photo_url = row['Photo']
            names = [row['First Name'], row['Middle Name'], row['Last Name'], row['Nickname']]
            filename = '_'.join([name for name in names if not pd.isnull(name)]) + '.jpg'
            filepath = contact_photos_dir / filename
            
            response = requests.get(photo_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded photo for {filename}")
            else:
                print(f"Failed to download photo for {filename}")


if __name__ == "__main__":
    df = read_inputs()
    download_photos(df)

# %%
