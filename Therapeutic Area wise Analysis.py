from Dash_variables import *


## Running well with 1 filter: Product Category  on Port 8002 ## 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    
    category_layout        
], fluid=True)





# ------------------------------------------------------------------------------



# Updating the number cards 

@app.callback(
    [Output('content-payments','children'),
    Output('content-amount','children'),
    Output('content-companies','children'),
    Output('content-disputes','children')],
    
    [Input('slct_cat','value')]
)


def update_cards(cat_slctd):
    
    # No. of Payments
    #num_payments =  Amount[(Amount.Date >= str(start_date)) & (Amount.Date<= str(end_date)) & (Amount.State == state_slctd) & (Amount.Category == cat_slctd)]['No. of Payments'].sum()
    num_payments =  my_df[(my_df.Category == cat_slctd)]['Total Amount (USD)'].count()

    # Amount
    #amount = Amount[(Amount.Date >= str(start_date)) & (Amount.Date<= str(end_date)) & (Amount.State == state_slctd) & (Amount.Category == cat_slctd)]['Total Amount Paid (USD)'].sum()
    amount = my_df[(my_df.Category == cat_slctd)]['Total Amount (USD)'].sum()
    amount = str(round((amount/1000000),3)) + " M"

    # No. of companies
    #num_comps =  Amount[(Amount.Date >= str(start_date)) & (Amount.Date<= str(end_date)) & (Amount.State == state_slctd) & (Amount.Category == cat_slctd)]['Manufacturer / GPO'].count()
    num_comps =  my_df[(my_df.Category == cat_slctd)]['Manufacturer / GPO'].nunique()

    # Disputes
    #dispute = Amount[(Amount.Date >= str(start_date)) & (Amount.Date<= str(end_date)) & (Amount.State == state_slctd) & (Amount.Category == cat_slctd) & (Amount.Disputed == 'Yes')]['Total Amount Paid (USD)'].sum()
    dispute = my_df[(my_df.Category == cat_slctd) & (my_df.Disputed == 'Yes')]['Total Amount (USD)'].sum()
    dispute = str(round((dispute/1000000),3)) + " M"

    return num_payments, amount, num_comps, dispute



# Updating the plots

@app.callback([Output(component_id='States_Bar',component_property='figure'),
    Output(component_id='Primary_Type',component_property='figure'),
    Output(component_id='Product_Type',component_property='figure'),
    Output(component_id='Spec_Bar',component_property='figure'),
   Output(component_id='Category',component_property='figure'),],
    
     [Input('slct_cat','value'),])
#      Input('start_date','value'),
#      Input('end_date','value')]



def update_graph(cat_slctd):
    
    
    
    dff1 = my_df[(my_df.Category == cat_slctd) ].groupby('Manufacturer / GPO', as_index=False)['Total Amount (USD)'].sum().sort_values(by='Total Amount (USD)',ascending=False)[:5]
    #dff1 = dff1[(my_df.Date >= s_date) & (my_df.Date <= e_date)].groupby('Manufacturer / GPO', as_index=False)['Total Amount (USD)'].sum().sort_values(by='Total Amount (USD)',ascending=False)[:5]

    dff2 = my_df[(my_df.Category == cat_slctd) & (my_df['Physician Specialty'] != 'nan')].sort_values(by='Total Amount (USD)', ascending=False)[:10]
    
   
    dff3 = my_df[my_df.Category == cat_slctd]['Primary Type'].value_counts()
    
    dff4 = my_df[my_df.Category == cat_slctd]['Product Type'].value_counts()
    
    dff5 = my_df[(my_df.Category ==  cat_slctd)].groupby('State')['Total Amount (USD)'].sum().sort_values(ascending=False)#[:10]
    
    
    

    
    # Plotly Express
    fig1 = px.bar(dff1, x='Manufacturer / GPO', y='Total Amount (USD)',
                 title="Highest Paying Manufacturers / GPOs for " + cat_slctd)
    
    fig2 = px.bar(dff2, x='Physician Specialty', y='Total Amount (USD)',
                 title="Highest Paid Pysician Specialities in " + cat_slctd)
    
    fig3 = px.pie(dff3, names=dff3.index, values=dff3.values, hole=0.6,
                 title="Physician's Primary Type Distribution")
    
    fig4 = px.pie(dff4,  names=dff4.index, values=dff4.values, hole=0.6,
                 title="Product Type Distribution")
    
    fig5 = px.treemap(dff5,
        names = dff5.index,
        parents = ['United States']*len(dff5.index),
        values = dff5.values,
        title = 'Top Paying States for '+ cat_slctd,
        hover_name=dff5.index)
    fig5.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    
    
    return fig1, fig3, fig4, fig2, fig5



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8002)
