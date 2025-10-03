# Custom SunSpec Models

This directory contains custom SunSpec model definitions.

## Adding Custom Models

### SMDX Format (XML)
Place `.xml` files in the `smdx/` subdirectory:
```
models/
  smdx/
    smdx_12345.xml
```

### JSON Format
Place `.json` files in the `json/` subdirectory:
```
models/
  json/
    model_12345.json
```

## Where to find models

- Official SunSpec models: https://github.com/sunspec/models
- Download from: https://github.com/sunspec/models/tree/master/smdx

## Example: Adding model 64110 (SMA specific)

1. Download the model from SunSpec repository
2. Copy to `smdx/smdx_64110.xml`
3. Rebuild the add-on
4. The model will be automatically detected

## Automatic Discovery

The pySunSpec2 library automatically:
- Scans the device for all available models
- Loads definitions from this directory
- Falls back to built-in models if available
