import matplotlib.pyplot as plt

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def Plot(parentFrame, plot, time, title):
    # Matplotlib 창 생성
    figure = plt.figure(figsize=(9, 2), dpi=100)
    axes = figure.add_subplot(111)
    
    if title == '강수확률':
        axes.set_ylim(0, 100)
    axes.set_title(title)
    axes.plot(time, plot)
    axes.fill_between(time, plot, color='skyblue', alpha=0.4)

    figure.tight_layout()
    # Matplotlib 그래프를 Tkinter 앱에 추가하기
    canvas = FigureCanvasTkAgg(figure, master=parentFrame)
    canvas.draw()

    return canvas.get_tk_widget()