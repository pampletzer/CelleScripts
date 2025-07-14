import pandas as pd
import folium
from folium.plugins import MarkerCluster, TimestampedGeoJson
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import re
import os
import numpy as np  # Import numpy for np.nan


# --- Configure logging to file and console ---
def configure_logging(excel_file_path=None):
    log_file_name = "map_generator_debug.txt"
    if excel_file_path:
        base_name = os.path.basename(excel_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        log_file_name = f"{name_without_ext}.txt"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
            handler.close()
        elif isinstance(handler, logging.StreamHandler) and handler.stream.name == '<stderr>':
            pass
        else:
            logger.removeHandler(handler)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file_name, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logging.info(f"Logging configured. Full debug log being written to '{log_file_name}'.")


configure_logging()


def get_file_path():
    """Opens a file dialog for the user to select an Excel file."""
    logging.debug("Initializing Tkinter root window.")
    root = tk.Tk()
    root.withdraw()
    logging.debug("Tkinter root window initialized.")
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    logging.debug(f"File dialog closed. File path: {file_path}")
    return file_path


def load_and_prepare_excel_data(file_path):
    """
    Loads data from an Excel file, attempts to detect headers, and prepares
    it for map generation. It now tries to find suitable header rows.
    """
    logging.debug("Calling load_and_prepare_excel_data.")
    logging.info(f"Attempting to load and process '{file_path}'...")

    try:
        xls = pd.ExcelFile(file_path)
        df = None

        required_time_cols = ['Time', 'Date', 'Timestamp', 'Uhrzeit']
        # Updated text_coord_col_candidates to reflect preferred order for coordinate extraction
        text_coord_col_candidates = ['Address', 'Description', 'Party',
                                     'Location']  # Added 'Location' as another potential text coordinate source

        # Define columns that should always be included in the popup if available
        # These are the columns explicitly requested by the user for popups.
        user_requested_popup_cols = [
            'Time', 'Map Address', 'Group', 'Subgroup', 'Description', 'Type', 'Source', 'Deleted', 'Tag'
        ]

        for sheet_name in xls.sheet_names:
            temp_df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

            for header_row_index in range(min(5, len(temp_df))):
                logging.debug(f"--- Trying header row index: {header_row_index} (Excel row {header_row_index + 1}) ---")
                current_header_row = temp_df.iloc[header_row_index]

                potential_df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index)
                potential_df.columns = potential_df.columns.astype(str)
                normalized_cols = {col.strip().lower().replace(" ", ""): col for col in potential_df.columns}

                time_col = next((col_orig for norm_col, col_orig in normalized_cols.items() if
                                 any(req.lower() in norm_col for req in required_time_cols)), None)
                lat_col = next((col_orig for norm_col, col_orig in normalized_cols.items() if 'latitude' in norm_col),
                               None)
                lon_col = next((col_orig for norm_col, col_orig in normalized_cols.items() if 'longitude' in norm_col),
                               None)

                primary_text_coord_col = None
                for candidate in text_coord_col_candidates:
                    if candidate.lower() in normalized_cols:
                        primary_text_coord_col = normalized_cols[candidate.lower()]
                        break

                logging.debug(f"Columns found at this header row: {list(potential_df.columns)}")

                timestamp_config_found = False
                if time_col:
                    if 'date' in normalized_cols and 'time' in normalized_cols:
                        timestamp_config_found = True
                        date_col = normalized_cols['date']
                        time_col = normalized_cols['time']
                        single_timestamp_col = None
                    elif 'timestamp' in normalized_cols:
                        timestamp_config_found = True
                        single_timestamp_col = normalized_cols['timestamp']
                        date_col = None
                        time_col = None
                    elif 'time' in normalized_cols and not 'date' in normalized_cols:
                        timestamp_config_found = True
                        single_timestamp_col = normalized_cols['time']
                        date_col = None
                        time_col = None
                    elif 'date' in normalized_cols and not 'time' in normalized_cols:
                        timestamp_config_found = True
                        single_timestamp_col = normalized_cols['date']
                        date_col = None
                        time_col = None

                logging.debug(f"Timestamp config found: {timestamp_config_found}")
                if timestamp_config_found:
                    logging.debug(
                        f"  Timestamp source(s): Date='{date_col}', Time='{time_col}', Single Timestamp='{single_timestamp_col}'")

                if timestamp_config_found and ((lat_col and lon_col) or primary_text_coord_col):
                    df = potential_df
                    df.columns = [col.strip() for col in df.columns]

                    lat_col_for_data = lat_col
                    lon_col_for_data = lon_col

                    logging.info(
                        f"SUCCESS: Detected header row at index: {header_row_index} (0-indexed, Excel row {header_row_index + 1}).")
                    logging.info(
                        f"  Geo columns for data processing: Lat_Orig='{lat_col_for_data}', Lon_Orig='{lon_col_for_data}', Primary Text_Coord Candidate='{primary_text_coord_col}'")
                    break
            if df is not None:
                break

        if df is None:
            messagebox.showerror("Error",
                                 "Could not find a suitable header row. Required: a Time column AND (Latitude/Longitude columns OR a text column like 'Address' or 'Description' containing coordinates).")
            logging.error("No suitable header row found in the Excel file.")
            return pd.DataFrame(), None, None, None, None, None, None

        logging.info("Excel data loaded with header at row %s (1-indexed).", header_row_index + 1)

        logging.debug(f"Raw data from all columns (first 20 rows) after header detection:\n{df.head(20).to_string()}")

        df['parsed_timestamp'] = pd.NaT
        # Initialize Latitude_Final and Longitude_Final with NaN (float type)
        df['Latitude_Final'] = np.nan
        df['Longitude_Final'] = np.nan

        if single_timestamp_col:
            logging.info(f"Attempting to parse single timestamp column '{single_timestamp_col}'.")

            if single_timestamp_col in df.columns:
                logging.debug(
                    f"Raw '{single_timestamp_col}' column head before parsing:\n{df[single_timestamp_col].head(20).to_string()}")
            else:
                logging.debug(f"Column '{single_timestamp_col}' not found in DataFrame for raw data logging.")

            if single_timestamp_col in df.columns:
                df[single_timestamp_col] = df[single_timestamp_col].astype(str).str.strip()
                df[single_timestamp_col] = df[single_timestamp_col].apply(
                    lambda x: re.sub(r'\(UTC[+-]\d+\)', '', x).strip())

                timestamp_formats_to_try = [
                    '%m/%d/%Y %H:%M:%S',
                    '%d.%m.%Y %H:%M:%S',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y/%m/%d %H:%M:%S',
                    '%m/%d/%Y %I:%M:%S %p',
                    '%d.%m.%Y',
                    '%Y-%m-%d',
                    '%H:%M:%S',
                ]

                parsed_successfully = False
                for fmt in timestamp_formats_to_try:
                    try:
                        temp_parsed = pd.to_datetime(df[single_timestamp_col], format=fmt, errors='coerce')
                        if temp_parsed.notna().any():
                            df['parsed_timestamp'] = temp_parsed
                            logging.info(
                                f"Successfully parsed {df['parsed_timestamp'].notna().sum()} timestamps using format '{fmt}'.")
                            parsed_successfully = True
                            break
                    except ValueError:
                        continue

                if not parsed_successfully:
                    df['parsed_timestamp'] = pd.to_datetime(df[single_timestamp_col], errors='coerce', dayfirst=True)
                    if df['parsed_timestamp'].notna().any():
                        logging.info(f"Parsed {df['parsed_timestamp'].notna().sum()} timestamps using generic coerce.")
                    else:
                        logging.warning(
                            "No timestamps could be parsed from single timestamp column even with generic coerce.")

                logging.debug(f"First 5 parsed timestamps from single column: {df['parsed_timestamp'].head()}")
            else:
                logging.warning(f"Single timestamp column '{single_timestamp_col}' not found in DataFrame.")

        elif date_col and time_col:
            logging.info(f"Attempting to combine '{date_col}' and '{time_col}' for timestamp.")

            if date_col in df.columns and time_col in df.columns:
                df['temp_combined_dt'] = df[date_col].astype(str) + ' ' + df[time_col].astype(str)

                logging.debug(
                    f"Raw combined '{date_col}' and '{time_col}' column head before parsing:\n{df['temp_combined_dt'].head(20).to_string()}")

                def parse_complex_datetime(dt_str):
                    if pd.isna(dt_str) or not isinstance(dt_str, str):
                        return pd.NaT

                    cleaned_str = re.sub(r'\(UTC[+-]\d+\)', '', dt_str).strip()

                    match_double_date_time = re.search(
                        r'(\d{2}\.\d{2}\.\d{4})\s+\d{2}\.\d{2}\.\d{4}\s+(\d{2}:\d{2}:\d{2})', cleaned_str)
                    if match_double_date_time:
                        cleaned_str_for_parsing = f"{match_double_date_time.group(1)} {match_double_date_time.group(2)}"
                        try:
                            return pd.to_datetime(cleaned_str_for_parsing, format='%d.%m.%Y %H:%M:%S')
                        except ValueError:
                            pass

                    try:
                        return pd.to_datetime(cleaned_str, format='%d.%m.%Y %H:%M:%S', dayfirst=True)
                    except ValueError:
                        pass

                    try:
                        return pd.to_datetime(cleaned_str, errors='coerce', dayfirst=True)
                    except ValueError:
                        return pd.NaT

                df['parsed_timestamp'] = df['temp_combined_dt'].apply(parse_complex_datetime)

                if df['parsed_timestamp'].isnull().all():
                    logging.warning("No timestamps could be parsed from 'Date' and 'Time' columns.")
                else:
                    logging.info(f"Successfully parsed {df['parsed_timestamp'].notna().sum()} timestamps.")
            else:
                logging.warning(
                    f"Date column '{date_col}' or Time column '{time_col}' not found in DataFrame for combined timestamp parsing.")

        # --- Start of improved coordinate extraction ---
        # First, try to fill Latitude_Final/Longitude_Final from existing Lat/Lon columns if they exist and have data
        if lat_col_for_data and lon_col_for_data:
            logging.info(f"Prioritizing coordinates from '{lat_col_for_data}' and '{lon_col_for_data}' columns.")

            if lat_col_for_data in df.columns and lon_col_for_data in df.columns:
                logging.debug(
                    f"Raw '{lat_col_for_data}' column head before conversion:\n{df[lat_col_for_data].head(10).to_string()}")
                logging.debug(
                    f"Raw '{lon_col_for_data}' column head before conversion:\n{df[lon_col_for_data].head(10).to_string()}")

                # Convert existing Latitude/Longitude columns to numeric, coercing errors
                temp_lat = pd.to_numeric(df[lat_col_for_data].astype(str).str.replace(',', '.', regex=False),
                                         errors='coerce')
                temp_lon = pd.to_numeric(df[lon_col_for_data].astype(str).str.replace(',', '.', regex=False),
                                         errors='coerce')

                # Update Latitude_Final/Longitude_Final only where they are currently NaN
                # and where the conversion from Lat/Lon columns was successful
                mask_valid_direct_coords = temp_lat.notna() & temp_lon.notna()
                df.loc[mask_valid_direct_coords, 'Latitude_Final'] = temp_lat[mask_valid_direct_coords]
                df.loc[mask_valid_direct_coords, 'Longitude_Final'] = temp_lon[mask_valid_direct_coords]
            else:
                logging.debug(
                    f"Latitude column '{lat_col_for_data}' or Longitude column '{lon_col_for_data}' not found for raw data logging.")

            logging.debug(
                f"Converted 'Latitude_Final' column head after direct Lat/Lon parsing:\n{df['Latitude_Final'].head(10).to_string()}")
            logging.debug(
                f"Converted 'Longitude_Final' column head after direct Lat/Lon parsing:\n{df['Longitude_Final'].head(10).to_string()}")

        mask_missing_coords = df['Latitude_Final'].isna() | df['Longitude_Final'].isna()
        if mask_missing_coords.any():
            logging.info("Attempting to extract coordinates from text columns for missing entries...")

            def extract_coords_from_specific_text(text_value):
                """Extracts (latitude, longitude) from a string."""
                if pd.isna(text_value):
                    return pd.NaT, pd.NaT  # Return NaT for both if input is NaN

                text = str(text_value)
                # Regex to find (latitude, longitude) pattern
                match = re.search(r'\(([-+]?\d{1,3}\.\d+),\s*([-+]?\d{1,3}\.\d+)\)', text)
                if match:
                    try:
                        lat = float(match.group(1))
                        lon = float(match.group(2))
                        return lat, lon
                    except ValueError:
                        pass  # Conversion to float failed
                return pd.NaT, pd.NaT  # Return NaT for both if no match or conversion failed

            for col_name_candidate in text_coord_col_candidates:
                if col_name_candidate in df.columns:
                    logging.debug(
                        f"Raw '{col_name_candidate}' column head before text coord extraction:\n{df[col_name_candidate].head(20).to_string()}")

                    # Apply extraction only to rows that still have missing coordinates
                    # and for the current text column candidate
                    temp_extracted = df.loc[mask_missing_coords, col_name_candidate].apply(
                        extract_coords_from_specific_text
                    )

                    # Unpack the Series of tuples into two new Series
                    # Ensure handling of NaT (which pd.isna will detect for tuple of NaT)
                    extracted_lat = temp_extracted.apply(
                        lambda x: x[0] if isinstance(x, tuple) and pd.notna(x[0]) else np.nan)
                    extracted_lon = temp_extracted.apply(
                        lambda x: x[1] if isinstance(x, tuple) and pd.notna(x[1]) else np.nan)

                    # Identify which of these newly extracted coordinates are valid
                    mask_newly_valid = extracted_lat.notna() & extracted_lon.notna()

                    # Get the indices of the original DataFrame where these new coords are valid
                    indices_to_update = temp_extracted.index[mask_newly_valid]

                    # Update Latitude_Final and Longitude_Final in the original DataFrame
                    # only for the rows that were missing coords and where extraction was successful
                    df.loc[indices_to_update, 'Latitude_Final'] = extracted_lat.loc[indices_to_update]
                    df.loc[indices_to_update, 'Longitude_Final'] = extracted_lon.loc[indices_to_update]

                    newly_extracted_count = len(indices_to_update)
                    if newly_extracted_count > 0:
                        logging.info(
                            f"Successfully extracted coordinates for {newly_extracted_count} entries from '{col_name_candidate}'.")

                # Re-evaluate mask for next iteration
                mask_missing_coords = df['Latitude_Final'].isna() | df['Longitude_Final'].isna()
                if not mask_missing_coords.any():
                    break  # All missing coordinates filled

        else:
            logging.info("No missing coordinates to extract from text column.")

        # --- End of improved coordinate extraction ---

        df_filtered = df[df['Latitude_Final'].notna() & df['Longitude_Final'].notna()].copy()

        logging.info(f"Number of valid data points after full cleaning and coordinate extraction: {len(df_filtered)}")
        logging.debug("Returned from load_and_prepare_excel_data.")

        # Determine the final list of popup columns based on what's available in the DataFrame
        # and what the user requested.
        final_popup_cols = [col for col in user_requested_popup_cols if col in df_filtered.columns]

        return df_filtered, lat_col_for_data, lon_col_for_data, date_col, time_col, single_timestamp_col, final_popup_cols

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load or process Excel file: {e}")
        logging.error(f"Error loading or processing Excel file: {e}")
        return pd.DataFrame(), None, None, None, None, None, None


