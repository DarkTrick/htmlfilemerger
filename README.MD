# What is this?

Program to Merge JS/HTML into one single html file.

![depiction of what the tool does](./ref/tool_explanation.png)


# Install / Run
## Run without Installation
```
# (download everything)
cd ./src
python3 htmlmerger inputfile [optional: outputfile]
```

## Install & Run
```
# install:
#(download everything)
cd ./src
python3 -m pip install .

# run:
htmlmerger inputfile [optional: outputfile]
```

# Dependencies

Only python-native libraries (`os`, `base64`, `html.parser`)


# Development

See [Readme within `src`](./src/README.MD)