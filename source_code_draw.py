import tkinter as tk
from tkinter import messagebox, colorchooser
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# 放大75%的字体大小
LARGE_FONT = ("Verdana", 12)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def draw_line_chart(title, x_label, y_label, data, show_data_labels):
    plt.clf()  # 清空当前的绘图区域

    for i, dataset in enumerate(data):
        x_data = dataset['x']
        y_data = dataset['y']
        label = dataset['label'] if 'label' in dataset else None
        color = dataset['color'] if dataset['color'] else 'blue'
        plt.plot(x_data, y_data, marker='o', label=label, color=color)
        if show_data_labels:
            for x, y in zip(x_data, y_data):
                plt.text(x, y, f'({x}, {y})', fontsize=8, ha='right')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig('line_chart.png')
    plt.show()
    messagebox.showinfo("提示", f"折线图已保存为 line_chart.png")

def draw_regression_line(title, x_label, y_label, data, show_data_labels):
    plt.clf()  # 清空当前的绘图区域

    for i, dataset in enumerate(data):
        x_data = dataset['x']
        y_data = dataset['y']
        color = dataset['color'] if dataset['color'] else 'red'
        # Plot data points
        plt.scatter(x_data, y_data, color=color, label=dataset.get('label', None))

        # Perform linear regression
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        coeffs = np.polyfit(x_data, y_data, 1)
        regression_line = np.polyval(coeffs, x_data)

        # Plot regression line with user-defined label
        label = dataset.get('label', None)
        if label:
            plt.plot(x_data, regression_line, linestyle='--', color=color, label=label)
        else:
            plt.plot(x_data, regression_line, linestyle='--', color=color)
        
        if show_data_labels:
            for x, y in zip(x_data, y_data):
                plt.text(x, y, f'({x}, {y})', fontsize=8, ha='right')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    # Only call legend if there are labels present
    if any(dataset.get('label', None) for dataset in data) and show_data_labels:
        plt.legend()
    plt.grid(True)
    plt.savefig('regression_line_chart.png')
    plt.show()
    messagebox.showinfo("提示", f"回归线图已保存为 regression_line_chart.png")

def draw_smooth_curve(title, x_label, y_label, data, show_data_labels):
    plt.clf()  # 清空当前的绘图区域

    for i, dataset in enumerate(data):
        x_data = dataset['x']
        y_data = dataset['y']
        color = dataset['color'] if dataset['color'] else 'green'
        # Ensure x_data is strictly increasing
        sorted_indices = np.argsort(x_data)
        x_data = np.array(x_data)[sorted_indices]
        y_data = np.array(y_data)[sorted_indices]

        # Use spline interpolation for smooth curve
        x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
        spl = make_interp_spline(x_data, y_data, k=3, bc_type='natural')
        y_smooth = spl(x_smooth)

        # Plot smooth curve with user-defined label
        plt.plot(x_smooth, y_smooth, linestyle='-', color=color, label=dataset.get('label', None))
        if show_data_labels:
            for x, y in zip(x_data, y_data):
                plt.text(x, y, f'({x}, {y})', fontsize=8, ha='right')
        
        # Plot data points
        if show_data_labels:
            plt.scatter(x_data, y_data, color=color, label=None)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if show_data_labels:
        plt.legend()
    plt.grid(True)
    plt.savefig('smooth_curve_chart.png')
    plt.show()
    messagebox.showinfo("提示", f"平滑曲线图已保存为 smooth_curve_chart.png")

class DataPoint:
    def __init__(self, parent_frame, index, dataset):
        self.frame = tk.Frame(parent_frame)
        self.frame.pack(fill='x', padx=10, pady=5)  # 修改 pady 为 10，使得表格垂直居中
        self.dataset = dataset  # 保存数据集对象的引用

        self.x_label = tk.Label(self.frame, text="X:", font=LARGE_FONT)
        self.x_label.pack(side='left', padx=(10, 5))

        self.x_entry = tk.Entry(self.frame, width=8)
        self.x_entry.pack(side='left', padx=(0, 5))

        self.y_label = tk.Label(self.frame, text="Y:", font=LARGE_FONT)
        self.y_label.pack(side='left', padx=(0, 5))

        self.y_entry = tk.Entry(self.frame, width=8)
        self.y_entry.pack(side='left', padx=(0, 5))

        self.delete_button = tk.Button(self.frame, text="删除", command=self.delete, font=LARGE_FONT)
        self.delete_button.pack(side='left', padx=(0, 10))

    def delete(self):
        self.frame.destroy()  # 销毁数据点的整个框架，包括内部的小部件
        self.dataset.remove_data_point(self)  # 通知数据集对象移除该数据点


