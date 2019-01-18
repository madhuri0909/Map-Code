# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 12:57:29 2019

@author: masonawa
"""

import pandas as pd
import geopandas as gpd
from shapely.ops import nearest_points
from shapely.geometry import Point
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import show,output_notebook,curdoc
from bokeh.layouts import widgetbox,layout, widgetbox, column, row
from bokeh.models import ColumnDataSource , HoverTool ,LogColorMapper,CustomJS, OpenURL, TapTool,Select,Legend,LegendItem
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import RdYlBu11 as palette
from bokeh.core.properties import value
from bokeh.models.widgets import Dropdown
import math

color = {
    "NASHVILLE FIELD OFFICE":"#E52B50",
    "DENVER FIELD OFFICE":"#F19CBB",
    "ATLANTA FIELD OFFICE":"#D3212D",
    "COLUMBUS FIELD OFFICE":"#FFBF00",
    "CHICAGO FIELD OFFICE":"#3B3B6D",
    "DALLAS FIELD OFFICE":"#915C83",
    "WALNUT CREEK FIELD OFFICE":"#00FFFF",
    "BETHESDA FIELD OFFICE":"#C0C0C0",
    "STAMFORD FIELD OFFICE":"#1DACD6",
    "LONG BEACH FIELD OFFICE":"#FF69B4", 
}
def near(point, pts):
     # find the nearest point and return the corresponding Place value
     nearest = gpd2.geometry == nearest_points(point, pts)[1]
     return gpd2[nearest].color.get_values()[0]

_color = []
iter_file = pd.read_csv(r'C:\Mcdonalds\Application Mngm\vaidehi_region_added_county_final_new.csv')
pointData=[]
for i in range(len(iter_file)):
    if iter_file.iloc[i]["Region"] in color:
        _color.append(color[iter_file.iloc[i]["Region"]])
#         xArray= list(file.iloc[i]["x"])
        store=[]
    #x,y coordinates of color region
        xArrayString= iter_file.iloc[i]["x"]
        yArrayString= iter_file.iloc[i]["y"]
        x=xArrayString[1:xArrayString.find(",")]
        y=yArrayString[1:yArrayString.find(",")]
        xx=float(x[0:int(x.find("."))+3])
        yy=float(y[0:int(y.find("."))+3])
        point=Point(xx,yy)
        store.append(color[iter_file.iloc[i]["Region"]])
        store.append(point)
        pointData.append(store)
        
    else:
        _color.append("#FFFFFF")
print('prepare dataframe')
gpd2= gpd.GeoDataFrame(pointData,columns=['color','geometry'])
pts3 = gpd2.geometry.unary_union
print('prepared dataframe')
for j in range(len(_color)):
    if _color[j]== "#FFFFFF":
        #x,y coordinates of None region
        xWhiteArray= iter_file.iloc[j]["x"]
        yWhiteArray= iter_file.iloc[j]["y"]
        xWhitePoint=xWhiteArray[1:xWhiteArray.find(",")]
        yWhitePoint=yWhiteArray[1:yWhiteArray.find(",")]
        xxx=float(xWhitePoint[0:int(xWhitePoint.find("."))+3])
        yyy=float(yWhitePoint[0:int(yWhitePoint.find("."))+3])
        whitePoint=Point(xxx,yyy)
        cc=near(whitePoint, pts3)
        _color[j]=cc
print("end")       
iter_file["Color"] = _color
     
#iter_file.to_pickle(r'C:\Users\atrivedy\Documents\Visualilzation\vaidehi_plot_data\gpd.pkl')
temp_gpd_file = gpd.read_file(r"C:\Mcdonalds\Application Mngm\gpd.shp")
temp_gpd_file["Color"] = _color
temp_gpd_file.to_file(r"C:\Mcdonalds\Application Mngm\gpdNew.shp")
countydata = gpd.read_file(r"C:\Mcdonalds\Application Mngm\gpdNew.shp")

import geopandas as gpd
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper

countydata = gpd.read_file(r"C:\Mcdonalds\Application Mngm\gpdNew.shp")

def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list(exterior.coords.xy[0])
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list(exterior.coords.xy[1])

countydata['x'] = countydata.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
countydata['y'] = countydata.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)

newCounty = countydata.drop('geometry', axis=1).copy()
newCountysource = ColumnDataSource(newCounty)
countyview = figure(plot_width=1180, plot_height=600, x_range=(-160, -60), y_range=(15, 55),tools="tap",title="US county")
renderer=countyview.patches('x','y',source=newCountysource,color ="Color",fill_alpha=0.6, 
                            line_color="black", line_width=0.1)
legend = Legend(items=[
    LegendItem(label="WALNUT CREEK FIELD OFFICE",renderers=[renderer],index=0),
    LegendItem(label="STAMFORD FIELD OFFICE",renderers=[renderer], index=1),
    LegendItem(label="ATLANTA FIELD OFFICE",renderers=[renderer],index=2),
    LegendItem(label="COLUMBUS FIELD OFFICE",renderers=[renderer], index=3),
    LegendItem(label="LONG BEACH FIELD OFFICE",renderers=[renderer],index=4),
    LegendItem(label="DALLAS FIELD OFFICE",renderers=[renderer], index=5),
    LegendItem(label="BETHESDA FIELD OFFICE",renderers=[renderer],index=6),
    LegendItem(label="BETHESDA FIELD OFFICE",renderers=[renderer], index=7),
    LegendItem(label="STAMFORD FIELD OFFICE",renderers=[renderer],index=8),
    LegendItem(label="LONG BEACH FIELD OFFICE",renderers=[renderer], index=9),
])
# countyview.title.text=title
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper,Select
import numpy as np
import datetime as datetime
regPoint= pd.read_csv(r'C:\Mcdonalds\Application Mngm\US Market stores data.csv')
points = pd.read_csv(r'C:\Mcdonalds\Application Mngm\Visualilzation\incident_p1_p2_dummy.csv')

#points.join(regPoint, lsuffix='_points', rsuffix='_regPoint')
allData=points.set_index('location').join(regPoint.set_index('Natl Str Num'))

# print(allData['x'].tolist())
xx=allData['x'].tolist()
yy=allData['y'].tolist()
yyy = np.array(yy)
y4 = yyy.astype(np.float)
incident=allData['number'].tolist()
# region=allData['Field_Office'].tolist()

dataa=[]
incident=allData['number'].tolist()
description=allData['short_description'].tolist()
state=allData['incident_state'].tolist()
region=allData['Field_Office'].tolist()
opentime=allData["opened_at"].tolist()
priority=allData["priority"].tolist()
for i in range(len(opentime)):
    if str(opentime[i]).find("/") != -1:
        dnt=str(opentime[i]).split(" ")
        dt=datetime.datetime.strptime(dnt[0], '%m/%d/%Y').strftime('%d-%m-%Y')
        opentime[i]="{} {}".format(dt, dnt[1])
size=[]
 
import json
for i in range(len(incident)):
    size.append(5);
    d={'incident':incident[i], 'description':description[i], 'state':state[i],
       'region':region[i], 'opentime':opentime[i],'priority':priority[i]}
    dataa.append(json.dumps(d))
#source = ColumnDataSource(data=dict(x=xx, y=y4,incident= incident,region= region,priority= priority,size=size,description= description))
#circle1=countyview.circle(x="x",y="y",size=5,color='blue', name='name',source=source)
source = ColumnDataSource(data=dict(x=xx, y=y4,incident= incident,region= region,priority= priority,size=size,description= description))
circle1=countyview.circle(x="x",y="y",size="size",color='blue', name='name',source=source)
countyview.add_tools(HoverTool(tooltips=TOOLTIPS, renderers=[circle1]))
url="http://127.0.0.1:5000/hello/@name"
taptool =countyview.select(type=TapTool)
taptool.callback = OpenURL(url=url)
TOOLTIPS ="""

    <h2 align='center' style='color:red;background-color:#f0f0f0'>Critical Incident Alert</h2>

