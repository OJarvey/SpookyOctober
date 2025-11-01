# Haunted Places CSV Import Instructions

## Overview

This document describes how to import haunted places into the ShriekedIn database using CSV files. There are two methods available:

1. **Admin Interface** (Recommended) - Easy-to-use web interface for admin users
2. **Management Command** - Command-line tool for bulk imports

## Method 1: Admin Interface (Recommended)

### Steps:

1. Log in to the Django admin at `/admin/`
2. Navigate to **Core → Haunted Places**
3. Click the **"Import from CSV"** button in the top right corner
4. Upload your CSV file
5. Optionally check **"Update Existing"** if you want to update haunted places that already exist
6. Click **"Import CSV"**
7. Review the import summary showing how many places were imported, updated, or skipped

### Features:

- User-friendly interface
- Real-time feedback on import results
- Error reporting with specific row numbers
- Automatic location creation and verification
- Option to update existing entries

## Method 2: Management Command

### Basic Usage:

```bash
python manage.py import_haunted_places haunted_places.csv
```

### Advanced Options:

```bash
# Specify a different user as creator
python manage.py import_haunted_places haunted_places.csv --user=johndoe

# Update existing haunted places instead of skipping them
python manage.py import_haunted_places haunted_places.csv --update
```

### Command Options:

- `csv_file` (required) - Path to the CSV file
- `--user USERNAME` - Username to assign as creator (default: "admin")
- `--update` - Update existing haunted places if they already exist

## CSV File Format

### Required Columns:

Your CSV file must include the following columns (in any order):

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `name` | Text | Location name | "Ordsall Hall" |
| `address` | Text | Street address | "322 Ordsall Ln, Salford" |
| `city` | Text | City name | "Salford" |
| `state` | Text | State/region | "Greater Manchester" |
| `zip_code` | Text | Postal code | "M5 3AN" |
| `country` | Text | Country name | "United Kingdom" |
| `location_type` | Text | Type of location | "haunted" |
| `story_title` | Text | Title of the ghost story | "The White Lady of Ordsall Hall" |
| `story_content` | Text | The complete story | "Ordsall Hall is possibly..." |
| `historical_context` | Text | Historical background | "Built in the 15th century..." |
| `scare_level` | Integer | Scare level (1-5) | "4" |
| `year_established` | Integer | Year established (optional) | "1500" |
| `reported_phenomena` | Text | Paranormal activity | "The White Lady, cold zones..." |
| `famous_for` | Text | What makes it notable | "Most famously haunted building..." |
| `view_count` | Integer | Number of views (optional) | "1341" |
| `visit_count` | Integer | Number of visits (optional) | "245" |

### Sample CSV:

```csv
name,address,city,state,zip_code,country,location_type,story_title,story_content,historical_context,scare_level,year_established,reported_phenomena,famous_for,view_count,visit_count
Ordsall Hall,"322 Ordsall Ln, Salford",Salford,Greater Manchester,M5 3AN,United Kingdom,haunted,The White Lady of Ordsall Hall,"Ordsall Hall is possibly the most famously haunted building in Greater Manchester...","Built in the 15th century, Ordsall Hall is a historic house...",4,1500,"The White Lady, cold zones, footsteps","Most famously haunted building in Greater Manchester",1341,245
```

### Important Notes:

- Fields containing commas must be enclosed in double quotes
- Multi-line text fields should be enclosed in double quotes
- Leave optional fields empty if not available
- The header row is required
- UTF-8 encoding is required for special characters

## Import Behavior

### Location Handling:

- If a location with the same name doesn't exist, it will be created
- If a location exists, its details will be updated with the CSV data
- All imported locations are automatically marked as **verified**
- The currently logged-in user (or specified user) is set as the creator

### Haunted Place Handling:

- If a haunted place doesn't exist for the location, it will be created
- If a haunted place exists:
  - **Without `--update` flag**: The entry is skipped
  - **With `--update` flag**: The entry is updated with new data
- The creator is preserved when updating existing entries

### Error Handling:

- If a row has missing required columns, it will be skipped with an error message
- If a row has invalid data, it will be skipped with an error message
- The import continues processing remaining rows after encountering errors
- A summary is displayed at the end showing successful imports, updates, skips, and errors

## Example Import Session

```bash
$ python manage.py import_haunted_places haunted_places.csv

Starting import from haunted_places.csv
Creator: admin

Processing: Ordsall Hall...
  ✓ Imported: The White Lady of Ordsall Hall

Processing: Ryecroft Hall...
  ✓ Imported: The Victorian Ghost Child of Ryecroft Hall

Processing: Wardley Hall...
  ✓ Imported: The Screaming Skull of Wardley Hall

==================================================
Import completed!
  • New imports: 3
  • Updated: 0
  • Skipped: 0
==================================================
```

## Included Sample Data

A sample CSV file `haunted_places.csv` is included in the project root directory containing 3 haunted places from Manchester:

1. **Ordsall Hall** - The White Lady
2. **Ryecroft Hall** - The Victorian Ghost Child
3. **Wardley Hall** - The Screaming Skull

You can use this file to test the import functionality or as a template for your own data.

## Troubleshooting

### Common Issues:

**"User does not exist" error:**
- Make sure the specified user exists in the database
- Default user is "admin" - create this user if it doesn't exist
- Use `--user` flag to specify a different user

**"Missing column" error:**
- Verify all required columns are present in your CSV
- Check column names match exactly (case-sensitive)
- Ensure the header row is present

**"File not found" error:**
- Provide the full path to the CSV file
- Check that the file exists and is readable
- Verify file permissions

**Encoding errors:**
- Save your CSV file with UTF-8 encoding
- Avoid special characters that may not be compatible

## Security Considerations

- Only admin users can access the import functionality
- CSV files are processed server-side and not stored permanently
- All Django security protections (CSRF, XSS) are active
- Input validation is performed on all data

## Need Help?

If you encounter issues or need assistance:

1. Check the Django admin logs for detailed error messages
2. Review the CSV file format requirements
3. Verify you have the necessary permissions
4. Contact the development team for support
