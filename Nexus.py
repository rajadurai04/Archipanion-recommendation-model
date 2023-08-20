

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

# Get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to Book1.csv
csv_file_path = os.path.join(script_dir, "Book1.csv")

# Load the CSV file
df = pd.read_csv(csv_file_path)


columns_to_clean = ["Product Name", "Domain"]
for column in columns_to_clean:
    df[column] = df[column].str.replace(" ", "_")

df['Product Name'] = df['Product Name'].str.lower()
df.columns = df.columns.str.replace(' ', '_')
df['Domain'] = df['Domain'].str.lower()
df['Energy-efficient_score'] = df['Energy-efficient_score'].str.lower()
df['Compatibility'] = df['Compatibility'].str.lower()
df['Multi-user_suppport'] = df['Multi-user_suppport'].str.lower()
df['Features'] = df['Features'].str.lower()
df['App_available'] = df['App_available'].str.lower()
df['Salary_support'] = df['Salary_support'].str.lower()
df['Sustainable-score_'] = df['Sustainable-score_'].str.lower()
df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
df['Learning_Difficulity'] = df['Learning_Difficulity'].str.lower()
df['Additional_benefits'] = df['Additional_benefits'].str.lower()


# Function to get multiple choices from user
def get_multiple_choices(prompt, options):
    st.write(f"Choose {prompt}:")
    choices = st.multiselect("", options)
    return choices

# Function to get domain choice from user


def get_domain_choice():
    st.write("Choose Domain:")
    domain_options = ["landscape_navigator", "urban", "residential",
                      "design_insipiration", "productivity", "commercial", "interior", "sustainable"]
    domain_choice = st.selectbox("", domain_options)
    return domain_choice

# Function to get price range from user


# def get_price_range():


def get_price_range():
    price_range_input = st.text_input("Enter Price Range (e.g., $250-$300):")
    price_range = price_range_input.split("-")

    try:
        min_price = int(price_range[0].replace("$", "").strip())
        max_price = int(price_range[1].replace("$", "").strip())
        random_price = (max_price + min_price) // 2
        return round(random_price, 2)
    except ValueError:
        return None
# Function to get user rating from user


def get_user_rating():
    user_rating = st.number_input(
        "Enter User Rating (e.g., 4.5): ", min_value=0.0, max_value=5.0, step=0.5)
    return user_rating

# Function to get yes/no choice from user


def get_yes_no_choice(prompt):
    choice = st.radio(prompt, ("y", "n"))
    return choice

# Function to gather user input


def get_user_input():
    user_input = {}
    user_input["Domain"] = get_domain_choice()
    user_input["Price"] = get_price_range()
    user_input["User_Rating"] = get_user_rating()
    user_input["Sustainable-score_"] = get_yes_no_choice(
        "Sustainability score")
    user_input["Energy-efficient_score"] = get_yes_no_choice(
        "Energy-efficient score")

    compatibility_options = ["android", "ios",  "linux", "macos", "windows"]
    compatibility_choices = get_multiple_choices(
        "Compatibility", compatibility_options)
    user_input["Compatibility"] = ", ".join(compatibility_choices)

    user_input["App_available"] = get_yes_no_choice("App available")
    user_input["Multi-user_suppport"] = get_yes_no_choice("Multi-user support")
    user_input["Salary_support"] = get_yes_no_choice("Salary support")
    return user_input


def onehotencoder(user_input):
    global df

    df = df._append(user_input, ignore_index=True)
    categorical_columns = ["Domain", "Compatibility", "App_available", "Multi-user_suppport",
                           "Energy-efficient_score", "Sustainable-score_", "Salary_support", "Learning_Difficulity"]
    data_encoded = pd.get_dummies(
        df, columns=categorical_columns, drop_first=True)
    df = df.drop(df.index[-1])
    a = data_encoded.iloc[-1]
    data_encoded = data_encoded.drop(data_encoded.index[-1])
    userchoice_df = pd.DataFrame([a])
    userchoice_df = userchoice_df.drop(
        columns=['Product_Id', 'Product_Name', 'Features', 'Additional_benefits'])
    similarity_scores = cosine_similarity(userchoice_df, data_encoded.drop(
        columns=['Product_Id', 'Product_Name', 'Features', 'Additional_benefits']))
    top_indices = np.argsort(similarity_scores[0])[::-1][:3]
    recommended_products = df.iloc[top_indices]
    st.write(recommended_products[['Product_Id', 'Product_Name']])

