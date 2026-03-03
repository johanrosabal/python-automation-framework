# core/decorators/test_decorator.py

import allure
import pytest
import functools
import inspect
from datetime import datetime
from core.config.logger_config import setup_logger
from pathlib import Path
from typing import Optional, Callable, Union, List
import json
from core.utils.JSONReader import JSONReader

logger = setup_logger('Decorator')


def test(
        # === OLD STYLE PARAMETERS (backward compatible) ===
        test_case_id: Optional[str] = None,
        test_description: Optional[str] = None,
        feature: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tag: Optional[Union[str, List[str]]] = None,
        severity: Optional[str] = None,
        link_url: Optional[str] = None,
        link_name: Optional[str] = None,

        # === NEW STYLE PARAMETERS ===
        json_path: Optional[str] = None,
        json_data: Optional[dict] = None,

        # === CONTROL ===
        skip: bool = False,
):
    """
    Unified test decorator supporting both legacy and JSON-based metadata.
    """

    # Handle skip
    if skip:
        reason = test_description or title or "Test skipped"
        return pytest.mark.skip(reason=f"Skipping test: {reason}")

    def decorator(func: Callable) -> Callable:
        # ============================================================
        # 1. LOAD METADATA
        # ============================================================
        metadata = _load_metadata(
            json_path=json_path,
            json_data=json_data,
            test_case_id=test_case_id,
            test_description=test_description,
            feature=feature,
            title=title,
            description=description,
            tag=tag,
            severity=severity,
            link_url=link_url,
            link_name=link_name,
            func=func
        )

        # ============================================================
        # 2. APPLY ALLURE DECORATORS DIRECTLY TO FUNCTION (FIX)
        #    This ensures pytest-allure detects metadata during collection
        # ============================================================
        decorated_func = func

        # Title
        allure_title = metadata.get('title') or f"{metadata.get('test_case_id', 'Test')} - Test"
        decorated_func = allure.title(allure_title)(decorated_func)

        # Description
        if metadata.get('description'):
            decorated_func = allure.description(metadata['description'])(decorated_func)

        # Feature
        if metadata.get('feature'):
            decorated_func = allure.feature(metadata['feature'])(decorated_func)

        # Severity
        if metadata.get('severity'):
            severity_map = {
                'blocker': allure.severity_level.BLOCKER,
                'critical': allure.severity_level.CRITICAL,
                'major': allure.severity_level.NORMAL,
                'minor': allure.severity_level.MINOR,
                'trivial': allure.severity_level.TRIVIAL,
            }
            level = severity_map.get(metadata['severity'].lower(), allure.severity_level.NORMAL)
            decorated_func = allure.severity(level)(decorated_func)

        # Tags
        if metadata.get('tag'):
            tags = metadata['tag'] if isinstance(metadata['tag'], list) else [metadata['tag']]
            for t in tags:
                decorated_func = allure.tag(t)(decorated_func)

        # Links
        if metadata.get('link_url'):
            decorated_func = allure.link(
                url=metadata['link_url'],
                name=metadata.get('link_name') or metadata.get('test_case_id') or 'Link',
                link_type='jira'
            )(decorated_func)

        # Test Case ID
        # if metadata.get('test_case_id'):
        #     decorated_func = allure.testcase(metadata['test_case_id'])(decorated_func)

        # ============================================================
        # 3. CREATE WRAPPER (for execution logic & evidence)
        # ============================================================
        @functools.wraps(decorated_func)
        def wrapper(*args, **kwargs):
            try:
                result = decorated_func(*args, **kwargs)
                metadata['_execution_status'] = 'PASS'
                return result
            except Exception as e:
                metadata['_execution_status'] = 'FAIL'
                metadata['_error'] = str(e)
                raise
            finally:
                _capture_evidence(wrapper, metadata)

        # ============================================================
        # 4. Preserve attributes for hooks (conftest.py)
        # ============================================================
        wrapper.test_case_id = metadata.get('test_case_id')
        wrapper.test_description = metadata.get('test_description')
        wrapper.description = metadata.get('description')
        wrapper.feature = metadata.get('feature')
        wrapper._metadata = metadata

        return wrapper

    return decorator


