import numpy as np
import pandas as pd
import streamlit as st
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset and preprocess it
df = pd.read_csv("Book1.csv")

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