# Main Streamlit app


def main():

    st.title("Product Recommendation System")

    st.sidebar.header("NEXUS AI")
    user_input = get_user_input()
    st.sidebar.subheader("User Input:")
    st.sidebar.write(user_input)

    if st.sidebar.button("Get Recommendations"):
        onehotencoder(user_input)
        # st.write(recommended_products[['Product_Id', 'Product_Name']])


if __name__ == '__main__':
    main()
# import pickle

# import numpy as np
# import pandas as pd
# import streamlit as st
# from sklearn import cosine_similarity
# from streamlit_option_menu import option_menu

# # -*- coding: utf-8 -*-


# df = pd.read_csv("Book1.csv")
# columns_to_clean = ["Product Name", "Domain"]
# for column in columns_to_clean:
#     df[column] = df[column].str.replace(" ", "_")
# df.duplicated(subset='Product Name').sum()
# df['Compatibility'] = df['Compatibility'].str.lower()
# df['Compatibility'] = df['Compatibility'].replace(
#     {'mac os': 'macos'}, regex=True)
# df['Compatibility'] = df['Compatibility'].apply(
#     lambda x: ','.join(sorted(x.split(','))))
# df['Product Name'] = df['Product Name'].str.lower()
# df.columns = df.columns.str.replace(' ', '_')
# df['Domain'] = df['Domain'].str.lower()
# df['Energy-efficient_score'] = df['Energy-efficient_score'].str.lower()
# df['Compatibility'] = df['Compatibility'].str.lower()
# df['Multi-user_suppport'] = df['Multi-user_suppport'].str.lower()
# df['Features'] = df['Features'].str.lower()
# df['App_available'] = df['App_available'].str.lower()
# df['Salary_support'] = df['Salary_support'].str.lower()
# df['Sustainable-score_'] = df['Sustainable-score_'].str.lower()
# df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
# df['Learning_Difficulity'] = df['Learning_Difficulity'].str.lower()
# df['Additional_benefits'] = df['Additional_benefits'].str.lower()
# categorical_columns = ["Domain", "Compatibility", "App_available", "Multi-user_suppport",
#                        "Energy-efficient_score", "Sustainable-score_", "Salary_support", "Learning_Difficulity"]
# data_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)


# # Function to get multiple choices from user
# def get_multiple_choices(f, options):
#     # print(f"Choose {prompt}:")
#     # for idx, option in enumerate(options, start=1):
#     #     print(f"{idx}. {option}")
#     choices = f
#     choices_indices = [int(choice.strip()) -
#                        1 for choice in choices.split(",")]
#     selected_options = [options[idx] for idx in choices_indices]
#     # return selected_options

# # Function to get domain choice from user


# def get_domain_choice(a):
#     # print("Choose Domain:")
#     # print("1. landscape")
#     # print("2. urban")
#     # print("3. residential")
#     # print("4.design inspiration")
#     # print("5.productivity")
#     # print("6.commercial")
#     # print("7.interior")
#     # print("8.sustainable")
#     domain_choice = a
#     domain_options = ["landscape_navigator", "urban", "residential",
#                       "design_insipiration", "productivity", "commercial", "interior", "sustainable"]
#     # return domain_options[int(domain_choice) - 1]

# # Function to get price range from user and generate a random price within the range


# def get_price_range(b):
#     price_range_input = b
#     price_range = price_range_input.split("-")
#     min_price = int(price_range[0].replace("$", ""))
#     max_price = int(price_range[1].replace("$", ""))
#     random_price = (max_price + min_price)//2
#     # return round(random_price, 2)

# # Function to get user rating from user


# def get_user_rating(c):
#     user_rating = float(c)
#     # return user_rating

# # Function to get yes/no choice from user
# # def get_yes_no_choice(d):
# #     choice = d
# #     # return choice

# # Function to gather user input


