#!/usr/bin/env python3
"""
Example usage of the NetCDF Reader

This script demonstrates how to use the NetCDFReader class programmatically.
"""

from nc_reader import NetCDFReader
import numpy as np

def example_usage():
    """Example of how to use the NetCDFReader class."""
    
    # Replace 'your_file.nc' with the path to your actual NetCDF file
    file_path = 'your_file.nc'
    
    try:
        # Create a NetCDF reader instance
        reader = NetCDFReader(file_path)
        
        # Print basic file information
        print("=== Basic File Information ===")
        reader.print_file_info()
        
        # List all variables
        print("\n=== Available Variables ===")
        reader.list_variables()
        
        # Get information about a specific variable (replace 'temperature' with actual variable name)
        variable_name = 'temperature'  # Change this to match your file's variables
        print(f"\n=== Variable Information for '{variable_name}' ===")
        reader.print_variable_info(variable_name)
        
        # Get statistics for a variable
        print(f"\n=== Statistics for '{variable_name}' ===")
        reader.print_variable_statistics(variable_name)
        
        # Read a variable (you can specify slice indices for large datasets)
        print(f"\n=== Reading Variable '{variable_name}' ===")
        data = reader.read_variable(variable_name)
        if data is not None:
            print(f"Data shape: {data.shape}")
            print(f"Data type: {data.dtype}")
            print(f"First 5 values: {data.flatten()[:5]}")
        
        # Example of reading with slicing (for large datasets)
        # slice_indices = {'time': slice(0, 10), 'lat': slice(0, 100), 'lon': slice(0, 100)}
        # data_slice = reader.read_variable(variable_name, slice_indices)
        
        # Plot a variable
        print(f"\n=== Plotting Variable '{variable_name}' ===")
        reader.plot_variable(variable_name, save_path=f'{variable_name}_plot.png')
        
        # Export to CSV
        print(f"\n=== Exporting Variable '{variable_name}' to CSV ===")
        reader.export_to_csv(variable_name, f'{variable_name}_data.csv')
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print("Please replace 'your_file.nc' with the path to your actual NetCDF file.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always close the reader
        if 'reader' in locals():
            reader.close()

def create_sample_netcdf():
    """Create a sample NetCDF file for testing purposes."""
    from netCDF4 import Dataset
    import numpy as np
    
    # Create a sample NetCDF file
    with Dataset('sample_data.nc', 'w', format='NETCDF4') as nc:
        # Create dimensions
        time_dim = nc.createDimension('time', 100)
        lat_dim = nc.createDimension('lat', 50)
        lon_dim = nc.createDimension('lon', 100)
        
        # Create variables
        times = nc.createVariable('time', 'f8', ('time',))
        lats = nc.createVariable('lat', 'f4', ('lat',))
        lons = nc.createVariable('lon', 'f4', ('lon',))
        temperature = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon'))
        
        # Add attributes
        times.units = 'days since 2020-01-01'
        times.long_name = 'time'
        lats.units = 'degrees_north'
        lats.long_name = 'latitude'
        lons.units = 'degrees_east'
        lons.long_name = 'longitude'
        temperature.units = 'celsius'
        temperature.long_name = 'air temperature'
        
        # Generate sample data
        times[:] = np.arange(100)
        lats[:] = np.linspace(-90, 90, 50)
        lons[:] = np.linspace(-180, 180, 100)
        
        # Create realistic temperature data
        for t in range(100):
            # Simple temperature model: varies with latitude and has some time variation
            temp = 30 * np.cos(np.radians(lats)) + 10 * np.sin(2 * np.pi * t / 365)
            temp = temp[:, np.newaxis] + np.random.normal(0, 2, (50, 100))
            temperature[t, :, :] = temp
        
        print("Sample NetCDF file 'sample_data.nc' created successfully!")

if __name__ == "__main__":
    print("NetCDF Reader Example Usage")
    print("=" * 50)
    
    # Check if sample file exists, if not create one
    import os
    if not os.path.exists('sample_data.nc'):
        print("Creating sample NetCDF file for demonstration...")
        create_sample_netcdf()
    
    # Use the sample file for demonstration
    print("\nUsing sample file 'sample_data.nc' for demonstration...")
    
    # Update the file path in the example
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
#!/usr/bin/env python3
from nc_reader import NetCDFReader

# Use the sample file
reader = NetCDFReader('sample_data.nc')

try:
    # Print basic file information
    print("=== Basic File Information ===")
    reader.print_file_info()
    
    # List all variables
    print("\\n=== Available Variables ===")
    reader.list_variables()
    
    # Get information about temperature variable
    print("\\n=== Variable Information for 'temperature' ===")
    reader.print_variable_info('temperature')
    
    # Get statistics for temperature
    print("\\n=== Statistics for 'temperature' ===")
    reader.print_variable_statistics('temperature')
    
    # Plot temperature (first time step)
    print("\\n=== Plotting Temperature (first time step) ===")
    reader.plot_variable('temperature', {'time': 0}, 'temperature_plot.png')
    
    # Export temperature data (first time step)
    print("\\n=== Exporting Temperature Data (first time step) ===")
    reader.export_to_csv('temperature', 'temperature_data.csv', {'time': 0})
    
finally:
    reader.close()
''')
        temp_file = f.name
    
    print(f"Example script created: {temp_file}")
    print("Run it with: python", temp_file) 