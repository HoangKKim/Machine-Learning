from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import curdoc
from bokeh.layouts import column, row
from math import pi
import pandas as pd
from bokeh.transform import cumsum
from bokeh.themes import Theme
# Đọc file csv và nhóm theo cột "Country/Region" (các giá trị sum lại với nhau)
df = pd.read_csv("./covid-19-cases.csv").groupby("Country/Region").sum().iloc[:, 4:]

# Chuyển đổi cột thành datetime
df.columns = pd.to_datetime(df.columns)

# Cập nhật danh sách các quốc gia có trong dữ liệu
asean_countries = [
    'Brunei', 'Cambodia', 'Indonesia', 'Laos', 
    'Malaysia','Philippines', 'Singapore', 'Thailand', 'Vietnam'
]

# Lọc và tạo biểu đồ với các quốc gia ở ĐNA
df_asean = df[df.index.isin(asean_countries)]

# Chọn ngày cuối cùng để hiển thị
latest_date = df_asean.columns[-1]

# Lấy dữ liệu số ca mắc và tính toán tỷ lệ phần trăm
cases = df_asean[latest_date].values
countries = df_asean.index.tolist()

# Tính toán tỷ lệ phần trăm và góc
total_cases = sum(cases)
angles = [case / total_cases * 2 * pi for case in cases]

# Tạo danh sách màu sắc cho mỗi quốc gia
colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
    "#9467bd", "#8c564b", "#e377c2", 
    "#bcbd22", "#17becf"
]

# Chuẩn bị dữ liệu cho ColumnDataSource
data = pd.DataFrame({
    'country': countries,
    'angle': angles,
    'color': colors,
    'cases': cases
})
source = ColumnDataSource(data)

def make_chart(title, title_font_size="20pt", legend_location="right", 
               legend_font_size="12pt", radius=0.4, x_range=(-1, 1), y_range=(-1, 1), theme='default'):
    
    p = figure(height=450, width=450, title=title,
               toolbar_location=None, tools="hover", tooltips="@country: @cases{0,0}",
               x_range=x_range, y_range=y_range)
    
    # Vẽ pie chart sử dụng wedge
    p.wedge(x=0, y=0, radius=radius,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=source)
    
    # Tùy chỉnh tiêu đề
    p.title.text_font_size = title_font_size
    
    # Tùy chỉnh legend
    legend = p.legend[0]
    legend.location = legend_location
    legend.label_text_font_size = legend_font_size
    legend.label_standoff = 10
    
    # Áp dụng theme
    if theme == 'dark':
        p.background_fill_color = "#2F2F2F"
        p.border_fill_color = "#2F2F2F"
        p.title.text_color = "white"
        p.xaxis.major_label_text_color = "white"
        p.yaxis.major_label_text_color = "white"
        p.legend.label_text_color = "gray"
        
    elif theme == 'light':
        p.background_fill_color = "#FFFFAA"
        p.border_fill_color = "#FFFFDA"
        p.title.text_color = "black"
        p.xaxis.major_label_text_color = "black"
        p.yaxis.major_label_text_color = "black"
        p.legend.label_text_color = "black"
        
    elif theme == 'pastel':
        p.background_fill_color = "#F0F8FF"
        p.border_fill_color = "#F0F8FF"
        p.title.text_color = "#4682B4"
        p.xaxis.major_label_text_color = "#4682B4"
        p.yaxis.major_label_text_color = "#4682B4"
        p.legend.label_text_color = "#4682B4"
    
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p

# Tạo các biểu đồ với các chủ đề khác nhau
chart1 = make_chart(
    title="COVID-19 Cases Distribution - Dark Theme",
    title_font_size="12pt",
    legend_location="top_left",
    legend_font_size="10pt",
    theme='dark'
)

chart2 = make_chart(
    title="COVID-19 Cases Distribution - Light Theme",
    title_font_size="15pt",
    legend_location="top_right",
    legend_font_size="10pt",
    theme='light'
)

chart3 = make_chart(
    title="COVID-19 Cases Distribution - Pastel Theme",
    title_font_size="10pt",
    legend_location="bottom_left",
    legend_font_size="10pt",
    theme='pastel'
)

# Sắp xếp các biểu đồ
layout = row(chart1, chart2, chart3, sizing_mode='stretch_width')

# Hiển thị layout
curdoc().add_root(layout)
