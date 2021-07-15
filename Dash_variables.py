import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime as dt
import calendar

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table 
import dash_bootstrap_components as dbc

my_df = pd.read_csv("my_df.csv", low_memory=False)

# Formatting Categories
cats = [str(c).title() for c in my_df.Category]
my_df.Category = cats


# Labels For Filter
op_labels = ['label', 'value']

states = [s for s in my_df.State.unique() if s is not np.NaN]
state_options = [{l:s for l in op_labels} for s in states]

cat = [c for c in my_df.Category.unique()]
cat.remove('Nan')
cat.remove('None')
category_options = [{l:c for l in op_labels} for c in cat]

gpo = [s for s in my_df['Manufacturer / GPO'].unique() if s is not np.NaN]
gpo_options = [{l:s for l in op_labels} for s in gpo]

d = my_df[my_df.Disputed == 'Yes'][['Manufacturer / GPO','Date','Disputed','Total Amount (USD)']]
d['Updated Amount'] = d['Total Amount (USD)']

##### For General Overview #####


### CARDS ###
 
# No. of Payments
num_payments =  my_df['Total Amount (USD)'].count()

# Amount
amount = my_df['Total Amount (USD)'].sum()
amount = str(round((amount/1000000),3)) + " M"

# No. of companies
num_comps =  my_df['Manufacturer / GPO'].nunique()

# Disputes
dispute = my_df[(my_df.Disputed == 'Yes')]['Total Amount (USD)'].sum()
dispute = str(round((dispute/1000000),3)) + " M"


### PLOTS ###


# # States receiving Payments
# dff1 = my_df.groupby(["Recipient State"])['Total Amount (USD)'].agg(['size','sum'])
# dff1.reset_index(inplace=True)
# dff1.columns = ['State', 'No. of Payments', 'Total Amount (USD)']
# fig1_1 = px.bar(dff1, x='State', y='No. of Payments', title="Payments Received by US States")
# fig1_2 = px.bar(dff1, x='State', y='Total Amount (USD)', title="Payments Received by US States")

# # Payment Origin
# cdf = df.groupby(['Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Country']).Total_Amount_of_Payment_USDollars.agg(['size','sum','mean'])
# cdf.reset_index(inplace=True)
# cdf.columns = ['Country','No. of Payments', 'Total Amount', 'Avg. Amount']
# cdf = cdf[cdf.Country != 'United States']

# fig2_1 = px.scatter(cdf, x='No. of Payments', y='Total Amount',
#                  size='Total Amount', color='Country', hover_name='Country',
#                  size_max=80, title='Payments Originated from Outside of The United States')

# usdf = df.groupby(['Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_State']).Total_Amount_of_Payment_USDollars.agg(['size','sum','mean'])
# usdf.reset_index(inplace=True)
# usdf.columns = ['State','No. of Payments', 'Total Amount', 'Avg. Amount']

# fig2_2 = px.scatter(usdf, x='No. of Payments', y='Total Amount',
#                  size='Total Amount', color='State', hover_name='State',
#                  size_max=80, title='Payments Originated from The United States')


# Product Categories
dff3 = my_df.groupby('Category')['Total Amount (USD)'].sum().sort_values(ascending=False)[:100]
if 'None' in dff3.index:
    dff3.drop('None', axis=0,inplace=True)
if 'Nan' in dff3.index:
    dff3.drop('Nan', axis=0,inplace=True)
    
fig3 = px.treemap(dff3,
    names = dff3.index,
    parents = ['All']*len(dff3.index),
    values = dff3.values,
    title = 'Highest Paid Therapeutic Areas',
    hover_name=dff3.index)

# Specialties
dff4 = my_df[(my_df['Physician Specialty'] != 'nan')]
dff4 = dff4.groupby('Physician Specialty')['Total Amount (USD)'].sum().sort_values(ascending=False)[:50]

fig4 = px.bar(dff4, x=dff4.index, y=dff4.values, title="Top Paid Physician Specialties")
#fig4 = fig4.update_layout(height=750)






###############  Dashboard layouts  ###################

# 1. General overview Dashboard

