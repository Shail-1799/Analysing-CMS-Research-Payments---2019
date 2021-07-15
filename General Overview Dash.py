
from Dash_variables import *


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    

    
    general_layout

        
        
], fluid=True)


# ------------------------------------------------------------------------------

@app.callback(
    Output(component_id='fig1', component_property='figure'),
    [Input(component_id='yaxis_raditem', component_property='value'),]
    
)

def update_graph(y_axis):
    
    if y_axis == '10N':
        
        dff1 = my_df.groupby('State', as_index=False)['Total Amount (USD)'].count().sort_values(by='Total Amount (USD)',ascending=False)[:10]
        dff1.columns=['State', 'No. of Payments']
        fig1 = px.bar(dff1, x='State', y='No. of Payments', title="Top 10 Overall Highest Payments Receiving States")
   
    elif y_axis == '10A':
        
        dff1 = my_df.groupby('State', as_index=False)['Total Amount (USD)'].sum().sort_values(by='Total Amount (USD)',ascending=False)[:10]
        fig1 = px.bar(dff1, x='State', y='Total Amount (USD)',  title="Top 10 Overall Highest Amount Receiving States")
    
    else:
    ## Without Stacked Categories


    #     dff1 = my_df.groupby(["Recipient State"])['Total Amount (USD)'].agg(['size','sum'])
    #     dff1.reset_index(inplace=True)
    #     dff1.columns = ['State', 'No. of Payments', 'Total Amount (USD)']


    #     fig1 = px.bar(dff1, x='State', y=y_axis, title="{0} Received by US States".format(y_axis))



     ## With Stacked Categories

        dff1 = my_df.groupby(["Recipient State", 'Category'])['Total Amount (USD)'].agg(['size','sum'])

        dff1.reset_index(inplace=True)
        dff1.columns = ['State', 'Category','No. of Payments', 'Total Amount (USD)']

        index_del = dff1[(dff1.Category == 'Nan') | (dff1.Category == 'None')].index
        dff1.drop(
            labels=index_del,
            axis=0,
            inplace=True    
        )

        d=dff1.sort_values(by='Total Amount (USD)', ascending=False).groupby(['State']).head(5)

        fig1 = px.bar(d, x='State', y=y_axis, color='Category', title="{0} Received by US States with Top Therapeutic Areas".format(y_axis))

        
    return (fig1)




@app.callback(
    Output(component_id='fig2', component_property='figure'),
    [Input(component_id='origin', component_property='value')]
)

def update_graph(origin):
    
    if origin == 'Country':
        
        cdf = df.groupby(['Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Country']).Total_Amount_of_Payment_USDollars.agg(['size','sum','mean'])
        cdf.reset_index(inplace=True)
        cdf.columns = ['Country','No. of Payments', 'Total Amount', 'Avg. Amount']
        cdf = cdf[cdf.Country != 'United States']

        fig2 = px.scatter(cdf, x='No. of Payments', y='Total Amount',
                         size='Total Amount', color='Country', hover_name='Country',
                         size_max=80, title='Payments Originated from Outside of The United States')
    else:
        
        usdf = df.groupby(['Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_State']).Total_Amount_of_Payment_USDollars.agg(['size','sum','mean'])
        usdf.reset_index(inplace=True)
        usdf.columns = ['State','No. of Payments', 'Total Amount', 'Avg. Amount']

        fig2 = px.scatter(usdf, x='No. of Payments', y='Total Amount',
                         size='Total Amount', color='State', hover_name='State',
                         size_max=80, title='Payments Originated from The United States')




    return (fig2)

# @app.callback(
#     Output('computed-table', 'data'),
#     Output('content-disputes', 'children'),
#     Input('computed-table', 'data_timestamp'),
#     State('computed-table', 'data'))

# def update_columns(timestamp, rows):
#     s=0
#     for i,row in enumerate(rows):
#         try:
            
#             d['Updated Amount'].iloc[i] = row['Updated Amount']
#             s+=float(row['Updated Amount'])
#         except:
#             row['output-data'] = 'NA'
#     #dispute = s
#     return rows, str(round((s/1000),3)) + " K"






if __name__ == '__main__':
    app.run_server(debug=True, port=8001)