# Utilities

## AAP Domains Bookmarklet

The AAP UI allows grouping job templates and workflows into domains based on labels. Domain configuration is stored in the browser's local storage, so it doesn't transfer between browsers or AAP instances. These tools let you generate a bookmarklet to import the [APD domain configuration](domains.json) into a new browser or AAP deployment.

### Files

- **`domains.json`** — The domains configuration to import. Edit this file to change the domain groupings.
- **`generate-bookmarklet.sh`** — Generates a `javascript:` bookmarklet URL from `domains.json`.

### Generating the import bookmarklet

```bash
./utils/generate-bookmarklet.sh
```

This outputs a `javascript:` URL. Copy the entire output, then create a bookmark for it using the steps below.

#### Firefox

1. Press `Ctrl+D` (or `Cmd+D` on macOS) to open the bookmark dialog.
2. Give it a name (e.g. "Import APD Domains") and save it.
3. Open the Library (`Ctrl+Shift+O` / `Cmd+Shift+O`), find the bookmark, and right-click it.
4. Select **Properties** and replace the URL field with the `javascript:` URL from the generator.
5. Click **Save**.

#### Chrome

1. Open the Bookmark Manager (`Ctrl+Shift+O` / `Cmd+Shift+O`).
2. Click the three-dot menu in the top right and select **Add new bookmark**.
3. Set the name (e.g. "Import APD Domains") and paste the `javascript:` URL into the URL field.
4. Click **Save**.

### Importing domains into a new AAP instance

1. Navigate to the AAP instance in your browser.
2. Click the import bookmarklet from the bookmarks bar or menu. The page will reload with the domains configuration applied.
