from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.layouts import layout

from bokeh.plotting import figure
from datetime import datetime
from math import radians
import numpy as np

# Tạo figure
p = figure(x_axis_type="datetime", width=900, height=350, title="DEMO FOR REAL TIME DATA")

# Hàm tạo dữ liệu giả
def create_value(): 
    draw = np.random.randint(0, 2, size=200)
    steps = np.where(draw > 0, 1, -1)
    walk = steps.cumsum()
    return walk[-1]

# Tạo nguồn dữ liệu
source = ColumnDataSource(dict(x=[], y=[]))

# Vẽ điểm và đường trên biểu đồ
p.circle(x='x', y='y', color='firebrick', line_color='firebrick', source=source, size=10)
p.line(x='x', y='y', source=source)

# Tạo công cụ HoverTool
hover = HoverTool()
hover.tooltips = [("Date", "@x{%F %T}"), ("Value", "@y")]
hover.formatters = {'@x': 'datetime'}  # Định dạng ngày tháng
p.add_tools(hover)

# Hàm cập nhật dữ liệu
def update():
    new_data = dict(x=[datetime.now()], y=[create_value()])
    source.stream(new_data, rollover=10)

# Hàm callback
def update_intermed(attrname, old, new):
    source.data = dict(x=[], y=[])
    update()

# Định dạng trục x
date_pattern = ['%Y-%m-%d\n%H:%M:%S']
p.xaxis.formatter = DatetimeTickFormatter(
    seconds=date_pattern,
    minsec=date_pattern,
    minutes=date_pattern,
    hourmin=date_pattern,
    hours=date_pattern, 
    days=date_pattern,
    months=date_pattern,
    years=date_pattern,
)
p.xaxis.major_label_orientation = radians(80)
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Value"

# Cấu hình layout
my_layout = layout(p)
curdoc().title = "Streaming Stock Data"
curdoc().add_root(my_layout)
curdoc().add_periodic_callback(update, 500)
