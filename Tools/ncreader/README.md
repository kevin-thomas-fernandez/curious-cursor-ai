# NetCDF File Reader

A comprehensive Python script for reading and analyzing NetCDF (.nc) files. NetCDF files are commonly used in scientific computing for storing multidimensional data like climate data, oceanographic data, and other geospatial datasets.

## Features

- **File Information**: Get detailed information about NetCDF files including dimensions, variables, and attributes
- **Variable Analysis**: Read, analyze, and get statistics for specific variables
- **Data Visualization**: Create plots of variables (1D, 2D, and higher dimensions)
- **Data Export**: Export variables to CSV format for further analysis
- **Command Line Interface**: Easy-to-use command line interface with various options
- **Programmatic Usage**: Use as a Python class in your own scripts

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install netCDF4 numpy matplotlib pandas
   ```

2. **Download the script**:
   - `nc_reader.py` - Main NetCDF reader script
   - `requirements.txt` - Python dependencies
   - `example_usage.py` - Example usage script
   - `README.md` - This documentation

## Quick Start

### Command Line Usage

1. **Basic file information**:
   ```bash
   python nc_reader.py your_file.nc
   ```

2. **List all variables**:
   ```bash
   python nc_reader.py your_file.nc --list-vars
   ```

3. **Get detailed file information**:
   ```bash
   python nc_reader.py your_file.nc --info
   ```

4. **Get information about a specific variable**:
   ```bash
   python nc_reader.py your_file.nc --var-info temperature
   ```

5. **Get statistics for a variable**:
   ```bash
   python nc_reader.py your_file.nc --var-stats temperature
   ```

6. **Plot a variable**:
   ```bash
   python nc_reader.py your_file.nc --plot-var temperature --output temp_plot.png
   ```

7. **Export a variable to CSV**:
   ```bash
   python nc_reader.py your_file.nc --export-var temperature --output temp_data.csv
   ```

### Programmatic Usage

```python
from nc_reader import NetCDFReader

# Create a reader instance
reader = NetCDFReader('your_file.nc')

try:
    # Print file information
    reader.print_file_info()
    
    # List variables
    reader.list_variables()
    
    # Get variable information
    reader.print_variable_info('temperature')
    
    # Get statistics
    reader.print_variable_statistics('temperature')
    
    # Read data
    data = reader.read_variable('temperature')
    print(f"Data shape: {data.shape}")
    
    # Plot variable
    reader.plot_variable('temperature', save_path='plot.png')
    
    # Export to CSV
    reader.export_to_csv('temperature', 'data.csv')
    
finally:
    reader.close()
```

## Advanced Usage

### Reading with Slicing

For large datasets, you can read specific slices to save memory:

```python
# Read only the first 10 time steps
slice_indices = {'time': slice(0, 10)}
data = reader.read_variable('temperature', slice_indices)

# Read specific latitude/longitude range
slice_indices = {
    'time': slice(0, 10),
    'lat': slice(0, 100),
    'lon': slice(0, 100)
}
data = reader.read_variable('temperature', slice_indices)
```

### Working with Different Data Types

The script handles various NetCDF data types:
- Regular arrays
- Masked arrays (with missing data)
- Different data types (float, int, etc.)

### Error Handling

The script includes comprehensive error handling:
- File not found errors
- Invalid variable names
- Memory issues with large datasets
- Data type compatibility issues

## Command Line Options

| Option | Description |
|--------|-------------|
| `file_path` | Path to the NetCDF file (required) |
| `--info` | Print detailed file information |
| `--list-vars` | List all variables in the file |
| `--var-info VARIABLE` | Print information about a specific variable |
| `--var-stats VARIABLE` | Print statistics for a specific variable |
| `--read-var VARIABLE` | Read and display a specific variable |
| `--plot-var VARIABLE` | Plot a specific variable |
| `--export-var VARIABLE` | Export a variable to CSV |
| `--output PATH` | Output path for plots or CSV files |

## Example Output

### File Information
```
============================================================
NETCDF FILE INFORMATION
============================================================
File Path: sample_data.nc
File Size: 2.45 MB
Format: NETCDF4
Num Dimensions: 3
Num Variables: 4
Num Global Attributes: 0

Dimensions (3):
  time: 100
  lat: 50
  lon: 100

Variables (4):
  time: float64 (100,) (time)
  lat: float32 (50,) (lat)
  lon: float32 (100,) (lon)
  temperature: float32 (100, 50, 100) (time, lat, lon)
```

### Variable Statistics
```
Statistics for variable 'temperature':
Shape: (100, 50, 100)
Size: 500,000
Min: -45.234567
Max: 45.123456
Mean: 15.678901
Std: 12.345678
```

## File Structure

```
Tools/
├── nc_reader.py          # Main NetCDF reader script
├── requirements.txt      # Python dependencies
├── example_usage.py      # Example usage script
└── README.md            # This documentation
```

## Dependencies

- **netCDF4**: For reading NetCDF files
- **numpy**: For numerical operations
- **matplotlib**: For plotting and visualization
- **pandas**: For data manipulation and CSV export

## Common Use Cases

1. **Climate Data Analysis**: Read temperature, precipitation, or other climate variables
2. **Oceanographic Data**: Analyze sea surface temperature, salinity, or current data
3. **Atmospheric Data**: Process pressure, wind, or humidity data
4. **Satellite Data**: Work with remote sensing data in NetCDF format
5. **Model Output**: Analyze output from climate or weather models

## Troubleshooting

### Common Issues

1. **Import Error for netCDF4**:
   ```bash
   pip install netCDF4
   ```
   If this fails, try:
   ```bash
   conda install netcdf4
   ```

2. **Memory Issues with Large Files**:
   - Use slicing to read only parts of the data
   - Close the reader when done to free memory

3. **Plotting Issues**:
   - Ensure matplotlib backend is properly configured
   - For headless environments, use 'Agg' backend

### Performance Tips

- Use slicing for large datasets
- Close the reader when done
- Use appropriate data types for your analysis
- Consider using dask for very large files

## Contributing

Feel free to extend the functionality by:
- Adding support for more data formats
- Implementing additional visualization options
- Adding data processing capabilities
- Improving error handling and performance

## License

This script is provided as-is for educational and research purposes. Feel free to modify and use as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example usage
3. Ensure all dependencies are properly installed
4. Verify your NetCDF file is not corrupted 