import streamlit as st
import pandas as pd
import requests
from collections import defaultdict
from datetime import datetime
import json
from api_predict import Inputs

# General CSS
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center; /* Center the title */
        color: #3CB371; /* Change text color */
        font-size: 36px; /* Change font size */
        font-weight: bold; /* Make the font bold */
    }
    .logo {
        border : solid;
        border-radius : 50%;
        width : 30%;
        height : auto;
        position : relative;
        left : 38%;
        top: -52px;
    }
    button {
        position : relative;
        left : 38%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

## Manual Input Features ( lists for dropbox selection)
color_list = ['silver', 'grey', 'white', 'blue', 'chocolate', 'brown',
       'other', 'black', 'gold', 'red', 'yellow', 'orange', 'beige',
       'green', 'violet', 'purple', 'black, red', 'brown, gold',
       'white, orange', 'black, orange', 'white, gold', 'silver, gold',
       'white, black', 'gold, beige', 'black, gold, beige', 'white, blue',
       'blue, black', 'grey, gold', 'gold, orange', 'white, yellow']

states_list = ['uttar pradesh','haryana','delhi','punjab','himachal pradesh',
              'jammu & kashmir','uttarakhand','chandigarh','karnataka','andhra pradesh',
              'telangana','tamil nadu','kerala','puducherry','maharashtra',
              'gujarat','rajasthan','goa','dadra and nagar haveli','daman and diu',
              'bihar','west bengal','assam','odisha','jharkhand','chhattisgarh',
              'tripura','meghalaya','arunachal pradesh','nagaland','manipur', 'sikkim']

transmission_list = ['manual','automatic']
fueltype_list = ['cng', 'lpg', 'electric', 'diesel', 'petrol']
ownertype_list = ['first', 'second', 'third', 'fourth', 'fifth',
       'unregistered car']

## VID related inputs ( dict of lists for dropbox selection)
vid_dict_list = {
    'pageType' : ['ucr', 'cls'],
    'carType' : ['corporate', 'partner', 'assured'],
    'ValueConfiguration' : ['dohc', 'sohc', 'ohv / pushrod'],
    'TurboCharger' : ['no', 'yes'],
    'SuperCharger' : ['no', 'yes'],
    'GearBox' : ['5 speed', '4 speed', '6 speed', '1 speed', '7 speed', '8 speed',
       '9 speed', '10 speed'],
    'DriveType' : ['2wd', '4wd'],
    'SteeringType' : ['power assisted', 'not assisted'],
    'FrontBrakeType' : ['disc', 'drum', 'other'],
    'RearBrakeType' : ['drum', 'disc', 'other'],
    'TyreType' : ['tubeless', 'radial', 'runflat'],
    'seller_type_new' : ['dealer', 'individual'],
    'car_segment' : ['hatchback', 'sedan', 'muv', 'minivans', 'pickup trucks', 'suv',
       'luxury vehicles', 'convertibles', 'coupe', 'wagon', 'hybrids'],
    }
#
# Title
# st.markdown("<h1 class='centered-title'>carAdvice</h1>", unsafe_allow_html=True)
st.markdown('<img src="app/static/CarAdvice.png" class="logo"/>', unsafe_allow_html=True)
features = defaultdict(str)
df = pd.read_csv("vid_data_nonull.csv")

vid =  st.selectbox('Model here', options=df['vid'].unique())

if vid:
    response = requests.get("https://cars-api-362710095189.europe-west1.run.app/car_features", params={"vid":vid})

    features['km'] = st.text_input('Kilometrage')
    features['Color'] = st.selectbox('Color',options = color_list)

    model_year_input = st.text_input('Model Year',placeholder=2024)
    if model_year_input:
        age_calculation = datetime.now().year - int(model_year_input)
    else:
        age_calculation = 0  # Or set to None if that makes sense
    features['car_age'] = age_calculation

    features['state'] = st.selectbox('State', options = states_list)
    features['transmissionType'] = st.selectbox('Transmission Type', options = transmission_list)
    features['ft'] = st.selectbox('Fuel Type', options = fueltype_list)
    features['owner_type'] = st.selectbox('owner_type',options = ownertype_list)

    for k,v in response.json()[0].items():
        if k not in ["vid"]:
            if k not in vid_dict_list :
                features[k] = st.text_input(k,value=v)
            else:
                features[k] = st.selectbox(k,options = vid_dict_list[k])

    btn =  st.button("Predict Price")
    # Prepare JSON for the POST request outside of button click
    prediction_features = {k: (float(v) if isinstance(v, str) and v.replace('.', '', 1).isdigit() else v) for k, v in features.items()}

    if btn:
        # Check for any empty features
        unfilled_features = [k for k, v in features.items() if v == '']

        if unfilled_features:
            st.warning(f"Please fill in the following features: {', '.join(unfilled_features)}")
        else:
            # Make a POST request to the prediction endpoint
            response = requests.post("https://cars-api-362710095189.europe-west1.run.app/predict", json=prediction_features)

            # Check if 'predicted_price' is in the response
            if 'predicted_price' in response.json():
                result = response.json()
                st.success(f"Predicted Price: {result['predicted_price']}")
            else:
                 st.error("Prediction could not be made. Please ensure all required features are filled correctly.")
