import pandas as pd
import streamlit as st

st.title("Why you should/shouldn't move out in Jan")
st.subheader('Use sidebar to change inputs <<<')

with st.sidebar:
    rent_858 = st.number_input('Current House Rent', value = 800)
    current_util = st.number_input('Current utilites Cost', value=50)
    travel_cost = st.number_input('Current Travel Cost per week', value=20)

    
    rent_new = st.number_input('New House Rent', value = 800)
    util = st.number_input('New House Utilites Cost', value=50)
    new_travel_cost = st.number_input('New Travel Cost per week', value=20)
    
    
if util:
    
    rent_new_total = rent_new + new_travel_cost*4 + util
    rent_858_new = rent_858 + current_util + travel_cost*4
    
    data = {'Rent Type': ['Current House', 'New House'], 'Cost': [rent_858_new, rent_new_total]}

    df = pd.DataFrame(data).set_index('Rent Type')

    st.write('Monthly Cost (rent,utilities and transport): ')
    st.bar_chart(df)
    
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    
    
    
    
    Months = st.slider('Number of sublet months', value = 3,max_value=7)
    living_months = 8 - Months
    sublet_months = int(Months)
    
    old_house_sublet_rent =0   
    old_house_agree = st.checkbox("You get a sublet in Current House")
    
    if old_house_agree:
        
        old_house_sublet_rent = st.number_input('Sublet Rent for Current House: ', value=rent_858)
        rent_858_sublet_months = [rent_858 - old_house_sublet_rent]*sublet_months
    else:
        rent_858_sublet_months = [rent_858]*sublet_months
        
    rent_858_sublet = [rent_858-old_house_sublet_rent]*sublet_months
    rent_858_months = [rent_858_new]*living_months
    rent_858_total = rent_858_months + rent_858_sublet_months
        
    new_house_agree = st.checkbox("You get a sublet in New House")
    
    if new_house_agree:
        new_house_sublet_rent = st.number_input('Rent charged for sublet', value=rent_new)
        rent_new_sublet_months = [rent_new-new_house_sublet_rent]*sublet_months
    else:
        rent_new_sublet_months = [rent_new]*sublet_months
    
    rent_new_living_months = [rent_new_total]*living_months 
    rent_new_final = rent_new_living_months + rent_new_sublet_months

    
    data_1 = {
    'Months': months,
    'Current House': rent_858_total,  # Use the generated list for rent_858_new
    'New House': rent_new_final  # Same rent for New House across 3 months
    }
    
    df1 = pd.DataFrame(data_1)
    
    df1['Current_House'] = df1['Current House'].cumsum()
    df1['New_house'] =  df1['New House'].cumsum()

    df1.pop('Current House')
    df1.pop('New House')
    
    df1['Date'] = pd.to_datetime(df1['Months'] + ' 2024', format='%b %Y')
    df1.set_index('Date', inplace=True)
    df1.pop('Months')
    
    st.line_chart(df1)
    st.dataframe(df1)
    
    Cum_858_rent = df1.iloc[7, df1.columns.get_loc('Current_House')]
    Cum_new_rent = df1.iloc[7, df1.columns.get_loc('New_house')]
    text = f"Cost of Current House: {Cum_858_rent}  |  Cost of New House: {Cum_new_rent}"
    st.write(text)
    Diff = Cum_858_rent - Cum_new_rent
    
    move_in = st.number_input('Potential Move-in costs', value = 50)
    diff1 = Diff-move_in
    conclusion1 = f"Total Savings (+ve)/ Loss (-ve): ${diff1}"
    st.header(conclusion1)
    
    more = st.checkbox("Want more?")
    if more:
        food = st.number_input('Enter Monthly Food costs',value=100)
        inflow = st.number_input('Monthly Budget', value = 1200)
        rent_new_total = rent_new + new_travel_cost*4 + util + food
        rent_858_new = rent_858 + current_util + travel_cost*4 + food
        
        monthly_savings_old = inflow - rent_858_new
        monthly_savings_new = inflow - rent_new_total
        text1 = f"Savings of Current House: {monthly_savings_old}  |  Savings of New House: {monthly_savings_new}"
        st.write(text1)
        
    
    
    
    
    
