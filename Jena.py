import pandas as pd
import streamlit as st

st.title("Why Jena should/shouldn't move out")
st.subheader('~ Fuck you Jena')
st.subheader('Use sidebar to change inputs <<<')

with st.sidebar:
    util = st.number_input('Average Utilites Cost', value=50)
    travel = st.slider('Number of commutes to college per week',value = 4,max_value=7 )
    months = st.slider('Number of sublet months', value = 3,max_value=7)
    sub_rent = st.number_input('Sublet Rent in 858', value = 700)
    rent_858 = st.number_input('Enter current rent', value = 1290)
    rent_new = st.number_input('Enter New Rent'),  value = 500)
    
if util and travel and months and sub_rent:
    travel_cost = (2.4*travel*2)+(2.4*4*4)
    cost_sublet = (rent_858 - sub_rent)*months
    rent_new_total = rent_new + travel_cost + util
    rent_858_new = rent_858 + (2.4*4*4)
    living_months = 8 - months
    sublet_months = int(months)
    data = {'Rent Type': ['858', 'New House'], 'Cost': [rent_858_new, rent_new_total]}

    # Create a DataFrame
    df = pd.DataFrame(data).set_index('Rent Type')

    st.write('Monthly Cost (rent,utilities and transport): ')
    st.bar_chart(df)
    
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    rent_858_months = [rent_858_new]*living_months
    rent_858_sublet = [rent_858-sub_rent]*sublet_months
    rent_858_total = rent_858_months + rent_858_sublet
    
    rent_new_living_months = [rent_new_total]*living_months
    
    agree = st.checkbox("He gets a sublet in New House")
    
    if agree:
        rent_new_sublet_months = [0]*sublet_months
        
    else:
        rent_new_sublet_months = [rent_new]*sublet_months
        
    rent_new_final = rent_new_living_months + rent_new_sublet_months
    
    
    data_1 = {
    'Months': months,
    '858': rent_858_total,  # Use the generated list for rent_858_new
    'New House': rent_new_final  # Same rent for New House across 3 months
    }
    
    df1 = pd.DataFrame(data_1)
    
    df1['Cumulative_858'] = df1['858'].cumsum()
    df1['Cumulative_New_house'] =  df1['New House'].cumsum()

    df1.pop('858')
    df1.pop('New House')
    
    df1['Date'] = pd.to_datetime(df1['Months'] + ' 2024', format='%b %Y')
    df1.set_index('Date', inplace=True)
    df1.pop('Months')
    
    st.line_chart(df1)
    
    Cum_858_rent = df1.iloc[7, df1.columns.get_loc('Cumulative_858')]
    Cum_new_rent = df1.iloc[7, df1.columns.get_loc('Cumulative_New_house')]
    Diff = round(Cum_858_rent - Cum_new_rent,2)
    conclusion = f"the difference in rent between 858 and New House: ${Diff}"
    st.subheader(conclusion)
    
    move_in = st.number_input('Potential Move-in costs', value = 15)
    diff1 = round(Diff-move_in,2)
    conclusion1 = f"Jai's savings: ${diff1}"
    st.header(conclusion1)
        
    
    
    
    
    