general_layout = html.Div([ 
    
    #ROW 1
    dbc.Row([
        

        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H4(className="title",id='title1-content'),
                    html.H1(
                        [
                            "CMS Research Payments - 2019: General Overview "            
                        ],
                    
                        style={'textAlign':'center','font-weight': 'bold'},
                        className="card-text",
                    ),
                    
                     
                ],
                style={'height':'100px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
       
        ),
        
   
        

            
    ],className='mb-2 mt-2'),
    
   ##########################################################################################################################
    # ROW 2
    dbc.Row([dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(num_payments,className="card-title",id='content-payments',style={'color':'#0B88CB','font-weight': 'bold'}),
                    html.H5(
                        [
                            "No. of Payments"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(amount,className="card-title",id='content-amount',style={'color':'#0B88CB','font-weight': 'bold'} ),
                    html.H5([
                            "Total Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                       
              ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(num_comps,className="card-title",id='content-companies',style={'color':'#0B88CB','font-weight': 'bold'}),
                    html.H5(
                        [
                            "No. of Companies"
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(dispute,className="card-title",id='content-disputes',style={'color':'#0B88CB','font-weight': 'bold'}),
                    html.H5(
                        [
                            "Disputed Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        )
 
            
    ],className='mb-2'),
    
  ############################################################################################################################  
    # ROW 3    
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     
                    
            dcc.RadioItems(
                id='yaxis_raditem',
                options=[
                         {'label': 'No. of Payments    ', 'value': 'No. of Payments'},
                         {'label': 'Total Amount', 'value': 'Total Amount (USD)'},
                ],
                value='No. of Payments',
                style={"width": "100%"}
                
            ,inputStyle={"margin-right": "10px","margin-left": "20px"}),
                    
#                      
                   dcc.Graph(id='fig1', figure={}) 
                ])
            ]),
        ], width=12),
        
   
        
 
        
            
    ],className='mb-2'),
    
    ##########################################################################################################################
    # ROW 4    
     dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     
#                     
                     
            dcc.RadioItems(
                id='origin',
                options=[
                         {'label': 'Within US', 'value': 'State'},
                         {'label': 'Outside US', 'value': 'Country'},
                ],
                value='State',
                style={"width": "100%"}
                
            ,inputStyle={"margin-right": "10px","margin-left": "20px"}),
                    
                   dcc.Graph(id='fig2', figure={}) 
                ])
            ]),
        ], width=12),
        
                    
       
        
            
    ],className='mb-2'),
    
     ##########################################################################################################################
    # ROW 5   
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig3)    
                ])
            ]),
        ], width=12),
        
        
                   
    ],className='mb-2'),
    
   
    
    ##########################################################################################################################
    # ROW 6   
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig4)    
                ])
            ]),
        ], width=12),
        
        
                   
    ],className='mb-2')     

        
])







# 2. State Dashboard