def _load_metadata(**kwargs) -> dict:
    """
    Loads metadata with priority: JSON > direct params > function docstring.
    """
    # Initialize metadata
    metadata = {
        'test_case_id': kwargs.get('test_case_id'),
        'test_description': kwargs.get('test_description') or kwargs.get('description'),
        'feature': kwargs.get('feature'),
        'title': kwargs.get('title'),
        'description': kwargs.get('description'),
        'tag': kwargs.get('tag'),
        'severity': kwargs.get('severity'),
        'link_url': kwargs.get('link_url'),
        'link_name': kwargs.get('link_name'),
        'data': {},
    }

    func = kwargs.get('func')
    json_path = kwargs.get('json_path')
    json_data = kwargs.get('json_data')

    # === PRIORITY 1: JSON ===
    if json_path or json_data:
        try:
            data = JSONReader().import_json(json_data or json_path)
            tests = data.get('tests', {})

            # Map JSON fields to metadata
            for json_key, meta_key in [
                ('idTC', 'test_case_id'),
                ('title', 'title'),
                ('description', 'description'),
                ('feature', 'feature'),
                ('severity', 'severity'),
            ]:
                if tests.get(json_key) and not metadata.get(meta_key):
                    metadata[meta_key] = tests[json_key]

            # Handle tags
            if tests.get('tag') and not metadata.get('tag'):
                metadata['tag'] = tests['tag']

            # Handle nested link
            if tests.get('link') and not metadata.get('link_url'):
                metadata['link_url'] = tests['link'].get('url')
                if not metadata.get('link_name'):
                    metadata['link_name'] = tests['link'].get('name')

            # Store test-specific data
            metadata['data'] = tests.get('data', {})
            metadata['json_source'] = json_path or 'json_data'

            # ✅ CRITICAL: Sync description fields
            if metadata.get('description') and not metadata.get('test_description'):
                metadata['test_description'] = metadata['description']

            logger.debug(f"✓ Loaded metadata from JSON: {metadata.get('test_case_id')}")

        except Exception as e:
            logger.warning(f"⚠ Failed to load JSON metadata: {e}. Falling back to direct parameters.")

    # === PRIORITY 2: Direct parameters fallbacks ===
    if not metadata['title'] and metadata['test_case_id']:
        metadata['title'] = f"{metadata['test_case_id']} - Test"

    # === PRIORITY 3: Function docstring ===
    if func and (not metadata['title'] or not metadata['description']):
        doc = inspect.getdoc(func) or ""
        if doc:
            lines = doc.strip().split('\n')
            if not metadata['title']:
                metadata['title'] = lines[0].strip()
            if not metadata['description'] and len(lines) > 1:
                metadata['description'] = '\n'.join(lines[1:]).strip()

    # ✅ Sync again after docstring processing
    if metadata.get('description') and not metadata.get('test_description'):
        metadata['test_description'] = metadata['description']

    # === Generate link_name if needed ===
    if metadata['link_url'] and not metadata['link_name']:
        tc_id = metadata.get('test_case_id') or 'Test'
        test_title = metadata.get('title') or 'Untitled'
        metadata['link_name'] = f"{tc_id} - {test_title}"

    # === Normalize tag to list ===
    if metadata['tag'] and isinstance(metadata['tag'], str):
        metadata['tag'] = [metadata['tag']]

    return metadata


def _capture_evidence(func: Callable, metadata: dict) -> None:
    """
    Captures simplified test evidence for Xray integration.
    Removes redundant information and keeps only essential data.
    """
    try:
        test_case_id = metadata.get('test_case_id', 'UNKNOWN')

        if not test_case_id:
            return

        # ✅ SIMPLIFIED: Only essential information for Xray
        evidence = {
            "testKey": test_case_id,
            "status": metadata.get('_execution_status', 'UNKNOWN'),
            "executionDate": datetime.now().isoformat(),
            "comment": metadata.get('_error') if metadata.get('_error') else None,
            # Optional: Include test data if needed for Xray
            "info": {
                "summary": metadata.get('title'),
                "description": metadata.get('description'),
            } if metadata.get('title') or metadata.get('description') else None,
            # Optional: Include test-specific data (xml_path, etc.)
            "testData": metadata.get('data') if metadata.get('data') else None,
        }

        # Remove None values to keep JSON clean
        evidence = {k: v for k, v in evidence.items() if v is not None}
        if evidence.get('info'):
            evidence['info'] = {k: v for k, v in evidence['info'].items() if v is not None}
        if evidence.get('testData'):
            evidence['testData'] = {k: v for k, v in evidence['testData'].items() if v is not None}

        # Attach to Allure report (simplified)
        allure.attach(
            json.dumps(evidence, indent=2, ensure_ascii=False),
            name=f"Evidence - {test_case_id}",
            attachment_type=allure.attachment_type.JSON
        )

        # Save to file for Xray import
        evidence_dir = Path("./reports/evidence")
        evidence_dir.mkdir(parents=True, exist_ok=True)

        evidence_file = evidence_dir / f"evidence_{test_case_id}.json"

        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)

        logger.debug(f"✓ Evidence saved: {evidence_file}")

    except Exception as e:
        logger.warning(f"⚠ Could not save evidence: {e}")