# def get_user_input(a, b, c, d, e, f, g, h, i):
#     user_input = {}
#     user_input["Domain"] = get_domain_choice()
#     user_input["Price"] = get_price_range()
#     user_input["User_Rating"] = get_user_rating()
#     user_input["Sustainable-score_"] = d
#     user_input["Energy-efficient_score"] = e

#     compatibility_options = ["android", "ios",  "linux", "macos", "windows"]
#     compatibility_choices = get_multiple_choices(
#         "Compatibility", compatibility_options)
#     compatibility_string = ", ".join(compatibility_choices)
#     user_input["Compatibility"] = compatibility_string

#     user_input["App_available"] = f
#     user_input["Multi-user_suppport"] = g
#     user_input["Salary_support"] = h
#     # return user_input


# def onehotencoder(user_input):
#     global df
#     df = df.append(user_input, ignore_index=True)
#     categorical_columns = ["Domain", "Compatibility", "App_available", "Multi-user_suppport",
#                            "Energy-efficient_score", "Sustainable-score_", "Salary_support", "Learning_Difficulity"]
#     data_encoded = pd.get_dummies(
#         df, columns=categorical_columns, drop_first=True)
#     df = df.drop(df.index[-1])
#     a = data_encoded.iloc[-1]
#     data_encoded = data_encoded.drop(data_encoded.index[-1])
#     userchoice_df = pd.DataFrame([a])
#     userchoice_df = userchoice_df.drop(
#         columns=['Product_Id', 'Product_Name', 'Features', 'Additional_benefits'])
#     similarity_scores = cosine_similarity(userchoice_df, data_encoded.drop(
#         columns=['Product_Id', 'Product_Name', 'Features', 'Additional_benefits']))
#     top_indices = np.argsort(similarity_scores[0])[::-1][:3]
#     recommended_products = df.iloc[top_indices]
#     print(recommended_products[['Product_Id', 'Product_Name']])


# # Main function to gather user input
# # def main():
# with st.sidebar:
#     selected = option_menu('Nexus.AI',
#                            ['Tool Prediction',
#                             'AI chatbot',
#                             ],
#                            menu_icon=["cast"],
#                            icons=['heart', 'list-task'],
#                            styles=[],
#                            default_index=0)

# # Diabetes Prediction Page
# if (selected == 'Tool Prediction'):

#     st.title('Tool Recommender using ML')

#     # getting the input data from the user
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         Domain = st.text_input('Choose your Domain')

#     with col2:
#         Price = st.text_input('Enter price range')

#     with col3:
#         User_Rating = st.text_input('User Rating')

#     with col1:
#         Sustainability_Score = st.text_input('Sustainability Score(Y/N)')

#     with col2:
#         Energy_Efficiency = st.text_input('Energy Efficient Score(Y/N)')

#     with col3:
#         Compatibility = st.text_input('Select Compatibility')

#     with col1:
#         App_Version = st.text_input(
#             'Is App version needed(Y/N)')

#     with col2:
#         Multi_User = st.text_input('Is Multi User Support needed(Y/N)')

#     with col3:
#         Salary_support = st.text_input("Is Salary support needed(Y/N)")

#     # Prediction
#     Recommendation_Result = ''

#     # Button for Prediction

#     # if (diab_prediction[0] == 1):
#     #     diab_diagnosis = 'Diabetes - Positive'
#     # else:
#     #     diab_diagnosis = 'Diabetes - Negative'

#     user_input = get_user_input(Domain, Price, User_Rating, Sustainability_Score,
#                                 Energy_Efficiency, Compatibility, App_Version, Multi_User, Salary_support)
#     # print("User Input:")
#     # print(user_input)

#     if st.button('Recommend Tool'):
#         Recommendation_Result = onehotencoder(user_input)

#     st.success(Recommendation_Result)

# # Run the main function
# # if __name__ == "__main__":
# #     main()


# # loading the saved models

# # Recommender_model = pickle.load(open(
# #     'C:\\Users\\arune\\developement\\SRM Hackathon\\copy_of_archipanion1_ipy.py', 'rb'))

# # heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))

# # parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))


# # sidebar for navigation
