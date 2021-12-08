import matplotlib.pyplot as plt
from io import StringIO


# Funciones que retornan la grafica en forma de String
def return_graphBar(df, x, y):
    fig = plt.figure()
    plt.bar(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graphScatter(df, x, y, label, labels):
    fig = plt.figure()
    print(labels)
    if len(labels)!=0:
        for i in labels:
            x1 = df[x].where(df[label] == i)
            y1 = df[y].where(df[label] == i)
            plt.scatter(x1, y1, label=str(i))
        plt.legend()
    else:
        x1 = df[x]
        y1 = df[y]
        plt.scatter(x1, y1)
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graphHist(df, x, label, labels):
    fig = plt.figure()
    if len(labels)!=0:
        for i in labels:
            x1 = df[x].where(df[label] == i)
            print(str(i))
            plt.hist(x1, label=str(i))
    else:
        plt.hist(df[x])
    plt.ylabel("Frequencia")
    plt.xlabel(x)
    plt.legend()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data
