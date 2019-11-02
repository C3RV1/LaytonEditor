import LaytonLib.gds

with open("../q105_param.gds", "rb") as file:
    raw = file.read()

script = LaytonLib.gds.GDSScript.from_bytes(raw)
print(script.to_simplified())