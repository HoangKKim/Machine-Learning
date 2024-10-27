from bokeh.plotting import figure, show, output_notebook, output_file
import pandas as pd
from bokeh.layouts import column, row, Spacer
from bokeh.models import Slider, HoverTool, ColumnDataSource, Select, NumeralTickFormatter
from bokeh.io import curdoc

# đọc file csv và nhóm theo cột "Country/Region"  (các giá tri sum lại với nhau)
df = pd.read_csv("./covid-19-cases.csv").groupby("Country/Region").sum().iloc[:, 4:]

df.columns = pd.to_datetime(df.columns)

asean_countries = ['Brunei', 'Cambodia', 'Indonesia', 'Laos', 
    'Malaysia' , 'Philippines', 'Singapore', 'Thailand', 'Vietnam'
]

# lọc và tạo biểu đồ với các quốc gia ở ĐNA
df_asean = df[df.index.isin(asean_countries)]

# data
source_1 = ColumnDataSource(
    data = dict(date = df_asean.columns, 
                cases = df_asean.loc["Vietnam"].values))

# Chuẩn bị màu sắc cho từng quốc gia
colors = ['#E6E6FA', '#D8BFD8', '#DDA0DD', '#DA70D6', '#FFE4E1', 
    '#FFB6C1', '#D87093', '#F5DEB3', '#E8BFD8']

# Chuẩn bị dataset cho ColumnDataSource
initial_date = df_asean.columns[0]
source_2 = ColumnDataSource(data=dict(
    country=asean_countries,
    cases=df_asean[initial_date].values,
    color=colors
))
print(source_2.data)

# chart 
def line_chart():
    # Tạo figure
    p = figure(
        title="COVID-19 CASES IN VIETNAM", 
        x_axis_label='DATE', 
        y_axis_label='CASES', 
        x_axis_type='datetime', 
        sizing_mode="stretch_width",
        width = 800, height=400)
    p.title.text_font_size = '20pt'
    p.title.align = 'center'
    p.line(x = 'date', 
        y = 'cases', 
        source=source_1, 
        line_width=2)
    p.vbar(x= 'date', top = 'cases', source = source_1, width = 0.1)

    p.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
    # Tạo và cấu hình HoverTool
    hover = HoverTool()
    hover.tooltips = [("Date", "@date{%F}"), ("Cases", "@cases{0,0}")]
    hover.formatters = {'@date': 'datetime'}  # Định dạng ngày tháng

    # Thêm HoverTool vào figure
    p.add_tools(hover)
    p.toolbar_location = "below"
    return p

def bar_chart():
    # Tạo figure
    p = figure(
        y_range=asean_countries, 
        title=f"COVID-19 CASES ON {initial_date.strftime('%d %B %Y')}", 
        x_axis_label='CASES', 
        y_axis_label='COUNTRY', 
        width=800, height=400, sizing_mode='stretch_width')

    # Vẽ hbar chart với màu sắc
    p.hbar(y='country', right='cases', source=source_2, height=0.4, color='color')
    p.title.text_font_size = '20pt'
    p.title.align = 'center'
    # Định dạng số trên trục x
    p.xaxis[0].formatter = NumeralTickFormatter(format="0,0")

    # Tạo và cấu hình HoverTool
    hover = HoverTool()
    hover.tooltips = [("Country", "@country"), ("Cases", "@cases{0,0}")]
    p.add_tools(hover)
    p.toolbar_location = "below"
    return p


p_1 = line_chart()
p_2 = bar_chart()


# widgets
select = Select(
    title = "Select Country", 
    value = "Vietnam", 
    options = list(df_asean.index))

slider = Slider(start=0, end=len(df_asean.columns)-1, value=0, step=1, title="Date")


# update data
def update_plot(attr, old, new):
    selected_country = select.value
    new_data= dict(date = df_asean.columns, 
                   cases = df_asean.loc[selected_country].values)
    source_1.data = new_data
    p_1.title.text = f"COVID-19 CASES IN {selected_country}"
    
# Hàm update data khi slider thay đổi
def update(attr, old, new):
    selected_date = df_asean.columns[int(slider.value)]
    
    # Cập nhật dữ liệu cho ColumnDataSource
    new_data = dict(
        country=asean_countries,
        cases=df_asean[selected_date].values,
        color=colors  # Giữ nguyên màu sắc, không cần cập nhật
    )
    source_2.data = new_data
    
    # Cập nhật tiêu đề
    p_2.title.text = f"COVID-19 CASES ON {selected_date.strftime('%d %B %Y')}"

# Liên kết slider với hàm update
slider.on_change('value', update)

# link widget with update function
select.on_change('value', update_plot)

# Sắp xếp layout
spacer1 = Spacer(height=50)
layout = column(
    row( p_1, select, sizing_mode='stretch_width'),
    spacer1,
    column(p_2, slider, sizing_mode='stretch_width'), sizing_mode='stretch_width')

# Nếu chạy trong Bokeh server
curdoc().add_root(layout)

# Hiển thị layout
show(layout)


