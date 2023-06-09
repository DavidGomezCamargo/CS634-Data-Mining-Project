# Installation Instructions

### Docker Desktop WSL 2 backend on Windows

1. Download <a href="https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?_gl=1*fclmnk*_ga*OTkwODUyOTg2LjE2ODYyMzk1ODI.*_ga_XJWPQMJYHQ*MTY4NjI1OTYwNi4yLjEuMTY4NjI1OTYwNy41OS4wLjA.">Docker Desktop for Windows.</a>
2. Follow the usual installation instructions to install Docker Desktop. If you are running a supported system, Docker Desktop prompts you to enable WSL 2 during installation. Read the information displayed on the screen and enable WSL 2 to continue. <a href="https://docs.docker.com/desktop/windows/wsl/">Install WSL command.</a>
3. Start Docker Desktop from the Windows Start menu.
4. From the Docker menu, select Settings and then General.
5. Select the Use WSL 2 based engine check box.
6. Select Apply & Restart.

Now docker commands work from Windows using the new WSL 2 engine.

# Set up a Development Environment

### Docker in action

1. Open a terminal window and create a new directory.
<pre><code>$ mkdir hello-docker </pre></code>
<pre><code>$ cd hello-docker </pre></code>
2. Open your editor and create a new file "app.js".
<pre><code>console.log("Hello Docker!"); </pre></code>
3. Create a file "Dockerfile".
<pre><code>FROM node:alpine
COPY . /app
WORKDIR /app
CMD node app.js </pre></code>
4. On the terminal window package the application.
<pre><code>$ docker build -t hello-docker . </pre></code>
<pre><code>$ docker image ls </pre></code>
5. Run Hello-docker.
<pre><code>$ docker run hello-docker </pre></code>
And the result must be <em>Hello Docker!</em>
6. Run Ubuntu (open-source Linux-based operating system).
<pre><code>$ docker run ubuntu</pre></code>
7. Start a container in the interactive mode using the Ubuntu image.
<pre><code>$ docker run -it ubuntu</pre></code>
<pre><code>{Shell prompt}:/# </pre></code>

# Screenshot of Docker container terminal prompt.
<img src="david\OneDrive\Pictures\Screenshots\Screenshot (118).png">
