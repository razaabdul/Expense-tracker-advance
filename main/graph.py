import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

def get_graph():
    # Create a new figure and plot some data
    fig = plt.subplots()
    
    x = np.linspace(0,5,11)
    # y  = x ** 2
    # x = [1, 2, 3, 4, 5]
    # y = [2, 3, 5, 7, 11]
    plt.plot(x, x**2.5, label = 'incomes',color='blue',linewidth = 2,linestyle = '--')
    plt.plot(x, x**2 , label = 'expenses',color='red')
   

    # Save the figure to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return string.decode('utf-8')