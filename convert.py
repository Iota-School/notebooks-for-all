from nbconvert import get_exporter

exporter = get_exporter("html5")

out = exporter().from_filename("tests/notebooks/lorenz.ipynb")


with open("tests/out.html", "w") as out_file:
    out_file.write(str(out[0]))
