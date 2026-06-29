import webbrowser

def open_website(name, url):
    print(f"Opening {name} buddy.")
    webbrowser.open(url)

    websites = {
    "google": ("Google", "https://www.google.com"),
    "youtube": ("YouTube", "https://www.youtube.com"),
    "github": ("GitHub", "https://github.com"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com")
}