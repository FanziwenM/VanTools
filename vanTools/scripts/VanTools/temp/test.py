import sys

print(sys.platform)

sys.stderr.write(
    "Failed to register command: %s\n" % "aaa"
)
a = [1, 2, 3]
try:
    a[3]
except Exception as e:
    traceback.print_exc()