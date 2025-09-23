# The `static` Folder  
This is an empty file:

This folder contains all the static assets for the Flask application, which are files served directly to the user's browser without being processed by the server-side Python code.

## Purpose

Even though the application may currently load assets like Bootstrap and jQuery from external CDNs, this folder is the designated location for any **custom, self-hosted files**.

You should place files in the following sub-directories:

*   `static/css/`: For your custom stylesheets (e.g., `custom_style.css`).
*   `static/js/`: For your custom JavaScript files (e.g., `main.js`).
*   `static/images/`: For images like logos, backgrounds, or other graphical assets.

## Why It's Here

Including this folder in the project structure, even when empty, is a best practice. It clearly communicates where static assets should go, making the project easier to maintain and scale.
