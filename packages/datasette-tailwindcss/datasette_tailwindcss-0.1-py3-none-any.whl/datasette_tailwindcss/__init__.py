from datasette import hookimpl

@hookimpl
def extra_js_urls():
    return ["/-/static-plugins/datasette-tailwindcss/tailwindcss_v3_3_3.js"]
