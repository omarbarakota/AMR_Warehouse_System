
# Project Static Files Structure

This document explains the structure and usage of the static files in this project. The static files are organized into three main folders: `css/`, `js/`, and `img/`. Each folder contains files that are used to style, add functionality, and provide images for the corresponding HTML files.

---

## Folder Structure

```bash
project-folder/
│
├── static/
│   ├── css/                  # Contains CSS files for styling
│   │   ├── index.css         # Styles for index.html
│   │   ├── about.css         # Styles for about.html
│   │   └── contact.css       # Styles for contact.html
│   │
│   ├── js/                   # Contains JavaScript files for functionality
│   │   ├── main.js           # Common JavaScript for all pages
│   │   ├── index.js          # JavaScript specific to index.html
│   │   └── contact.js        # JavaScript specific to contact.html
│   │
│   └── img/                  # Contains images used in the project
│       ├── logo.png          # Logo image
│       ├── banner.jpg        # Banner image for the homepage
│       └── profile.jpg       # Profile image for the about page
│
└── templates/                # Contains HTML files
    ├── index.html            # Homepage
    ├── about.html            # About page
    └── contact.html          # Contact page
```

---

## Usage of Static Files

### 1. **CSS Files (`css/`)**

Each CSS file is specific to a particular HTML file. Here’s how they are used:

- **`index.css`**: Styles for `index.html` (Homepage).
- **`about.css`**: Styles for `about.html` (About Page).
- **`contact.css`**: Styles for `contact.html` (Contact Page).

To link a CSS file to an HTML file, use the following code in the `<head>` section of the HTML file:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
```

(Replace `index.css` with the appropriate CSS file name.)

---

### 2. **JavaScript Files (`js/`)**

JavaScript files are used to add interactivity and functionality to the project. Here’s how they are used:

- **`main.js`**: Common JavaScript used across all pages.
- **`index.js`**: JavaScript specific to `index.html`.
- **`contact.js`**: JavaScript specific to `contact.html`.

To link a JavaScript file to an HTML file, use the following code at the end of the `<body>` section of the HTML file:

```html
<script src="{{ url_for('static', filename='js/index.js') }}"></script>
```

(Replace `index.js` with the appropriate JavaScript file name.)

---

### 3. **Images (`img/`)**

Images are stored in the `img/` folder and are used in the HTML files. Here’s how they are used:

- **`logo.png`**: Logo image used in the navigation bar.
- **`banner.jpg`**: Banner image for the homepage.
- **`profile.jpg`**: Profile image for the about page.

To use an image in an HTML file, use the following code:

```html
<img src="{{ url_for('static', filename='img/logo.png') }}" alt="Logo">
```

(Replace `logo.png` with the appropriate image file name.)

---

## How to Use This Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. **Navigate to the Project Folder**:

   ```bash
   cd your-repo-name
   ```

3. **Run the Application**:
   If this is a web application (e.g., Flask or Django), follow the instructions in the main `README.md` file to set up and run the project.

4. **View the HTML Files**:
   Open the HTML files in your browser to see the styled and functional pages.

---

## Notes for Contributors

- **CSS**: Add new CSS files in the `css/` folder and link them to the corresponding HTML files.
- **JavaScript**: Add new JavaScript files in the `js/` folder and link them to the corresponding HTML files.
- **Images**: Add new images in the `img/` folder and reference them in the HTML files.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
