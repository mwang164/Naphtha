from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server
xls_file = pd.ExcelFile("month spreads.xlsx")

# Extract data from the "MOPJ" sheet
MOPJdf = xls_file.parse("MOPJ", header=1)
MOPJdf = MOPJdf.dropna()
MOPJdf['Date'] = pd.to_datetime(MOPJdf['Date'])
MOPJdf.set_index('Date', inplace=True)

# Extract data from the "NWE" sheet
NWEdf = xls_file.parse("NWE", header=1)
NWEdf = NWEdf.dropna()
NWEdf['Date'] = pd.to_datetime(NWEdf['Date'])
NWEdf.set_index('Date', inplace=True)
# Read FEI
FEIdf = xls_file.parse("FEI", header=1)
FEIdf = FEIdf.dropna()
FEIdf['Date'] = pd.to_datetime(FEIdf['Date'])
FEIdf.set_index('Date', inplace=True)
# Read R92
R92df = xls_file.parse("R92", header=1)
R92df = R92df.dropna()
R92df['Date'] = pd.to_datetime(R92df['Date'])
R92df.set_index('Date', inplace=True)
# Read EBOB
EBOBdf = xls_file.parse("EBOB", header=1)
EBOBdf = EBOBdf.dropna()
EBOBdf['Date'] = pd.to_datetime(EBOBdf['Date'])
EBOBdf.set_index('Date', inplace=True)
# Read NWEC3
NWEC3df = xls_file.parse("NWEC3", header=1)
NWEC3df = NWEC3df.dropna()
NWEC3df['Date'] = pd.to_datetime(NWEC3df['Date'])
NWEC3df.set_index('Date', inplace=True)
# Read MOPJCRK
MOPJCRKdf = xls_file.parse("MOPJCRK", header=1)
MOPJCRKdf = MOPJCRKdf.dropna()
MOPJCRKdf['Date'] = pd.to_datetime(MOPJCRKdf['Date'])
MOPJCRKdf.set_index('Date', inplace=True)
# Read NWECRK
NWECRKdf = xls_file.parse("NWECRK", header=1)
NWECRKdf = NWECRKdf.dropna()
NWECRKdf['Date'] = pd.to_datetime(NWECRKdf['Date'])
NWECRKdf.set_index('Date', inplace=True)
# Read R92CRK
R92CRKdf = xls_file.parse("R92CRK", header=1)
R92CRKdf = R92CRKdf.dropna()
R92CRKdf['Date'] = pd.to_datetime(R92CRKdf['Date'])
R92CRKdf.set_index('Date', inplace=True)
# Read EBOBCRK
EBOBCRKdf = xls_file.parse("EBOBCRK", header=1)
EBOBCRKdf = EBOBCRKdf.dropna()
EBOBCRKdf['Date'] = pd.to_datetime(EBOBCRKdf['Date'])
EBOBCRKdf.set_index('Date', inplace=True)
# Read EW
EWdf = xls_file.parse("EW", header=1)
EWdf = EWdf.dropna()
EWdf['Date'] = pd.to_datetime(EWdf['Date'])
EWdf.set_index('Date', inplace=True)
# Read R92MOPJ
R92MOPJdf = xls_file.parse("R92MOPJ", header=1)
R92MOPJdf = R92MOPJdf.dropna()
R92MOPJdf['Date'] = pd.to_datetime(R92MOPJdf['Date'])
R92MOPJdf.set_index('Date', inplace=True)
# Read EBOBNWE
EBOBNWEdf = xls_file.parse("EBOBNWE", header=1)
EBOBNWEdf = EBOBNWEdf.dropna()
EBOBNWEdf['Date'] = pd.to_datetime(EBOBNWEdf['Date'])
EBOBNWEdf.set_index('Date', inplace=True)
# Read FEIMOPJ
FEIMOPJdf = xls_file.parse("FEIMOPJ", header=1)
FEIMOPJdf = FEIMOPJdf.dropna()
FEIMOPJdf['Date'] = pd.to_datetime(FEIMOPJdf['Date'])
FEIMOPJdf.set_index('Date', inplace=True)
# Read NWEC3NAP
NWEC3NAPdf = xls_file.parse("NWEC3NAP", header=1)
NWEC3NAPdf = NWEC3NAPdf.dropna()
NWEC3NAPdf['Date'] = pd.to_datetime(NWEC3NAPdf['Date'])
NWEC3NAPdf.set_index('Date', inplace=True)
# Read BRT
BRTdf = xls_file.parse("BRT", header=1)
BRTdf = BRTdf.dropna()
BRTdf['Date'] = pd.to_datetime(BRTdf['Date'])
BRTdf.set_index('Date', inplace=True)