def generate_map(data_df, lat_col, lon_col, time_col, popup_text_cols):
    """
    Generates an HTML map from the processed DataFrame.
    If timestamps are present, it creates an animated map.
    Otherwise, it creates a static map with markers.
    """
    if data_df.empty:
        messagebox.showinfo("Map Generation", "No valid data points to display on the map.")
        return

    timed_points_df = data_df[data_df['parsed_timestamp'].notna()].copy()
    static_points_df = data_df[data_df['parsed_timestamp'].isna()].copy()

    logging.info(f"Points with valid timestamps for animation: {len(timed_points_df)}")
    logging.info(f"Points without valid timestamps (static): {len(static_points_df)}")

    if not data_df.empty:
        center_lat = data_df['Latitude_Final'].mean()
        center_lon = data_df['Longitude_Final'].mean()
    else:
        center_lat, center_lon = 0, 0

    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    if not static_points_df.empty:
        marker_cluster_static = MarkerCluster().add_to(m)
        for idx, row in static_points_df.iterrows():
            popup_html = ""  # Start with empty string for dynamic content

            # Add requested columns to popup if they exist and are not empty
            for col_name in popup_text_cols:
                # Special handling for 'Time' to use the original or parsed if original is missing/empty
                if col_name == 'Time' and 'parsed_timestamp' in row and pd.notna(row['parsed_timestamp']):
                    popup_html += f"<b>Time:</b> {row['parsed_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>"
                elif col_name in row and pd.notna(row[col_name]):
                    display_col_name = col_name.replace('_', ' ').title()
                    popup_html += f"<b>{display_col_name}:</b> {row[col_name]}<br>"

            # Always add Lat/Lon at the end if they are valid
            if pd.notna(row['Latitude_Final']) and pd.notna(row['Longitude_Final']):
                popup_html += f"<b>Lat:</b> {row['Latitude_Final']:.4f}<br><b>Lon:</b> {row['Longitude_Final']:.4f}<br>"

            folium.Marker(
                location=[row['Latitude_Final'], row['Longitude_Final']],
                popup=popup_html,
                tooltip="Static Point"
            ).add_to(marker_cluster_static)
        logging.info(f"Added {len(static_points_df)} static points to the map.")

    if not timed_points_df.empty:
        logging.debug("Preparing timed points for animation.")
        features = []
        for idx, row in timed_points_df.iterrows():
            if pd.notna(row['parsed_timestamp']):
                properties = {
                    "time": row['parsed_timestamp'].isoformat(),
                    "popup": ""  # Start with empty string for dynamic content
                }

                # Add requested columns to popup if they exist and are not empty
                for col_name in popup_text_cols:
                    # Special handling for 'Time' to use the original or parsed if original is missing/empty
                    if col_name == 'Time' and 'parsed_timestamp' in row and pd.notna(row['parsed_timestamp']):
                        properties[
                            "popup"] += f"<b>Time:</b> {row['parsed_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>"
                    elif col_name in row and pd.notna(row[col_name]):
                        display_col_name = col_name.replace('_', ' ').title()
                        properties["popup"] += f"<b>{display_col_name}:</b> {row[col_name]}<br>"

                # Always add Lat/Lon at the end if they are valid
                if pd.notna(row['Latitude_Final']) and pd.notna(row['Longitude_Final']):
                    properties[
                        "popup"] += f"<b>Lat:</b> {row['Latitude_Final']:.4f}<br><b>Lon:</b> {row['Longitude_Final']:.4f}<br>"

                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [row['Longitude_Final'], row['Latitude_Final']],
                    },
                    "properties": properties,
                })

        if features:
            features.sort(key=lambda x: x['properties']['time'])

            TimestampedGeoJson(
                {
                    "type": "FeatureCollection",
                    "features": features,
                },
                period="PT1H",
                add_last_point=True,
                auto_play=False,
                loop=False,
                max_speed=100,
                min_speed=0.1,
                loop_button=True,
                date_options="YYYY/MM/DD HH:MM:SS",
                transition_time=100
            ).add_to(m)
            logging.info(f"Added {len(features)} animated points to the map.")
        else:
            logging.warning("No timed points found for animation after filtering.")
            messagebox.showinfo("Map Generation",
                                "No timed points found for animation. Only static points will be shown if available.")
    else:
        logging.info("No timed points found for animation.")

    output_html_file = "koordinaten_karte.html"
    logging.debug("Saving the map HTML file.")
    m.save(output_html_file)
    logging.info(f"Map successfully saved as '{output_html_file}'.")
    messagebox.showinfo("Map Generated", f"Map saved to '{output_html_file}'")
    logging.debug("Showing success messagebox.")


def main():
    file_path = get_file_path()
    if not file_path:
        logging.info("No file selected. Exiting.")
        return

    configure_logging(file_path)

    data_df, lat_col, lon_col, date_col, time_col, single_timestamp_col, popup_text_cols_final = load_and_prepare_excel_data(
        file_path)

    if data_df.empty:
        logging.warning("No valid data loaded from Excel. Cannot generate map.")
        return

    # Pass the finally determined popup columns to generate_map
    generate_map(data_df, lat_col, lon_col, 'parsed_timestamp', popup_text_cols_final)


if __name__ == "__main__":
    main()