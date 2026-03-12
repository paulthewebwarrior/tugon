# Deployment to PythonAnywhere

## Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account
3. Verify your email

## Step 2: Upload Files
1. Log in to PythonAnywhere
2. Go to **Files** tab
3. Upload these files/folders:
   - `app.py`
   - `database.py`
   - `requirements.txt`
   - `templates/` (entire folder)
   - `static/` (entire folder)
   - `data/tugon.db` (upload to a `data` folder you create)

## Step 3: Create Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Select **Flask** and Python version (e.g., 3.10)
4. For the WSGI configuration file, click to edit it

## Step 4: Configure WSGI
Edit the WSGI file to point to your app:

```python
import sys

# Add your project directory to the path
path = '/home/YOUR_USERNAME/'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

## Step 5: Install Dependencies
1. Go to **Consoles** tab
2. Start a Bash console
3. Run:
   ```
   pip install -r requirements.txt
   ```

## Step 6: Reload
1. Go to **Web** tab
2. Click **Reload** button

## Step 7: Visit Your Site
Your site will be available at: `https://yourusername.pythonanywhere.com`

---

## Troubleshooting

### 500 Error
- Check the **Web** tab → Click "Last 100 lines of error log"
- Common issues: missing files, database path issues

### Database not found
- Make sure `data/tugon.db` is uploaded to a `data` folder
- The path in database.py uses relative path from app.py location

### Static files not loading
- Make sure `static/` folder is uploaded with correct structure
- Go to **Web** tab → Check "Static files" section matches your /static URL

---

## Updating Your Site
1. Upload new files via **Files** tab
2. Go to **Web** tab
3. Click **Reload**
