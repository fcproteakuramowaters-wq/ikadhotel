Static site export and Vercel deployment
======================================

This repository can be exported to a static site and deployed to Vercel (or Netlify). A helper script is provided to render the site and copy static assets.

How to export to static files (locally)
--------------------------------------

1. Activate your Python virtualenv and install requirements (same as development):

```powershell
cd "C:\Users\vkayo841\Documents\Current-link and Marriott Phase 2\CUrrent_link\ikadhotel"
pip install -r requirements.txt
```

2. Run the export script (it will create a `public/` folder):

```powershell
python scripts/export_static.py
```

3. Verify the `public/` folder contains `index.html` and a `static/` folder with assets.

Deploy to Vercel
----------------

1. Install the Vercel CLI (optional) and login:
```powershell
npm i -g vercel
vercel login
```

2. From the project root, run:
```powershell
vercel --prod
```

When Vercel asks what to deploy, choose the `public/` folder. You can also connect the GitHub repository in the Vercel web UI and set the 'Build & Output Settings' to use the `public` directory.

Notes
-----

- The export script uses Django's test client to render pages. If some views require database data, ensure the local database file exists (or adjust views to work without DB) before exporting.
- If some pages are missing after export, rerun the script adding their paths to the `initial` list in `scripts/export_static.py`.
