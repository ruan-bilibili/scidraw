import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties
import numpy as np
import io
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from io import BytesIO
import base64
######################################顶部设计###############################################################

######################################顶部设计###############################################################







######################################侧边栏###############################################################
# 选择图表类型
chart_type = st.sidebar.selectbox("选择图表类型", ["1. 条形图", "2. 频率直方图", "3. 折线图", "4. 散点图", "5. 饼图", "6. 箱线图", "7. 热力图", "8. 等高线图", "9. 3D直方图"])

# 在选择图表类型时显示相应的图像和子标题
chart_images = {
    "1. 条形图": ("Image/bar_chart_example.png", "条形图示例", "1. 条形图（Bar Chart）"),
    "2. 频率直方图": ("Image/histogram_example.png", "频率直方图示例", "2. 频率直方图（Frequency histogram）"),
    "3. 折线图": ("Image/Line_Chart_Example.png", "折线图示例", "3. 折线图（Line Plot）"),
    "4. 散点图": ("Image/Scatter_Plot_Example.png", "散点图示例", "4. 散点图（Scatter Plot）"),
    "5. 饼图": ("Image/Pie_Chart_Example.png", "饼图示例", "5. 饼图（Pie Chart）"),
    "6. 箱线图": ("Image/Box_Plot_Example.png", "箱线图示例", "6. 箱线图（Box Plot）"),
    "7. 热力图": ("Image/Heatmap_Example.png", "热力图示例", "7. 热力图（Heatmap）"),
    "8. 等高线图": ("Image/Contour_Plot_Example.png", "等高线图示例", "8. 等高线图（Contour Plot）"),
    "9. 3D直方图": ("Image/3D_Bar_Chart_Example.png", "3D直方图示例", "9. 3D直方图（3D Histogram）")
}

st.sidebar.image(chart_images[chart_type][0], caption=chart_images[chart_type][1])


# 提供对应图表类型的Excel模板
templates = {
    "1. 条形图": pd.DataFrame(columns=['Category', 'Value']),
    "2. 频率直方图": pd.DataFrame(columns=['Category', 'X', 'Y']),
    "3. 折线图": pd.DataFrame(columns=['Category', 'X', 'Y']),
    "4. 散点图": pd.DataFrame(columns=['Category', 'X', 'Y']),
    "5. 饼图": pd.DataFrame(columns=['Category', 'Value']),
    "6. 箱线图": pd.DataFrame(columns=['Category', 'Value']),
    "7. 热力图": pd.DataFrame(columns=['X', 'Y', 'Value']),
    "8. 等高线图": pd.DataFrame(columns=['X', 'Y', 'Value']),
    "9. 3D直方图": pd.DataFrame(columns=['Category', 'X', 'Y', 'Z'])
}

excel_template = templates[chart_type]
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    excel_template.to_excel(writer, index=False, sheet_name='Sheet1')
excel_buffer.seek(0)


st.sidebar.markdown('---')
######################################添加个人介绍###############################################################
st.sidebar.title("关于我")

st.sidebar.write("""
大家好，我是阮同学，目前在北京师范大学攻读博士。我平时喜欢编程捣鼓一些有趣的玩意儿。如果你有什么新奇的想法或者对我的作品有什么改进建议，欢迎告诉我！\n商务与学习交流：ruan_bilibili@163.com
""")
profile_image = Image.open("Image/me2.png")  # 替换为你的个人图片路径


# 将图像转换为 base64 编码
buffered = BytesIO()
profile_image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# 使用st.markdown和HTML/CSS显示图像并使其居中
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{img_str}" style="width: 150px; border-radius: 50%;">
    </div>
    """,
    unsafe_allow_html=True
)
######################################添加个人介绍###############################################################
######################################侧边栏####################################################################################






######################################主界面###############################################################

##滚动字幕
# 定义滚动字幕的HTML和CSS
scrolling_text = """
<div style="overflow: hidden; white-space: nowrap;">
  <div style="display: inline-block; padding-left: 100%; animation: scroll-left 30s linear infinite;font-size: 24px;">
    长期接定制化科研作图，联系方式：ruan_bilibili@163.com。
  </div>
</div>