color_map = {
    2018: "#4472C4",
    2019: "#ED7D31",
    2020: "#A5A5A5",
    2021: "#FFC000",
    2022: "#70AD47",
    2023: "#C76257",
    2024: "#FD03FF"
}


# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 51) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# MOPJ Charts
# Create an empty list to store all the figures
MOPJfigures = []

# Loop through each column (excluding the 'Date' column)
for column in MOPJdf.columns:
    fig = px.line(
        MOPJdf.assign(
            year=MOPJdf.index.year,
            date=pd.to_datetime(MOPJdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=MOPJdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-10, 22], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="MOPJ " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    MOPJfigures.append(fig)


# NWE Charts
# Create an empty list to store all the figures
NWEfigures = []

# Loop through each column (excluding the 'Date' column)
for column in NWEdf.columns:
    fig = px.line(
        NWEdf.assign(
            year=NWEdf.index.year,
            date=pd.to_datetime(NWEdf.index.day_of_year.values + (2021 * 1000), format="%Y%j"),
            value=NWEdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-10, 22], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": "%b-%d"},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="NWE " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    NWEfigures.append(fig)

# FEI Charts
# Set the major unit for the y-axis
major_unit = 4

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 51) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
FEIfigures = []

# Loop through each column (excluding the 'Date' column)
for column in FEIdf.columns:
    fig = px.line(
        FEIdf.assign(
            year=FEIdf.index.year,
            date=pd.to_datetime(FEIdf.index.day_of_year.values + (2021 * 1000), format="%Y%j"),
            value=FEIdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-20, 50], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="FEI " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    FEIfigures.append(fig)


#R92 Charts
# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 51) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
R92figures = []

# Loop through each column (excluding the 'Date' column)
for column in R92df.columns:
    fig = px.line(
        R92df.assign(
            year=R92df.index.year,
            date=pd.to_datetime(R92df.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=R92df[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-10, 22], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="R92 " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    R92figures.append(fig)

# EBOB Charts
# Set the major unit for the y-axis
major_unit = 4

# Calculate tick positions and labels
tick_positions = [i for i in range(-80, 101) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
EBOBfigures = []

# Loop through each column (excluding the 'Date' column)
for column in EBOBdf.columns:
    fig = px.line(
        EBOBdf.assign(
            year=EBOBdf.index.year,
            date=pd.to_datetime(EBOBdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=EBOBdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")


    fig.update_yaxes(range=[-20, 32], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="EBOB " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    EBOBfigures.append(fig)

# NWEC3 Charts
# Set the major unit for the y-axis
major_unit = 4

# Calculate tick positions and labels
tick_positions = [i for i in range(-80, 101) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
NWEC3figures = []

# Loop through each column (excluding the 'Date' column)
for column in NWEC3df.columns:
    fig = px.line(
        NWEC3df.assign(
            year=NWEC3df.index.year,
            date=pd.to_datetime(NWEC3df.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=NWEC3df[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-20, 32], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="NWEC3 " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    NWEC3figures.append(fig)

# MOPJCRK Charts
# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 13) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
MOPJCRKfigures = []

# Loop through each column (excluding the 'Date' column)
for column in MOPJCRKdf.columns:
    fig = px.line(
        MOPJCRKdf.assign(
            year=MOPJCRKdf.index.year,
            date=pd.to_datetime(MOPJCRKdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=MOPJCRKdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-20, 12], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="MOPJCRK " + column + " $/bbl",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    MOPJCRKfigures.append(fig)

# NWECRK Charts
# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 13) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
NWECRKfigures = []

# Loop through each column (excluding the 'Date' column)
for column in NWECRKdf.columns:
    fig = px.line(
        NWECRKdf.assign(
            year=NWECRKdf.index.year,
            date=pd.to_datetime(NWECRKdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=NWECRKdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-20, 12], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="NWE Naphtha CRK " + column + " $/bbl",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    NWECRKfigures.append(fig)

# R92CRK Charts
# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 25) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
R92CRKfigures = []

# Loop through each column (excluding the 'Date' column)
for column in R92CRKdf.columns:
    fig = px.line(
        R92CRKdf.assign(
            year=R92CRKdf.index.year,
            date=pd.to_datetime(R92CRKdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=R92CRKdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-10, 20], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="R92 Crk " + column + " $/bbl",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    R92CRKfigures.append(fig)

# EBOBCRK Charts
# Set the major unit for the y-axis
major_unit = 2

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 41) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
EBOBCRKfigures = []

# Loop through each column (excluding the 'Date' column)
for column in EBOBCRKdf.columns:
    fig = px.line(
        EBOBCRKdf.assign(
            year=EBOBCRKdf.index.year,
            date=pd.to_datetime(EBOBCRKdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=EBOBCRKdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-10, 20], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="EBOB CRK " + column + " $/bbl",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    EBOBCRKfigures.append(fig)

# EW Charts
# Set the major unit for the y-axis
major_unit = 4

# Calculate tick positions and labels
tick_positions = [i for i in range(-80, 101) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
EWfigures = []

# Loop through each column (excluding the 'Date' column)
for column in EWdf.columns:
    fig = px.line(
        EWdf.assign(
            year=EWdf.index.year,
            date=pd.to_datetime(EWdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=EWdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-12, 32], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="EW " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    EWfigures.append(fig)

# R92MOPJ Charts
# Set the major unit for the y-axis
major_unit = 20

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 201) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
R92MOPJfigures = []

# Loop through each column (excluding the 'Date' column)
for column in R92MOPJdf.columns:
    fig = px.line(
        R92MOPJdf.assign(
            year=R92MOPJdf.index.year,
            date=pd.to_datetime(R92MOPJdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=R92MOPJdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-20, 180], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="R92/MOPJ " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    R92MOPJfigures.append(fig)

# EBOBNWE Charts
# Set the major unit for the y-axis
major_unit = 20

# Calculate tick positions and labels
tick_positions = [i for i in range(-20, 201) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
EBOBNWEfigures = []

# Loop through each column (excluding the 'Date' column)
for column in EBOBNWEdf.columns:
    fig = px.line(
        EBOBNWEdf.assign(
            year=EBOBNWEdf.index.year,
            date=pd.to_datetime(EBOBNWEdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=EBOBNWEdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")
    
    fig.update_yaxes(range=[-20, 220], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="EBOB/NWE Naphtha " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    EBOBNWEfigures.append(fig)

# FEIMOPJ Charts
# Set the major unit for the y-axis
major_unit = 20

# Calculate tick positions and labels
tick_positions = [i for i in range(-140, 161) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
FEIMOPJfigures = []

# Loop through each column (excluding the 'Date' column)
for column in FEIMOPJdf.columns:
    fig = px.line(
        FEIMOPJdf.assign(
            year=FEIMOPJdf.index.year,
            date=pd.to_datetime(FEIMOPJdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=FEIMOPJdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-140, 140], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="FEI/MOPJ " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    FEIMOPJfigures.append(fig)

# NWEC3NAP Charts
# Set the major unit for the y-axis
major_unit = 20

# Calculate tick positions and labels
tick_positions = [i for i in range(-200, 101) if i % major_unit == 0]
tick_labels = [str(i) for i in tick_positions]

# Create an empty list to store all the figures
NWEC3NAPfigures = []

# Loop through each column (excluding the 'Date' column)
for column in NWEC3NAPdf.columns:
    fig = px.line(
        NWEC3NAPdf.assign(
            year=NWEC3NAPdf.index.year,
            date=pd.to_datetime(NWEC3NAPdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=NWEC3NAPdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-200, 100], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="NWE C3/NWE Naphtha " + column + " $/mt",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    NWEC3NAPfigures.append(fig)

# BRT Charts
# Set the major unit for the y-axis
major_unit = 0.4

# Calculate tick positions and labels
tick_positions = [i * major_unit for i in range(-20, 21)]  # Adjust the range based on your requirements
tick_labels = ["{:.1f}".format(i) for i in tick_positions]

# Create an empty list to store all the figures
BRTfigures = []

# Loop through each column (excluding the 'Date' column)
for column in BRTdf.columns:
    fig = px.line(
        BRTdf.assign(
            year=BRTdf.index.year,
            date=pd.to_datetime(BRTdf.index.day_of_year.values + (2023 * 1000), format="%Y%j"),
            value=BRTdf[column],
        ),
        x="date",
        y="value",
        color="year",
        template="plotly_dark",
        render_mode='svg'
    )

# Make traces invisible for demo purposes
    for t in fig.data:
        year = int(t["name"])
        if year < 2018:
            t["visible"] = "legendonly"
        else:
            t["line"]["color"] = color_map.get(year, "purple")

    fig.update_yaxes(range=[-1.5, 2], zeroline=True, zerolinewidth=2, zerolinecolor='White',
                     tickvals=tick_positions, ticktext=tick_labels)
    fig.update_layout(
        xaxis={"tickformat": '%m/%d', "dtick": 'M1',"tickfont": {"size": 8}},
        margin=dict(l=10, r=10, t=30, b=10),
        width=450,
        height=300,
        title="Brent " + column + " $/bbl",
        xaxis_title=None,
        yaxis_title=None
    )
    
# Append the figure to the list
    BRTfigures.append(fig)


# Layout
app.layout = html.Div([
    html.H1("Naphtha Swap Updates"),
    dcc.Tabs([
        dcc.Tab(label='MOPJ', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=MOPJfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(MOPJfigures))])
        ]),
        dcc.Tab(label='NWE', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=NWEfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(NWEfigures))])
        ]),
        dcc.Tab(label='FEI', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=FEIfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(FEIfigures))])
        ]),
        dcc.Tab(label='NWEC3', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=NWEC3figures[i], style={'display': 'inline-block'}) for i in
                               range(len(NWEC3figures))])
        ]),    
        dcc.Tab(label='R92', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=R92figures[i], style={'display': 'inline-block'}) for i in
                               range(len(R92figures))])
        ]),
        dcc.Tab(label='EBOB', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=EBOBfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(EBOBfigures))])
        ]),
        dcc.Tab(label='MOPJ Crk', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=MOPJCRKfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(MOPJCRKfigures))])
        ]),
        dcc.Tab(label='NWE Naphtha Crk', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=NWECRKfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(NWECRKfigures))])
        ]),
        dcc.Tab(label='R92 Crk', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=R92CRKfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(R92CRKfigures))])
        ]),
        dcc.Tab(label='EBOB Crk', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=EBOBCRKfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(EBOBCRKfigures))])
        ]),
        dcc.Tab(label='EW', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=EWfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(EWfigures))])
        ]),
        dcc.Tab(label='R92/MOPJ', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=R92MOPJfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(R92MOPJfigures))])
        ]),
        dcc.Tab(label='EBOB/NWE Naphtha', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=EBOBNWEfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(EBOBNWEfigures))])
        ]),
        dcc.Tab(label='FEI/MOPJ', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=FEIMOPJfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(FEIMOPJfigures))])
        ]),  
        dcc.Tab(label='NWE C3/NWE Naphtha', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=NWEC3NAPfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(NWEC3NAPfigures))])
        ]),
        dcc.Tab(label='Brent', children=[
            html.Div(children=[dcc.Graph(id=f"fig{i + 1}", figure=BRTfigures[i], style={'display': 'inline-block'}) for i in
                               range(len(BRTfigures))])
        ]),             
        # Add more tabs as needed
    ])
])

if __name__ == '__main__':
    app.run(debug=True)