<div class="row">
  <div class="column1" style="background-color:#f0f0f0;">
    <h3>Priority 1</h3>
    	<table>
    		<tr>
            	<td height='50'><font face='Helvetica Neue' size='4' color='black'>Incident</font></td>
                <td><font face='Helvetica Neue' size='4' color='blue'>@incident</font></td>
            </tr>
            <tr>
            	<td height='50'><font face='Helvetica Neue' size='4' color='black'>Market</font></td>
                <td><font face='Helvetica Neue' size='4' color='blue'>@region</font></td>
            </tr>
			<tr>
            	<td height='50'><font face='Helvetica Neue' size='4' color='black'>Application</font></td>
                <td><font face='Helvetica Neue' size='4' color='blue'>McDelivery</font></td>
            </tr>
		</table>
  </div>
  <div class="column2" style="background-color:#fff9f4;">
    <h3>Details</h3>
        <table>
    		<tr>
            	<td height='100' valign="top"><font face='Helvetica Neue' size='3' color='black'><strong>Description</strong><br>@{description}</font></td>
            </tr>
            
		</table>
  </div> 

"""
countyview.add_layout(legend,'left')
countyview.legend.location = "top_left"
countyview.legend.click_policy="hide"
#
#def update_plot(attrname, old, new):
#   def update_plot(attrname, old, new):
#    if select.options == 'P1 Tickets':
#        layout = row(select, countyview)
#    else:
#        layout = row(select,countyview_p1)
callback = CustomJS(args=dict(source=source), code="""
                    data=source.data;
                    console.log(data)
                    console.log(data['size']);
                    pp=data['priority'];
                    if(cb_obj.value == 'ALL')
                    {
                    var sss=new Array()
                    for(i=0; i<pp.length; i++)
                    {
                        sss[i]=5;    
                    }
                    data['size']=sss
                    }
                    else
                    {
                   
                    ss=data['size'];
                    
                    var sss=new Array()
                   
                    
                    
                    for(i=0; i<pp.length; i++)
                    {
                            
                            if(pp[i]==cb_obj.value){
                            sss.push(5);
                           
                            }
                            else{
                            sss.push(0);
                            }
                    }
                    data['size']=sss
                   
                   
                    }
                      
                    
                    source.change.emit();
                    """)

select = Select(title="Tickets Priority", options=['ALL','1 - High', '2 - High'], width=250)
select.js_on_change('value', callback)
l = layout(select,countyview)

show(l)