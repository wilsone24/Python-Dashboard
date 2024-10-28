# Chicago Crime Dashboard 🌆

<div align="center">

[![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An interactive dashboard for analyzing and visualizing crime data in the city of Chicago.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing) • [License](#-license)

</div>

## 🚀 Features

- 📊 Interactive visualization of crime types, locations, and time trends.
- 🌍 Geospatial maps for regional analysis.
- 🔎 Data filtering by FBI code, crime location description or crime type.
- 📈 Bar and line charts to identify patterns and compare categories.

## 📑 Dashboard Pages

The Chicago Crime Dashboard includes two main pages to help users explore and understand the data more effectively:

1. **Introduction Page**: Explains the importance and context of analyzing crime data in Chicago. This page includes a brief overview of the data sources, purpose, and how the dashboard aids in making informed decisions.

2. **Dashboard Page**: Provides interactive visualizations and tools for analyzing crime data by type, location, and time. Users can apply filters, view geospatial maps, and explore various graphs to find patterns or trends in the data.

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wilsone24/chicago-crime-dashboard.git
   ```

2. Navigate to the project directory:
   ```bash
   cd chicago-crime-dashboard
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥 Usage

Make sure you have **Streamlit** installed, then run the following command to start the dashboard:

```bash
streamlit run main.py
```

### Prerequisites

- **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
- **Streamlit**: Install with `pip install streamlit`

## 📁 Project Structure

```
chicago-crime-dashboard/
├── main.py                      # Main entry point for the Streamlit dashboard
├── views/                       # Project pages
├── Crimes2023.csv               # Dataset
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## 🔧 Dependencies

This project uses the following key dependencies:

- [Streamlit](https://streamlit.io/): ^1.8.0
- [Pandas](https://pandas.pydata.org/): ^1.3.5
- [Plotly](https://plotly.com/python/): ^5.5.0
- [Geopandas](https://geopandas.org/): ^0.10.2

For a full list of dependencies, please check the `requirements.txt` file.

## 🎥 Demonstration

For a complete demonstration of the dashboard, watch the following video:

[![Watch the video](https://img.youtube.com/vi/VJGfD6h6tps/maxresdefault.jpg)](https://www.youtube.com/watch?v=VJGfD6h6tps)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add some NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