<style>
@keyframes scroll-left {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}
</style>
"""

# 在Streamlit应用中显示滚动字幕
st.markdown(scrolling_text, unsafe_allow_html=True)




# 设置页面标题
st.markdown("<h1 style='white-space: nowrap;'>科研绘图平台（Scientific Drawing Platform）</h1>", unsafe_allow_html=True)
st.subheader(chart_images[chart_type][2])



#st.markdown('---')
st.markdown('<p style="font-size:25px; color:black; font-weight:bold;">批量上传数据</p>',unsafe_allow_html=True)
#批量上传数据
# 使用st.columns将按钮放在同一行
col1, col2 = st.columns(2)

# 表单内容
with col1:
    # 添加文字说明
    st.markdown(
        """
        <div style="width: 150px;">
            <p style="font-size: 12px;">请下载模板，填写好数据，再点击右边->批量上传！--></p>
        </div>
        """, unsafe_allow_html=True
    )
    # 下载Excel模板按钮
    st.download_button(
        label="下载Excel模板",
        data=excel_buffer,
        file_name=f"{chart_type}_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:
    # Excel文件上传按钮
    uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx"])

# 处理上传文件
if uploaded_file is not None:
    uploaded_data = pd.read_excel(uploaded_file)
    if set(uploaded_data.columns) == set(excel_template.columns):
        if 'data' not in st.session_state:
            st.session_state.data = pd.DataFrame()
        st.session_state.data = pd.concat([st.session_state.data, uploaded_data], ignore_index=True)
        st.success("Excel文件上传成功!")
    else:
        st.error("Excel文件的列与模板不匹配，请使用正确的模板格式。")

    st.write("上传的数据:")
    st.dataframe(uploaded_data)








st.markdown('---')
st.markdown('<p style="font-size:25px; color:black; font-weight:bold;">逐个上传数据</p>',unsafe_allow_html=True)
# 初始化数据存储
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Category', 'Value', 'X', 'Y'])

# 重置表单输入
if 'form_reset' not in st.session_state:
    st.session_state.form_reset = False

def reset_form():
    st.session_state.form_reset = True


# 输入表单
with st.form(key='data_form'):
    if chart_type not in ["7. 热力图", "8. 等高线图"]:
        category = st.text_input('类别', '' if st.session_state.form_reset else st.session_state.get('category', ''))
    if chart_type in ["1. 条形图", "2. 频率直方图","5. 饼图", "6. 箱线图"]:
        value = st.number_input('数值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('value', 0.0))
    elif chart_type == "9. 3D直方图":
        x_value = st.number_input('X值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('x_value', 0.0))
        y_value = st.number_input('Y值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('y_value', 0.0))
        z_value = st.number_input('Z值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('z_value', 0.0))
    else:
        x_value = st.number_input('X值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('x_value', 0.0))
        y_value = st.number_input('Y值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('y_value', 0.0))
        if chart_type in ["7. 热力图", "8. 等高线图"]:
            value = st.number_input('数值', min_value=0.0, step=1.0, value=0.0 if st.session_state.form_reset else st.session_state.get('value', 0.0))
    submit = st.form_submit_button(label='添加数据')

    if submit:
        if chart_type in ["1. 条形图", "2. 频率直方图","5. 饼图", "6. 箱线图"]:
            new_data = pd.DataFrame({'Category': [category], 'Value': [value]})
        elif chart_type in ["7. 热力图", "8. 等高线图"]:
            new_data = pd.DataFrame({'X': [x_value], 'Y': [y_value], 'Value': [value]})
        elif chart_type == "9. 3D直方图":
            new_data = pd.DataFrame({'Category': [category], 'X': [x_value], 'Y': [y_value], 'Z': [z_value]})
        else:
            new_data = pd.DataFrame({'Category': [category], 'X': [x_value], 'Y': [y_value]})
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.success(f"数据添加成功: {('Category: ' + category + ' - ' if category else '')}{'Value: ' + str(value) if chart_type in ['1. 条形图',"2. 频率直方图" ,'5. 饼图', '6. 箱线图', '7. 热力图', '8. 等高线图'] else 'X: ' + str(x_value) + ', Y: ' + str(y_value) + (', Z: ' + str(z_value) if chart_type == '9. 3D直方图' else '')}")
        st.session_state.form_reset = False

# 显示当前数据
if not st.session_state.data.empty:
    st.write('当前数据:')
    st.dataframe(st.session_state.data.dropna(axis=1, how='all'))

    # 设置字体路径
    font_path = 'TTF/simsun.ttc'  # 替换为本地字体的路径
    font_prop = FontProperties(fname=font_path)

    # 绘制图表的函数
    def draw_bar_chart(data):
        histogram_title = st.text_input('条形图标题', '条形图')
        x_axis_label = st.text_input('X轴标签', '类别')
        y_axis_label = st.text_input('Y轴标签', '数值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        fig, ax = plt.subplots()
        sns.barplot(data=data.dropna(subset=['Value']), x='Category', y='Value', ax=ax, palette='viridis')
        ax.set_title(histogram_title, fontproperties=font_prop, fontsize=title_size)
        ax.set_xlabel(x_axis_label, fontproperties=font_prop, fontsize=xlabel_size)
        ax.set_ylabel(y_axis_label, fontproperties=font_prop, fontsize=ylabel_size)
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(font_prop)
        
        if add_grid:
            ax.grid(True)
        
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="bar_chart.png", mime="image/png")
            


    def draw_histogram(data):
        title = st.text_input('直方图标题', value='直方图')
        xlabel = st.text_input('X轴标签', value='值')
        ylabel = st.text_input('Y轴标签', value='频率')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')

        plt.figure(figsize=(10, 6))

        # 绘制直方图
        for category in data['Category'].unique():
            subset = data[data['Category'] == category]
            plt.hist(subset=['Value'], bins=20, alpha=0.7, label=category, edgecolor='black')

        plt.title(title, fontproperties=font_prop,fontsize=title_size)
        plt.xlabel(xlabel, fontproperties=font_prop,fontsize=xlabel_size)
        plt.ylabel(ylabel,fontproperties=font_prop, fontsize=ylabel_size)
        plt.legend()
        
        if add_grid:
            plt.grid(True)

        st.pyplot(plt)
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="histogram.png", mime="image/png")


    
    def draw_line_plot(data):
        title = st.text_input('折线图标题', value='折线图')
        xlabel = st.text_input('X轴标签', value='X值')
        ylabel = st.text_input('Y轴标签', value='Y值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        plt.figure(figsize=(10, 6))
        categories = data['Category'].unique()
        
        for category in categories:
            subset = data[data['Category'] == category]
            plt.plot(subset['X'], subset['Y'], marker='o', label=category)
        
        plt.title(title, fontproperties=font_prop, fontsize=title_size)
        plt.xlabel(xlabel, fontproperties=font_prop, fontsize=xlabel_size)
        plt.ylabel(ylabel, fontproperties=font_prop, fontsize=ylabel_size)
        plt.legend(prop=font_prop)
        
        if add_grid:
            plt.grid(True)
        
        st.pyplot(plt)
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="line_plot.png", mime="image/png")
    
    def draw_scatter_plot(data):
        title = st.text_input('散点图标题', value='散点图')
        xlabel = st.text_input('X轴标签', value='X值')
        ylabel = st.text_input('Y轴标签', value='Y值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        plt.figure(figsize=(10, 6))
        categories = data['Category'].unique()
        
        for category in categories:
            subset = data[data['Category'] == category]
            plt.scatter(subset['X'], subset['Y'], label=category)
        
        plt.title(title, fontproperties=font_prop, fontsize=title_size)
        plt.xlabel(xlabel, fontproperties=font_prop, fontsize=xlabel_size)
        plt.ylabel(ylabel, fontproperties=font_prop, fontsize=ylabel_size)
        plt.legend(prop=font_prop)
        
        if add_grid:
            plt.grid(True)
        
        st.pyplot(plt)
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="scatter_plot.png", mime="image/png")
    
    def draw_pie_chart(data):
        title = st.text_input('饼图标题', value='饼图')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        
        fig, ax = plt.subplots()
        data = data.dropna(subset=['Value'])
        ax.pie(data['Value'], labels=data['Category'], autopct='%1.1f%%', startangle=90, textprops={'fontproperties': font_prop})
        ax.set_title(title, fontproperties=font_prop, fontsize=title_size)
        
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="pie_chart.png", mime="image/png")
    
    def draw_box_plot(data):
        title = st.text_input('箱线图标题', value='箱线图')
        x_axis_label = st.text_input('X轴标签', '类别')
        y_axis_label = st.text_input('Y轴标签', '数值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        fig, ax = plt.subplots()
        sns.boxplot(data=data.dropna(subset=['Value']), x='Category', y='Value', ax=ax, palette='viridis')
        ax.set_title(title, fontproperties=font_prop, fontsize=title_size)
        ax.set_xlabel(x_axis_label, fontproperties=font_prop, fontsize=xlabel_size)
        ax.set_ylabel(y_axis_label, fontproperties=font_prop, fontsize=ylabel_size)
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(font_prop)
        
        if add_grid:
            ax.grid(True)
        
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(label="下载图像", data=buf, file_name="box_plot.png", mime="image/png")
    
    def draw_heatmap(data):
        title = st.text_input('热力图标题', value='热力图')
        x_axis_label = st.text_input('X轴标签', 'X值')
        y_axis_label = st.text_input('Y轴标签', 'Y值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        fig, ax = plt.subplots()
        try:
            heatmap_data = data.pivot_table(index='Y', columns='X', values='Value', fill_value=0)
            sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="viridis", ax=ax)
            ax.set_title(title, fontproperties=font_prop, fontsize=title_size)
            ax.set_xlabel(x_axis_label, fontproperties=font_prop, fontsize=xlabel_size)
            ax.set_ylabel(y_axis_label, fontproperties=font_prop, fontsize=ylabel_size)
            
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties(font_prop)
            
            if add_grid:
                ax.grid(True)
            
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(label="下载图像", data=buf, file_name="heatmap.png", mime="image/png")
        except ValueError as e:
            st.error(f"数据格式不正确: {e}")
    
    def draw_contour_plot(data):
        title = st.text_input('等高线图标题', value='等高线图')
        x_axis_label = st.text_input('X轴标签', 'X值')
        y_axis_label = st.text_input('Y轴标签', 'Y值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')
        
        fig, ax = plt.subplots()
        try:
            contour_data = data.pivot_table(index='Y', columns='X', values='Value', fill_value=0)
            if contour_data.shape[0] > 1 and contour_data.shape[1] > 1:
                X, Y = np.meshgrid(contour_data.columns, contour_data.index)
                Z = contour_data.values
                ax.contour(X, Y, Z, cmap='viridis')
                ax.set_title(title, fontproperties=font_prop, fontsize=title_size)
                ax.set_xlabel(x_axis_label, fontproperties=font_prop, fontsize=xlabel_size)
                ax.set_ylabel(y_axis_label, fontproperties=font_prop, fontsize=ylabel_size)

                for label in ax.get_xticklabels() + ax.get_yticklabels():
                    label.set_fontproperties(font_prop)

                if add_grid:
                    ax.grid(True)

                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.download_button(label="下载图像", data=buf, file_name="contour_plot.png", mime="image/png")
            else:
                st.error("数据点不足，无法绘制等高线图。请添加更多数据点。")
        except ValueError as e:
            st.error(f"数据格式不正确: {e}")
    
    def draw_3d_histogram(data):
        title = st.text_input('3D直方图标题', value='3D直方图')
        xlabel = st.text_input('X轴标签', value='X值')
        ylabel = st.text_input('Y轴标签', value='Y值')
        zlabel = st.text_input('Z轴标签', value='Z值')
        title_size = st.slider('标题字体大小', 10, 40, 20)
        xlabel_size = st.slider('X轴标签字体大小', 10, 40, 15)
        ylabel_size = st.slider('Y轴标签字体大小', 10, 40, 15)
        zlabel_size = st.slider('Z轴标签字体大小', 10, 40, 15)
        add_grid = st.checkbox('添加辅助线')

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        try:
            categories = data['Category'].unique()
            colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
            for category, color in zip(categories, colors):
                subset = data[data['Category'] == category]
                x = subset['X']
                y = subset['Y']
                z = np.zeros(len(subset))
                dx = dy = 0.5
                dz = subset['Z']
                ax.bar3d(x, y, z, dx, dy, dz, color=color, alpha=0.7, edgecolor='black', label=category)

            ax.set_title(title, fontproperties=font_prop, fontsize=title_size)
            ax.set_xlabel(xlabel, fontproperties=font_prop, fontsize=xlabel_size)
            ax.set_ylabel(ylabel, fontproperties=font_prop, fontsize=ylabel_size)
            ax.set_zlabel(zlabel, fontproperties=font_prop, fontsize=zlabel_size)
            ax.legend(prop=font_prop)

            for label in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
                label.set_fontproperties(font_prop)

            if add_grid:
                ax.grid(True)

            st.pyplot(fig)

            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(label="下载图像", data=buf, file_name="3d_histogram.png", mime="image/png")
        except ValueError as e:
            st.error(f"数据格式不正确: {e}")

    # 图表绘制函数字典
    chart_functions = {
        "1. 条形图": draw_bar_chart,
        "2. 频率直方图": draw_histogram,
        "3. 折线图": draw_line_plot,
        "4. 散点图": draw_scatter_plot,
        "5. 饼图": draw_pie_chart,
        "6. 箱线图": draw_box_plot,
        "7. 热力图": draw_heatmap,
        "8. 等高线图": draw_contour_plot,
        "9. 3D直方图": draw_3d_histogram
    }
    
    # 调用对应的绘制函数
    if chart_type in chart_functions:
        chart_functions[chart_type](st.session_state.data)
else:
    st.warning('尚未添加数据')

# 重置按钮
# 使用st.button创建一个按钮
if st.button('刷新页面（重新画请点这里！）'):
    # 使用st.markdown插入JavaScript代码
    st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
