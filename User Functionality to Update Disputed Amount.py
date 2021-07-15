from Dash_variables import *



d = my_df[my_df.Disputed == 'Yes'][['Manufacturer / GPO','Date','Disputed','Total Amount (USD)']]
d['Updated Amount'] = d['Total Amount (USD)']

app = dash.Dash(__name__)

app.layout = html.Div([

   dbc.Row([dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content-disputes',style={'color':'#0B88CB','font-weight': 'bold'}),
                    html.H5(
                        [
                            "Disputed Amount"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ), ],className='mb-2 mt-2'),
    
        dash_table.DataTable(
        id='computed-table',
        columns=[{"name": i, "id": i} for i in d.columns],
        editable=True,
        data=d.to_dict('records'),
        style_cell={'textAlign': 'left'},
            
    ),
])


@app.callback(
    Output('computed-table', 'data'),
    Output('content-disputes', 'children'),
    Input('computed-table', 'data_timestamp'),
    State('computed-table', 'data'))

def update_columns(timestamp, rows):
    s=0
    for i,row in enumerate(rows):
        try:
            
            d['Updated Amount'].iloc[i] = row['Updated Amount']
            s+=float(row['Updated Amount'])
        except:
            row['output-data'] = 'NA'
    dispute = s
    return rows, s


if __name__ == '__main__':
    app.run_server(debug=True)