state_layout = html.Div([ 
    
    
    
    # ROW 1
    dbc.Row([
        

        dbc.Col([
            dbc.Card(
            dbc.CardBody(
                [
                    html.H4(className="title",id='title2-content'),
                    html.H1(
                        [
                            "CMS Research Payments - 2019: State Wise Analysis"            
                        ],
                        style={'textAlign':'center'},
                        className="card-text",
                    ),
                ],
                style={'height':'100px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
       
        ], width = 10),
        
#         dbc.Col([
            
#             dbc.Card([
                
#                 dbc.CardBody([
                    
#                     dcc.DatePickerSingle(
#                         id='start_date',
#                         date=date(2019, 1, 1),
#                         className='ml-5'),
                    
#                     dcc.DatePickerSingle(
#                         id='end_date',
#                         date=date(2019, 12, 31),
#                         className="ml-5")
                    
#                 ])
#             ], color="info")
#         ], width=4),
        
#         dbc.Col([
#             dbc.Card(
#                 dbc.CardBody([
                    
#                     dcc.DatePickerSingle(
#                         id='start_date',
#                         date=date(2019, 1, 1),
#                         className='ml-5'),
                    
#                     dcc.DatePickerSingle(
#                         id='end_date',
#                         date=date(2019, 12, 31),
#                         className="ml-5")
                    
#                 ],
#                 style={'height':'90px'}
#             ),
#             className="w-100",
#             style={'box-shadow':'2px 2px 10px grey'},
#             color="info")
#         ], width=4),
        

        
        dbc.Col([
            dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(id="slct_state",
                     options=state_options,
                     multi=False,
                     value='CA',
                     style={'width': "100%"},
                     ),
                    
                ],
                style={'height':'100px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'},
            color="info")
                 
        ], width=2)
        
        

            
    ],className='mb-2 mt-2'),
    
   ##########################################################################################################################
    # ROW 2
    dbc.Row([dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content2-payments',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "No. of Payments"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content2-amount',style={'color':'#0B88CB'}),
                    html.H5([
                            "Total Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content2-companies',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "No. of Companies"
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content2-disputes',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "Disputed Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        )
 
            
    ],className='mb-2'),
    
  ############################################################################################################################  
    # ROW 3    
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='States_Bar')    
                ])
            ]),
        ], width=6),
        
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                   dcc.Graph(id='Primary_Type', figure={})
                ])
            ]),
        ], width=6)
            
    ],className='mb-2'),
    
    ##########################################################################################################################
    # ROW 4    
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='Product_Type', figure={})    
                ])
            ]),
        ], width=6),
        
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                   dcc.Graph(id='Spec_Bar', figure={})
                ])
            ]),
        ], width=6)
            
    ],className='mb-2'),
       
    
     ##########################################################################################################################
    # ROW 5   
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='Category', figure={})    
                ])
            ]),
        ], width=12),
        
        
                   
    ],className='mb-2'),
    
    
        
                
])








# 3. Category Dashboard

category_layout = html.Div([ 
    
    # ROW 1
    dbc.Row([
        

        dbc.Col([
            dbc.Card(
            dbc.CardBody(
                [
                    html.H4(className="title",id='title3-content'),
                    html.H1(
                        [
                            "CMS Research Payments - 2019: Category Wise Analysis"            
                        ],
                        style={'textAlign':'center'},
                        className="card-text",
                    ),
                ],
                style={'height':'100px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
       
        ], width = 10),
  
        
        dbc.Col([
            dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(id="slct_cat",
                     options=category_options,
                     multi=False,
                     value='Oncology',
                     style={'width': "100%"},
                     ),
                    
                ],
                style={'height':'100px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'},
            color="info")
                 
        ], width=2)
        
        

            
    ],className='mb-2 mt-2'),
    
   ##########################################################################################################################
    # ROW 2
    dbc.Row([dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content3-payments',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "No. of Payments"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content3-amount',style={'color':'#0B88CB'}),
                    html.H5([
                            "Total Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content3-companies',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "No. of Companies"
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        ),
        dbc.Col(
            dbc.Card(
            dbc.CardBody(
                [
                    html.H2(className="card-title",id='content3-disputes',style={'color':'#0B88CB'}),
                    html.H5(
                        [
                            "Disputed Amount (USD)"            
                        ],
                        className="card-text",
                    ),
                ],
                style={'height':'120px'}
            ),
            className="w-100",
            style={'box-shadow':'2px 2px 10px grey'}
        )
        )
 
            
    ],className='mb-2'),
    
  ############################################################################################################################  
    # ROW 3    
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='States_Bar3')    
                ])
            ]),
        ], width=6),
        
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                   dcc.Graph(id='Primary_Type3', figure={})
                ])
            ]),
        ], width=6)
            
    ],className='mb-2'),
    
    ##########################################################################################################################
    # ROW 4    
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='Product_Type3', figure={})    
                ])
            ]),
        ], width=6),
        
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                   dcc.Graph(id='Spec_Bar3', figure={})
                ])
            ]),
        ], width=6)
            
    ],className='mb-2'),
       
    
     ##########################################################################################################################
    # ROW 5   
    dbc.Row([
                
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='Category3', figure={})    
                ])
            ]),
        ], width=12),
        
        
                   
    ],className='mb-2'),
    
    
        
        
        
])



