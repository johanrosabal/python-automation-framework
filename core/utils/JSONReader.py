# core/utils/json_reader.py

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import traceback


class JSONReader:
    """Utility class for reading test metadata from JSON files."""

    @staticmethod
    def import_json(source: str) -> Dict[str, Any]:
        """
        Loads JSON data from a file path or returns dict if already parsed.

        Automatically resolves paths by detecting the project context.

        Args:
            source: File path (str) or already parsed dict

        Returns:
            dict: Parsed JSON data
        """
        if isinstance(source, dict):
            return source

        if isinstance(source, str):
            # Try as absolute path first
            if os.path.isabs(source) and os.path.exists(source):
                return JSONReader._load_file(source)

            # Try relative to current working directory
            cwd_path = Path.cwd() / source
            if cwd_path.exists():
                return JSONReader._load_file(str(cwd_path))

            # Try to detect project and resolve path
            resolved_path = JSONReader._resolve_project_path(source)
            if resolved_path and resolved_path.exists():
                return JSONReader._load_file(str(resolved_path))

            # Try as JSON string
            try:
                return json.loads(source)
            except json.JSONDecodeError:
                pass

            # File not found - provide helpful error
            raise FileNotFoundError(
                f"JSON file not found: {source}\n"
                f"Tried:\n"
                f"  - Absolute path: {source}\n"
                f"  - CWD: {cwd_path}\n"
                f"  - Project-relative: {resolved_path}\n"
                f"  Current directory: {Path.cwd()}"
            )

        raise ValueError(f"Could not load JSON from source: {source}")

    @staticmethod
    def _load_file(file_path: str) -> Dict[str, Any]:
        """Loads and parses a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _resolve_project_path(relative_path: str) -> Optional[Path]:
        """
        Resolves path by detecting project context from test file location.

        Detects projects in any subfolder within applications/:
        - applications/api/{project_name}/...
        - applications/web/{project_name}/...
        - applications/desktop/{project_name}/...
        - applications/{project_name}/...

        Strategy:
        1. Find test file in call stack
        2. Search for 'data' folder in the same project directory
        3. Build path: {project_root}/data/...

        Args:
            relative_path: Path relative to project root

        Returns:
            Path object or None if not found
        """
        # Get the call stack to find the test file
        stack = traceback.extract_stack()

        # Look for test files in the stack
        for frame in stack:
            frame_path = Path(frame.filename)

            # Strategy 1: Look for 'data' folder in parent directories
            # This works for any project structure
            for parent in frame_path.parents:
                data_folder = parent / 'data'
                if data_folder.is_dir():
                    # Found project root (folder containing 'data')
                    full_path = data_folder.parent / relative_path
                    return full_path

            # Strategy 2: Detect projects inside applications/{type}/{project}/
            for parent in frame_path.parents:
                # Check if this is a project folder (not 'applications' itself)
                if (parent.parent.name in ['applications'] or
                        parent.parent.parent.name == 'applications'):

                    # This is likely a project root
                    # Check if it has a 'data' folder
                    data_folder = parent / 'data'
                    if data_folder.is_dir():
                        full_path = parent / relative_path
                        return full_path

            # Strategy 3: Direct search for applications/{...}/{project}/data
            for parent in frame_path.parents:
                if parent.name == 'applications':
                    # Search in all subdirectories
                    for app_type in parent.iterdir():
                        if app_type.is_dir():
                            # Check if this is a project (has 'data' folder)
                            if (app_type / 'data').is_dir():
                                full_path = app_type / relative_path
                                if full_path.exists():
                                    return full_path
                            # Or check subdirectories (applications/web/{project})
                            for project in app_type.iterdir():
                                if project.is_dir():
                                    if (project / 'data').is_dir():
                                        full_path = project / relative_path
                                        if full_path.exists():
                                            return full_path

        # Fallback: return None and let caller handle error
        return None

    @staticmethod
    def get_project_root(test_file_path: Optional[str] = None) -> Optional[Path]:
        """
        Gets the project root for a given test file.

        Args:
            test_file_path: Path to test file (uses caller if None)

        Returns:
            Path to project root or None
        """
        if test_file_path:
            path = Path(test_file_path)
        else:
            stack = traceback.extract_stack()
            path = Path(stack[-2].filename)  # Caller's file

        # Search for 'data' folder in parent directories
        for parent in path.parents:
            data_folder = parent / 'data'
            if data_folder.is_dir():
                return parent

        return None