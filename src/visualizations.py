import json
import pandas as pd
import numpy as np
import plotly.express as px
from pprint import pprint


def main():
    # append data folder path
    # import sys

    # JSON file
    filename = "src\data\profiler_data.json"
    file = open(filename, "r")
    
    # Reading from file
    data = json.loads(file.read())
    pprint(data)

    generated_elements = []
    for function in data:
        generated_elements.append(function)

    print(generated_elements)

    def create_iterative_bar_chart(function, query_type, framework, iter_or_cmlt):
        fig = px.bar(x=list(range(1,len(data[function][query_type])+1)), y=data[function][query_type])
        
        # draw average line
        average = np.sum(data[function][query_type]) / (len(data[function][query_type]))

        fig.add_shape(type='line',
                        x0=0,
                        y0=average,
                        x1=100,
                        y1=average,
                        line=dict(color='Red'))
        
        # modify axis label properties
        fig.update_layout(title=f"{function} {framework} Query Performance ({iter_or_cmlt})", xaxis_title="Query Number", yaxis_title="Time (in Seconds)")
        fig.update_xaxes(title_font={"size":18, "family": "Courier", "color":"gray"}, 
                        tickfont = {"size":16, "family": "Courier", "color":"gray"})
        fig.update_yaxes(title_font={"size":18, "family": "Courier", "color":"gray"}, 
                                    tickfont = {"size":16, "family": "Courier New, monospace", "color":"gray"})

        fig.show()
        
    def create_iterative_line_chart(function, query_type, framework, iter_or_cmlt):
        fig = px.line(x=list(range(1,len(data[function][query_type])+1)), y=data[function][query_type])
        
        # draw average line
        average = np.sum(data[function][query_type]) / (len(data[function][query_type]))

        fig.add_shape(type='line',
                        x0=0,
                        y0=average,
                        x1=100,
                        y1=average,
                        line=dict(color='Red'))
        
        # modify axis label properties
        fig.update_layout(title=f"{function} {framework} Query Performance ({iter_or_cmlt})", xaxis_title="Query Number", yaxis_title="Time (in Seconds)", legend_title="Legend Title")
        fig.update_xaxes(title_font={"size":18, "family": "Courier", "color":"gray"}, 
                        tickfont = {"size":16, "family": "Courier", "color":"gray"})
        fig.update_yaxes(title_font={"size":18, "family": "Courier", "color":"gray"}, 
                                    tickfont = {"size":16, "family": "Courier New, monospace", "color":"gray"})


        fig.update_traces(mode = "lines+markers")
        fig.show()
        
    # create iterative line charts
    for function in generated_elements:
        create_iterative_line_chart(function, "spark_i", "Spark", "Iterative")
    for function in generated_elements:
        create_iterative_line_chart(function, "mongo_i", "Mongo", "Iterative")

    # create cumulative line charts
    for function in generated_elements:
        create_iterative_line_chart(function, "mongo_c", "Mongo", "Cummulative")
    for function in generated_elements:
        create_iterative_line_chart(function, "spark_c", "Spark", "Cummulative")
        
    # create iterative bar graphs
    for function in generated_elements:
        create_iterative_bar_chart(function, "mongo_i", "Mongo", "Iterative")
    for function in generated_elements:
        create_iterative_bar_chart(function, "spark_i", "Spark", "Iterative")
        
        

    # compile query data
    query_type = []
    framework = []
    times = []
    functions = []

    for function in data:
        for name in data[function]:
            for time in data[function][name]:
                if name == "mongo_c":
                        functions.append(function)
                        query_type.append("mongo_cummulative_time")
                        framework.append("mongo")
                        times.append(time)
                elif name == "mongo_i":
                        functions.append(function)
                        query_type.append("mongo_iterative_time")
                        framework.append("mongo")
                        times.append(time)
                elif name == "spark_c":
                        functions.append(function)
                        query_type.append("spark_cummulative_time")
                        framework.append("spark")
                        times.append(time)
                elif name == "spark_i":
                        functions.append(function)
                        query_type.append("spark_iterative_time")
                        framework.append("spark")
                        times.append(time)

    # check entry sizes
    print("Mongo Cummulative Entries: ", query_type.count("mongo_cummulative_time"))
    print("Mongo Iterative Entries: ", query_type.count("mongo_iterative_time"))
    print("Spark Cummulative Entries: ", query_type.count("spark_cummulative_time"))
    print("Spark Iterative Entries: ", query_type.count("spark_iterative_time"))

    # check data
    create_df = {"Function":functions,
            "Framework":framework,
            "Query Type": query_type,
            "Performance Time": times}

    df = pd.DataFrame(create_df)
    iterative_df = df[(df["Query Type"] == "mongo_iterative_time") | (df["Query Type"] == "spark_iterative_time")]


    # create bar graphs
    fig = px.bar(iterative_df, x="Function", y="Performance Time", color="Framework", barmode="group")
    # modify axis label properties
    fig.update_layout(title="Iterative Query Performances", xaxis_title="Function", yaxis_title="Time (in Seconds)", legend_title="Framework")
    fig.update_xaxes(title_font={"size":18, "family": "Courier", "color":"black"}, 
                    tickfont = {"size":16, "family": "Courier", "color":"black"})
    fig.update_yaxes(title_font={"size":18, "family": "Courier", "color":"black"}, 
                                tickfont = {"size":16, "family": "Courier New, monospace", "color":"black"})
    fig.show()

    cummulative_df = df[(df["Query Type"] == "mongo_cummulative_time") | (df["Query Type"] == "spark_cummulative_time")]

    fig = px.bar(cummulative_df, x="Function", y="Performance Time", color="Framework", barmode="group", color_discrete_sequence=px.colors.qualitative.D3)
    # modify axis label properties
    fig.update_layout(title="Cummulative Query Performances", xaxis_title="Function", yaxis_title="Time (in Seconds)", legend_title="Framework")
    fig.update_xaxes(title_font={"size":18, "family": "Courier", "color":"black"}, 
                    tickfont = {"size":16, "family": "Courier", "color":"black"})
    fig.update_yaxes(title_font={"size":18, "family": "Courier", "color":"black"}, 
                                tickfont = {"size":16, "family": "Courier New, monospace", "color":"black"})
    fig.show()

    fig = px.scatter(iterative_df, x="Function", y="Performance Time", color="Framework",
                    facet_col='Query Type', facet_col_wrap=4)
    fig.show()
    
if __name__ == "__main__":
    main()