# What is this?

Program to Merge JS/HTML into one single html file.

![depiction of what the tool does](./ref/tool_explanation.png)


# Install / Run

## Install
`pip install git+https://github.com/DarkTrick/htmlfilemerger.git#subdirectory=src`

## Uninstall
`pip uninstall htmlmerger`

## Run

`htmlmerger inputfile [optional: outputfile]`

## Run without Installation
```
cd ./src
python3 -m htmlmerger inputfile [optional: outputfile]
```

# Dependencies

Only python-native libraries (`os`, `base64`, `html.parser`)


# Development

See also [Readme within `src`](./src/README.MD)
## venv
(No external packages are needed so far; so no venv should be necessary)

## Testing

```
cd ./src
python -m unittest
```

There are also files for manual testing in `... /test_manual/`

## Build
```
cd src
pip install build # <-- only if not yet installed
python -m build
```