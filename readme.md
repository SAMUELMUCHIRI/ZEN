# ZEN
> ### a Static Site Generator made in Python

## Usage
<ol>
<li>Develop executables  in the root</li>

- The Tests are located in the src Folder with a prefix of  <strong>test_</strong>
- The main.sh build sthe file for local development
- The build.sh build s the file for Github pages deployment .
```bash
# for linux 
chmod +x test.sh
chmod +x main.sh
chmod +x build.sh
 # For tests
 ./test.sh
 # to build the project locally
 ./main.sh
 # For deploying to Github pages
 ./build.sh

```
<li>Directory Structure</li>

```bash
  
├──   .git
├──   .gitignore
├──   build.sh # For deploying to Github pages
├──   content
│  ├── # The markdown to Be converted are placed here with their direcoties
├──   docs
│  ├── # Files build for Github pages appear here
├──   main.sh # Executable for local development
├──   readme.md
├──   src # Tests and Logic are Contained here 
│  ├──   __pycache__
│  ├──   block.py
│  ├──   delimiters.py
│  ├──   functions.py
│  ├──   htmlnode.py
│  ├──   index.html
│  ├──   main.py
│  ├──   test_block.py
│  ├──   test_functions.py
│  ├──   test_htmlnode.py
│  ├──   test_textnode.py
│  ├──   testdata.py
│  └──   textnode.py
├──   static  # Place all the assets here to be accessed  by your site
│  ├──   images
│  └──   index.css
├──   template.html # Html template to be used
└──   test.sh # Directory structure
```
<li>How it all works </li>

 ```bash
+----------------------+        +----------------------+        +-----------------------------+
|        MARKDOWN      |        |          NODES       |        |            HTML             |
|                      |        |                      |        |                             |
|  # Header            |        |  # Header            |        |  <html>                     |
|                      |        |   |                  |        |    <body>                   |
|                      |        |       |              |        |      <header>Header</header>|
|  Paragraph           |        |   +-- Paragraph      |        |                             |
|  - List item         | --->   |       +-- List item  | --->   |      <p>Paragraph</p>       |
|  - List item         |        |       +-- List item  |        |                             |
|                      |        |                      |        |      <ul>                   |
|  [link](somewhere)   |        |  [link](somewhere)   |        |        <li>List item</li>   |
|                      |        |                      |        |        <li>List item</li>   |
|  ![image](something) |        |  ![image](something) |        |      </ul>                  |
|                      |        |                      |        |                             |
|  _italics_           |        |  _italics_           |        |      <em>italics</em>       |
|                      |        |                      |        |                             |
|  **bold**            |        |  **bold**            |        |      <strong>bold</strong>  |
|                      |        |                      |        |                             |
+----------------------+        +----------------------+        +-----------------------------+

 ```
</ol>

## This Repo static site is [Deployed Here](https://samuelmuchiri.github.io/ZEN/)


> Have fun Forking and Coding 
<br>
> The Project uses just Python internal libraries