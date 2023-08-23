import glob
import os
import subprocess
import re


def compile_protos():
    proto_path = f"protos"
    output_dir = "gradiently/protos"

    protos_pattern = f"{proto_path}/**/*.proto"  # update here
    proto_files = glob.glob(protos_pattern, recursive=True)  # update here
    js_output_dir = "ui/src/protos"  # added this line
    js_out = f"{js_output_dir}/"  # added this line

    if not proto_files:
        print(f"No .proto files found in {proto_path}")
        return

    python_out = f"{output_dir}/"

    if not os.path.exists(python_out):
        os.makedirs(python_out)
        
    if not os.path.exists(js_out):  # added this block
        os.makedirs(js_out)        

    command = [
        "python",
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_path}",
        f"--python_out={python_out}",
        f"--grpc_python_out={python_out}",
        # for JS. npm install -g protoc-gen-js
        f"--js_out=import_style=commonjs,binary:{js_out}",
        f"--grpc-web_out=import_style=commonjs+dts,mode=grpcweb:{js_out}",        
        *proto_files,
    ]

    try:
        subprocess.check_call(command)
        print("Protos compiled successfully!")
        update_import_statements(python_out)
        print("Updated protos successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print(
            "Error: grpc_tools.protoc not found. Make sure you have gRPC tools installed."
        )


def update_import_statements(proto_directory: str):
    PROTO_SUBDIRS = ["core", "services"]

    for root, subdirs, files in os.walk(proto_directory):
        for subdir in subdirs:
            if subdir not in PROTO_SUBDIRS:
                continue
            subdir_path = os.path.join(root, subdir)

            for filename in os.listdir(subdir_path):
                print(filename, "SHIIT", subdir)
                if filename.endswith("pb2.py") or filename.endswith("grpc.py"):
                    filepath = os.path.join(root, subdir, filename)
                    with open(filepath, "r") as file:
                        content = file.read()

                    # Use regular expression to find the import statements
                    # and replace them with the absolute import paths
                    updated_content = re.sub(
                        r"from gradiently.(\w+)(\s+.*)",
                        rf"from gradiently.protos.gradiently.\1\2",
                        content,
                        flags=re.MULTILINE,
                    )

                    print(updated_content)

                    # Write the updated content back to the file
                    with open(filepath, "w") as file:
                        file.write(updated_content)


if __name__ == "__main__":
    compile_protos()
