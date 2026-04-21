import pytest
import os
from tools import file, search, shell

@pytest.fixture
def temp_workdir(tmp_path):
    # Set workdir for tools
    file.WORKDIR = str(tmp_path)
    search.WORKDIR = str(tmp_path)
    shell.WORKDIR = str(tmp_path)
    return tmp_path

def test_file_write_read(temp_workdir):
    file_path = "test.txt"
    content = "Hello Forge"
    
    # Test Write
    res_write = file.tool_write(file_path, content)
    assert "Written" in res_write
    assert (temp_workdir / file_path).exists()
    
    # Test Read
    res_read = file.tool_read(file_path)
    assert content in res_read

def test_file_mkdir_list(temp_workdir):
    dir_name = "new_folder"
    file.tool_mkdir(dir_name)
    assert (temp_workdir / dir_name).is_dir()
    
    res_list = search.tool_list()
    assert "[D] new_folder" in res_list

def test_shell_tool(temp_workdir):
    # Test simple echo
    res = shell.tool_shell("echo forge_test")
    assert "forge_test" in res
    assert "[exit: 0]" in res
