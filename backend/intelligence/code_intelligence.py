import difflib
from tree_sitter import Language, Parser
import tree_sitter_languages
import os
import logging

class CodeIntelligenceEngine:
    def __init__(self, root_dir="/data/data/com.termux/files/home/Monu-1"):
        self.root_dir = root_dir
        self.logger = logging.getLogger("CodeIntelligenceEngine")

    def analyze_code(self, file_path, language_name):
        full_path = os.path.join(self.root_dir, file_path)
        if not os.path.exists(full_path):
            return {"error": "File not found"}
        
        parser = Parser()
        language = tree_sitter_languages.get_language(language_name)
        parser.set_language(language)
        
        with open(full_path, "rb") as f:
            tree = parser.parse(f.read())
            
        root_node = tree.root_node
        return {"root": root_node.type, "children": [child.type for child in root_node.children]}

    def propose_patch(self, file_path, original_code, new_code):
        # 1. Generate diff using difflib
        diff = difflib.unified_diff(
            original_code.splitlines(),
            new_code.splitlines(),
            fromfile=file_path,
            tofile=file_path + ".new",
            lineterm=''
        )
        return {"status": "PROPOSED", "diff": "\n".join(diff)}
