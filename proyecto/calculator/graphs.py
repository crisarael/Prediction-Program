import matplotlib.pyplot as plt
from io import StringIO


def return_graphBar(x, label):
    fig = plt.figure()
    plt.bar(x, label)
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graphScatter(df, x, y, label, labels):
    fig = plt.figure()
    if labels:
        for i in labels:
            x1 = df[x].where(df[label] == i)
            y1 = df[y].where(df[label] == i)
            plt.scatter(x1, y1, label=i)
    else:
        x1 = df[x]
        y1 = df[y]
        plt.scatter(x1, y1)
    plt.legend()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graphHist(df, x, label, labels):
    fig = plt.figure()
    if labels:
        for i in labels:
            x1 = df[x].where(df[label] == i)
            plt.hist(x1, label=i)
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
