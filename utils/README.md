# Utilities

## AAP Domains Bookmarklet

The AAP UI allows grouping job templates and workflows into domains based on labels. Domain configuration is stored in the browser's local storage, so it doesn't transfer between browsers or AAP instances. These tools let you generate a bookmarklet to import the [APD domain configuration](apd-domains.json) into a new browser or AAP deployment.

### Files

- **`generate-bookmarklet.sh`** — Generates a `javascript:` bookmarklet URL from `apd-domains.json`.
- **`apd-domains.json`** — The domains configuration to import. Edit this file to change the domain groupings if needed.
- **`apd-domain-bookmarklet.js`** - Pre-populated javascript bookmarklet URL that can be used instead of generating one.

### Generating the import bookmarklet

```bash
./utils/generate-bookmarklet.sh
```

This outputs a `javascript:` URL from `apd-domains.json`. Copy the entire output, then create a bookmark for it using the steps below.  

Alternately, use the content of `apd-domains-bookmarklet.js` directly in the browser bookmark configured below.

#### Firefox

1. Open the Bookmark Library (`Ctrl+Shift+O` / `Cmd+Shift+O`).
2. Click the gear icon in the top left and select **Add new bookmark**.
3. Set the name (e.g. "Import APD Domains") and paste either the contents of the pre-built `apd-domains-bookmarklet.js` file, or the `javascript:` URL from the generator in the URL field.
4. Click **Save**.

#### Chrome

1. Open the Bookmark Manager (`Ctrl+Shift+O` / `Cmd+Shift+O`).
2. Click the three-dot menu in the top right and select **Add new bookmark**.
3. Set the name (e.g. "Import APD Domains") and paste either the contents of the pre-built `apd-domains-bookmarklet.js` file, or the `javascript:` URL from the generator in the URL field.
4. Click **Save**.

### Importing domains into a new AAP instance

1. Navigate to the AAP instance in your browser.
2. Click the import bookmarklet from the bookmarks bar or menu. The page will reload with the domains configuration applied.
