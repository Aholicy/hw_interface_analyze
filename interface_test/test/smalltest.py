import re

class_methods_content = """
onInit(want: Want): void;
onConnect(want: Want): rpc.RemoteObject | Promise<rpc.RemoteObject> {
    // method body
}
onRelease(): void;
onDisconnect(want: Want): void | Promise<void>;
onDump(params: Array<string>): Array<string>;
"""

method_matches = re.finditer(
    r"(\w+)\s?\(([^)]*)\)\s*:\s*([\w<>\|\[\]]+(\s*\|\s*[\w<>\|\[\]]+)*)\s*(?=\s*({|;))"
,
    class_methods_content
)


for match in method_matches:
    print(match.group(0))  # This will print the matched method signatures
