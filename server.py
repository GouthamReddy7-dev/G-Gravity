from mcp.server import FastMCP
import os
mcp=FastMCP("access_files")


@mcp.tool()
def get_file_names()->list:
    """This is used to get all the file names that are in the current directory"""
    curr_dir=os.path.dirname(os.path.abspath(__file__))
    all_files=os.listdir(curr_dir)
    return all_files


@mcp.tool()
def read_file(filename:str)->str:
    """This is used to read the content of a file by filename"""
    with open(filename,"r") as f:
        content=f.read()
    return content

@mcp.tool()
def write_file(filename:str,file_content:str)->str:
    """This is used to write into a file and if file not available it creates a file and writes into it"""
    try:
        with open(filename,"w") as file:
            file.write(file_content)
        return "success !, written to the file"
    except Exception as e:
        return f"failed to write to file {e}"


if __name__=="__main__":
    mcp.run(transport="stdio")