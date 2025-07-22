#!/usr/bin/env python3
"""
NetCDF File Reader Script

This script provides functionality to read and analyze NetCDF (.nc) files.
NetCDF files are commonly used in scientific computing for storing
multidimensional data like climate data, oceanographic data, etc.

Requirements:
- netCDF4
- numpy
- matplotlib (for plotting)
- pandas (for data manipulation)

Install dependencies:
pip install netCDF4 numpy matplotlib pandas
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import warnings
warnings.filterwarnings('ignore')

# Add tkinter for file dialog
try:
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox
except ImportError:
    tk = None
    filedialog = None
    simpledialog = None
    messagebox = None


class NetCDFReader:
    """A class to read and analyze NetCDF files."""
    
    def __init__(self, file_path):
        """
        Initialize the NetCDF reader.
        
        Args:
            file_path (str): Path to the NetCDF file
        """
        self.file_path = file_path
        self.dataset = None
        self.load_file()
    
    def load_file(self):
        """Load the NetCDF file."""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")
            
            self.dataset = Dataset(self.file_path, 'r')
            print(f"Successfully loaded: {self.file_path}")
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)
    
    def get_file_info(self):
        """Get basic information about the NetCDF file."""
        if not self.dataset:
            return None
        
        info = {
            'file_path': self.file_path,
            'file_size': f"{os.path.getsize(self.file_path) / (1024*1024):.2f} MB",
            'format': self.dataset.file_format,
            'num_dimensions': len(self.dataset.dimensions),
            'num_variables': len(self.dataset.variables),
            'num_global_attributes': len(self.dataset.ncattrs())
        }
        
        return info
    
    def print_file_info(self):
        """Print detailed information about the NetCDF file."""
        info = self.get_file_info()
        if not info:
            return
        
        print("\n" + "="*60)
        print("NETCDF FILE INFORMATION")
        print("="*60)
        for key, value in info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Print dimensions
        print(f"\nDimensions ({len(self.dataset.dimensions)}):")
        for dim_name, dim in self.dataset.dimensions.items():
            size = len(dim) if not dim.isunlimited() else "unlimited"
            print(f"  {dim_name}: {size}")
        
        # Print variables
        print(f"\nVariables ({len(self.dataset.variables)}):")
        for var_name, var in self.dataset.variables.items():
            dims = ', '.join(var.dimensions)
            shape = var.shape
            dtype = var.dtype
            print(f"  {var_name}: {dtype} {shape} ({dims})")
        
        # Print global attributes
        if self.dataset.ncattrs():
            print(f"\nGlobal Attributes ({len(self.dataset.ncattrs())}):")
            for attr_name in self.dataset.ncattrs():
                attr_value = self.dataset.getncattr(attr_name)
                # Truncate long attribute values
                if len(str(attr_value)) > 100:
                    attr_value = str(attr_value)[:100] + "..."
                print(f"  {attr_name}: {attr_value}")
    
    def get_variable_info(self, var_name):
        """Get detailed information about a specific variable."""
        if var_name not in self.dataset.variables:
            print(f"Variable '{var_name}' not found in the dataset.")
            return None
        
        var = self.dataset.variables[var_name]
        info = {
            'name': var_name,
            'dimensions': var.dimensions,
            'shape': var.shape,
            'dtype': var.dtype,
            'attributes': {}
        }
        
        # Get variable attributes
        for attr_name in var.ncattrs():
            info['attributes'][attr_name] = var.getncattr(attr_name)
        
        return info
    
    def print_variable_info(self, var_name):
        """Print detailed information about a specific variable."""
        info = self.get_variable_info(var_name)
        if not info:
            return
        
        print(f"\nVariable: {info['name']}")
        print(f"Dimensions: {info['dimensions']}")
        print(f"Shape: {info['shape']}")
        print(f"Data Type: {info['dtype']}")
        
        if info['attributes']:
            print("Attributes:")
            for attr_name, attr_value in info['attributes'].items():
                print(f"  {attr_name}: {attr_value}")
    
    def read_variable(self, var_name, slice_indices=None):
        """
        Read data from a variable.
        
        Args:
            var_name (str): Name of the variable to read
            slice_indices (dict): Dictionary of dimension names and slice indices
        
        Returns:
            numpy.ndarray: Variable data
        """
        if var_name not in self.dataset.variables:
            print(f"Variable '{var_name}' not found in the dataset.")
            return None
        
        try:
            if slice_indices:
                # Apply slicing
                var = self.dataset.variables[var_name]
                slices = []
                for dim in var.dimensions:
                    if dim in slice_indices:
                        slices.append(slice_indices[dim])
                    else:
                        slices.append(slice(None))
                
                data = var[slices]
            else:
                # Read entire variable
                data = self.dataset.variables[var_name][:]
            
            return data
        except Exception as e:
            print(f"Error reading variable '{var_name}': {e}")
            return None
    
    def read_specific_row(self, var_name, row_indices, dimension_name=None):
        """
        Read specific rows from a variable.
        
        Args:
            var_name (str): Name of the variable to read
            row_indices (int or list): Row index or list of row indices to read
            dimension_name (str): Name of the dimension to slice (if None, uses first dimension)
        
        Returns:
            numpy.ndarray: Variable data for specified rows
        """
        if var_name not in self.dataset.variables:
            print(f"Variable '{var_name}' not found in the dataset.")
            return None
        
        var = self.dataset.variables[var_name]
        
        # If no dimension specified, use the first one
        if dimension_name is None:
            dimension_name = var.dimensions[0]
        
        if dimension_name not in var.dimensions:
            print(f"Dimension '{dimension_name}' not found in variable '{var_name}'.")
            print(f"Available dimensions: {var.dimensions}")
            return None
        
        try:
            # Create slice indices
            slice_indices = {dimension_name: row_indices}
            return self.read_variable(var_name, slice_indices)
        except Exception as e:
            print(f"Error reading rows from variable '{var_name}': {e}")
            return None
    
    def print_row_data(self, var_name, row_indices, dimension_name=None, max_cols=10, max_rows=20):
        """
        Print specific row data in a readable format.
        
        Args:
            var_name (str): Name of the variable to read
            row_indices (int or list): Row index or list of row indices to read
            dimension_name (str): Name of the dimension to slice
            max_cols (int): Maximum number of columns to display
            max_rows (int): Maximum number of rows to display
        """
        data = self.read_specific_row(var_name, row_indices, dimension_name)
        if data is None:
            return
        
        print(f"\nRow data for variable '{var_name}':")
        print(f"Shape: {data.shape}")
        print(f"Data type: {data.dtype}")
        
        # Handle different data dimensions
        if data.ndim == 1:
            # 1D data - show as a simple list
            print("Data:")
            if len(data) <= max_cols:
                print(data)
            else:
                print(f"First {max_cols} values: {data[:max_cols]}")
                print(f"Last {max_cols} values: {data[-max_cols:]}")
                print(f"... (showing {max_cols} of {len(data)} values)")
        
        elif data.ndim == 2:
            # 2D data - show as a table
            print("Data (rows x columns):")
            rows_to_show = min(data.shape[0], max_rows)
            cols_to_show = min(data.shape[1], max_cols)
            
            for i in range(rows_to_show):
                row_data = data[i, :cols_to_show]
                print(f"Row {i}: {row_data}")
                if data.shape[1] > max_cols:
                    print(f"      ... (showing {cols_to_show} of {data.shape[1]} columns)")
        
        else:
            # Higher dimensional data
            print("Data (higher dimensional):")
            print(f"Showing first few elements: {data.flatten()[:max_cols]}")
            if data.size > max_cols:
                print(f"... (showing {max_cols} of {data.size} total elements)")
    
    def get_data_summary(self, var_name, slice_indices=None):
        """
        Get a summary of data including sample values.
        
        Args:
            var_name (str): Name of the variable
            slice_indices (dict): Optional slicing parameters
        
        Returns:
            dict: Summary information about the data
        """
        data = self.read_variable(var_name, slice_indices)
        if data is None:
            return None
        
        # Handle masked arrays
        if hasattr(data, 'mask'):
            data_clean = data.compressed()
        else:
            data_clean = data.flatten()
        
        summary = {
            'shape': data.shape,
            'size': data.size,
            'dtype': str(data.dtype),
            'min': float(np.min(data_clean)),
            'max': float(np.max(data_clean)),
            'mean': float(np.mean(data_clean)),
            'std': float(np.std(data_clean)),
            'first_10_values': data_clean[:10].tolist(),
            'last_10_values': data_clean[-10:].tolist() if len(data_clean) > 10 else data_clean.tolist()
        }
        
        return summary
    
    def get_variable_statistics(self, var_name):
        """Get basic statistics for a variable."""
        data = self.read_variable(var_name)
        if data is None:
            return None
        
        # Handle masked arrays
        if hasattr(data, 'mask'):
            data = data.compressed()
        
        stats = {
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'mean': float(np.mean(data)),
            'std': float(np.std(data)),
            'shape': data.shape,
            'size': data.size
        }
        
        return stats
    
    def print_variable_statistics(self, var_name):
        """Print statistics for a variable."""
        stats = self.get_variable_statistics(var_name)
        if not stats:
            return
        
        print(f"\nStatistics for variable '{var_name}':")
        print(f"Shape: {stats['shape']}")
        print(f"Size: {stats['size']:,}")
        print(f"Min: {stats['min']:.6f}")
        print(f"Max: {stats['max']:.6f}")
        print(f"Mean: {stats['mean']:.6f}")
        print(f"Std: {stats['std']:.6f}")
    
    def list_variables(self):
        """List all variables in the dataset."""
        print("\nAvailable variables:")
        for i, var_name in enumerate(self.dataset.variables.keys(), 1):
            var = self.dataset.variables[var_name]
            print(f"{i:2d}. {var_name} ({', '.join(var.dimensions)})")
    
    def plot_variable(self, var_name, slice_indices=None, save_path=None):
        """
        Create a simple plot of a variable.
        
        Args:
            var_name (str): Name of the variable to plot
            slice_indices (dict): Dictionary of dimension names and slice indices
            save_path (str): Path to save the plot (optional)
        """
        data = self.read_variable(var_name, slice_indices)
        if data is None:
            return
        
        # Handle masked arrays
        if hasattr(data, 'mask'):
            data = data.filled(np.nan)
        
        # Create plot based on data dimensions
        plt.figure(figsize=(10, 6))
        
        if data.ndim == 1:
            plt.plot(data)
            plt.title(f'{var_name}')
            plt.xlabel('Index')
            plt.ylabel('Value')
        elif data.ndim == 2:
            plt.imshow(data, cmap='viridis', aspect='auto')
            plt.colorbar(label=var_name)
            plt.title(f'{var_name}')
        else:
            # For higher dimensions, take a slice
            if data.ndim > 2:
                # Take the middle slice for each extra dimension
                slices = [data.shape[i]//2 for i in range(2, data.ndim)]
                data = data[:, :, *slices]
                plt.imshow(data, cmap='viridis', aspect='auto')
                plt.colorbar(label=var_name)
                plt.title(f'{var_name} (slice)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        else:
            plt.show()
    
    def export_to_csv(self, var_name, output_path, slice_indices=None):
        """
        Export a variable to CSV format.
        
        Args:
            var_name (str): Name of the variable to export
            output_path (str): Path for the output CSV file
            slice_indices (dict): Dictionary of dimension names and slice indices
        """
        data = self.read_variable(var_name, slice_indices)
        if data is None:
            return
        
        # Handle masked arrays
        if hasattr(data, 'mask'):
            data = data.filled(np.nan)
        
        # Convert to DataFrame
        if data.ndim == 1:
            df = pd.DataFrame({var_name: data})
        elif data.ndim == 2:
            df = pd.DataFrame(data)
            df.columns = [f'{var_name}_col_{i}' for i in range(data.shape[1])]
            df.index.name = f'{var_name}_row'
        else:
            print(f"Cannot export {data.ndim}-dimensional data to CSV directly.")
            return
        
        # Save to CSV
        df.to_csv(output_path, index=True)
        print(f"Data exported to: {output_path}")
    
    def close(self):
        """Close the NetCDF dataset."""
        if self.dataset:
            self.dataset.close()


def get_file_path_via_dialog():
    """Open a file dialog to select a NetCDF file."""
    if tk is None or filedialog is None:
        print("tkinter is not available. Please provide the file path as a command-line argument.")
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select NetCDF file",
        filetypes=[("NetCDF files", "*.nc"), ("All files", "*.*")]
    )
    root.destroy()
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit(1)
    return file_path

def get_n_rows_via_dialog():
    """Prompt the user for the number of rows to display."""
    if tk is None or simpledialog is None:
        print("tkinter is not available. Please provide the number of rows as a command-line argument.")
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    n = simpledialog.askinteger("Number of Rows", "How many rows do you want to display?", minvalue=1, initialvalue=5)
    root.destroy()
    if n is None:
        print("No number entered. Exiting.")
        sys.exit(1)
    return n

def get_variable_name_via_dialog(var_names):
    """Prompt the user to select a variable name from a list using a dropdown."""
    if tk is None:
        print("tkinter is not available. Please provide the variable name as a command-line argument.")
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    # Use a simple dropdown dialog
    var_name = None
    def on_select():
        nonlocal var_name
        var_name = var_var.get()
        select_win.destroy()
    select_win = tk.Toplevel(root)
    select_win.title("Select Variable Name")
    tk.Label(select_win, text="Select variable to preview:").pack(padx=10, pady=10)
    var_var = tk.StringVar(select_win)
    var_var.set(var_names[0])
    dropdown = tk.OptionMenu(select_win, var_var, *var_names)
    dropdown.pack(padx=10, pady=10)
    tk.Button(select_win, text="OK", command=on_select).pack(pady=10)
    select_win.grab_set()
    root.wait_window(select_win)
    root.destroy()
    if var_name is None or var_name not in var_names:
        print("Invalid or no variable name selected. Exiting.")
        sys.exit(1)
    return var_name

def get_save_path_via_dialog(default_name="output.csv"):
    """Prompt the user for a save file path using a file dialog."""
    if tk is None or filedialog is None:
        print("tkinter is not available. Please provide the output file path as a command-line argument.")
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Save CSV As",
        defaultextension=".csv",
        initialfile=default_name,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    if not file_path:
        print("No output file selected. Exiting.")
        sys.exit(1)
    return file_path

def get_row_indices_via_dialog(coord_values):
    """Prompt the user to select specific row indices or values from the first dimension. Blank means all rows."""
    if tk is None or simpledialog is None:
        print("tkinter is not available. Please provide the row indices as a command-line argument.")
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    preview = ', '.join(str(v) for v in coord_values[:20])
    prompt = f"First dimension has {len(coord_values)} values.\nSample: {preview}\n\nEnter indices (comma-separated, e.g. 0,1,2), a range (e.g. 0:10), or leave blank for all rows:"
    indices_str = simpledialog.askstring("Select Rows", prompt)
    root.destroy()
    if not indices_str or indices_str.strip() == '':
        return None  # None means all rows
    indices = []
    if ':' in indices_str:
        parts = indices_str.split(':')
        if len(parts) == 2:
            start = int(parts[0])
            end = int(parts[1])
            indices = list(range(start, end))
        else:
            print("Invalid range format. Use start:end.")
            sys.exit(1)
    else:
        indices = [int(i.strip()) for i in indices_str.split(',') if i.strip().isdigit()]
    if not indices:
        print("No valid indices parsed. Exiting.")
        sys.exit(1)
    return indices

def main():
    """Main function to run the NetCDF reader."""
    parser = argparse.ArgumentParser(description='Read and analyze NetCDF files')
    parser.add_argument('file_path', nargs='?', help='Path to the NetCDF file')
    parser.add_argument('--info', action='store_true', help='Print file information')
    parser.add_argument('--list-vars', action='store_true', help='List all variables')
    parser.add_argument('--var-info', type=str, help='Print information about a specific variable')
    parser.add_argument('--var-stats', type=str, help='Print statistics for a specific variable')
    parser.add_argument('--read-var', type=str, help='Read and display a specific variable')
    parser.add_argument('--read-row', type=str, help='Read specific row(s) from a variable (format: variable_name:row_index or variable_name:start:end)')
    parser.add_argument('--dimension', type=str, help='Dimension name for row reading (default: first dimension)')
    parser.add_argument('--plot-var', type=str, help='Plot a specific variable')
    parser.add_argument('--export-var', type=str, help='Export a variable to CSV')
    parser.add_argument('--output', type=str, help='Output path for export/plot')
    parser.add_argument('--ui-preview', action='store_true', help='Use UI to select file, variable, and number of rows to preview')
    
    args = parser.parse_args()
    
    # UI preview mode
    if args.ui_preview:
        file_path = get_file_path_via_dialog()
        reader = NetCDFReader(file_path)
        try:
            var_names = list(reader.dataset.variables.keys())
            var_name = get_variable_name_via_dialog(var_names)
            var_obj = reader.dataset.variables[var_name]
            dim0 = var_obj.dimensions[0]
            max_rows = var_obj.shape[0]
            var_info = f"Variable: {var_name}\nShape: {var_obj.shape}\nDimensions: {var_obj.dimensions}\nDtype: {var_obj.dtype}"
            print(var_info)
            if messagebox is not None:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Variable Info", var_info)
                root.destroy()
            if dim0 in reader.dataset.variables:
                coord_values = reader.dataset.variables[dim0][:]
            else:
                coord_values = list(range(max_rows))
            row_indices = get_row_indices_via_dialog(coord_values)
            output_path = get_save_path_via_dialog(f"{var_name}_all_rows.csv" if row_indices is None else f"{var_name}_rows_{'_'.join(map(str, row_indices[:3]))}.csv")
            if row_indices is None:
                print(f"\nExporting ALL rows of variable '{var_name}' to {output_path}")
                reader.export_to_csv(var_name, output_path)
            else:
                print(f"\nExporting selected rows of variable '{var_name}' to {output_path}")
                reader.export_to_csv(var_name, output_path, slice_indices={dim0: row_indices})
        finally:
            reader.close()
        return
    
    # If file_path is not provided, open a file dialog
    file_path = args.file_path
    if not file_path:
        file_path = get_file_path_via_dialog()
    
    # Create NetCDF reader
    reader = NetCDFReader(file_path)
    
    try:
        # Print file information
        if args.info:
            reader.print_file_info()
        
        # List variables
        if args.list_vars:
            reader.list_variables()
        
        # Variable information
        if args.var_info:
            reader.print_variable_info(args.var_info)
        
        # Variable statistics
        if args.var_stats:
            reader.print_variable_statistics(args.var_stats)
        
        # Read variable
        if args.read_var:
            data = reader.read_variable(args.read_var)
            if data is not None:
                print(f"\nData for variable '{args.read_var}':")
                print(f"Shape: {data.shape}")
                print(f"Type: {data.dtype}")
                print(f"First few values: {data.flatten()[:10]}")
        
        # Read specific rows
        if args.read_row:
            try:
                # Parse the row specification (format: variable_name:row_index or variable_name:start:end)
                if ':' in args.read_row:
                    parts = args.read_row.split(':')
                    var_name = parts[0]
                    
                    if len(parts) == 2:
                        # Single row index
                        row_index = int(parts[1])
                        reader.print_row_data(var_name, row_index, args.dimension)
                    elif len(parts) == 3:
                        # Range of rows
                        start_row = int(parts[1])
                        end_row = int(parts[2])
                        row_indices = slice(start_row, end_row)
                        reader.print_row_data(var_name, row_indices, args.dimension)
                    else:
                        print("Invalid row specification. Use format: variable_name:row_index or variable_name:start:end")
                else:
                    print("Invalid row specification. Use format: variable_name:row_index or variable_name:start:end")
            except ValueError as e:
                print(f"Error parsing row specification: {e}")
        
        # Plot variable
        if args.plot_var:
            output_path = args.output if args.output else None
            reader.plot_variable(args.plot_var, save_path=output_path)
        
        # Export variable
        if args.export_var:
            output_path = args.output if args.output else f"{args.export_var}.csv"
            reader.export_to_csv(args.export_var, output_path)
        
        # If no specific action is specified, print file info
        if not any([args.info, args.list_vars, args.var_info, args.var_stats, 
                   args.read_var, args.plot_var, args.export_var]):
            reader.print_file_info()
            reader.list_variables()
    
    finally:
        reader.close()


if __name__ == "__main__":
    main() 