class Dataset:
    def __init__(self, parent_frame, index):
        self.frame = tk.Frame(parent_frame)
        self.frame.pack(fill='x', padx=10, pady=5)  # 修改 pady 为 10，使得表格垂直居中

        self.label_label = tk.Label(self.frame, text="标签:", font=LARGE_FONT)
        self.label_label.pack(side='left', padx=(10, 5))

        self.label_entry = tk.Entry(self.frame)
        self.label_entry.pack(side='left', padx=(0, 5))
        self.label_entry.insert(tk.END, f"数据集 {index}")

        self.color_label = tk.Label(self.frame, text="颜色:", font=LARGE_FONT)
        self.color_label.pack(side='left', padx=(0, 5))

        self.color_button = tk.Button(self.frame, text="选择颜色", command=self.choose_color, font=LARGE_FONT)
        self.color_button.pack(side='left', padx=(0, 5))

        self.add_point_button = tk.Button(self.frame, text="添加数据点", command=self.add_data_point, font=LARGE_FONT)
        self.add_point_button.pack(side='left', padx=(0, 5))

        self.delete_button = tk.Button(self.frame, text="删除数据组", command=self.delete, font=LARGE_FONT)
        self.delete_button.pack(side='left', padx=(0, 10))

        self.data_points_frame = tk.Frame(parent_frame)
        self.data_points_frame.pack(fill='x', padx=10, pady=5)

        self.data_points = []
        self.color = None

    def add_data_point(self):
        data_point = DataPoint(self.data_points_frame, len(self.data_points) + 1, self)
        self.data_points.append(data_point)

    def remove_data_point(self, data_point):
        self.data_points.remove(data_point)

    def delete(self):
        # 提取标签值
        label_value = self.label_entry.get()
        # 销毁数据组及其相关部件
        self.frame.destroy()
        self.data_points_frame.destroy()
        # 返回标签值
        return label_value

    def choose_color(self):
        color = colorchooser.askcolor()[1]  # Open color chooser dialog and get the chosen color
        if color:
            self.color = color


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("公众号:T宇奇说话")
        self.geometry("1024x576")  # 设置窗口大小

        self.title_label = tk.Label(self, text="图表标题:", font=LARGE_FONT)
        self.title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self, font=LARGE_FONT)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.data_labels_var = tk.BooleanVar()
        self.data_labels_check = tk.Checkbutton(self, text="显示数据点标签", variable=self.data_labels_var, font=LARGE_FONT)
        self.data_labels_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.chart_type_label = tk.Label(self, text="图表类型:", font=LARGE_FONT)
        self.chart_type_label.grid(row=2, column=0, padx=5, pady=5)

        self.chart_type_options = {"折线图": "1", "回归线图": "2", "平滑曲线图": "3"}
        self.chart_type_var = tk.StringVar()
        self.chart_type_var.set(list(self.chart_type_options.keys())[0])  # 设置默认选项

        self.chart_type_dropdown = tk.OptionMenu(self, self.chart_type_var, *self.chart_type_options.keys())
        self.chart_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.x_label_label = tk.Label(self, text="横坐标名称:", font=LARGE_FONT)
        self.x_label_label.grid(row=3, column=0, padx=5, pady=5)
        self.x_label_entry = tk.Entry(self, font=LARGE_FONT)
        self.x_label_entry.grid(row=3, column=1, padx=5, pady=5)

        self.y_label_label = tk.Label(self, text="纵坐标名称:", font=LARGE_FONT)
        self.y_label_label.grid(row=4, column=0, padx=5, pady=5)
        self.y_label_entry = tk.Entry(self, font=LARGE_FONT)
        self.y_label_entry.grid(row=4, column=1, padx=5, pady=5)

        self.dataset_container = tk.Frame(self)
        self.dataset_container.grid(row=6, column=0, columnspan=2, pady=5)

        self.add_dataset_button = tk.Button(self, text="添加数据组", command=self.add_dataset, font=LARGE_FONT)
        self.add_dataset_button.grid(row=7, column=0, pady=5)

        self.draw_button = tk.Button(self, text="绘制图表", command=self.draw_chart, font=LARGE_FONT)
        self.draw_button.grid(row=7, column=1, pady=5)

        self.datasets = []

    def add_dataset(self):
        dataset = Dataset(self.dataset_container, len(self.datasets) + 1)
        self.datasets.append(dataset)

    def draw_chart(self):
        title = self.title_entry.get()
        show_data_labels = self.data_labels_var.get()

        chart_type = self.chart_type_options[self.chart_type_var.get()]
        x_label = self.x_label_entry.get()
        y_label = self.y_label_entry.get()

        data = []
        deleted_labels = []
        for dataset in self.datasets:
            label = dataset.label_entry.get()
            color = dataset.color
            x_data = []
            y_data = []
            for data_point in dataset.data_points:
                x = data_point.x_entry.get()
                y = data_point.y_entry.get()
                if x and y:
                    x_data.append(float(x))
                    y_data.append(float(y))
            if x_data and y_data:
                data.append({'x': x_data, 'y': y_data, 'label': label, 'color': color})
            else:
                deleted_labels.append(label)

        for label in deleted_labels:
            messagebox.showerror("错误", f"数据集 '{label}' 不完整，请补充数据点后再绘制图表。")

        if chart_type == '1':
            draw_line_chart(title, x_label, y_label, data, show_data_labels)
        elif chart_type == '2':
            draw_regression_line(title, x_label, y_label, data, show_data_labels)
        elif chart_type == '3':
            draw_smooth_curve(title, x_label, y_label, data, show_data_labels)
        else:
            messagebox.showerror("错误", "无效的图表类型")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
